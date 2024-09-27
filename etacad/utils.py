# Imports.
# Local imports.

# External imports.


def expand_dictionary(dictionary) -> list:
    """
    Expands a dictionary into a list based on the dictionary's values.

    :param dictionary: A dictionary where keys represent bar numbers and values represent the quantity of each number.
    :type dictionary: dict
    :return: A list with each bar number repeated according to its value in the dictionary.
    :rtype: list
    """
    expanded_list = []
    for key, value in dictionary.items():

        expanded_list.extend([key] * value)

    return expanded_list


def gen_symmetric_list(dictionary: dict, nomenclature: str = None, number_init: int = None, factor: float = 1) -> tuple:
    """
    Generates a symmetric list and a list of denominations based on the provided dictionary.

    :param dictionary: A dictionary where keys represent bar diameters and values represent the quantity of bars.
    :type dictionary: dict
    :param nomenclature: Prefix to use in the denomination, defaults to None.
    :type nomenclature: str, optional
    :param number_init: Initial number for the denomination, defaults to None.
    :type number_init: int, optional
    :param factor: Factor by which the bar diameter is divided, defaults to 1.
    :type factor: float, optional
    :return: A tuple containing a symmetric list of bar diameters and a corresponding list of denominations.
    :rtype: tuple
    """
    if nomenclature is None:
        nomenclature = "#"

    if number_init is None:
        n = 0
    else:
        n = number_init

    first_odd = False
    symmetryc_list = []
    denomination_list = []

    for key, value in sorted([*dictionary.items()]):
        key_factored = key / factor
        for i in range(value // 2):
            symmetryc_list.insert(0, key_factored)
            symmetryc_list.insert(len(symmetryc_list), key_factored)
            denomination_list.insert(0, "{2}{3} {0}Ø{1}".format(value, key, nomenclature, n))
            denomination_list.insert(len(denomination_list), "{2}{3} {0}Ø{1}".format(value, key, nomenclature, n))

        if is_odd(value):
            symmetryc_list.insert(len(symmetryc_list) // 2, key_factored)
            denomination_list.insert(len(denomination_list) // 2, "{2}{3} {0}Ø{1}".format(value, key, nomenclature, n))
            if first_odd:
                return ()
            else:
                first_odd = True
        n += 1

    return symmetryc_list, denomination_list


def is_odd(number):
    """
    Checks if a number is odd.

    :param number: The number to check.
    :type number: int
    :return: True if the number is odd, False otherwise.
    :rtype: bool
    """
    return bool(number % 2)


def max_per_position(*lists):
    """
    Returns a new list containing the maximum value at each position
    across multiple input lists.

    :param lists: A variable number of lists (at least two) with numerical values.
    :type lists: list of float or int
    :raises ValueError: If the lists do not all have the same length.
    :return: A list containing the maximum value at each position.
    :rtype: list

    :example:

    >>> list1 = [1.5, 3.2, 4.7, 2.9]
    >>> list2 = [2.1, 2.8, 5.0, 1.7]
    >>> list3 = [1.8, 3.3, 4.6, 2.5]
    >>> max_per_position(list1, list2, list3)
    [2.1, 3.3, 5.0, 2.9]
    """
    # Check that all lists have the same length.
    if not all(len(lst) == len(lists[0]) for lst in lists):
        raise ValueError("All lists must have the same length.")

    # Use zip to group elements by their position across all lists.
    return [max(values) for values in zip(*lists)]


def text_width_estimation(text: str, text_height: float, proportion: float = 1) -> float:
    """
    Estimate the width of a text string based on its height.

    This function approximates the width of a text string by assuming each character
    in the string occupies a width proportional to the given text height.

    :param text: The text string whose width needs to be estimated.
    :type text: str
    :param text_height: The height of the text used for the width estimation.
    :type text_height: float
    :param proportion: The proportion estimator.
    :type proportion: float
    :return: The estimated width of the text string.
    :rtype: float

    :example:

    >>> text_width_estimation("Hello", 10.0)
    37.5

    . note::
       This is a simple estimation and may not be accurate for all fonts or
       character sets. The constant `0.65` for default used for width estimation
       is based on a typical average and might need adjustment for different fonts
       or styles.
    """
    text_width = 0
    for character in text:
        text_width += text_height * proportion

    return text_width


def str_to_dict_bar(data: str) -> dict:
    """
    Converts a string representing bars into a dictionary.

    :param data: A string where each element is in the format "quantity db diameter" and separated by "+".
    :type data: str
    :return: A dictionary where keys are bar diameters and values are the corresponding quantities.
    :rtype: dict
    """
    data_list = data.replace(" ", "").split("+")

    data_dict = {}
    for element in data_list:
        key_value = element.split("db")

        data_dict[int(key_value[1])] = int(key_value[0])

    data_dict_ordered = {k: v for k, v in sorted(data_dict.items(), key=lambda item: item[0], reverse=False)}

    return data_dict_ordered


def unpack_nested_dicts(nested_dict: dict | list[dict]):
    """
    Recursively unpacks all values from a (potentially) nested dictionary and returns them in a single list.

    :param dict nested_dict: The nested dictionary to unpack.
    :return: A list of all the values from the dictionary, including nested dictionaries.
    :rtype: list

    The function handles dictionaries with multiple levels of nesting. If a value is a dictionary, it recursively
    processes it. Non-dictionary values are directly appended to the result list.

    :example:
    >>> nested_dict = {
           'key1': {'a': 1, 'b': {'x': 7, 'y': 8}, 'c': 3},
           'key2': {'d': 4, 'e': 5},
           'key3': 6,
           'key4': {'f': {'g': 9, 'h': 10}},
           'key5': 'value'}

    >>> result = unpack_nested_dicts(nested_dict)
    [1, 7, 8, 3, 4, 5, 6, 9, 10, 'value']
    """
    print(nested_dict)
    result = []
    if isinstance(nested_dict, list) and all([isinstance(dictionary, dict) for dictionary in nested_dict]):
        for dictionary in nested_dict:
            for value in dictionary.values():
                if isinstance(value, dict):  # If the value is another dictionary, process it recursively.
                    result.extend(unpack_nested_dicts(value))
                elif isinstance(value, list):
                    result += value  # If not a dictionary, add the value directly.
                else:
                    result.append(value)
        return result

    elif isinstance(nested_dict, dict):
        for value in nested_dict.values():
            if isinstance(value, dict):  # If the value is another dictionary, process it recursively.
                result.extend(unpack_nested_dicts(value))
            elif isinstance(value, list):
                result += value  # If not a dictionary, add the value directly.
            else:
                result.append(value)
        return result

    else:
        return nested_dict
