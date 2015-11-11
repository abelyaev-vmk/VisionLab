import camera
from PIL import Image


class CameraProperties:
    def __init__(self, image_path='',
                 xml_path='', xml_type=1, location=None, quaternion=None, q_order="xyzw"):
        if image_path:
            self.image = Image.open(image_path)
        self.camera = camera.Camera()
        self.camera.UseGL()
        if xml_path:
            pass
        elif location:
            self.camera.SetLocation(location)
            self.camera.SetQuaternion(quaternion)

    def get_location(self):
        return self.camera.GetLocation()

    def get_quaternion(self):
        return self.camera.GetQuaternion()

    def get_view_matrix(self):
        return self.camera.GetViewMatrix()

    def get_up(self):
        return self.camera.GetUp()

    def get_right(self):
        return self.camera.GetRight()

    def get_rotation_matrix(self):
        return self.camera.GetRotationMatrix()

    def get_forward(self):
        return self.camera.GetForward()

    def get_eye_center_up(self, reducing=1):
        eye = map(lambda a: a / reducing, self.get_location())
        cen = map(lambda a: a / reducing, map(lambda b, c: b + c, eye, self.get_forward()))
        up = self.get_up()
        return eye, cen, up

    def point_projection(self, point=(0, 0), plane=(0, 0, 1, 0)):
        pass
