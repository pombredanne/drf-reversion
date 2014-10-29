#!/usr/bin/env python
# coding: utf-8
from rest_framework import viewsets

from drf_reversion.mixins import CreateCreationRevisionMixin, CreateUpdateRevisionMixin, CreateDeletionRevisionMixin
from tests.support.models import TestModel


class CreateRevisionTestView(CreateCreationRevisionMixin, viewsets.ModelViewSet):
    model = TestModel


class UpdateRevisionTestView(CreateUpdateRevisionMixin, viewsets.ModelViewSet):
    model = TestModel


class DeleteRevisionTestView(CreateDeletionRevisionMixin, viewsets.ModelViewSet):
    model = TestModel