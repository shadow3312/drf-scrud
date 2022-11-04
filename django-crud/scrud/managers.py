"""
Model manager to add active_rows and inactive_rows methods to model objects

e.g: models.User.objects.inactive_rows()
"""

from django.db import models

class TemporalQuerySet(models.Manager):
    def current(self):
        return self.first()
    def active_rows(self):
        return super().get_queryset().filter(is_active=True)
    def inactive_rows(self):
        return super().get_queryset().filter(is_active=False)
   