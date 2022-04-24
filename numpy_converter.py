import numpy as np
# from io import BytesIO
# import pickle


# # not needed, for documentation only
# def from_array_to_byte(np_array):
#     bytes_ = BytesIO()
#     np.save(bytes_, np_array, allow_pickle=True)
#     return bytes_.getvalue()
#
#
# # not needed, for documentation only
# def from_byte_to_array(bytes_):
#     bytes_ = BytesIO(bytes_)
#     np_array = np.load(bytes_, allow_pickle=True)
#     return np_array
#
#
# # not needed, for documentation only
# def from_array_to_pickle(np_array):
#     pickled = pickle.dumps(np_array)
#     return pickled
#
#
# # not needed, for documentation only
# def from_pickle_to_array(pickled):
#     np_array = pickle.loads(pickled)
#     return np_array


# converts a numpy array to a string, with "," and ";" as separators
# input: numpy array
# output: string
def array_to_string(array: np.ndarray):
    as_string = ""
    for part_array in array:
        for element in part_array:
            as_string += str(element).replace(",", "(comma)").replace(";", "(semicolon)") + ","
        as_string = as_string[0:-1]+";"
    as_string = as_string[0:-1]
    print(as_string)
    return as_string


# converts a properly formatted string to a numpy array
# input: string
# output: numpy array
def string_to_array(message: str):
    array_as_list = message.split(";")
    print(array_as_list)
    for i in range(len(array_as_list)):
        array_as_list[i] = array_as_list[i].split(",")

    array = np.array(array_as_list, dtype=str)
    print(array)
    return array


if __name__ == '__main__':
    array1 = np.array([["1,", 2, 3], [4, 5, 6], [7, 8, 9]])
    print(array1)
    match string_to_array(array_to_string(array1))[0,0]:
        case "1":
            print("case1")
    # print(array)
    # bytes_2 = from_array_to_byte(array)
    # print(bytes_2)
    # decoded_array = from_byte_to_array(bytes_2)
    # print(decoded_array)
    #
    # pickled = from_array_to_pickle(array)
    # print(pickled)
    # decoded_array2 = from_pickle_to_array(pickled)
    # print(decoded_array2)

