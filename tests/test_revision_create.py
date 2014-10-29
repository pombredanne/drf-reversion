#!/usr/bin/env python
# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from rest_framework.routers import DefaultRouter
from rest_framework.test import APITransactionTestCase
import reversion
from tests.support.models import TestModel
from tests.support.views import CreateRevisionTestView

router = DefaultRouter()
router.register('testmodel', CreateRevisionTestView)

urlpatterns = patterns('',
   url(r'', include(router.urls))
)


class CreateRevisionTestCase(APITransactionTestCase):
    urls = 'tests.test_revision_create'

    def test_that_a_revision_is_created_when_creating_an_object(self):
        response = self.client.post('/testmodel/')

        created_model = TestModel.objects.get(pk=response.data['id'])

        version_list = reversion.get_for_object(created_model)

        self.assertEqual(len(version_list), 1)

    def test_that_a_revision_is_associated_to_the_creating_user(self):
        user = User.objects.create_user('a')
        self.client.force_authenticate(user=user)

        response = self.client.post('/testmodel/')

        created_model = TestModel.objects.get(pk=response.data['id'])

        revision = reversion.get_for_object(created_model)[0].revision

        self.assertEqual(revision.user, user)