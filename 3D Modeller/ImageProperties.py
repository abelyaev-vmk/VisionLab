import numpy as np
import camera
from Renderer import Renderer, make_lines
from CameraProperties import CameraProperties
get_pos = lambda mouse: mouse.pos

class RectProperties:
    def __init__(self, size=(0, 0), loc=(0, 0), percentage=(1, 1)):
        self.size = size
        self.location = loc
        self.percentage = percentage


class ImageProperties:
    def __init__(self, image_path=''):
        self.image_path = image_path
        self.rp = RectProperties()
        self.cp = CameraProperties(project=CameraProperties.make_project_name(image_path)) if image_path else None

        self.parallel_lines_on_ground_count = 0
        self.perpendicular_lines_count = 0
        self.walls_count = 0
        self.sky_count = 'None'
        self.ground_count = 'None'

        self.parallel_lines_on_ground = []
        self.perpendicular_lines = []
        self.walls = []
        self.sky = []
        self.ground = []

        self.lines_on_image_count = 0
        self.lines_on_image = []
        self.colors_of_lines = []

    def add_line_on_image(self, line=None, color=None):
        self.lines_on_image.append(line)
        self.colors_of_lines.append(color)
        self.lines_on_image_count += 1

    def add_parallel_line(self, line=None, out=True):
        if not (type(line[0]) == list or type(line[0]) == tuple):
            line = map(get_pos, line)
        if out:
            print 'Add parallel', line
        self.parallel_lines_on_ground_count += 1
        self.parallel_lines_on_ground.append(line)

    def add_perpendicular_line(self, line=None, out=True):
        if not (type(line[0]) == list or type(line[0]) == tuple):
            line = map(get_pos, line)
        if out:
            print 'Add perpendicular', line
        self.perpendicular_lines_count += 1
        self.perpendicular_lines.append(line)

    def add_wall(self, wall=None, out=True):
        if not (type(wall[0]) == list or type(wall[0]) == tuple):
            wall = map(get_pos, wall)
        if out:
            print 'Add wall', wall
        self.walls_count += 1
        self.walls.append(wall)

    def set_sky(self, sky=None, out=True):
        if not (type(sky[0]) == list or type(sky[0]) == tuple):
            sky = map(get_pos, sky)
        if out:
            print 'Add sky', sky
        self.sky_count = 'Exist'
        self.sky = sky

    def set_ground(self, ground=None, out=True):
        if not (type(ground[0]) == list or type(ground[0]) == tuple):
            ground = map(get_pos, ground)
        if out:
            print 'Add sky', ground
        self.ground_count = 'Exist'
        self.ground = ground

    def set_rect(self, rp):
        assert rp.__class__.__name__ == RectProperties.__name__
        self.rp = rp

    def apply_rect(self, rp=None):
        if not rp:
            rp = self.rp
        get_local_points = lambda p: [p[0] - rp.location[0], p[1] - rp.location[1]]
        ip = ImageProperties(self.image_path)
        ip.set_rect(RectProperties(size=rp.size, loc=rp.location))
        for line in self.parallel_lines_on_ground:
            ip.add_parallel_line(map(get_local_points, line), out=False)
        for line in self.perpendicular_lines:
            ip.add_perpendicular_line(map(get_local_points, line), out=False)
        for wall in self.walls:
            ip.add_wall(map(get_local_points, wall), out=False)
        if self.ground:
            ip.set_ground(map(get_local_points, self.ground), out=False)
        if self.sky:
            ip.set_sky(map(get_local_points, self.sky), out=False)
        return ip

    def print_data(self, rp=RectProperties(), set_rect=False):
        return
        # if set_rect:
        #     self.rp = rp
        # self.cp = CameraProperties(self)
        # print '=========GLOBAL COORDINATES==========='
        # self.cp.print_properties()
        # cp = CameraProperties(self.apply_rect(rp))
        # print '=========LOCAL COORDINATES============'
        # cp.print_properties()

    def set_data(self, rp=RectProperties(), set_rect=False):
        return
        # if set_rect:
        #     self.rp = rp
        # self.cp = CameraProperties(self.apply_rect(rp))
        # self.cp.set_view_matrix()


def render(ip=ImageProperties()):
    renderer = Renderer(ground=make_lines(ip.ground),
                        project=CameraProperties.make_project_name(ip.image_path),
                        reducing=1)
    renderer.render()
