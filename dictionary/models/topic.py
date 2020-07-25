from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.utils.translation import gettext as _, gettext_lazy as _lazy

from uuslug import uuslug

from ..utils import get_generic_superuser, i18n_lower
from ..utils.validators import validate_user_text
from .author import Author
from .category import Category
from .m2m import TopicFollowing
from .managers.topic import TopicManager, TopicManagerPublished
from .messaging import Message


TOPIC_TITLE_VALIDATORS = [
    RegexValidator(
        r"^[a-z0-9 ğçıöşü₺&()_+=':%/\",.!?~\[\]{}<>^;\\|-]+$",
        message=_lazy("the definition of this topic includes forbidden characters"),
    ),
    MaxLengthValidator(50, message=_lazy("this title is too long")),
]


class Topic(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        validators=TOPIC_TITLE_VALIDATORS,
        verbose_name=_lazy("Definition"),
        help_text=_lazy(
            "In order to change the definition of the topic after it"
            " has been created, you need to use topic moving feature."
        ),
    )

    slug = models.SlugField(max_length=96, unique=True, editable=False)

    created_by = models.ForeignKey(
        Author,
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
        verbose_name=_lazy("First user to write an entry"),
        help_text=_lazy("The author or novice who entered the first entry for this topic publicly."),
    )

    category = models.ManyToManyField(Category, blank=True, verbose_name=_lazy("Channels"))
    wishes = models.ManyToManyField("Wish", blank=True, editable=False, verbose_name=_lazy("Wishes"))

    mirrors = models.ManyToManyField(
        "self",
        blank=True,
        verbose_name=_lazy("Title disambiguation"),
        help_text=_lazy(
            "<p style='color: #ba2121'><b>Warning!</b> The topics that you enter will automatically"
            " get related disambiguations. For this reason you should be working on a main topic that you"
            " selected.<br> Removing a topic from will cause the removal of <b>ALL</b> disambiguations, so"
            " you should note down the topics that you don't want to be removed to add them later.</p>"
        ),
    )

    media = models.TextField(blank=True, null=True, verbose_name=_lazy("Media links"))

    is_banned = models.BooleanField(
        default=False,
        verbose_name=_lazy("Prohibited"),
        help_text=_lazy(
            "Check this if you want to hinder authors and novices from entering new entries to this topic."
        ),
    )

    is_censored = models.BooleanField(
        default=False,
        verbose_name=_lazy("Censored"),
        help_text=_lazy(
            "Check this if you don't want this topic to appear"
            " in in-site searches and <strong>public</strong> topic lists."
        ),
    )

    is_pinned = models.BooleanField(
        default=False,
        verbose_name=_lazy("Pinned"),
        help_text=_lazy(
            "Check this if you want this topic to be pinned in popular topics."
            "<br>The topic needs to have at least one entry."
        ),
    )

    is_ama = models.BooleanField(
        default=False,
        verbose_name=_lazy("Ask me anything"),
        help_text=_lazy(
            "If checked, comments will be visible in this topic. Authorized users will be able to comment on entries."
        ),
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_lazy("Date created"),
        help_text=_lazy("<i>Might not always correspond to first entry.</i>"),
    )

    objects = TopicManager()
    objects_published = TopicManagerPublished()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        permissions = (("move_topic", _lazy("Can move topics")),)
        verbose_name = _lazy("topic")
        verbose_name_plural = _lazy("topics")

    def get_absolute_url(self):
        return reverse("topic", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.title = i18n_lower(self.title)
        self.slug = uuslug(self.title, instance=self)
        super().save(*args, **kwargs)

    def follow_check(self, user):
        return TopicFollowing.objects.filter(topic=self, author=user).exists()

    def latest_entry_date(self, sender):
        try:
            return (
                self.entries.exclude(Q(author__in=sender.blocked.all()) | Q(author=sender))
                .latest("date_created")
                .date_created
            )
        except ObjectDoesNotExist:
            return self.date_created

    def register_wishes(self, fulfiller_entry=None):
        """To delete fulfilled wishes and inform wishers."""

        if self.wishes.exists() and self.has_entries:
            invoked_by_entry = fulfiller_entry is not None
            wishes = self.wishes.all().select_related("author")

            for wish in wishes:
                self_fulfillment = invoked_by_entry and fulfiller_entry.author == wish.author

                if not self_fulfillment:
                    message = (
                        _(
                            "%(title)s, the topic you wished for, had an entry"
                            " entered by %(username)s: (see: #%(entry)d)"
                        )
                        % {
                            "title": self.title,
                            "username": fulfiller_entry.author.username,
                            "entry": fulfiller_entry.pk,
                        }
                        if invoked_by_entry
                        else _("%(title)s, the topic you wished for, is now populated with some entries.")
                        % {"title": self.title}
                    )

                    Message.objects.compose(get_generic_superuser(), wish.author, message)

            return wishes.delete()
        return None

    @property
    def exists(self):
        return True

    @property
    def valid(self):
        return True

    @property
    def entry_count(self):
        return self.entries(manager="objects_published").count()

    @property
    def has_entries(self):
        return self.entries.exclude(is_draft=True).exists()


class Wish(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="wishes")
    hint = models.TextField(validators=[validate_user_text], null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.__class__.__name__}#{self.pk} u:{self.author.username}"

    class Meta:
        ordering = ("-date_created",)
