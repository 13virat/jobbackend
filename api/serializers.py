from rest_framework import serializers
from .models import Job, Contact, Document

class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["user"]

        extra_kwargs = {
            "deadline": {"required": False, "allow_null": True},
            "applied_date": {"required": False, "allow_null": True},
            "interview_datetime": {"required": False, "allow_null": True},
            "offer_date": {"required": False, "allow_null": True},
            "rejected_date": {"required": False, "allow_null": True},
        }

    def validate(self, data):

        status = data.get("status", getattr(self.instance, "status", None))

        deadline = data.get("deadline")
        applied_date = data.get("applied_date")
        interview_datetime = data.get("interview_datetime")

        if status == "wishlist" and not deadline:
            raise serializers.ValidationError({
                "deadline": "Deadline is required for wishlist jobs"
            })

        if status == "applied" and not applied_date:
            raise serializers.ValidationError({
                "applied_date": "Applied date is required"
            })

        if status == "interview" and not interview_datetime:
            raise serializers.ValidationError({
                "interview_datetime": "Interview datetime required"
            })

        return data


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['user']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['user']