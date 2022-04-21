import numpy as np


cost_array = None


# update has form [final destination: str, ]
def bellman_ford(final_destination: str, cost: int, sender_name: str) -> None:
    destination_index = np.argwhere(cost_array[:, 0] == final_destination)

    sender_index = np.argwhere(cost_array[:, 0] == sender_name)
    sender_cost = int(cost_array[sender_index, 1])
    new_cost = cost+sender_cost

    new_cost_smaller = int(cost_array[destination_index, 1]) > new_cost
    no_connection_yet = int(cost_array[destination_index, 1]) < 0

    if no_connection_yet or new_cost_smaller:
        cost_array[destination_index, 1] = cost + sender_cost
        cost_array[destination_index, 2] = sender_name
        # TODO send to all neighbors


if __name__ == '__main__':
    cost_list = [["Node1", 0, "Node1"], ["Node2", 5, "Node2"], ["Node3", 2, "Node3"], ["Node4", -1, ""]]
    cost_array = np.array(cost_list)
    print(cost_array)
    bellman_ford("Node2", 1, "Node3")
    print(cost_array)
