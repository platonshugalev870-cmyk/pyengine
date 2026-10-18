import math

class Vec2:
    __slots__ = ('x', 'y')

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, o):
        return Vec2(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vec2(self.x - o.x, self.y - o.y)

    def __mul__(self, s):
        return Vec2(self.x * s, self.y * s)

    __rmul__ = __mul__

    def __truediv__(self, s):
        return Vec2(self.x / s, self.y / s)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

    def length(self):
        return math.hypot(self.x, self.y)

    def length_sq(self):
        return self.x * self.x + self.y * self.y

    def normalized(self):
        l = self.length()
        if l == 0:
            return Vec2(0, 0)
        return Vec2(self.x / l, self.y / l)

    def dot(self, o):
        return self.x * o.x + self.y * o.y

    def rotate(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return Vec2(self.x * c - self.y * s, self.x * s + self.y * c)

    def copy(self):
        return Vec2(self.x, self.y)

class Rect:
    __slots__ = ('x', 'y', 'w', 'h')

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def intersects(self, o):
        return (self.x < o.x + o.w and self.x + self.w > o.x and
                self.y < o.y + o.h and self.y + self.h > o.y)

    def contains_point(self, px, py):
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

    def __repr__(self):
        return f"Rect({self.x},{self.y},{self.w},{self.h})"

def lerp(a, b, t):
    return a + (b - a) * t


def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def circle_intersects_circle(c1, r1, c2, r2):
    dx = c1.x - c2.x
    dy = c1.y - c2.y
    return dx * dx + dy * dy <= (r1 + r2) ** 2

def rect_intersects_circle(rect, cx, cy, r):
    closest_x = clamp(cx, rect.x, rect.x + rect.w)
    closest_y = clamp(cy, rect.y, rect.y + rect.h)
    dx = cx - closest_x
    dy = cy - closest_y
    return dx * dx + dy * dy <= r * r