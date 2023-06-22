import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    With this fixture we don't need to add

    "pytest.mark.django_db()" to every test!!

    Source:
    https://pytest-django.readthedocs.io/en/latest/faq.html#how-can-i-give-database-access-to-all-my-tests-without-the-django-db-marker
    """
    pass
