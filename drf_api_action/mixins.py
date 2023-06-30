from rest_framework import viewsets
from django.db.models.query import QuerySet


class APIRestMixin(viewsets.GenericViewSet):
    """
    creates our custom get_serializer in order to use our serializer injection
    """
    api_mixin_exists = True

    def get_serializer(self, request_or_query_set=None, *args, **kwargs):  # pylint: disable=keyword-arg-before-vararg
        if isinstance(request_or_query_set, QuerySet):
            # handling ListView (with default queryset & default serializer)
            args = [request_or_query_set] + list(args)
        elif isinstance(request_or_query_set, list):
            # handling pagination
            args = [request_or_query_set]
        # handling all other views
        serializer_class = self.kwargs.get("serializer_class", self.serializer_class)
        return serializer_class(*args, **kwargs)
