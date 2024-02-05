#!/usr/bin/python

import os
from graph import Graph,Vertex
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import BOTH, Button, Entry, Frame, IntVar, Label, LEFT, RIGHT, Tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Combobox

class ui:
    """
    User Interface class displays GUI for the project and is the main class
    """

    default_coord_filename = "coords.txt"
    default_graph_filename = "graph.txt"
    label_graph = None

    def centerWindow(self):
        """
        Center the window in screen
        """
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_pathname(self.root.winfo_id()))


    def createGraph(self, master, action = None):
        """
        Open file selection dialog
        """

        # form validation
        if action != None:
            if self.cb_start['values'] == '' or self.cb_start['values'] == '':
                mb.showerror("Missing Graph Attributes",
                             "Please press the \"Create Graph\" button")
                return
            elif self.cb_start.get() == '':
                mb.showerror("Missing Start Node/Vertex",
                             "Please select a Start node/vertex")
                return
            elif self.cb_goal.get() == '':
                mb.showerror("Missing Goal Node/Vertex",
                             "Please select a Goal node/vertex")
                return
            elif self.cb_start.get() == self.cb_goal.get():
                mb.showerror("Missing Path Goal is Start",
                             "Please a different Start and Goal node/vertex")
                return

        graph = Graph()
        image_file = "graph.jpg"

        # dimensions of graph image
        width = 1536
        height = 1536
        node_radius = 20

        # color constants for PIL
        gray = (100, 100, 100)
        black = (0, 0, 0)
        red = (255, 0, 0)
        green = (0,128,0)
        pink = (255, 105, 180)
        purple = (153, 119, 187)

        # create empty PIL image to draw on in memory, image saved at end
        image = Image.new("RGBA", (width, height), (255, 0, 0, 0))
        lines = Image.new("RGB", (width, height), black)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", node_radius)

        # read coords and add vertices to graph
        with open(self.entry_coords.get(), "r") as file_coords:
            for line in file_coords :
                values = line.split()
                vertex = Vertex(int(values[0]), (float(values[1]), float(values[2])))
                # add to graph
                graph.add_vertex(vertex)
                # add to comboboxes
                self.cb_goal['values'] = tuple(list(self.cb_goal['values']) + [vertex.id])
                self.cb_start['values'] = tuple(list(self.cb_start['values']) + [vertex.id])
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
        with open(self.entry_graph.get(), "r") as file_graph:
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
                        ImageDraw.Draw(lines).line([vertex.coords, neighbor.coords], gray, width=4)

            file_graph.close()

        path = None
        if action == "A*":
            # get A* path from start to goal
            path = graph.aStar(graph.vertices[int(self.cb_start.get())],
                               graph.vertices[int(self.cb_goal.get())])
        elif action == "Dijkstra":
            # get Dijkstra path from start to goal
            path = graph.dijkstra(graph.vertices[int(self.cb_start.get())],
                                  graph.vertices[int(self.cb_goal.get())])
        if path:
            path_len = len(path) - 1
            print("%s path: %s" % (action, path))
            for i in range(0, path_len):
                ImageDraw.Draw(lines).line([graph.vertices[path[i]].coords,
                                            graph.vertices[path[i+1]].coords], pink, width=4)
            self.label_graph.destroy()

        # paste transparent vertices with ids over lines
        lines.paste(image, (0, 0), image)
        image = lines

        # scale down to reduce pixelation
        image = image.resize((width // 2, height // 2), resample=Image.LANCZOS)
        image.save(image_file)

        print("Graph image written to: %s" % image_file)

        tkImage = ImageTk.PhotoImage(image)
        self.label_graph = Label(master, image = tkImage)
        self.label_graph.image = tkImage
        self.label_graph.pack(expand = True, fill = BOTH)
        self.centerWindow()


    def getFileName(self, title):
        """
        Open file selection dialog to select a file

        :param title a title to be added to the dialog title
        :return the base filename
        """
        filename = fd.askopenfilename(filetypes=[("Text files","*.txt")],
                                      initialdir=".",
                                      title=("Select " + title + " File"))

        if filename == () or filename == "":
            return

        return os.path.basename(filename)


    def setEntry(self, entry, text):
        """
        Clear and set new text for a entry field

        :param entry tkinter entry widget object
        :param text entry field text
        """
        entry.delete(0, 'end')
        entry.insert(0, text)


    def openCoordsFileCallback(self, title):
        """
        Coords file open callback method
        """
        self.setEntry(self.entry_coords, self.getFileName(title))


    def openGraphFileCallback(self, title):
        """
        Graph file open callback method
        """
        self.setEntry(self.entry_graph, self.getFileName(title))


    def reset(self):
        """
        Reset form fields
        """
        self.cb_goal.set("")
        self.cb_start.set("")
        self.setEntry(self.entry_coords, self.default_coord_filename) 
        self.setEntry(self.entry_graph, self.default_graph_filename)
        if self.label_graph:
            self.label_graph.destroy()
        self.centerWindow()


    def run(self):
        """
        Run the GUI create the root window, frames, and all GUI widgets
        """
        root = Tk()
        root.resizable(False, False)
        root.title("Assignment 1 - A* shortest path graph search")

        frame = Frame(root)
        frame.pack()

        frame_input = Frame(frame)
        frame_input.pack()

        title = "Coordinates"
        Label(frame_input,text=title + " File").grid(row=0, column=0, padx=5, pady=5)
        self.entry_coords = Entry(frame_input)
        self.entry_coords.grid(row=0, column=1, padx=5, pady=5)

        func  = lambda: self.openCoordsFileCallback(title)
        open_file = Button(frame_input, text='Select File', command=func)
        open_file.grid(row=0, column=2, padx=5, pady=5)

        Label(frame_input,text="Start").grid(row=0, column=3, padx=5, pady=5)
        selected_start = IntVar()
        self.cb_start = Combobox(frame_input, textvariable=selected_start)
        self.cb_start.grid(row=0, column=4, padx=5, pady=5)

        title = "Adjacency"
        Label(frame_input,text=title + " File").grid(row=1, column=0, padx=5, pady=5)
        self.entry_graph = Entry(frame_input)
        self.entry_graph.grid(row=1, column=1, padx=5, pady=5)

        func  = lambda: self.openGraphFileCallback(title)
        open_file = Button(frame_input, text='Select File', command=func)
        open_file.grid(row=1, column=2, padx=5, pady=5)

        Label(frame_input,text="Goal").grid(row=1, column=3, padx=5, pady=5)
        selected_goal = IntVar()
        self.cb_goal = Combobox(frame_input, textvariable=selected_goal)
        self.cb_goal.grid(row=1, column=4, padx=5, pady=5)

        # create graph button
        func  = lambda: self.createGraph(frame, None)
        btn_create_graph = Button(root, text='Create Graph', command=func)
        btn_create_graph.pack(side=LEFT, padx=5, pady=5)

        # A* search button
        func  = lambda: self.createGraph(frame, "A*")
        btn_a_star = Button(root, text='A* Search', command=func)
        btn_a_star.pack(side=LEFT, padx=5, pady=5)

        # Dijkstra search button
        func  = lambda: self.createGraph(frame, "Dijkstra")
        btn_dijkstra = Button(root, text='Dijkstra', command=func)
        btn_dijkstra.pack(side=LEFT, padx=5, pady=5)

        # quit button
        btn_quit = Button(root, text='Quit', command=root.quit)
        btn_quit.pack(side=RIGHT, padx=5, pady=5)

        # reset button
        btn_reset = Button(root, text='Reset', command=self.reset)
        btn_reset.pack(side=RIGHT, padx=5, pady=5)

        self.root = root
        self.reset()
        root.mainloop()


if __name__ == '__main__':
    ui = ui()
    ui.run()

