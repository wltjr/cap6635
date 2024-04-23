"""
Random Informed RRT* path planning with random new obstacle

"""

from informed_rrt_star import InformedRRTStar
from shapes import Circle, Rectangle
from tkinter import Button, Checkbutton, END, Frame, IntVar, Label, LEFT, RIGHT, Text
from tkinter.ttk import Combobox

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
        navigationToolbar2Tk.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        canvas.grid(row=1, column=0, padx=5, pady=5)

        plt.xlim(range_min, range_max)
        plt.ylim(range_min, range_max)
        plt.grid(True)
        plt.tight_layout()

        # add primary frame
        frame = Frame(root)
        frame.grid(row=1, column=1, padx=5, pady=5)

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
        selected_size = IntVar()
        self.collision_size = Combobox(frame_input, textvariable=selected_size, width=3)
        self.collision_size.grid(row=0, column=5, padx=5, pady=5)
        self.collision_size['values'] = [int(i + 1) for i in range(10)]
        self.collision_size.set(5)

        Label(frame_input,text="Loops").grid(row=0, column=6, padx=5, pady=5)
        selected_loops = IntVar()
        self.loops = Combobox(frame_input, textvariable=selected_loops, width=3)
        self.loops.grid(row=0, column=7, padx=5, pady=5)
        self.loops['values'] = [int(i + 1) for i in range(10)]
        self.loops.set(5)

        self.output_text = Text(frame_input, height=25, width=60)
        self.output_text.grid(row=1, column=0, columnspan=8, padx=5, pady=5)

        frame_buttons = Frame(frame)
        frame_buttons.pack()

        # run button
        btn_dijkstra = Button(frame_buttons, text='Run', command=self.run)
        btn_dijkstra.pack(side=LEFT, padx=5, pady=5)

        # quit button
        btn_quit = Button(frame_buttons, text='Quit', command=plt.close)
        btn_quit.pack(side=RIGHT, padx=5, pady=5)

        # reset button
        btn_reset = Button(frame_buttons, text='Reset', command=self.reset)
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
        self.collision_size.set(5)
        self.loops.set(5)
        self.output_text.delete(1.0,END)
        plt.show()


    def run(self):
        """
        Run the general algorithm, IRRT* + Bug* with any newly added obstacles
        with up to 5 random new obstacles
        """
        for _ in range(int(self.loops.get())):
            self.obstacle_list = []
            self.goal = []
            count = random.randrange(1, 5)
            self.output_text.delete(1.0,END)
            self.output_text.insert(END, "new obstacles = %d\n" % (count))
            count -= 1
            x_y = self.irrtStarWithTangentBugStar()
            if x_y != None:
                for _ in range(count):
                    x,y = x_y
                    x_y = self.irrtStarWithTangentBugStar((x,y),False)
                    if x_y == None:
                        break
                if x_y == None:
                    continue
                x,y = x_y
                self.irrtStarWithTangentBugStar((x,y),False,False)
            self.output_text.insert(END, "done\n")


    def bugAroundObstacle(self, new_obstacle, start, goal, path):
        """
        Run Bug 2/Tangent Bug algorithm against a random circle or rectangle obstacle

        :param start                the new obstacle coordinates, center x,y
        :param start                the start coordinates
        :param start                the goal coordinates
        :param start                the current path
        """
        shape = random.randint(0, 1)
        plt.pause(0.1)
        radius = random.uniform(radius_min, radius_max)
        if shape:
            marker = 'bo'
        else:
            marker = 'bs'
        plt.plot(new_obstacle[0], new_obstacle[1], marker, ms=10 * radius)
        plt.pause(0.1)

        # get all points of new obstacle diameter
        radius *= 3
        if shape:
            obstacle = Circle(new_obstacle, radius)
        else:
            obstacle = Rectangle(new_obstacle, radius, radius)

        plt.plot(obstacle.x, obstacle.y, linestyle='dashed', color='purple')
        plt.pause(0.1)

        plt.title("IRRT* + Tangent Bug*")
        degrees = 225
        x = 0
        y = 0
        obstacle_x = []
        obstacle_y = []
        radius += int(self.collision_size.get())
        plot = False
        goal_dist = math.dist(self.goal, path[-1])
        m = round((start[1] - goal[1]) / (start[0] - goal[0]), 4)
        degrees += math.degrees(math.atan(m)) + 10
        self.output_text.insert(END, "slope = %.4f  angle = %.2f°  degrees = %.2f°\n" %
                                    (round(m, 4),
                                     round(math.degrees(math.atan(m)), 2),
                                     round(degrees, 2)))
        degree_change = 0
        while degrees >= -45:
            if shape:
                x,y = Circle.coords(new_obstacle, radius, degrees)
            else:
                x,y = Rectangle.coords(new_obstacle, radius, radius, degrees)

            if math.dist((x,y), path[-1]) < goal_dist:
                self.output_text.insert(END, "Bug euclidean end =  %s\n" % ((round(x, 4), round(y, 4)),))
                plt.plot(x, y, "o", color='orange')
                obstacle_x.append(x)
                obstacle_y.append(y)
                break

            if (degree_change == 0 or degree_change - degrees > 2) and \
               round((y - start[1]), 1) == round((m * (x - start[0])), 1):
                plt.plot(x, y, "o", color='orange')
                if plot:
                    self.output_text.insert(END, "Bug end =  %s\n" % ((round(x, 4), round(y, 4)),))
                    break
                else:
                    self.output_text.insert(END, "Bug start = %s\n" % ((round(x, 4), round(y, 4)),))
                    plot = True
                    degree_change = degrees

            if plot:
                obstacle_x.append(x)
                obstacle_y.append(y)

            degrees -= 0.25

        return obstacle_x, obstacle_y


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

        goal = self.goal
        path.reverse()
        self.output_text.insert(END, "IRRT* path len = %d\n" % (len(path)))
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
                    self.output_text.insert(END, "start = %s  goal = %s\n" % 
                                                ((round(start[0], 4), round(start[1], 4)),
                                                 (round(goal[0], 4), round(goal[1], 4))))
                    new_obstacle = ((inner_path[i][0] + inner_path[i+1][0])/2,
                                    (inner_path[i][1] + inner_path[i+1][1])/2)

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

        obstacle_x, obstacle_y = self.bugAroundObstacle(new_obstacle, start, goal, path)
        plt.plot(obstacle_x, obstacle_y, linestyle='dashed', color='orange')
        plt.pause(0.5)
        self.output_text.insert(END, "next\n")
        
        return obstacle_x[-1], obstacle_y[-1]



if __name__ == '__main__':
    ui()
