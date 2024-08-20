import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


class Media(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'image', _('Image')
        VIDEO = 'vidio', _('Vidio')
        AUDIO = 'audio', _('Audio')
        OTHER = 'other', _('Other')

    file = models.FileField(_('file'), upload_to='all_media_files/', validators=[FileExtensionValidator(
        ['jpn', 'jpeg', 'png', 'mp4', 'mp3'])])
    type = models.CharField(_('type'), max_length=28, choices=MediaType.choices, default=MediaType.IMAGE)

    def __str__(self):
        return f"{self.file.name}-{self.type}"

    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Media')

    def clean(self):
        ext = os.path.splitext(self.file.name)[1][1:].lower()
        if self.type == Media.MediaType.IMAGE and ext not in ['jpg', 'jpeg', 'png']:
            raise ValidationError(_('Only jpg, jpeg, png are allowed'))
        elif self.type == Media.MediaType.VIDEO and ext != 'mp4':
            raise ValidationError(_('Only mp4 is allowed'))
        elif self.type == Media.MediaType.AUDIO and ext != 'mp3':
            raise ValidationError(_('Only mp3 is allowed'))

