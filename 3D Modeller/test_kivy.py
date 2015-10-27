from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen,FallOutTransition
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import BorderImage
from kivy.graphics import Color, Rectangle ,Line

#################     Images   ######################
S = Image(source='SOuRCE-2.jpg')
L = 'images/spinnin.gif'
#################     Images   ######################


class CButtonW(BoxLayout):
    def __init__(self, **kwargs):
        print "init --> CButton self.pos is ",self.pos
        super(CButtonW, self).__init__(**kwargs)
        self.orientation = 'vertical'
        with self.canvas.before:
            Color(1, 1, 0, 1, mode='rgba')
            Rectangle(pos=self.pos,size=self.size)
            BorderImage(
                     border=(10, 10, 10, 10),
                    source='images/tex.png')

        self.add_widget(S)
        self.add_widget(Button(text="Button 1"))
        self.add_widget(Image(source=L))


class LevelScreen(Screen,GridLayout):
    def __init__(self, **kwargs):
        super(LevelScreen, self).__init__(**kwargs)
        with self.canvas:
            Line(points=(10, 10, 20, 30, 40, 50))
            Color(1, 0, 1, 1, mode='rgba')
            Rectangle(pos=self.pos, size=Window.size)

        self.layout = GridLayout(cols=3,spacing=1,padding=10)
        self.Button1 = CButtonW(id='1',text='Level 1')
        # self.Button2 = Button(id='2',text='Level 2')
        # self.Button3 = Button(id='3',text='Level 3')
        # self.Button4 = Button(id='4',text='Level 4')
        self.layout.add_widget(self.Button1)
        # self.layout.add_widget(self.Button2)
        # self.layout.add_widget(self.Button3)
        # self.layout.add_widget(self.Button4)

        LevelScreen.cols=3
        LevelScreen.add_widget(self,self.layout)
        # print "position of 1st button is ",self.Button1.pos
        # print "position of 2 button is ",self.Button2.pos


# App Class
class MyJBApp(App):
    def build(self):
        sm = ScreenManager(transition= FallOutTransition())
        sm.add_widget(LevelScreen(name='level'))
        return sm

if __name__ == '__main__':
    MyJBApp().run()
