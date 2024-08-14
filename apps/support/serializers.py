from rest_framework import serializers

from apps.support.models import RightholderAppeal, HelpAppeal


class RightholderAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightholderAppeal
        fields = (
            'organization', 'contact_person', 'email', 'release_url', 'document_url', 'explanation',
            'message'
        )


class HelpAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpAppeal
        fields = (
            'title', 'email', 'message'
        )
