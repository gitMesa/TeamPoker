
player_order = [0, 1, 2, 3, 4, 5, 6]

for i in range(player_order.index(4)):
    player_order.append(player_order[0])
    player_order.remove(player_order[0])

print(player_order)