def get_first_existing_value(d, keys, default=None):
    """Returns the value for the first key that exists in the dictionary.

    :param d: The dictionary to search.
    :param keys: A list of keys to check for existence in order.
    :param default: The default value to return if the key does not exist.
    :return: The value of the first existing key, or None if none are found.
    """

    return next((d[k] for k in keys if k in d), default)
