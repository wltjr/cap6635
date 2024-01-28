#!/usr/bin/python3

from graph import Graph,Vertex
from PIL import Image, ImageDraw, ImageFont

graph = Graph()
image_file = "graph.jpg"

# bounds for the graph image
x_lower = 0
x_upper = 1536
y_lower = 0
y_upper = 1536

# dimensions of graph image
width = x_upper - x_lower
height = y_upper - y_lower
node_radius = 20

# color constants for PIL
gray = (100, 100, 100)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0,128,0)
pink = (255, 105, 180)
purple = (153, 119, 187)

# create empty PIL image to draw on in memory, image saved at end
image = Image.new("RGB", (width, height), black)
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", node_radius)

# read coords and add vertices to graph
with open("coords.txt", "r") as file_coords:
    for line in file_coords :
        values = line.split()
        vertex = Vertex(int(values[0]), (float(values[1]), float(values[2])))
        # add to graph
        graph.add_vertex(vertex)
        # draw node with id
        x1 = int(vertex.coords[0]) - node_radius
        y1 = int(vertex.coords[1]) - node_radius
        x2 = int(vertex.coords[0]) + node_radius
        y2 = int(vertex.coords[1]) + node_radius
        draw.ellipse((x1, y1, x2, y2), purple)
        if vertex.id < 10:
            draw.text((int(vertex.coords[0]) - node_radius/4, int(vertex.coords[1]) - node_radius/2),
                    str(vertex.id), font=font)
        else :
            draw.text((int(vertex.coords[0]) - node_radius/2, int(vertex.coords[1]) - node_radius/2),
                    str(vertex.id), font=font)

# read graph edges
with open("graph.txt", "r") as file_graph:
    for line in file_graph :
        ids =  [float(i) for i in line.split()]
        ids_len = len(ids)
        # first id is me rest are my edges
        my_id = int(ids[0])
        vertex = graph.vertices[my_id]

        # go through remaining ids on line after the first
        for i in range(1,ids_len):
            neighbor = graph.vertices[ids[i]]
            if not graph.has_edge(vertex, neighbor) :
                print("adding edge from %d to %d" % (my_id , ids[i]))
                graph.add_edge(vertex, neighbor)
                draw.line([vertex.coords, neighbor.coords], gray, width=2)

    file_graph.close()

# scale down to reduce pixelation
image = image.resize((width // 2, height // 2), resample=Image.LANCZOS)
image.save(image_file)

print("Graphs image written to: %s" % image_file)
