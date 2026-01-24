from rest_framework import serializers

from .models import LiteratureArticle, Participant, Study


class ParticipantSerializer(serializers.ModelSerializer):
    study_title = serializers.CharField(source="study.title", read_only=True)

    class Meta:
        model = Participant
        fields = ["id", "study", "study_title", "code", "age", "sex", "enrolled_on"]
        read_only_fields = ["id"]

    def validate_age(self, value):
        if value < 0 or value > 150:
            raise serializers.ValidationError("Age must be between 0 and 150")
        return value

    def validate_sex(self, value):
        allowed_values = ["M", "F", "Other", "Male", "Female"]
        if value not in allowed_values:
            raise serializers.ValidationError(
                f"Sex must be one of: {', '.join(allowed_values)}"
            )
        return value


class StudySerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    participant_count = serializers.IntegerField(source="participants.count", read_only=True)

    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "condition",
            "status",
            "start_date",
            "end_date",
            "created_at",
            "participants",
            "participant_count",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_status(self, value):
        allowed_statuses = ["planning", "recruiting", "active", "completed", "cancelled"]
        if value not in allowed_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(allowed_statuses)}"
            )
        return value

    def validate(self, data):
        from django.utils import timezone
        
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        
        # End date must be after start date
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                "End date must be after start date"
            )
        
        # Start date should not be in the past for new studies
        if start_date and start_date < timezone.now().date():
            # Allow past dates for existing studies being updated
            if not self.instance:
                raise serializers.ValidationError(
                    "Start date cannot be in the past for new studies"
                )
        
        # If status is completed, end_date should be set
        if data.get("status") == "completed" and not end_date:
            raise serializers.ValidationError(
                "End date is required for completed studies"
            )
        
        # If status is active, start_date should be set and in the past or today
        if data.get("status") == "active":
            if not start_date:
                raise serializers.ValidationError(
                    "Start date is required for active studies"
                )
            if start_date > timezone.now().date():
                raise serializers.ValidationError(
                    "Active studies must have a start date in the past or today"
                )
        
        return data


class LiteratureArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiteratureArticle
        fields = [
            "id",
            "title",
            "authors",
            "journal",
            "year",
            "doi",
            "abstract",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_year(self, value):
        from datetime import date
        current_year = date.today().year
        if value < 1900 or value > current_year:
            raise serializers.ValidationError(
                f"Year must be between 1900 and {current_year}"
            )
        return value

    def validate_doi(self, value):
        if value and not value.startswith("10."):
            raise serializers.ValidationError(
                "DOI must start with '10.'"
            )
        return value
