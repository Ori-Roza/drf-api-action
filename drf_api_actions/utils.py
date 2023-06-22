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
