import pytest
from rest_framework.exceptions import ValidationError

from drf_api_action.utils import extract_page_number
from tests.test_app.models import DummyModel
from tests.test_app.views import DummyViewSetFixture, DummyAPIViewSet
from drf_api_action import action_api


@pytest.mark.action_api(view_set_class=DummyViewSetFixture)
def test_call_as_api_fixture(db, action_api):
    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()
    res = action_api.api_dummy(pk=1)
    assert res["dummy_int"] == 1


@pytest.mark.action_api(view_set_class=DummyAPIViewSet)
def test_pagination(db, action_api):
    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()
    obj = action_api.by_dummy_int(dummy_int=1)["results"][0]
    assert obj['dummy_int'] == 1


@pytest.mark.action_api(view_set_class=DummyAPIViewSet)
def test_pagination_data(db, action_api):
    for i in range(1, 3):
        dummy_model = DummyModel()
        dummy_model.dummy_int = 1
        dummy_model.save()

    response = action_api.by_dummy_int(dummy_int=1)
    assert extract_page_number(response['next']) == 2

    obj = response['results'][0]
    assert obj['dummy_int'] == 1

    response = action_api.by_dummy_int(dummy_int=1, page=2)
    assert extract_page_number(response['previous']) == 1
    assert extract_page_number(response['next']) is None


@pytest.mark.action_api(view_set_class=DummyAPIViewSet)
def test_exceptions(db, action_api):
    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()
    with pytest.raises(ValidationError):
        _ = action_api.by_dummy_int(dummy_int=-1)
