import numpy as np
import cv2
import math

class Camera:
    """A class for camera parameters convertion"""

    def __init__(self):
        # camera location
        self.location = np.zeros(3)
        # camera rotation matrix in nonGL mode
        self.rotation = np.eye(3, 3)
        self.isGL = False

    # sets location of the camera in 3D
    def SetLocation(self, in_location):
        if (in_location.size != 3):
            raise ValueError('Location has to have 3 components')
        self.location = np.copy(in_location).reshape(3)

    def SetDirection(self, forward=None, up=None, right=None):
        nDefined = 0
        if forward is not None:
            checkVector(forward, 'forward')
            nDefined += 1
        if up is not None:
            checkVector(up, 'up')
            nDefined += 1
        if right is not None:
            checkVector(right, 'right')
            nDefined += 1
        if (nDefined < 2):
            raise ValueError('At least two directions have to be specified')
        if forward is None:
            forward = np.cross(up, right)
        if up is None:
            up = np.cross(right, forward)
        if right is None:
            right = np.cross(forward, up)
        R = np.vstack((right, -up, forward))
        if (self.isGL):
            R1 = cv2.Rodrigues(np.array([np.pi, 0, 0]))[0]
            R = R1.dot(R)
        self.rotation = R

    # rotation from scene to camera coordinates
    def SetRotationVector(self, in_vector):
        self.rotation = cv2.Rodrigues(in_vector)[0]
        if (self.isGL):
            R1 = cv2.Rodrigues(np.array([np.pi, 0, 0]))[0]
            R = R1.dot(R1)

    # rotation from scene to camera coordinates
    def SetQuaternion(self, in_quaternion, order="xyzw"):
        if order[0] == 'x':
            w = in_quaternion[3]
            axis = in_quaternion[0:3]
        else:
            w = in_quaternion[0]
            axis = in_quaternion[1:4]
        rt = 2 * math.acos(w) / math.sin(math.acos(w)) * axis
        self.SetRotationVector(rt)

    def GetRotationMatrix(self):
        R = self.rotation
        if self.isGL:
            R1 = cv2.Rodrigues(np.array([np.pi, 0, 0]))[0]
            R = R1.dot(R)
        return R

    def GetViewMatrix(self):
        t = -self.rotation.dot(self.location)
        viewMatrix = np.hstack((self.rotation, t.reshape((3, 1))))
        if self.isGL:
            R = cv2.Rodrigues(np.array([np.pi, 0, 0]))[0]
            viewMatrix = R.dot(viewMatrix)
        return viewMatrix

    def GetForward(self):
        R = self.GetRotationMatrix()
        return R[2, :]

    def GetUp(self):
        R = self.GetRotationMatrix()
        return -R[1, :]

    def GetRight(self):
        R = self.GetRotationMatrix()
        return R[0, :]

    def GetLocation(self):
        return self.location

    def GetRotationVector(self):
        R = self.GetRotationMatrix()
        angle = math.acos((np.trace(R) - 1) / 2.)
        axis = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
        return angle / 2 / math.sin(angle) * axis

    def GetQuaternion(self, order="xyzw"):
        rt = self.GetRotationVector()
        angle = np.linalg.norm(rt)
        w = math.cos(angle / 2.)
        axis = rt / angle
        if order[0] == 'x':
            return np.concatenate((axis * math.sin(angle / 2), np.array(w).reshape(1)))
        else:
            return np.concatenate((np.array(w).reshape(1), axis * math.sin(angle / 2)))

    # indicates usage of openGL
    def UseGL(self):
        self.isGL = True

    # indicates usage of non-GL camera
    def UseNonGL(self):
        self.isGL = False


# checks vector
def checkVector(in_vector, in_vectorName=''):
    if in_vector.size != 3:
        raise ValueError('The {$1} vector has to have 3 components'.format(in_vectorName))
