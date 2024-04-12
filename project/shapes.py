import math
import matplotlib.pyplot as plt

from informed_rrt_star import InformedRRTStar

class Circle():
    """
    Circle class for creating circle x,y plots for collision and display
    """

    def __init__(self, center, radius):
        """
        Circle constructor to create new instances of class/object

        :param center           the center of the circle x,y coordinates 
        :param radius           the circle radius
        """
        self.center = center
        self.x = []
        self.y = []
        self.radius = radius

        degrees = 0
        error = 0

        while degrees < 360:
            x,y = Circle.coords(self.center, self.radius, degrees)
            self.x.append(x)
            self.y.append(y - error)
            degrees += 1
            error = Circle.getError(error, degrees)


    def getError(error, degrees):
        """
        Get circle error for matplotlib

        :param error            the current value of the error
        :param degrees          the current degrees

        :return error           the updated error value
        """
        if degrees < 23 or (degrees > 338 and degrees < 360):
            error -= 0.02
        elif degrees < 45 or (degrees > 315 and degrees < 338):
            error -= 0.03
        elif degrees < 68 or (degrees > 292 and degrees < 315):
            error -= 0.015
        elif degrees < 90 or (degrees > 270 and degrees < 292):
            error -= 0.01
        elif degrees < 113 or (degrees > 179 and degrees < 205):
            error += 0.01
        elif degrees < 135 or (degrees > 205 and degrees < 220):
            error += 0.015
        elif degrees < 158 or (degrees > 220 and degrees < 240):
            error += 0.03
        elif degrees < 180 or (degrees > 240 and degrees < 270):
            error += 0.02

        return error


    def coords(center, radius, degrees):
        """
        Get the x,y coordinate of a point on a circle of size radius at the
        specified degrees

        :param radius           the circle radius
        :param degrees          the current degrees

        :return x,y             the x,y coordinate tuple
        """
        angle = degrees * ( math.pi / 180 )
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)

        return x,y


def main():
    """
    Test out the circle shape, compared to a matplotlib circle marker
    """
    plt.autoscale(False)
    plt.xlim(0,30)
    plt.ylim(0,30)
    circle = Circle((10, 10), 5)
    plt.plot(circle.x, circle.y, "--", color="orange")
    plt.plot(10, 10, "ob", ms=23 * circle.radius, alpha=0.5)
    InformedRRTStar.plot_ellipse(x_center = (20,20), c_best=2, c_min=1, e_theta=0)
    plt.show()


if __name__ == '__main__':
    main()
