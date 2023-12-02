![Alt text](resources/drf-api-action-banner.png?raw=true "")


[![python - 3.8 | 3.9 | 3.10 | 3.11](https://img.shields.io/badge/python-3.8_|_3.9_|_3.10_|_3.11-blue)](https://)[![CI](https://github.com/Ori-Roza/drf-api-action/actions/workflows/tests.yaml/badge.svg?branch=master)](https://github.com/Ori-Roza/drf-api-action/actions/workflows/tests.yaml)
![Alt text](resources/coverage_badge.svg)
[![license - MIT](https://img.shields.io/badge/license-MIT-yellow)](https://)


The drf-api-action Python package is designed to elevate your testing experience for Django Rest Framework (DRF) REST endpoints.
With the custom decorator api-action, this package empowers you to effortlessly test your REST endpoints as if they were conventional functions.

Features:

* **Simplified Testing:** Easily test DRF REST endpoints using the api-action decorator, treating them like regular functions.

* **Seamless Integration:** Replace DRF's action decorator with api-action in your WebViewSet for a smooth transition.


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

### Step 2: Define Your View Class

Create your view class by inheriting from `APIRestMixin` and `ModelViewSet`:

```python
class DummyView(APIRestMixin, ModelViewSet):
    queryset = DummyModel.objects.all()
    serializer_class = DummySerializer
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

In the example above, the `dummy_func` function is decorated with `action_api`. It specifies that the action does not require a detail argument, supports the `POST` method, and uses the `DummySerializer` for serialization.

### Step 4: test REST methods

Create an instance of your view class and call the API actions as regular functions:

```python
def test_dummy():
    api = DummyView()
    result = api.dummy(**args)
    assert result['dummy_int'] == 1
```

In the example above, we create an instance of `DummyAPI` and call the `dummy` REST call as if it were a function.

**query parameters/post payload are treated as function arguments**


## Package Testing

The `drf-api-action` library includes tests to ensure the functionality works as expected. To run the tests, follow these steps:

1. Navigate to the root directory of the `drf-api-action/` project.
```bash
cd tests/
```

2. Run the tests using `pytest`

 ```shell
 python -m pytest -vv
 ```

The tests will be executed, and the results will be displayed in the console.

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
