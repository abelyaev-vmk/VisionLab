import numpy as np
from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line
from GUI_consts import *
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from os import getcwd
from os.path import isfile
from ImageProperties import ImageProperties, RectProperties, get_pos
from ioImageData import save_image_data, load_image_data
import warnings


def empty_function(*args):
    pass


class iButton(Button):
    pass


def get_color(name):
    try:
        return {
            'BParallel': (1, 0, 0),
            'BPerpendicular': (0, 1, 0),
            'BWall': (1, 1, 0),
            'BGround': (1, 0, 1),
            'BSky': (0, 0, 1),
        }[name]
    except KeyError:
        return 0, 0, 0


class GUILayout(Widget):
    def __init__(self):
        super(GUILayout, self).__init__()
        self.rect = self.find_rectangle()
        self.input = self.find_input()
        self.image_properties = ImageProperties(self.input.text)
        self.getting_function = None
        self.getting_button = None
        self.mouse_coordinates = []
        self.input_count = 0

    def find_rectangle(self):
        for obj in self.canvas.children:
            if type(obj) == Rectangle:
                return obj

    def find_input(self):
        for obj in self.children:
            if type(obj) == TextInput:
                return obj

    def get_button(self, touch):
        for obj in self.children:
            if not type(obj) == iButton:
                continue
            if -obj.width <= touch.x - obj.right <= 0 and -obj.height <= touch.y - obj.top <= 0:
                return obj
        return None

    def open_image(self, button=None, reset=False, end_of_input=False):
        if reset:
            return
        image_path = self.input.text
        self.reset_image(image_path)
        if not isfile(getcwd() + '\\' + image_path):
            print 'No such file or directory'
            warnings.warn('No such file or directory: ' + image_path)
        else:
            self.rect.source = image_path

    def reset_image(self, button=None, reset=False, end_of_input=False):
        if reset:
            return
        self.rect.source = ''
        self.image_properties = ImageProperties()
        self.getting_function = None
        self.getting_button = None
        self.mouse_coordinates = []
        for temp_button in self.children:
            if type(temp_button) == iButton:
                self.action(temp_button.name)(temp_button, reset=True)
        for line in self.canvas.children:
            if type(line) == Line:
                self.canvas.remove(line)

    def getting_functional(self, getting_function=None, getting_button=None, input_counts=0,
                           image_properties_function=None, end_of_input=False, min_input_counts=4):
        if end_of_input:
            if not (len(self.mouse_coordinates) == self.input_count or
                        (self.input_count == -1 and len(self.mouse_coordinates) >= min_input_counts)):
                print 'Wrong number of points to \"' + image_properties_function.__name__ + '\"'
            else:
                r, g, b = get_color(self.getting_button.name)
                self.getting_button = None
                self.getting_function = None
                image_properties_function(self.mouse_coordinates)
                print self.mouse_coordinates
                with self.canvas:
                    Color(r, g, b)
                    line = Line(points=self.mouse_coordinates[0].pos, width=2)
                for points in reversed(self.mouse_coordinates):
                    line.points += points.pos
                self.image_properties.add_line_on_image(line.points, (r, g, b))
        else:
            self.getting_function = getting_function
            self.getting_button = getting_button
            self.input_count = input_counts
            self.mouse_coordinates = []

    def new_parallel(self, button, reset=False, end_of_input=False):
        if not reset:
            self.getting_functional(getting_function=self.new_parallel, getting_button=button, input_counts=2,
                                    image_properties_function=self.image_properties.add_parallel_line,
                                    end_of_input=end_of_input)
        button.text = 'Parallel lines\n(%d)' \
                      % self.image_properties.parallel_lines_on_ground_count

    def new_perpendicular(self, button, reset=False, end_of_input=False):
        if not reset:
            self.getting_functional(getting_function=self.new_perpendicular, getting_button=button, input_counts=2,
                                    image_properties_function=self.image_properties.add_perpendicular_line,
                                    end_of_input=end_of_input)
        button.text = 'Perpendicular lines\n(%d)' \
                      % self.image_properties.perpendicular_lines_count

    def new_wall(self, button, reset=False, end_of_input=False):
        if not reset:
            self.getting_functional(getting_function=self.new_wall, getting_button=button, input_counts=-1,
                                    image_properties_function=self.image_properties.add_wall,
                                    end_of_input=end_of_input, min_input_counts=3)
        button.text = 'Walls (%d)' % self.image_properties.walls_count

    def new_sky(self, button, reset=False, end_of_input=False):
        if not reset:
            self.getting_functional(getting_function=self.new_sky, getting_button=button, input_counts=-1,
                                    image_properties_function=self.image_properties.set_sky,
                                    end_of_input=end_of_input, min_input_counts=3)
        button.text = 'Sky (%s)' % self.image_properties.sky_count

    def new_ground(self, button, reset=False, end_of_input=False):
        if not reset:
            self.getting_functional(getting_function=self.new_ground, getting_button=button, input_counts=-1,
                                    image_properties_function=self.image_properties.set_ground,
                                    end_of_input=end_of_input, min_input_counts=3)
        button.text = 'Ground (%s)' % self.image_properties.ground_count

    def save_data(self, button=None, reset=False, end_of_input=False):
        if reset:
            return
        if '.' in self.input.text:
            save_path = self.input.text[:self.input.text.find('.')] + '_data'
        else:
            save_path = self.input.text + '_data'
        save_image_data(self.image_properties, save_path)
        print 'Saving data as', save_path

    def load_data(self, button=None, reset=False, end_of_input=False):
        if reset:
            return
        if '.' in self.input.text:
            path = self.input.text[:self.input.text.find('.')] + '_data'
        else:
            path = self.input.text + '_data'
        self.image_properties = load_image_data(path)
        print 'Loading data from', path
        for i in range(self.image_properties.lines_on_image_count):
            r, g, b = self.image_properties.colors_of_lines[i]
            with self.canvas:
                Color(r, g, b)
                Line(points=self.image_properties.lines_on_image[i], width=2)
        self.upgrade()

    def calculate(self, button=None, reset=False, end_of_input=False):
        if reset:
            return
        rp = RectProperties(size=self.rect.size, loc=self.rect.pos)
        self.image_properties.print_data(rp)
        # self.image_properties.set_data(rp=rp, set_rect=True)

    def quit_GUI(self, button=None, reset=False, end_of_input=False):
        if reset:
            return
        App.get_running_app().stop()

    def upgrade(self):
        self.input.text = self.image_properties.image_path
        self.rect.source = self.input.text
        upgrade_dict = {
            'BParallel': 'Parallel lines\n(%d)'
                         % self.image_properties.parallel_lines_on_ground_count,
            'BPerpendicular': 'Perpendicular lines\n(%d)'
                              % self.image_properties.perpendicular_lines_count,
            'BWall': 'Walls (%d)' % self.image_properties.walls_count,
            'BGround': 'Ground (%s)' % self.image_properties.ground_count,
            'BSky': 'Sky (%s)' % self.image_properties.sky_count,
        }
        for obj in self.children:
            if type(obj) == iButton:
                if obj.name in upgrade_dict:
                    obj.text = upgrade_dict[obj.name]

    def action(self, name):
        try:
            return {
                None: empty_function,
                'BReset': self.reset_image,
                'BOpen': self.open_image,
                'BParallel': self.new_parallel,
                'BPerpendicular': self.new_perpendicular,
                'BWall': self.new_wall,
                'BGround': self.new_ground,
                'BSky': self.new_sky,
                'BSave': self.save_data,
                'BLoad': self.load_data,
                'BQuit': self.quit_GUI,
                'BCalc': self.calculate,
            }[name]
        except KeyError:
            print 'Bad key'
            return empty_function

    def on_touch_down(self, touch):
        super(GUILayout, self).on_touch_down(touch)

        button = self.get_button(touch)
        if button:
            if self.getting_function:
                self.getting_function(button=self.getting_button, end_of_input=True)
            self.action(button.name)(button=button)
        if not button and self.getting_function:
            self.mouse_coordinates.append(touch)
            if 0 < self.input_count == len(self.mouse_coordinates):
                self.getting_function(button=self.getting_button, end_of_input=True)

        # print self.canvas.add(Line(points=(10, 10, 100, 100)))


class GUIApp(App):
    def build(self):
        return GUILayout()


if __name__ == '__main__':
    GUIApp().run()
