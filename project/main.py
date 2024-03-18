"""
Random Informed RRT* path planning with random new obstacle

"""

from informed_rrt_star import InformedRRTStar
from tkinter import Button, Entry, Frame, Label, LEFT, RIGHT, TOP, X

import matplotlib.pyplot as plt
import matplotlib
import random
import sys

matplotlib.use('TkAgg')

range_min = -2
range_max = 25

radius_min = 0.5
radius_max = 2

class ui:
    """
    User Interface class displays GUI for the project and is the main class
    """

    def setEntry(self, entry, text):
        """
        Clear and set new text for a entry field

        :param entry tkinter entry widget object
        :param text entry field text
        """
        entry.delete(0, 'end')
        entry.insert(0, text)

    def reset(self):
        """
        Reset form fields
        """
        self.setEntry(self.collision_size, "")

    def run(self):

        path = None

        while path is None:
            print("Random IRRT* planning attempt")
            # create random obstacles
            obstacle_list = []
            for n in range(10):
                obstacle_list.append((random.randrange(range_min, range_max),
                                    random.randrange(range_min, range_max),
                                    random.uniform(radius_min, radius_max)))

            # Set params
            goal = [random.randrange(int(range_max/3), range_max),
                    random.randrange(int(range_max/3), range_max)]
            rrt = InformedRRTStar(start=[0, 0],
                                goal=goal,
                                obstacle_list=obstacle_list,
                                rand_area=[range_min, range_max])
            path = rrt.informed_rrt_star_search(animation=False)

        new_obstacle = random.choice(path[2:-1])
        while (goal[0] == new_obstacle[0] and goal[1] == new_obstacle[1]) or \
            new_obstacle in obstacle_list:
            new_obstacle = random.choice(path[1:-1])
        size = random.uniform(radius_min, radius_max/2)

        # get canvas from matplotlib
        canvas =  plt.gcf().canvas.get_tk_widget()

        # get window root
        self.root = root = canvas.winfo_toplevel()
        root.resizable(True, True)

        # get NavigationToolbar2Tk
        navigationToolbar2Tk = root.pack_slaves()[0]
        # remove from root
        canvas.pack_forget()
        navigationToolbar2Tk.pack_forget()
        # add back to root
        navigationToolbar2Tk.pack(side=TOP, fill=X)
        canvas.pack(side=TOP, fill=X)

        # add primary frame
        frame = Frame(root)
        frame.pack()

        # Plot path and new obstacle
        rrt.draw_graph()
        plt.plot([x for (x, y) in path], [y for (x, y) in path], '-r')
        plt.grid(True)
        plt.plot(new_obstacle[0], new_obstacle[1], 'bo', ms=30 * size)

        # add input form frame
        frame_input = Frame(frame)
        frame_input.pack()

        Label(frame_input,text="Collision Size").grid(row=0, column=0, padx=5, pady=5)
        self.collision_size = Entry(frame_input)
        self.collision_size.grid(row=0, column=1, padx=5, pady=5)

        # run button
        func  = lambda: self.reset()
        btn_dijkstra = Button(root, text='Run', command=func)
        btn_dijkstra.pack(side=LEFT, padx=5, pady=5)

        # quit button
        btn_quit = Button(root, text='Quit', command=root.quit)
        btn_quit.pack(side=RIGHT, padx=5, pady=5)

        # reset button
        btn_reset = Button(root, text='Reset', command=self.reset)
        btn_reset.pack(side=RIGHT, padx=5, pady=5)

        root.mainloop()

if __name__ == '__main__':
    ui = ui()
    ui.run()
