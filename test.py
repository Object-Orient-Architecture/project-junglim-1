"""test_list = [0, 1, 2, 3, 7, 4, 5, 6]
sorted()

test_list.sort()
# test_list.sort()
print(test_list)

"""


# test_list.sort()
# test_list_sorted = sorted(test_list)
# print(test_list_sorted, test_list)
def first_element():
    print("print")


def pick_second(k):
    return k[1]


def activate(list, func):
    for elm in list:
        print(func(elm))


test_list = [("이름", 10), ("이름", 20), ("이름", 13)]

activate(test_list, pick_second)
