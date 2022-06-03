from rest_framework import serializers

from preferences.models import Preference


class PreferenceSerializer(serializers.Serializer):

    uuid = serializers.UUIDField()
    label = serializers.FloatField(required=False)

    def create(self, validated_data):
        return Preference.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.label = validated_data.get('label', instance.label)
        instance.save()
        return instance
