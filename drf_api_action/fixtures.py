import pytest

from drf_api_action.api_utils import run_as_api
from drf_api_action.mixins import APIRestMixin


def run_function(self, func):
    def api_item(*args, **kwargs):
        serializer_class = func.kwargs['serializer_class']
        return run_as_api(self, func, serializer_class, *args, **kwargs)
    return api_item


@pytest.fixture
def action_api(request):
    view_set_class = request.keywords['action_api'].kwargs["view_set_class"]

    class WrapperApiClass(APIRestMixin, view_set_class):
        def __getattribute__(self, item):
            class_attribute = super().__getattribute__(item)

            if callable(class_attribute) and hasattr(class_attribute, 'detail'):
                return run_function(self, class_attribute)

            return class_attribute

    api = WrapperApiClass()
    return api
