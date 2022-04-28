import numpy as np
import pandas as pd
import numpy_converter as np_c


# cost_array[0, :] = Nothing (allows for easier indexing)
# cost_array[1, :] = destination names
# cost_array[2, :] = path cost
# cost_array[3, :] = next addressee
# cost_array[4, :] = destination ip (if directly connected)
# cost_array[5, :] = destination port (if directly connected)


def bellman_ford(cost_array, final_destination: str, cost: int, sender_name: str) -> []:
    destination_index = np.argwhere(cost_array[1, :] == final_destination)

    sender_index = np.argwhere(cost_array[1, :] == sender_name)
    sender_cost = int(cost_array[2, sender_index])
    new_cost = cost + sender_cost

    new_cost_smaller = int(cost_array[2, destination_index]) > new_cost
    no_connection_yet = int(cost_array[2, destination_index]) < 0

    if not no_connection_yet and not new_cost_smaller:
        return []

    cost_array[2, destination_index] = cost + sender_cost
    cost_array[3, destination_index] = sender_name

    update_array = cost_array[:3, destination_index[0]]
    update_array[0, 0] = "update"

    print(update_array)
    return update_array

    # message = np_c.array_to_string(update_array)

    # ip_indexes = np.argwhere(cost_array[4, :] != "")
    # for ip_index in ip_indexes:
    #     ip = str(cost_array[4, ip_index])
    #     port = int(cost_array[5, ip_index])
    #     print(ip, port)
    #     # TODO send to all neighbors
    #     # send(message, (ip, port))


if __name__ == '__main__':
    cost_list = [["command", "Node1", 0, "Node1", "192.7123912", 65432],
                 ["message", "Node2", 5, "Node2", ".102837", 65432],
                 ["", "Node3", 2, "Node3", "", 65432],
                 ["", "Node4", -1, "", "", 65432]]
    cost_array1 = np.array(cost_list).T

    cost_array = cost_array1[1:, :]
    shape = np.shape(cost_array1)
    cost_array = np.vstack((np.full(shape[1], ""), cost_array))
    print(cost_array)

    bellman_ford(cost_array, "Node2", 1, "Node3")

