import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

#1 - вперед
#2 - назад
#3 - вправо
#4 - влево
def move_robot(symbol):
    orientation = {
        3: "right",
        4: "left",
        1: "forward",
        2: "backward",
    }
    url = "http://127.0.0.1:8801/api/v1/robot-cells/" + orientation[symbol]
    token = "afa44b00-7d0e-4f53-b6cf-e062b81b7657c4af354b-4757-4099-b6d2-e6ec72ccc2a3"
    headers = {
        "accept": "application/json"
    }
    params = {
        "token": token
    }
    response = requests.post(url, headers=headers, params=params, data="")
    if response.status_code == 200:
        print("Успех:", response.json())
    else:
        print(f"Ошибка: {response.status_code} - {response.text}")

def get_data():
    url = "http://127.0.0.1:8801/api/v1/robot-cells/sensor-data"
    token = "afa44b00-7d0e-4f53-b6cf-e062b81b7657c4af354b-4757-4099-b6d2-e6ec72ccc2a3"
    headers = {
    "accept": "application/json"
    }
    params = {
     "token": token
    }
    response = requests.get(url, headers=headers, params=params)
    d_temp = response.json()
    data = {
        'r': d_temp['right_side_distance'],
        'l': d_temp['left_side_distance'],
        'f': d_temp['front_distance'],
        'b': d_temp['back_distance'],
        'o_x': d_temp['down_x_offset'],
        'o_y': d_temp['down_y_offset'],
        'yaw': d_temp['rotation_yaw']
    }
    return data

def scan_box(data):
    box = [0,0,0,0] 
    j=0
    for i in ['f','b','r','l']:
        if data[i] <100:
            box[j] = 1
        else: 
            box[j] = 0
        j+=1
    #Преобразование координат в зависимости от ориентации   
    if data['yaw'] == 90:
       box = [box[3]]+[box[2]]+[box[0]]+[box[1]]
    if data['yaw'] == 180:
        box = [box[1]]+[box[0]]+[box[3]]+[box[2]]
    if data['yaw'] == -90:
       box = [box[2]]+[box[3]]+[box[1]]+[box[0]]
    return box

def det_obstacle(box):
    if box == [0,0,0,0]:
        number = 0
    elif box == [0,0,0,1]:
        number = 1
    elif box == [1,0,0,0]:
        number = 2
    elif box == [0,0,1,0]:
        number = 3
    elif box == [0,1,0,0]:
        number = 4
    elif box == [0,1,0,1]:
        number = 5
    elif box == [0,1,1,0]:
        number = 6
    elif box == [1,0,1,0]:
        number = 7
    elif box == [1,0,0,1]:
        number = 8
    elif box == [0,0,1,1]:
        number = 9
    elif box == [1,1,0,0]:
        number = 10
    elif box == [1,1,1,0]:
        number = 11
    elif box == [1,0,1,1]:
        number = 12
    elif box == [1,1,0,1]:
        number = 13
    elif box == [0,1,1,1]:
        number = 14
    elif box == [1,1,1,1]:
        number = 15
    return number

# def edit_map(number,graph):

graph = {
    '1': [['2'],[15,0],0]
}   
graph['1'][1] = 10
print(graph['1'][1])


g = nx.Graph()
stack = [] #Стек обрабатываемых вершин
class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_node(self, coord):
        self.adjacency_list[coord] = {'neighbours': []}

    def can_connect(self, coord1, coord2):
        # Логика проверки доступности (например, проверка на наличие препятствий)
        # Здесь мы просто предполагаем, что все соседние клетки доступны
        return coord2 in self.adjacency_list

    def scan_and_connect(self, coord):
        # Определяем возможные смещения для соседей
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # север, юг, запад, восток
        for direction in directions:
            neighbour_coord = (coord[0] + direction[0], coord[1] + direction[1])
            if self.can_connect(coord, neighbour_coord):
                self.adjacency_list[coord]['neighbours'].append(neighbour_coord)

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_node(self, coord):
        self.adjacency_list[coord] = {'neighbours': []}

    def can_connect(self, coord1, coord2):
        return coord2 in self.adjacency_list

    def scan_and_connect(self, coord):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # север, юг, запад, восток
        for direction in directions:
            neighbour_coord = (coord[0] + direction[0], coord[1] + direction[1])
            if self.can_connect(coord, neighbour_coord):
                self.adjacency_list[coord]['neighbours'].append(neighbour_coord)

# Создаем граф
g = Graph()
map_size = (16, 16)

# Добавляем клетки на карту
for x in range(map_size[0]):
    for y in range(map_size[1]):
        g.add_node((x, y))

# Робот сканирует и соединяет клетки
for x in range(map_size[0]):
    for y in range(map_size[1]):
        g.scan_and_connect((x, y))

# Визуализация графа
G = nx.Graph()

# Добавляем узлы и рёбра в NetworkX граф
for node, data in g.adjacency_list.items():
    G.add_node(node)
    for neighbour in data['neighbours']:
        G.add_edge(node, neighbour)

# Настройка визуализации
pos = {(x, y): (y, -x) for x, y in G.nodes()}  # Позиции узлов для визуализации
nx.draw(G, pos, with_labels=True, node_size=600, node_color='lightblue', font_size=10,
        font_color='black', font_weight='bold', edge_color='gray')

# Инвертируем ось Y
plt.gca().invert_yaxis()

# Показать граф
plt.title('Graph Visualization with (0,0) in the Bottom Left Corner')
plt.show()