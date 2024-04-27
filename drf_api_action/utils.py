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
        return ''


def run_as_api(self, func, serializer_class, *args, **kw):
    kw.update({"serializer_class": serializer_class})
    request = CustomRequest(kw, kw)
    self.kwargs = kw
    self.request = request

    try:
        if hasattr(func, 'detail'):
            # called from pytest fixture
            ret = func(request, **kw)
        else:
            # called straight from viewer
            ret = func(self, request, **kw)
        if isinstance(ret.data, list):  # multiple results
            results = [dict(res) for res in ret.data]
        else:
            results = {k.lower(): v for k, v in ret.data.items()}
    except Exception as error:  # pylint: disable=broad-except
        error_type = type(error)
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
