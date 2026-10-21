
from rest_framework import serializers

from .models import Panchayath, Ward


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = [
            "id",
            "panchayath",
            "number",
            "location_name",
            "is_active",
        ]
        read_only_fields = ["id"]

    def validate_panchayath(self, value):
        if not value.is_active:
            raise serializers.ValidationError(
                "Cannot assign a ward to an inactive Panchayath."
            )
        return value

    def validate(self, attrs):
        panchayath = attrs.get(
            "panchayath",
            getattr(self.instance, "panchayath", None),
        )
        number = attrs.get(
            "number",
            getattr(self.instance, "number", None),
        )

        if panchayath is not None and number is not None:
            queryset = Ward.objects.filter(
                panchayath=panchayath,
                number=number,
            )

            if self.instance is not None:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError({
                    "number": (
                        "This ward number already exists "
                        "within the selected Panchayath."
                    )
                })

        return attrs


class PanchayathSerializer(serializers.ModelSerializer):
    wards = WardSerializer(many=True, read_only=True)

    class Meta:
        model = Panchayath
        fields = [
            "id",
            "name",
            "code",
            "district",
            "state",
            "is_active",
            "wards",
        ]
        read_only_fields = ["id", "wards"]
