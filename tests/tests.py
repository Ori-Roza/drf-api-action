import pytest
from rest_framework.exceptions import ValidationError

from drf_api_action.utils import extract_page_number
from tests.test_server.test_app.models import DummyModel
from tests.test_server.test_app.views import DummyViewSetFixture, DummyAPIViewSet


@pytest.mark.api_action(view_set_class=DummyViewSetFixture)
def test_call_as_api_fixture(db, api_action):
    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()
    res = api_action.api_dummy(pk=1)
    assert res["dummy_int"] == 1


@pytest.mark.api_action(view_set_class=DummyAPIViewSet)
def test_pagination(db, api_action):
    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()
    obj = api_action.by_dummy_int(dummy_int=1)["results"][0]
    assert obj['dummy_int'] == 1


@pytest.mark.api_action(view_set_class=DummyAPIViewSet)
def test_pagination_data(db, api_action):
    for i in range(1, 3):
        dummy_model = DummyModel()
        dummy_model.dummy_int = 1
        dummy_model.save()

    response = api_action.by_dummy_int(dummy_int=1)
    assert extract_page_number(response['next']) == 2

    obj = response['results'][0]
    assert obj['dummy_int'] == 1

    response = api_action.by_dummy_int(dummy_int=1, page=2)
    assert extract_page_number(response['previous']) == 1
    assert extract_page_number(response['next']) is None


@pytest.mark.api_action(view_set_class=DummyAPIViewSet)
def test_exceptions(db, api_action):
    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()
    with pytest.raises(ValidationError):
        _ = api_action.by_dummy_int(dummy_int=-1)
