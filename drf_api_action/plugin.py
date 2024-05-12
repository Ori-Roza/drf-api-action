import pytest

from drf_api_action.utils import run_as_api
from drf_api_action.exceptions import ActionsAPIException


def run_function(self, func):
    def api_item(*args, **kwargs):
        # here we retrieve serializer_class from @action decorator in order to inject it to the ViewSet
        serializer_class = func.kwargs['serializer_class']
        return run_as_api(self, func, serializer_class, *args, **kwargs)

    return api_item


@pytest.fixture
def api_action(request):
    """
    Make Dango WebView endpoints accessible
    """
    from drf_api_action.mixins import APIRestMixin  # pylint: disable=import-outside-toplevel

    if request.keywords['api_action'].kwargs.get("view_set_class") is None:
        raise ActionsAPIException('using api_action fixture must require a view_set_class kwarg')

    view_set_class = request.keywords['api_action'].kwargs["view_set_class"]

    class WrapperApiClass(APIRestMixin, view_set_class):
        def __getattribute__(self, item):
            class_attribute = super().__getattribute__(item)

            # running our logic on endpoints only
            if callable(class_attribute) and hasattr(class_attribute, 'detail'):
                return run_function(self, class_attribute)

            return class_attribute

    api = WrapperApiClass()
    return api
