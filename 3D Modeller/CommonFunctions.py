import numpy as np
from math import *


def axis_rotation_matrix(axis=(1, 1, 0), theta=pi):
    axis = np.asarray(axis)
    theta = np.asarray(theta)
    axis /= sqrt(np.dot(axis, axis))
    a = cos(theta / 2)
    b, c, d = -axis * sin(theta / 2)
    aa, bb, cc, dd = a ** 2, b ** 2, c ** 2, d ** 2
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    M = np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                  [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                  [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])
    return M


def normalize(vect):
    norm = np.linalg.norm(vect)
    return vect / norm if norm > 0 else vect


def make_lines(points):
    lines = []
    for i in range(len(points)):
        line = [points[i], points[(i + 1) % len(points)]]
        lines.append(line)
    return lines


def dist(p1, p2):
    return sqrt(sum(map(lambda a, b: (a - b) ** 2, p1, p2)))


def ground_axis(points=()):
    if not points:
        return None
    ground_points = []
    for point in points:
        if abs(point[2]) < 1:
            ground_points.append(point)
    ground_points.sort(key=lambda p: abs(p[2]))
    ans = ground_points[:2]
    ans.sort(key=lambda p: sqrt(p[0] ** 2 + p[1] ** 2))
    return float(ans[1][0] - ans[0][0]), float(ans[1][1] - ans[1][0]), 0
