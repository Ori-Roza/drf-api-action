import pytest
from django.test import Client
from rest_framework.exceptions import ValidationError
from drf_api_action.fixtures import action_api
from drf_api_action.exceptions import ActionsAPIException
from tests.test_app.models import DummyModel
from tests.test_app.views import DummyAPIViewSet, DummyViewSet

from drf_api_action.utils import extract_page_number


@pytest.mark.action_api(view_set_class=DummyViewSet)
def test_call_as_api_fixture(db, action_api):
    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()
    res = action_api.api_dummy(pk=1)
    assert res["dummy_int"] == 1
