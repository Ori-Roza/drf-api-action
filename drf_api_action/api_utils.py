from drf_api_action.exceptions import ActionsAPIExceptionMiddleware
from drf_api_action.utils import CustomRequest


def run_as_api(self, func, serializer_class, *args, **kw):
    kw.update({"serializer_class": serializer_class})
    request = CustomRequest(kw, kw)
    self.kwargs = kw
    self.request = request

    try:
        if hasattr(func, 'detail'):
            ret = func(request, **kw)
        else:
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
