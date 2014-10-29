#!/usr/bin/env python
# coding: utf-8
import reversion


class CreateCreationRevisionMixin(object):
    @reversion.create_revision()
    def create(self, *args, **kwargs):
        return super(CreateCreationRevisionMixin, self).create(*args, **kwargs)

    def pre_save(self, obj):
        user = self.request.user
        if user and not user.is_anonymous():
            reversion.set_user(user)

        super(CreateCreationRevisionMixin, self).pre_save(obj)


class CreateUpdateRevisionMixin(object):
    @reversion.create_revision()
    def update(self, *args, **kwargs):
        return super(CreateUpdateRevisionMixin, self).update(*args, **kwargs)

    def pre_save(self, obj):
        user = self.request.user
        if user and not user.is_anonymous():
            reversion.set_user(user)

        super(CreateUpdateRevisionMixin, self).pre_save(obj)


class RevisionMixin(CreateCreationRevisionMixin, CreateUpdateRevisionMixin):
    pass