import pytest
from django.test import Client
from rest_framework.exceptions import ValidationError

from drf_api_action.exceptions import ActionsAPIException
from tests.test_app.models import DummyModel
from tests.test_app.views import DummyAPIViewSet, DummyViewSet

from drf_api_action.utils import extract_page_number


def test_call_as_api(db):
    api = DummyAPIViewSet()
    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()

    res = api.dummy(request=None, pk=1)
    assert res["dummy_int"] == 1


def test_call_as_api_no_api_mixin(db):
    api = DummyViewSet()
    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()
    with pytest.raises(ActionsAPIException):
        _ = api.dummy(request=None, pk=1)


def test_call_as_rest(db):
    test_client = Client()

    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()

    response = test_client.get("/rest-as-api/django-rest/dummy/1/dummy/")
    assert response.data["dummy_int"] == 1


def test_pagination(db):
    api = DummyAPIViewSet()

    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()
    obj = api.by_dummy_int(request=None, dummy_int=1)["results"][0]
    assert obj['dummy_int'] == 1


def test_pagination_data(db):
    api = DummyAPIViewSet()

    for i in range(1, 3):
        dummy_model = DummyModel()
        dummy_model.dummy_int = 1
        dummy_model.save()

    response = api.by_dummy_int(request=None, dummy_int=1)
    assert extract_page_number(response['next']) == 2

    obj = response['results'][0]
    assert obj['dummy_int'] == 1

    response = api.by_dummy_int(request=None, dummy_int=1, page=2)
    assert extract_page_number(response['previous']) == 1
    assert extract_page_number(response['next']) is None


def test_exceptions(db):
    api = DummyAPIViewSet()

    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()
    with pytest.raises(ValidationError):
        _ = api.by_dummy_int(request=None, dummy_int=-1)