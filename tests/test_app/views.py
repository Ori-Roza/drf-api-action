from .models import DummyModel
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_api_action.decorators import action_api
from drf_api_action.mixins import APIRestMixin
from rest_framework.serializers import IntegerField, ModelSerializer, Serializer


class DummySerializer(ModelSerializer):
    dummy_int = IntegerField()

    class Meta:
        model = DummyModel
        fields = "__all__"


class GetDummyByIntSerializer(Serializer):
    id = IntegerField(read_only=True)
    dummy_int = IntegerField(read_only=True)

    class Meta:
        model = DummyModel
        fields = "__all__"


class DummyViewSet(ModelViewSet):
    queryset = DummyModel.objects.all()
    serializer_class = DummySerializer

    @action_api(detail=True, methods=["get"], serializer_class=DummySerializer)
    def dummy(self, request, **kwargs):
        serializer = self.get_serializer(instance=self.get_object())
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DummyAPIViewSet(APIRestMixin, ModelViewSet):
    queryset = DummyModel.objects.all()
    serializer_class = DummySerializer

    def get_serializer_context(self):
        return {
            "request": self.request,
            "view": self,
            "pk": self.kwargs.get("pk"),
        }

    @action_api(detail=True, methods=["get"], serializer_class=DummySerializer)
    def dummy(self, request, **kwargs):
        serializer = self.get_serializer(instance=self.get_object())
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action_api(detail=False, methods=["post"], serializer_class=GetDummyByIntSerializer)
    def by_dummy_int(self, request, **kwargs):
        self.get_serializer(data=request.data).is_valid(raise_exception=True)
        queryset = DummyModel.objects.filter(dummy_int=request.data["dummy_int"]).order_by("id")
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
