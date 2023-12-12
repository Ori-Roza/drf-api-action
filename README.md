![Alt text](resources/drf-api-action-banner.png?raw=true "")
[![codecov](https://codecov.io/gh/Ori-Roza/drf-api-action/graph/badge.svg?token=2PB7NG8A4W)](https://codecov.io/gh/Ori-Roza/drf-api-action)
[![python - 3.8 | 3.9 | 3.10 | 3.11](https://img.shields.io/badge/python-3.8_|_3.9_|_3.10_|_3.11-blue)](https://)[![CI](https://github.com/Ori-Roza/drf-api-action/actions/workflows/tests.yaml/badge.svg?branch=master)](https://github.com/Ori-Roza/drf-api-action/actions/workflows/tests.yaml)
[![license - MIT](https://img.shields.io/badge/license-MIT-yellow)](https://)


The drf-api-action Python package is designed to elevate your testing experience for Django Rest Framework (DRF) REST endpoints.
With the custom decorator api-action, this package empowers you to effortlessly test your REST endpoints as if they were conventional functions.

Features:

* **Simplified Testing:** Testing DRF REST endpoints using the api-action decorator, treating them like regular functions.

* **Seamless Integration:** Replacing DRF's action decorator with api-action in your WebViewSet seamlessly.

* **Clear Traceback:** Instead of getting a response with error code, get the real traceback that led to the error.

* **Pagination Support**: Paginating easily through pages by a single kwarg.  


## Installation

You can install `drf-api-action` using pip:

```shell
pip install drf-api-action
```

## Usage

To use `drf-api-action`, you need to follow these steps:

### Step 1: Import the Required Classes and Decorators

Import the necessary classes and decorators from `drf-api-action` and `rest_framework`:

```python
from drf_api_action.decorators import action_api
from drf_api_action.mixins import APIRestMixin
from rest_framework.viewsets import ModelViewSet
```

### Step 2: Inherit `APIRestMixin` in your View 

Create your view class by inheriting the `APIRestMixin` class.

For example, we want to inherit `ModelViewSet` (Could be any ViewSet) in our View:

```python
class DummyView(APIRestMixin, ModelViewSet):
    queryset = DummyModel.objects.all()
    serializer_class = DummySerializer
```

Another example:

```python
class UsersViewSet(APIRestMixin, mixins.RetrieveModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UsersSerializer
```

### Step 3: Define Your API Actions

Use the `action_api` decorator instead of `action` decorator to define your API actions as functions inside your view class:

From:
```python
    @action(detail=True, methods=["get"], serializer_class=DummySerializer)
    def dummy(self, request, **kwargs):
        serializer = self.get_serializer(instance=self.get_object())
        return Response(data=serializer.data, status=status.HTTP_200_OK)
```

To:

```python
    @action_api(detail=True, methods=["get"], serializer_class=DummySerializer)
    def dummy(self, request, **kwargs):
        serializer = self.get_serializer(instance=self.get_object())
        return Response(data=serializer.data, status=status.HTTP_200_OK)
```

In the example above, the `dummy` function is decorated with `action_api`.
It specifies that the action requires a detail argument, supports the `GET` method, and uses the `DummySerializer` for serialization.

### Step 4: test REST methods

* Create an instance of your view class and call the API actions as regular functions:

```python
def test_dummy():
    api = DummyView()
    result = api.dummy(pk=1)
    assert result['dummy_int'] == 1
```

**query parameters/post payload are treated as function arguments as kwargs**

* Exceptions are raised explicitly:
```python
def test_dummy():
    api = DummyView()
    result = api.dummy(pk='bbb')
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

and so on....
```

* Pagination support with `page`/`offset` kwarg (depends on `DEFAULT_PAGINATION_CLASS`):
```python
>>> api = DummyAPIViewSet()
>>> response = api.by_dummy_int(request=None, dummy_int=1, page=2)

>>> {'count': 2, 'next': None, 'previous': '', 'results': [OrderedDict([('id', 2), ('dummy_int', 1)])]}

```


## Package Testing

The `drf-api-action` library includes tests to ensure the functionality works as expected. To run the tests, follow these steps:

1. Navigate to the root directory of the `drf-api-action/` project.
```shell
cd tests/
```

2. Run the tests using `pytest`

 ```shell
 python -m pytest -vv
 ```

The tests will be executed, and the results will be displayed in the console.


## Example

Example of using drf-api-action in a [DRF project](https://github.com/Ori-Roza/drf-api-action-example)


## Contribution

Contributions to the `drf-api-action` library are welcome. If you would like to contribute, please follow these steps:

1. Fork the `drf-api-action` repository on GitHub.

2. Create a new branch for your feature or bug fix.

3. Make the necessary changes and additions.

4. Write tests to cover the new functionality or bug fix.

5. Run the existing tests to ensure all tests pass successfully.

6. Commit your changes and push them to your forked repository.

7. Open a pull request on the original `drf-api-action` repository and provide a detailed description of your changes.

The maintainers will review your pull request, provide feedback, and work with you to merge the changes into the main repository.

Thank you for considering contributing to `drf-api-action`!
