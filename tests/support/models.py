#!/usr/bin/env python
# coding: utf-8
from django.db import models
import reversion


@reversion.register
class TestModel(models.Model):
    pass