import pytest
from tests.test_app.models import DummyModel
from tests.test_app.views import DummyViewSet


@pytest.mark.action_api(view_set_class=DummyViewSet)
def test_call_as_api_fixture(db, action_api):
    dummy_model = DummyModel()
    dummy_model.dummy_int = 1
    dummy_model.save()
    res = action_api.api_dummy(pk=1)
    assert res["dummy_int"] == 1
