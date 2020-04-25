

test_list = [0, 1, 3, 4, 5]

raiser = 3

for i in range(test_list.index(raiser)):
    test_list.append(test_list[0])
    test_list.remove(test_list[0])

print(test_list)

