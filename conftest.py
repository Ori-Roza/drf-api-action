

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "action_api: add ViewSet class"
    )