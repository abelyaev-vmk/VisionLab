import numpy as np
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen,FallOutTransition
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import BorderImage
from kivy.graphics import Color, Rectangle ,Line
from GUI_consts import *
from kivy.uix.textinput import TextInput
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from os import getcwd
from os.path import isfile
import warnings


def empty_function(arg1=None, arg2=None, arg3=None, arg4=None):
        pass


class ImageProperties:
    def __init__(self):
        self.parallel_lines_on_ground_count = 0
        self.perpendicular_lines_count = 0
        self.walls_count = 0
        self.sky_count = 'None'

        self.parallel_lines_on_ground = []
        self.perpendicular_lines = []
        self.walls = []
        self.sky = []

    def add_parallel_line(self, line=None):
        self.parallel_lines_on_ground_count += 1
        self.parallel_lines_on_ground.append(line)

    def add_perpendicular_line(self, line=None):
        self.perpendicular_lines_count += 1
        self.perpendicular_lines.append(line)

    def add_wall(self, wall=None):
        self.walls_count += 1
        self.walls.append(wall)

    def set_sky(self, sky=None):
        self.sky_count = 'Exist'
        self.sky = sky


class iButton(Button):
    pass


class GUILayout(Widget):
    def __init__(self):
        super(GUILayout, self).__init__()
        self.rect = self.canvas.children[1]
        self.image_properties = ImageProperties()

    def find_rectangle(self):
        for obj in self.canvas.children:
            if type(obj) == Rectangle:
                self.rect = obj
                return

    def get_button(self, touch):
        if not self.rect:
            self.find_rectangle()
        for obj in self.children:
            if not type(obj) == iButton:
                continue
            if -obj.width <= touch.x - obj.right <= 0 and -obj.height <= touch.y - obj.top <= 0:
                return obj
        return None

    def open_image(self, button=None, reset=False):
        if reset:
            return
        image_path = self.children[-1].text
        if not isfile(getcwd() + '\\' + image_path):
            print 'No such file or directory'
            warnings.warn('No such file or directory: ' + image_path)
            self.reset_image()
        else:
            self.rect.source = image_path

    def reset_image(self, button=None, reset=False):
        if reset:
            return
        self.rect.source = ''
        self.image_properties = ImageProperties()
        for obj in self.children:
            if type(obj) == iButton:
                self.action(button.name)(button, reset=True)

    def new_parallel(self, button, reset=False):
        if not reset:
            self.image_properties.add_parallel_line()
        button.text = 'Parallel lines\n(%d)' \
                      % self.image_properties.parallel_lines_on_ground_count

    def new_perpendicular(self, button, reset=False):
        if not reset:
            self.image_properties.add_perpendicular_line()
        button.text = 'Perpendicular lines\n(%d)' \
                      % self.image_properties.perpendicular_lines_count

    def new_wall(self, button, reset=False):
        if not reset:
            self.image_properties.add_wall()
        button.text = 'Walls (%d)' % self.image_properties.walls_count

    def new_sky(self, button, reset=False):
        if not reset:
            self.image_properties.set_sky()
        button.text = 'Sky (%s)' % 'Exist' if not reset else 'None'

    def save_data(self, button, reset=False):
        if reset:
            # BACKUP!!
            return
        pass

    def load_data(self, button, reset=False):
        if reset:
            return
        pass

    def quit_GUI(self, button, reset=False):
        if reset:
            return
        self.save_data(button=None, reset=True)
        quit()

    def action(self, name):
        try:
            return {
                None: empty_function,
                'BReset': self.reset_image,
                'BOpen': self.open_image,
                'BParallel': self.new_parallel,
                'BPerpendicular': self.new_perpendicular,
                'BWall': self.new_wall,
                'BSky': self.new_sky,
                'BSave': self.save_data,
                'BLoad': self.load_data,
                'BQuit': self.quit_GUI,
            }[name]
        except KeyError:
            print 'Bad key'
            return empty_function

    def on_touch_down(self, touch):
        super(GUILayout, self).on_touch_down(touch)
        button = self.get_button(touch)
        self.action(button.name if button else None)(button)



class GUIApp(App):
    def build(self):
        # self.load_kv('GUI.kv')
        return GUILayout()


if __name__=='__main__':
    ip = ImageProperties()
    GUIApp().run()


# class iButton(BoxLayout):
#     def __init__(self, **kwargs):
#         print 'iButton.pos -> ', self.pos
#         super(iButton, self).__init__(**kwargs)
#         self.orientation = 'horizontal'
#         with self.canvas:
#             Color(1, 1, 1, 1, mode='rgba')
#             Rectangle(pos=self.pos, size=self.size)
#
#         self.add_widget(Button(**kwargs))
#
#
# class ManyLayouts(Screen, GridLayout):
#     def __init__(self, **kwards):
#         super(ManyLayouts, self).__init__(**kwards)
#         with self.canvas:
#             Color(1, 1, 1, 1, mode='rgba')
#             rectPos = map(lambda x, y: x+ y, self.pos, LD_edge)
#             Rectangle(pos=rectPos, source=imgTownCenterPath)
#
#         self.layout = GridLayout(rows=3, spaceing=1, padding=5)
#         self.Button1 = iButton(id='1', text='Level 1', size=(100, 100))
#         # self.Button2 = iButton(id='2', text='Level 2')
#         # self.Button3 = Button(id='3', text='Level 3')
#         # self.Button4 = Button(id='4', text='Level 4')
#         self.layout.add_widget(self.Button1)
#         # self.layout.add_widget(self.Button2)
#         # self.layout.add_widget(self.Button3)
#         # self.layout.add_widget(self.Button4)
#         ManyLayouts.add_widget(self, self.layout)
#
#
# class GUIApp(App):
#     def build(self):
#         sm = ScreenManager()
#         sm.add_widget(ManyLayouts(name='level'))
#         return sm
#
# if __name__ == '__main__':
#     # img = Image(source='SOURCE-2.jpg', allow_stretch=False, keep_ratio=True)
#     GUIApp().run()
