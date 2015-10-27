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

# class GUI(App):
#     def build(self):
#         pass
#
# if __name__ == '__main__':
#     # img = Image(source='SOURCE-2.jpg', allow_stretch=False, keep_ratio=True)
#     # print img.size, img.norm_image_size
#     GUI().run()


# runTouchApp(Builder.load_string('''
# ActionBar:
#     pos_hint: {'top':1}
#     ActionView:
#         use_separator: True
#         ActionPrevious:
#             title: 'Action Bar'
#             with_previous: False
#         ActionOverflow:
#         ActionButton:
#             text: 'Btn1'
#         ActionButton:
#             text: 'Btn2'
#         ActionButton:
#             text: 'Btn3'
#         ActionButton:
#             text: 'Btn4'
#         ActionGroup:
#             text: 'Group1'
#             ActionButton:
#                 text: 'Btn5'
#             ActionButton:
#                 text: 'Btn6'
#             ActionButton:
#                 text: 'Btn7'
# '''))
