"""
Random Informed RRT* path planning with random new obstacle

"""

from informed_rrt_star import InformedRRTStar
from shapes import Circle
from tkinter import Button, Checkbutton, Entry, Frame, IntVar, Label, LEFT, RIGHT, TOP, X

import math
import matplotlib.pyplot as plt
import matplotlib
import random
import sys

matplotlib.use('TkAgg')

goal_min = 10

range_min = -5
range_max = 200

obstacle_min = 5
obstacles = 20

radius_min = 1
radius_max = 2

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

        plt.xlim(range_min, range_max)
        plt.ylim(range_min, range_max)
        plt.grid(True)
        plt.tight_layout()

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
        self.obstacle_list.clear()
        plt.clf()
        plt.xlim(range_min, range_max)
        plt.ylim(range_min, range_max)
        plt.grid(True)
        self.setEntry(self.collision_size, "")
        plt.show()


    def run(self):
        self.obstacle_list = []
        self.goal = []
        count = random.randrange(1, 5)
        x_y = self.irrtStarWithTangentBugStar()
        if x_y != None:
            for _ in range(count):
                x,y = x_y
                x_y = self.irrtStarWithTangentBugStar((x,y),False)
                if x_y == None:
                    return
            self.irrtStarWithTangentBugStar((x,y),False,False)


    def irrtStarWithTangentBugStar(self, start=(0,0), create=True, bug=True):
        """
        Clear and set new text for a entry field

        :param start                the start coordinates
        :param create               create random obstacles and goal before running IRRT*
        :param bug                  create a new obstacle and run bug algo
        """
        path = None

        while path is None:
            plt.title("Random IRRT* planning attempt")
            if create:
                self.obstacle_list.clear()
                # create random obstacles
                for n in range(obstacles):
                    self.obstacle_list.append((random.randrange(obstacle_min, range_max),
                                               random.randrange(obstacle_min, range_max),
                                               random.uniform(radius_min, radius_max)))
                # Set params
                self.goal = [random.randrange(random.randrange(goal_min, range_max), range_max),
                             random.randrange(random.randrange(goal_min, range_max), range_max)]

            rrt = InformedRRTStar(start=start,
                                  goal=self.goal,
                                  obstacle_list=self.obstacle_list,
                                  rand_area=[range_min, range_max],
                                  expand_dis=4,
                                  goal_sample_rate=20)
            path = rrt.informed_rrt_star_search(animation=(self.animate.get() and
                                                           self.animate_full.get()))

        if len(path) < 10:
            bug = False
            return start

        goal = self.goal
        path.reverse()
        if bug:
            inner_path = path[2:5]
            inner_len = len(inner_path) - 1
            new_obstacle = random.choice(inner_path[:-1])
            while new_obstacle in self.obstacle_list:
                new_obstacle = random.choice(inner_path[:-1])
            for i in range(inner_len):
                if inner_path[i] == new_obstacle:
                    start = (inner_path[i][0], inner_path[i][1])
                    goal = (inner_path[i+1][0], inner_path[i+1][1])
                    new_obstacle = ((inner_path[i][0] + inner_path[i+1][0])/2,
                                    (inner_path[i][1] + inner_path[i+1][1])/2)
            radius = random.uniform(radius_min, radius_max)

        # Plot path and new obstacle
        rrt.draw_graph()
        plt.title("IRRT*")
        if self.animate.get():
            path_len = len(path) - 1
            for i in range(path_len):
                plt.plot([path[i][0], path[i+1][0]],
                         [path[i][1], path[i+1][1]], linestyle='dashed', color='yellow')
                plt.pause(0.1)
        else:
            plt.plot([x for (x, y) in self.path], [y for (x, y) in self.path], '-r')

        if not bug:
            return

        plt.plot(new_obstacle[0], new_obstacle[1], 'bo', ms=10 * radius)

        # store all points of new obstacle diameter
        degrees = 0
        error = 0
        obstacle_x = []
        obstacle_y = []
        radius *= 3
        while degrees <= 360:
            x,y = Circle.coords(new_obstacle, radius, degrees)
            obstacle_x.append(x)
            obstacle_y.append(y - error)
            degrees += 1
            error = Circle.getError(error, degrees)

        plt.title("IRRT* + Tangent Bug*")
        degrees = 180
        error = 0
        x = 0
        y = 0
        obstacle_x.clear()
        obstacle_y.clear()
        radius += 5
        plot = False
        goal_dist = math.dist(self.goal, path[-1])
        m = round((start[1] - goal[1]) / (start[0] - goal[0]), 4)
        degrees += math.degrees(math.atan(m)) + 10
        while degrees >= 0:
            x,y = Circle.coords(new_obstacle, radius, degrees)
            # y -= error

            if math.dist((x,y), path[-1]) < goal_dist:
                plt.plot(x, y, "o", color='orange')
                obstacle_x.append(x)
                obstacle_y.append(y)
                break

            if round((y - start[1]), 1) == round((m * (x - start[0])), 1):
                plt.plot(x, y, "o", color='orange')
                if plot:
                    break
                else:
                    plot = True

            if plot:
                obstacle_x.append(x)
                obstacle_y.append(y)

            degrees -= 0.5
            error = Circle.getError(error, degrees)

        plt.plot(obstacle_x, obstacle_y, linestyle='dashed', color='orange')
        plt.pause(0.5)
        
        return x,y



if __name__ == '__main__':
    ui()
