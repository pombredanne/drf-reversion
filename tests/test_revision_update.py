#!/usr/bin/env python
# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from rest_framework.routers import DefaultRouter
from rest_framework.test import APITransactionTestCase
import reversion

from tests.support.models import TestModel
from tests.support.views import UpdateRevisionTestView


router = DefaultRouter()
router.register('testmodel', UpdateRevisionTestView)

urlpatterns = patterns('',
   url(r'', include(router.urls))
)


class UpdateRevisionTestCase(APITransactionTestCase):
    urls = 'tests.test_revision_update'

    def test_that_a_revision_is_created_when_updating_an_object(self):
        created_model = TestModel.objects.create()
        self.client.put('/testmodel/%d/' % created_model.pk)

        version_list = reversion.get_for_object(created_model)

        self.assertEqual(len(version_list), 1)

    def test_that_a_revision_is_created_when_partially_updating_an_object(self):
        created_model = TestModel.objects.create()
        self.client.patch('/testmodel/%d/' % created_model.pk)

        version_list = reversion.get_for_object(created_model)

        self.assertEqual(len(version_list), 1)

    def test_that_a_revision_is_associated_to_the_updating_user(self):
        user = User.objects.create_user('a')
        self.client.force_authenticate(user=user)

        created_model = TestModel.objects.create()
        response = self.client.put('/testmodel/%d/' % created_model.pk)

        created_model = TestModel.objects.get(pk=response.data['id'])

        revision = reversion.get_for_object(created_model)[0].revision

        self.assertEqual(revision.user, user)

    def test_that_a_revision_is_associated_to_the_patially_updating_user(self):
        user = User.objects.create_user('a')
        self.client.force_authenticate(user=user)

        created_model = TestModel.objects.create()
        response = self.client.put('/testmodel/%d/' % created_model.pk)

        created_model = TestModel.objects.get(pk=response.data['id'])

        revision = reversion.get_for_object(created_model)[0].revision

        self.assertEqual(revision.user, user)