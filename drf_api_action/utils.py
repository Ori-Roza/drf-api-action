from typing import Optional
from drf_api_action.exceptions import ActionsAPIExceptionMiddleware


class CustomRequest:
    """
    Mock for a custom request
    """

    def __init__(self, data, query_params):
        self.data = data
        self.query_params = query_params

    def build_absolute_uri(self, _=None):
        """
        mocking django/http/request.py::HTTPRequest::build_absolute_uri
        It's irrelevant since we do not provide any web resource
        """
        return ''


def run_as_api(self, func, serializer_class, *args, **kw):
    # adding to the view the request & kwargs including the serializer class
    kw.update({"serializer_class": serializer_class})  # adding serializer class from @action
    # decorator into our instance
    request = CustomRequest(kw, kw)
    self.kwargs = kw  # adding our enhanced kwargs into instance kwargs
    self.request = request  # mocking request with our arguments as data in the instance

    try:
        ret = func(request, **kw)
        if isinstance(ret.data, list):  # multiple results
            results = [dict(res) for res in ret.data]
        else:  # only one json
            results = {k.lower(): v for k, v in ret.data.items()}
    except Exception as error:  # pylint: disable=broad-except
        error_type = type(error)
        # re-constructing the error with the actual traceback
        raised_exception = ActionsAPIExceptionMiddleware(*error.args,
                                                         error_type=error_type,
                                                         traceback=error.__traceback__)  # fixing stack frames
        raise raised_exception  # pylint: disable=raising-non-exception

    return results


def extract_page_number(data_input: Optional[str]) -> Optional[int]:
    """
    extracts the page number from restframework pagination output string
    :param data_input: restframework pagination output string
    :return: None if data_input is None else the page number extracted
    """
    if data_input is None:
        return None
    if data_input == '':
        return 1
    return int(data_input.split("=")[-1])


def extract_limit(data_input: Optional[str]) -> Optional[int]:
    """
    extracts the limit from restframework pagination output string
    :param data_input: restframework pagination output string
    :return: None if data_input is None else the limit extracted
    """
    if data_input is None:
        return None
    return int(data_input.split("&")[0].split("=")[1])


def extract_next_offset(data_input: Optional[str]) -> Optional[int]:
    """
    extracts the limit from restframework pagination output string
    :param data_input: restframework pagination output string
    :return: None if data_input is None else the limit extracted
    """
    if data_input is None:
        return None
    return int(data_input.split("&")[1].split("=")[1])
