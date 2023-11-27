class ActionsAPIException(RuntimeError):
    pass


class ActionsAPIExceptionMiddleware:
    def __new__(cls, *args, **kwargs):
        error_type = kwargs.pop('error_type', Exception)
        error = error_type(*args)
        error.__traceback__ = kwargs.pop('traceback', error_type.__traceback__)
        return error
