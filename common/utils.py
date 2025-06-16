import time


def get_first_existing_value(d, keys, default=None):
    """Returns the value for the first key that exists in the dictionary.

    :param d: The dictionary to search.
    :param keys: A list of keys to check for existence in order.
    :param default: The default value to return if the key does not exist.
    :return: The value of the first existing key, or None if none are found.
    """

    return next((d[k] for k in keys if k in d), default)


def retry_with_exponential_backoff(func, args=(), kwargs=None, exceptions=(Exception,), max_retries=7, base_delay=5,
                                   max_delay=600):
    """
    Executes a function with exponential backoff retry on specified exceptions.

    :param func: Callable to execute
    :param args: Positional arguments for the function
    :param kwargs: Keyword arguments for the function
    :param exceptions: Tuple of exception classes to catch and retry on
    :param max_retries: Maximum number of retries before raising
    :param base_delay: Initial delay (in seconds) before retrying
    :param max_delay: Maximum delay (in seconds) allowed between retries
    :return: The return value of the function if successful
    :raises: Last exception encountered if retries are exhausted
    """

    if kwargs is None:
        kwargs = {}

    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            return func(*args, **kwargs)
        except exceptions as e:
            last_exception = e
            if attempt == max_retries:
                break
            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            time.sleep(delay)

    raise RuntimeError('Exceeded max retries ({})'.format(max_retries)) from last_exception
