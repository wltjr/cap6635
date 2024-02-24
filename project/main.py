"""
Random Informed RRT* path planning with random new obstacle

"""

from informed_rrt_star import InformedRRTStar
import matplotlib.pyplot as plt
import random

range_min = -2
range_max = 25

radius_min = 0.5
radius_max = 2

def main():

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
        rrt = InformedRRTStar(start=[0, 0],
                              goal=[random.randrange(int(range_max/3), range_max),
                                    random.randrange(int(range_max/3), range_max)],
                              obstacle_list=obstacle_list,
                              rand_area=[range_min, range_max])
        path = rrt.informed_rrt_star_search(animation=False)

    new_obstacle = random.choice(path[1:-1])
    size = random.uniform(radius_min, radius_max)

    # Plot path and new obstacle
    rrt.draw_graph()
    plt.plot([x for (x, y) in path], [y for (x, y) in path], '-r')
    plt.grid(True)
    plt.plot(new_obstacle[0], new_obstacle[1], 'bo', ms=30 * size)
    plt.show()


if __name__ == '__main__':
    main()