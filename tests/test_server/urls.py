"""
Testing URL routing definition
"""
from tests.test_server.test_app.views import DummyAPIViewSet, DummyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("api/django-rest/api_dummy", DummyViewSet)
router.register("rest-as-api/django-rest/api_dummy", DummyAPIViewSet)

urlpatterns = router.urls
