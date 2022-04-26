import numpy as np
import shortest_path as sp


cost_array = None


def initialize(init_array):
    global cost_array
    cost_array = init_array[1:, :]
    shape = np.shape(init_array)
    cost_array = np.vstack((np.full(shape[1], ""), cost_array))


def update(update_array):
    global cost_array
    sp.bellman_ford(cost_array, update_array[0], int(update_array[1]), update_array[2])


if __name__ == '__main__':
    NotImplemented
    # cost_list = [["command", "Node1", 0, "Node1", "192.7123912", 65432],
    #              ["message", "Node2", 5, "Node2", ".102837", 65432],
    #              ["", "Node3", 2, "Node3", "", 65432],
    #              ["", "Node4", -1, "", "", 65432]]
    # cost_array1 = np.array(cost_list).T
    #
    # initialize(cost_array1)
    # print(cost_array)
    #
    # array = ["Node2", 1, "Node3"]
    # array = np.array(array)
    # update(array)
    # print(cost_array)
