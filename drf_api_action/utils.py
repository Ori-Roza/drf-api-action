from typing import Optional


class CustomRequest:
    """
    Mock for a custom request
    """

    def __init__(self, data, query_params):
        self.data = data
        self.query_params = query_params

    def build_absolute_uri(self, _=None):
        return ''


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
