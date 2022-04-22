import numpy as np
import pandas as pd

cost_array = None


# cost_array[0, 0] = command
# cost_array[1, 0] = message
# cost_array[:, 1] = destination names
# cost_array[:, 2] = path cost
# cost_array[:, 3] = next addressee
# cost_array[:, 4] = addressee address


def bellman_ford(final_destination: str, cost: int, sender_name: str) -> None:
    destination_index = np.argwhere(cost_array[:, 1] == final_destination)

    sender_index = np.argwhere(cost_array[:, 1] == sender_name)
    sender_cost = int(cost_array[sender_index, 2])
    new_cost = cost + sender_cost

    new_cost_smaller = int(cost_array[destination_index, 2]) > new_cost
    no_connection_yet = int(cost_array[destination_index, 2]) < 0

    if no_connection_yet or new_cost_smaller:
        cost_array[destination_index, 2] = cost + sender_cost
        cost_array[destination_index, 3] = sender_name
        # TODO send to all neighbors


if __name__ == '__main__':
    cost_list = [["command", "Node1", 0, "Node1", "192.7123912"], ["message", "Node2", 5, "Node2", ".102837"],
                 ["", "Node3", 2, "Node3", ""], ["", "Node4", -1, "", ""]]
    cost_list.index()
    cost_array = np.array(cost_list)
    print(cost_array)
    bellman_ford("Node2", 1, "Node3")
