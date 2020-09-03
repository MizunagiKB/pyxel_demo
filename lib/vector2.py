import math


class Vector2(object):
    def __init__(self, x, y):
        enumerate
        self.x = x
        self.y = y

    def angle(self):
        return math.atan2(self.y, self.x)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def length_squared(self):
        return self.x * self.x + self.y * self.y

    def normalize(self) -> float:
        ln = self.x * self.x + self.y * self.y
        if ln != 0:
            ln = math.sqrt(ln)
            self.x /= ln
            self.y /= ln

    def normalized(self):
        v = Vector2(self.x, self.y)
        v.normalize()
        return v

    def is_normalized(self) -> bool:
        raise NotImplementedError()

    def distance_to(self, p_vector2):
        return math.sqrt(
            (self.x - p_vector2.x) * (self.x - p_vector2.x)
            + (self.y - p_vector2.y) * (self.y - p_vector2.y)
        )

    def distance_squared_to(self, p_vector2):
        return (self.x - p_vector2.x) * (self.x - p_vector2.x) + (
            self.y - p_vector2.y
        ) * (self.y - p_vector2.y)

    def angle_to(self, p_vector2):
        return math.atan2(self.cross(p_vector2), self.dot(p_vector2))

    def angle_to_point(self, p_vector2):
        return math.atan2(self.y - p_vector2.y, self.x - p_vector2.x)

    def dot(self, p_other):
        return self.x * p_other.x + self.y * p_other.y

    def cross(self, p_other):
        return self.x * p_other.y - self.y * p_other.x

    def sign(self):
        raise NotImplementedError()

    def floor(self):
        return Vector2(math.floor(self.x), math.floor(self.y))

    def ceil(self):
        return Vector2(math.ceil(self.x), math.ceil(self.y))

    def round(self):
        return Vector2(round(self.x), round(self.y))

    def rotated(self, p_by: float):
        sv = math.sin(p_by)
        cv = math.cos(p_by)
        return Vector2(self.x * cv - self.y * sv, self.x * sv + self.y * cv)

    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
        return self

    def __add__(self, p_other):
        return Vector2(self.x + p_other.x, self.y + p_other.y)

    def __sub__(self, p_other):
        return Vector2(self.x - p_other.x, self.y - p_other.y)

    def __mul__(self, p_v1):
        if isinstance(p_v1, Vector2):
            return Vector2(self.x * p_v1.x, self.y * p_v1.y)
        elif isinstance(p_v1, (int, float)):
            return Vector2(self.x * p_v1, self.y * p_v1)
        else:
            raise ValueError()
