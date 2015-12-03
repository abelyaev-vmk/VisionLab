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


def translate_and_scale_matrix(translation=(0, 0, 0), scale=1):
    tx, ty, tz = translation
    translation_matrix = np.matrix([[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]])
    scale_matrix = np.matrix([[scale, 0, 0, 0], [0, scale, 0, 0], [0, 0, scale, 0], [0, 0, 0, 1]])
    print translation_matrix, '\n', scale_matrix, '\n', scale
    return scale_matrix * translation_matrix


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
    print 'Points:', points
    ground_points = []
    for point in points:
        if abs(point[2]) < 1:
            ground_points.append(point)
    print 'Ground points:', ground_points
    ground_points.sort(key=lambda p: abs(p[2]))
    ans = ground_points[:2]
    ans.sort(key=lambda p: sqrt(p[0] ** 2 + p[1] ** 2))
    print 'Ans:', ans
    return float(ans[1][0] - ans[0][0]), float(ans[1][1] - ans[1][0]), 0


def hom2het(vector=None, matrix=None):
    if vector is not None:
        return np.append(np.array(vector), 1)
    if matrix is not None:
        temp = np.zeros((4, 4))
        temp[:3, :3] = matrix[:, :]
        temp[3, 3] = 1
        return temp


def het2hom(vector=None, matrix=None):
    if vector is not None:
        return np.array(vector[:3]) / vector[3]
    if matrix is not None:
        return matrix[:3, :3] / matrix[3][3]
