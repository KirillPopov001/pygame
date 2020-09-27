import  pygame
from random import  random
from math import sqrt

SCREEN_SIZE = (1280, 720)

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def int_pair(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __len__(self):
        return ((self.x**2 + self.y**2)**0.5)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            return Vector(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):

        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y

        elif isinstance(other, int):
            return Vector(self.x * other, self.y * other)

    def __repr__(self):
        bb = (self.x, self.y)
        return str(bb)

    def __str__(self):
        bb = (self.x, self.y)
        return str(bb)


class Line:

    def set_points(self, points, speeds):
        for point in range(len(points)):
            points[point] = points[point] + speeds[point]

            if points[point].x > SCREEN_SIZE[0] or points[point].x < 0:
                if isinstance(speeds[point], Vector):
                    speeds[point] = (-speeds[point].x, speeds[point].y)
                else:
                    speeds[point] = (-speeds[point][0], speeds[point][1])
            if points[point].y > SCREEN_SIZE[1] or points[point].y < 0:
                if isinstance(speeds[point], Vector):
                    speeds[point] = (speeds[point].x, -speeds[point].y)
                else:
                    speeds[point] = (speeds[point][0], -speeds[point][1])

    def draw_points(self, points, style="points", width=4, color=(255, 255, 255)):
        if style == "line":
            for point_number in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, (int(points[point_number].x), int(points[point_number].y)),
                             (int(points[point_number + 1].x), int(points[point_number + 1].y)), width)

        elif style == "points":
            for point in points:
                pygame.draw.circle(gameDisplay, color, (int(point.x), int(point.y)), width)


class Joint(Line):

    def get_point(self, points, alpha, deg=None):
        bb = 0
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + (Joint.get_point(bb, points, alpha, deg - 1) * 1 - alpha)


    def get_points(self, base_points, count):
        bb = 0
        alpha = 1 / count
        result = []
        for i in range(count):
            result.append(Joint.get_point(bb, base_points, i * alpha))
        return result


    def get_joint(self, points, count):
        bb = 0
        if len(points) < 3:
            return []
        result = []
        for i in range(-2, len(points) - 2):
            pnt = []
            pnt.append(points[i + 1])
            result.extend(Joint.get_points(bb, pnt, count))
        return result


def faster(speeds):
    print(speeds)
    for i in range(len(speeds)):
        if isinstance(i, Vector):
            speeds[i] = (speeds[i].x + 0.9, speeds[i].y + 0.9)
    

def slower(speeds):
    print(speeds)
    for i in range(len(speeds)):
        if isinstance(i, Vector):
            speeds[i] = (speeds[i].x - 0.9, speeds[i].y - 0.9)
    
        
def display_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["F", "Ускорить точки"])
    data.append(["S", "Замедлить точки"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(["", ""])
    data.append([str(steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    points = []
    speeds = []
    show_help = False
    pause = False

    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_f:
                    faster(speeds)
                if event.key == pygame.K_s:
                    slower(speeds)

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(Vector(event.pos[0], event.pos[1]))
                
                speeds.append(Vector(random() * 2, random() * 2))
                
        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        bb = 0
        Line.draw_points(bb, points)
        Line.draw_points(bb, Joint.get_joint(bb, points, steps), "line", 4, color)
        if not pause:
            a = 0
            Line.set_points(a, points, speeds)
        if show_help:
            display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
