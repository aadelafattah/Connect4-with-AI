import math
from queue import PriorityQueue

data_set = [
    [3, 5, 3.1, True],
    [3, 5, 2.0, False],
    [2, 7, 3.5, True],
    [4, 9, 2.5, True],
    [3, 11, 3.9, False],
    [2, 3, 2.9, False],
    [3, 3, 1.9, False],
    [4, 9, 3.2, True]
]

tests = [
    [2, 2, 3.0],
    [3, 3, 4.0],
    [4, 6, 2.0],
    [2, 5, 3.5],
]


def get_min_max(data, feature):
    min_value = max_value = data[0][feature]
    for record in data:
        if max_value < record[feature]:
            max_value = record[feature]
        if min_value > record[feature]:
            min_value = record[feature]

    return min_value, max_value


def normalize_data_set(data, number_of_labels):
    for feature in range(0, len(data[0]) - number_of_labels):
        (min_value, max_value) = get_min_max(data, feature)
        for record in data:
            record[feature] = (record[feature] - min_value) / (max_value - min_value)


def distance(set_1, set_2):
    if len(set_1) == len(set_2):
        sum_square = 0
        for i in range(len(set_1)):
            sum_square += (set_1[i] - set_2[i]) ** 2
        return math.sqrt(sum_square)
    return -1


def get_label(K, record, data):
    near_neighbour_queue = PriorityQueue()
    for i in range(len(data)):
        near_neighbour_queue.put((distance(record, data[i][0:-1]), data[i]))

    label_1 = 0
    label_2 = 0
    for j in range(K):
        (d, record_of_distance_d) = near_neighbour_queue.get()
        if record_of_distance_d[-1]:
            label_1 += 1
        else:
            label_2 += 1

    if label_1 > label_2:
        return True
    elif label_1 <= label_2:
        return False


normalize_data_set(data_set, 1)
for test in tests:
    print(f"Student{test} has{' ' if (get_label(3, test, data_set)) else ' not '}passed the exam")
