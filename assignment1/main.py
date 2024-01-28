#!/usr/bin/python3

from graph import Graph,Vertex
from PIL import Image, ImageDraw

graph = Graph()
image_file = "graph.jpg"

# bounds for the graph image
x_lower = 0
x_upper = 100
y_lower = 0
y_upper = 100

# dimensions of graph image
width = x_upper - x_lower
height = y_upper - y_lower
node_radius = 2

# color constants for PIL
gray = (100, 100, 100)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0,128,0)
purple = (153, 119, 187)

# create empty PIL image to draw on in memory, image saved at end
image = Image.new("RGB", (width, height), black)
draw = ImageDraw.Draw(image)

# read coords and add vertices to graph
with open("coords.txt", "r") as file_coords:
    for line in file_coords :
        values = line.split()
        print("vertex x%f y%f" % (float(values[1]), float(values[2])))
        vertex = Vertex(int(values[0]), (float(values[1]), float(values[2])))
        # add to graph
        graph.add_vertex(vertex)
        # draw
        x1 = int(vertex.coords[0]) - node_radius
        y1 = int(vertex.coords[1]) - node_radius
        x2 = int(vertex.coords[0]) + node_radius
        y2 = int(vertex.coords[1]) + node_radius
        draw.ellipse((x1, y1, x2, y2), purple)

image.save(image_file)

print("Graphs image written to: %s" % image_file)
