from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import glutInit, glutInitDisplayMode
from PIL import Image  # PIL
import sys
import math

angle = 0.0
angle2 = 0.0
texture = 0
object = 0
d = 3.0 / math.sqrt(3)


def drawBox(x1, x2, y1, y2, z1, z2):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_POLYGON)  # front face
    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(0, 0)
    glVertex3f(x1, y1, z2)
    glTexCoord2f(1, 0)
    glVertex3f(x2, y1, z2)
    glTexCoord2f(1, 1)
    glVertex3f(x2, y2, z2)
    glTexCoord2f(0, 1)
    glVertex3f(x1, y2, z2)
    glEnd()

    glBegin(GL_POLYGON)  # back face
    glNormal3f(0.0, 0.0, -1.0)
    glTexCoord2f(1, 0)
    glVertex3f(x2, y1, z1)
    glTexCoord2f(0, 0)
    glVertex3f(x1, y1, z1)
    glTexCoord2f(0, 1)
    glVertex3f(x1, y2, z1)
    glTexCoord2f(1, 1)
    glVertex3f(x2, y2, z1)
    glEnd()

    glBegin(GL_POLYGON)  # left face
    glNormal3f(-1.0, 0.0, 0.0)
    glTexCoord2f(0, 0)
    glVertex3f(x1, y1, z1)
    glTexCoord2f(0, 1)
    glVertex3f(x1, y1, z2)
    glTexCoord2f(1, 1)
    glVertex3f(x1, y2, z2)
    glTexCoord2f(1, 0)
    glVertex3f(x1, y2, z1)
    glEnd()

    glBegin(GL_POLYGON)  # right face
    glNormal3f(1.0, 0.0, 0.0)
    glTexCoord2f(0, 1)
    glVertex3f(x2, y1, z2)
    glTexCoord2f(0, 0)
    glVertex3f(x2, y1, z1)
    glTexCoord2f(1, 0)
    glVertex3f(x2, y2, z1)
    glTexCoord2f(1, 1)
    glVertex3f(x2, y2, z2)
    glEnd()

    glBegin(GL_POLYGON)  # top face
    glNormal3f(0.0, 1.0, 0.0)
    glTexCoord2f(0, 1)
    glVertex3f(x1, y2, z2)
    glTexCoord2f(1, 1)
    glVertex3f(x2, y2, z2)
    glTexCoord2f(1, 0)
    glVertex3f(x2, y2, z1)
    glTexCoord2f(0, 0)
    glVertex3f(x1, y2, z1)
    glEnd()

    glBegin(GL_POLYGON)  # bottom face
    glNormal3f(0.0, -1.0, 0.0)
    glTexCoord2f(1, 1)
    glVertex3f(x2, y1, z2)
    glTexCoord2f(1, 0)
    glVertex3f(x1, y1, z2)
    glTexCoord2f(0, 0)
    glVertex3f(x1, y1, z1)
    glTexCoord2f(0, 1)
    glVertex3f(x2, y1, z1)
    glEnd()


def loadTexture(fileName):
    image = Image.open(fileName)
    width = image.size[0]
    height = image.size[1]
    image = image.tobytes("raw", "RGBX", 0, -1)
    texture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture)  # 2d texture (x and y size)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image)

    return texture


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width) / float(height), 1.0, 60.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 0, 1, 1, 1, 0, 1, 0)
    glTranslatef(4, 4, 4)
    glRotatef(angle2, 1, -1, 0)
    glTranslatef(d - 1.5, d - 1.5, d - 1.5)
    glTranslatef(1.5, 1.5, 1.5)  # move cube from the center
    glRotatef(angle, 1.0, 1.0, 0.0)
    glTranslatef(-1.5, -1.5, -1.5)  # move cube into the center
    drawBox(1, 2, 1, 2, 1, 2)

    glutSwapBuffers()


def keyPressed(*args):
    if args[0] == '\033':
        sys.exit()


def animate():
    global angle, angle2

    angle = 0.04 * glutGet(GLUT_ELAPSED_TIME)
    angle2 = 0.01 * glutGet(GLUT_ELAPSED_TIME)

    glutPostRedisplay()


def main():
    global texture

    print bool(glutInit)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)

    glutCreateWindow("Simple PyOpenGL example")
    glutDisplayFunc(display)
    # glutIdleFunc(animate)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyPressed)
    init()

    texture = loadTexture("Results\\EmptyInterface.png")

    glutMainLoop()


print "Hit ESC key to quit."
main()
