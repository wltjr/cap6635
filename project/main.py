"""
Random Informed RRT* path planning with random new obstacle

"""

from bug import BugPlanner
from informed_rrt_star import InformedRRTStar
from tkinter import Button, Checkbutton, Entry, Frame, IntVar, Label, LEFT, RIGHT, TOP, X

import matplotlib.pyplot as plt
import matplotlib
import random
import sys

matplotlib.use('TkAgg')

goal_min = 10

range_min = -2
range_max = 50

obstacle_min = 5

radius_min = 0.5
radius_max = 1.25

class ui:
    """
    User Interface class displays GUI for the project and is the main class
    """
    def __init__(self):
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

        # add input form frame
        frame_input = Frame(frame)
        frame_input.pack()

        self.animate = IntVar(value=1)
        Label(frame_input,text="Animate").grid(row=0, column=0, padx=5, pady=5)
        animate_chkbtn = Checkbutton(frame_input, variable=self.animate)
        animate_chkbtn.grid(row=0, column=1, padx=5, pady=5)

        self.animate_full = IntVar()
        Label(frame_input,text="Full").grid(row=0, column=2, padx=5, pady=5)
        animate_full_chkbtn = Checkbutton(frame_input, variable=self.animate_full)
        animate_full_chkbtn.grid(row=0, column=3, padx=5, pady=5)

        Label(frame_input,text="Collision Size").grid(row=0, column=4, padx=5, pady=5)
        self.collision_size = Entry(frame_input)
        self.collision_size.grid(row=0, column=5, padx=5, pady=5)


        # run button
        btn_dijkstra = Button(root, text='Run', command=self.run)
        btn_dijkstra.pack(side=LEFT, padx=5, pady=5)

        # quit button
        btn_quit = Button(root, text='Quit', command=plt.close)
        btn_quit.pack(side=RIGHT, padx=5, pady=5)

        # reset button
        btn_reset = Button(root, text='Reset', command=self.reset)
        btn_reset.pack(side=RIGHT, padx=5, pady=5)

        self.centerWindow()

        root.mainloop()


    def centerWindow(self):
        """
        Center the window in screen
        """
        if sys.version_info[1] > 9:
            self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_pathname(self.root.winfo_id()))

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
        plt.clf()
        self.setEntry(self.collision_size, "")
        plt.show()

    def run(self):

        start = (0,0)
        path = None

        while path is None:
            print("Random IRRT* planning attempt")
            # create random obstacles
            obstacle_list = []
            for n in range(10):
                obstacle_list.append((random.randrange(obstacle_min, range_max),
                                    random.randrange(obstacle_min, range_max),
                                    random.uniform(radius_min, radius_max)))

            # Set params
            goal = [random.randrange(random.randrange(goal_min, range_max), range_max),
                    random.randrange(random.randrange(goal_min, range_max), range_max)]
            rrt = InformedRRTStar(start=start,
                                  goal=goal,
                                  obstacle_list=obstacle_list,
                                  rand_area=[range_min, range_max])
            path = rrt.informed_rrt_star_search(animation=(self.animate.get() and
                                                                       self.animate_full.get()))

        path.reverse()
        inner_path = path[2:-2]
        inner_len = len(inner_path) - 1
        new_obstacle = random.choice(inner_path)
        while new_obstacle in obstacle_list:
            new_obstacle = random.choice(inner_path)
        for i in range(inner_len):
            if inner_path[i] == new_obstacle:
                start = (int(inner_path[i][0]), int(inner_path[i][1]))
                goal = (int(inner_path[i+1][0]), int(inner_path[i+1][1]))
                new_obstacle = ((inner_path[i][0] + inner_path[i+1][0])/2,
                                (inner_path[i][1] + inner_path[i+1][1])/2)
        size = random.uniform(radius_min, radius_max/2)

        # Plot path and new obstacle
        rrt.draw_graph()
        plt.plot(new_obstacle[0], new_obstacle[1], 'bo', ms=30 * size)
        if self.animate.get():
            path_len = len(path) - 1
            for i in range(path_len):
                plt.plot([path[i][0], path[i+1][0]],
                         [path[i][1], path[i+1][1]], linestyle='dashed', color='yellow')
                plt.pause(1)
        else:
            plt.plot([x for (x, y) in self.path], [y for (x, y) in self.path], '-r')

        print(start, goal, new_obstacle)
        my_Bug = BugPlanner(start[0], start[1], goal[0], goal[1], [new_obstacle[0]], [new_obstacle[1]])
        my_Bug.bug2()

        plt.show()



if __name__ == '__main__':
    ui()
