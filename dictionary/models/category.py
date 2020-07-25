from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _lazy

from uuslug import uuslug

from ..utils.validators import validate_category_name


class Category(models.Model):
    name = models.CharField(max_length=24, unique=True, verbose_name=_lazy("Name"), validators=[validate_category_name])
    slug = models.SlugField(editable=False)
    description = models.TextField(null=True, blank=True, verbose_name=_lazy("Description"))
    weight = models.SmallIntegerField(default=0, verbose_name=_lazy("Weight"))

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("topic_list", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-weight"]
        verbose_name = _lazy("channel")
        verbose_name_plural = _lazy("channels")
