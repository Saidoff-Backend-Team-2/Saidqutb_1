from rest_framework import serializers
from .models import Banner, AboutUs, AboutUsGallery, Contacts
from common.serializers import MediaURLSerializer
from company.models import SocialMedia, ContactWithUs


class BannerListSerializers(serializers.ModelSerializer):
    bg_image = MediaURLSerializer()
    class Meta:
        model = Banner
        exclude = ('id', )
        read_only_fields = ('title', 'subtitle', 'bg_image')


class AboutUsGallerySerializer(serializers.ModelSerializer):
    image = MediaURLSerializer()

    class Meta:
        model = AboutUsGallery
        fields = ('image', )


class AboutUsHomeSerializer(serializers.ModelSerializer):
    galleries = serializers.SerializerMethodField()

    class Meta:
        model = AboutUs
        fields = ('desc', 'galleries')

    def get_galleries(self, obj):
        return AboutUsGallerySerializer(obj.galleries.order_by('?')[:6], many=True, context=self.context).data


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('address', 'phone_number1', 'phone_number2', 'work_time')


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia()
        fields = ('link', 'icon')


class ContactWithUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactWithUs
        fields = ('full_name', 'phone_number')




