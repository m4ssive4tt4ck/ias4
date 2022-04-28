import numpy as np
import shortest_path as sp


cost_array = None
pending_messages = []  # list of tuples with ((ip, port), np_array))
known_connections = []  # list of (ip, port)


def initialize(init_array):
    global cost_array
    cost_array = init_array[1:, :]
    shape = np.shape(init_array)
    cost_array = np.vstack((np.full(shape[1], ""), cost_array))
    global known_connections
    known_connections = []
    message_arrays = []
    indexes = np.argwhere(cost_array[4, :] != "")
    for index in indexes:
        known_connections.append((str(cost_array[4, index][0]), int(cost_array[5, index])))
        message_arrays.append(np.array(["update", cost_array[1, index], cost_array[2, index]], dtype=str))
    for connection in known_connections:
        for message_array in message_arrays:
            pending_messages.append((connection, message_array))


def update(update_array):
    global cost_array
    message = sp.bellman_ford(cost_array, update_array[0], int(update_array[1]), update_array[2])
    for connection in known_connections:
        pending_messages.append((connection, message))


if __name__ == '__main__':

    cost_list = [["command", "Node1", 0, "Node1", "192.7123912", 65432],
                 ["message", "Node2", 5, "Node2", ".102837", 65432],
                  ["", "Node3", 2, "Node3", "", 65432],
                  ["", "Node4", -1, "", "", 65432]]
    cost_array1 = np.array(cost_list).T

    initialize(cost_array1)
    print(cost_array)
    array = ["Node2", 1, "Node3"]
    array = np.array(array)
    update(array)
    print(cost_array)
