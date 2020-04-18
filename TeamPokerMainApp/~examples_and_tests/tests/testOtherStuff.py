

def get_table_spots_from_client_index_point_of_view(client_index):
    table_spots = [0, 1, 2, 3, 4, 5, 6, 7]
    for i in range(table_spots.index(client_index)):
        table_spots.append(table_spots[0])
        table_spots.remove(table_spots[0])
    return table_spots


print(get_table_spot_from_client_index(2))

