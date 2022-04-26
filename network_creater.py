import pickle

import numpy as np

if __name__ == '__main__':
    connections = []
    connections.append([
        ["Node1", 0, "Node1", "localhost", 65432],
        ["Node2", 5, "Node1", "192.168.1.x", 65432],
        ["Node3", 5, "Node1", "192.168.1.x", 65432]])
    connections.append([
        ["Node2", 0, "Node1", "localhost", 65432],
        ["Node1", 5, "Node1", "192.168.1.x", 65432],
        ["Node4", 5, "Node1", "192.168.1.x", 65432],
        ["Node5", 2, "Node1", "192.168.1.x", 65432]])

    print(connections)

    connections = np.ndarray(connections, dtype=str)
    print(connections)

    connections[2] = [
        ["Node3", 0, "Node1", "localhost", 65432],
        ["Node1", 2, "Node1", "192.168.1.x", 65432],
        ["Node5", 2, "Node1", "192.168.1.x", 65432]]
    connections[3] = [
        ["Node3", 0, "Node1", "localhost", 65432],
        ["Node1", 2, "Node1", "192.168.1.x", 65432],
        ["Node5", 2, "Node1", "192.168.1.x", 65432]]
