from rest_framework import serializers
from django.conf import settings


class MediaURLSerializer(serializers.Serializer):
    def to_representation(self, obj):
        request = self.context['request']
        try:
            return self.build_absolute_url(obj.file.url)
        except:
            return settings.HOST + obj.file.url
