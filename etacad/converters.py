def to_list(arg: list | float) -> list | None:
    """
    Converts a float value into a single-element list or returns the original list.

    :param arg: A value that can be a list or a float.
    :type arg: list | float
    :return: The original list if `arg` is already a list, a list containing `arg` if it's a float,
             or None if `arg` is None.
    :rtype: list | None
    """
    if arg is None:
        return arg
    if isinstance(arg, list):
        return arg
    return [arg]
