import requests
import numpy as np
import networkx as nx

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

def DFA(graph,stack,position):
    while not stack == True:
        neghbours = []
        v = stack.pop()
        data = get_data()
        box = scan_box(data)
        for i in range(len(box)):
            if box[i] ==0:
                if i==0 and not g.has_edge(v,v+16):
                    g.add_edge(v,v+16)
                elif i==1 and not g.has_edge(v,v-16):
                    g.add_edge(v,v-16)
                elif i==2 and not g.has_edge(v,v+1):
                    g.add_edge(v,v+1)
                elif i==3 and not g.has_edge(v,v-1):
                    g.add_edge(v,v-1)
        for n in g.neighbors(v):
            neghbours = neghbours+[n]
        g.nodes[v]['neghbours'] = neghbours
        g.nodes[v]['visible'] = True
        for i in neghbours:
            if g.nodes[i]['visible'] != True:
                g.nodes[i]['parent'] = v
                stack.append(i)
        Move_robot(g,position,v,data['yaw'])
        position = v








g = nx.Graph()
stack = []
j = 15
start = 0
for i in range(256):
    if i%16==0 and i!=0:
        j-=1
    g.add_node(i,coord = np.array([j,i%16]), visible = "False", neighbours = [], parent = 0)
stack.append(start)
DFS(g,stack,start)
