import pytest

from drf_api_action.api_utils import run_as_api
from drf_api_action.mixins import APIRestMixin
from drf_api_action.utils import CustomRequest
from drf_api_action.exceptions import ActionsAPIExceptionMiddleware


def run_function(self, func):
    serializer_class = func.kwargs['serializer_class']
    return run_as_api(self, func, serializer_class)


@pytest.fixture
def api_action(request):
    view_set_class = request.keywords['api_action'].kwargs["view_set_class"]

    class WrapperApiClass(APIRestMixin, view_set_class):
        def __getattribute__(self, item):
            class_attribute = super(WrapperApiClass, self).__getattribute__(item)

            if callable(class_attribute) and hasattr(class_attribute, 'detail'):
                return run_function(self, class_attribute)

            return class_attribute

    api = WrapperApiClass()
    return api
