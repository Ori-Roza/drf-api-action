![Alt text](resources/drf-api-action-banner-current.png?raw=true "")

[![codecov](https://codecov.io/gh/Ori-Roza/drf-api-action/graph/badge.svg?token=2PB7NG8A4W)](https://codecov.io/gh/Ori-Roza/drf-api-action)
[![python - 3.8 | 3.9 | 3.10 | 3.11](https://img.shields.io/badge/python-3.8_|_3.9_|_3.10_|_3.11-blue)](https://)[![CI](https://github.com/Ori-Roza/drf-api-action/actions/workflows/tests.yaml/badge.svg?branch=master)](https://github.com/Ori-Roza/drf-api-action/actions/workflows/tests.yaml)
[![license - MIT](https://img.shields.io/badge/license-MIT-yellow)](https://)


The drf-api-action Python package is designed to elevate your testing experience for Django Rest Framework (DRF) REST endpoints.
With the api_action fixture, this package empowers you to effortlessly test your REST endpoints as if they were conventional functions.

Features:

* **Simplified Testing:** Testing DRF REST endpoints using the api_action plugin, treating them like regular functions.

* **Seamless Integration:** you don't need to do anything in existing server code.

* **Easy Debugging:** Instead of getting a response with error code by using default drf testing `client` object , get the real traceback that led to the error.

* **Pagination Support**: Paginating easily through pages by using `page` argument.


## Installation

You can install `drf-api-action` using pip:

```shell
pip install drf-api-action
```

## Usage

### To use `drf-api-action` as a Pytest fixture, you need to follow these steps:

#### Step 1: Import your Viewsets explicitly:

```python
import pytest
from tests.test_server.test_app.models import DummyModel
from tests.test_server.test_app.views import DummyViewSetFixture
```

#### Step 2: use the following action_api mark decorator:

`@pytest.mark.api_action(view_set_class={YOUR VIEW_SET})`

e.g:
our ViewSet is called `DummyViewSetFixture`

```python
import pytest
from tests.test_server.test_app.views import DummyViewSetFixture


@pytest.mark.api_action(view_set_class=DummyViewSetFixture)
def test_call_as_api_fixture(db, api_action):
  pass
```
Now you can use all `DummyViewSetFixture` functionality!

#### Step 3: write your tests

e.g:
our ViewSet is called `DummyViewSetFixture`

```python
import pytest
from tests.test_server.test_app.models import DummyModel
from tests.test_server.test_app.views import DummyViewSetFixture


@pytest.mark.api_action(view_set_class=DummyViewSetFixture)
def test_call_as_api_fixture(db, api_action):
  dummy_model = DummyModel()
  dummy_model.dummy_int = 1
  dummy_model.save()
  res = api_action.api_dummy(pk=1)
  assert res["dummy_int"] == 1

```
Here as an example, the real exception and trace will be thrown, make it easy to understand what the issue is:

```python
import pytest
from tests.test_server.test_app.views import DummyViewSetFixture


@pytest.mark.api_action(view_set_class=DummyViewSetFixture)
def test_dummy(db, api_action):
  result = api_action.dummy(pk='bbb')
  assert result['dummy_int'] == 1
```

```shell
tests/functionality_tests/test_as_api.py:11 (test_call_as_api)
self = <django.db.models.fields.BigAutoField: id>, value = 'bb'

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None
        try:
>           return int(value)
E           ValueError: invalid literal for int() with base 10: 'bb'

../venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py:2053: ValueError

The above exception was the direct cause of the following exception:

queryset = <QuerySet [<DummyModel: DummyModel object (1)>]>, filter_args = ()
filter_kwargs = {'pk': 'bb'}

    def get_object_or_404(queryset, *filter_args, **filter_kwargs):
        """
        Same as Django's standard shortcut, but make sure to also raise 404
        if the filter_kwargs don't match the required types.
        """
        try:
>           return _get_object_or_404(queryset, *filter_args, **filter_kwargs)

../venv/lib/python3.9/site-packages/rest_framework/generics.py:19: 
....
....
...
```

Call endpoints with pagination:
```python
@pytest.mark.api_action(view_set_class=DummyAPIViewSet)
def test_pagination_data(db, api_action):
    for i in range(1, 3):
        dummy_model = DummyModel()
        dummy_model.dummy_int = 1
        dummy_model.save()

    response = api_action.by_dummy_int(dummy_int=1, page=1)

    obj = response['results'][0]
    assert obj['dummy_int'] == 1

    assert extract_page_number(response['next']) == 2

    response = api_action.by_dummy_int(dummy_int=1, page=2)
    assert extract_page_number(response['previous']) == 1
    assert extract_page_number(response['next']) is None

```


## Package Testing

The `drf-api-action` library includes tests to ensure the functionality works as expected. To run the tests run `pytest`:

 ```shell
 pytest
 ```

The tests will be executed, and the results will be displayed in the console.

## Example

Example of using drf-api-action in a [DRF project](https://github.com/Ori-Roza/drf-api-action-example)

## Support & Contribution

For guidance on support & contribution, see the [contributing guidelines](https://github.com/Ori-Roza/drf-api-action/blob/master/docs/CONTRIBUTING.md).

## Bug Report 

For guidance on how to open a bug, see the [bug report template](https://github.com/Ori-Roza/drf-api-action/blob/master/docs/BUG_REPORT.md).

## Open an Issue

For guidance on how to open an issue, see the [issue template](https://github.com/Ori-Roza/drf-api-action/blob/master/docs/ISSUE_TEMPLATE.md).

## Code Of Conduct

[code of conduct](https://github.com/Ori-Roza/drf-api-action/blob/master/docs/CODE_OF_CONDUCT.md).
