from rest_framework.decorators import action

from drf_api_action.utils import CustomRequest
from drf_api_action.exceptions import ActionsAPIException, ActionsAPIExceptionMiddleware


def action_api(methods=None, detail=None, url_path=None, url_name=None, **kwargs):
    """
    custom decorator that handles 2 ways of calling conventions:
        * rest
        * api

    if function is executed as rest, then mark a ViewSet method as a routable action
    otherwise, injects the kwargs and create a CustomRequest in order to run the function as an api call:

    *** View must inherit APIRestMixin in order to use action_api otherwise ApiActionsException is raised ***

    class DummyView(APIRestMixin, ModelViewSet):
        queryset = DummyModel.objects.all()
        serializer_class = DummySerializer

        @action_api(detail=True, methods=["get"], serializer_class=DummySerializer)
        def dummy_func(self, request, **kwargs):
            serializer = self.get_serializer(instance=self.get_object())
            return Response(data=serializer.data, status=status.HTTP_200_OK)


    view = DummyView()
    results = view.dummy_func(**args)

    returns response.data output and if there is an error raise ApiActionsException


    actions docs:

    :param methods: A list of HTTP method names this action responds to.
                    Defaults to GET only.
    :param detail: Required. Determines whether this action applies to
                   instance/detail requests or collection/list requests.
    :param url_path: Define the URL segment for this action. Defaults to the
                     name of the method decorated.
    :param url_name: Define the internal (`reverse`) URL name for this action.
                     Defaults to the name of the method decorated with underscores
                     replaced with dashes.
    :param kwargs: Additional properties to set on the view.  This can be used
                   to override viewset-level *_classes settings, equivalent to
                   how the `@renderer_classes` etc. decorators work for function-
                   based API views.


    """
    methods = ['get'] if methods is None else methods
    methods = [method.lower() for method in methods]

    serializer_class = kwargs.pop("serializer_class")

    def decorator(func):
        def run_as_rest(self, request, **kw):
            return func(self, request, **kw)

        def run_as_api(self, **kw):
            kw.update({"serializer_class": serializer_class})
            request = CustomRequest(kw, kw)
            self.kwargs = kw
            self.request = request

            try:
                ret = func(self, request, **kw)
                if isinstance(ret.data, list):  # multiple results
                    results = [dict(res) for res in ret.data]
                else:
                    results = {k.lower(): v for k, v in ret.data.items()}
            except Exception as error:  # pylint: disable=broad-except
                error_type = type(error)
                raised_exception = ActionsAPIExceptionMiddleware(error,
                                                                 error_type=error_type,
                                                                 traceback=error.__traceback__)  # fixing stack frames
                raise raised_exception  # pylint: disable=raising-non-exception

            return results

        def run_func_by_method(self, request=None, **kw):
            if not hasattr(self, 'api_mixin_exists'):
                raise ActionsAPIException("in order to use action_api you must inherit APIRestMixin in the view")
            if request:
                return run_as_rest(self, request, **kw)
            return run_as_api(self, **kw)

        run_func_by_method.kwargs = kwargs
        run_func_by_method.__name__ = func.__name__

        return action(methods=methods,
                      detail=detail,
                      url_path=url_path,
                      url_name=url_name,
                      serializer_class=serializer_class, **kwargs)(run_func_by_method)

    return decorator
