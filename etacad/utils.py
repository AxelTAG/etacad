# Imports.
# Local imports.

# External imports.


# Function that returns list of bar numbers.
def expand_dictionary(dictionary) -> list:
    expanded_list = []
    for key, value in dictionary.items():

        expanded_list.extend([key] * value)

    return expanded_list


# Function that returns a simetric list.
def gen_symmetric_list(dictionary: dict, nomenclature: str = None, number_init: int = None, factor: float = 1) -> tuple:

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


# Function that check is an odd number.
def is_odd(number):
    return bool(number % 2)


# Function that analize str for bars.
def str_to_dict_bar(data: str) -> dict:
    data_list = data.replace(" ", "").split("+")

    data_dict = {}
    for element in data_list:
        key_value = element.split("db")

        data_dict[int(key_value[1])] = int(key_value[0])

    data_dict_ordered = {k: v for k, v in sorted(data_dict.items(), key=lambda item: item[0], reverse=False)}

    return data_dict_ordered
