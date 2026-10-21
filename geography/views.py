
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Panchayath, Ward
from .serializers import PanchayathSerializer, WardSerializer


class PanchayathListView(generics.ListCreateAPIView):
    serializer_class = PanchayathSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return (
            Panchayath.objects.filter(is_active=True)
            .prefetch_related("wards")
        )


class WardListView(generics.ListCreateAPIView):
    serializer_class = WardSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Ward.objects.filter(
            is_active=True,
            panchayath__is_active=True,
        ).select_related("panchayath")

        panchayath_id = self.request.query_params.get("panchayath")
        if panchayath_id:
            queryset = queryset.filter(panchayath_id=panchayath_id)

        return queryset
