'''
TODO: Use a list of vertices, a list of surfaces, and a list of surface normals.
      Render using this list

'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
from math import pi, sin, cos, asin
import numpy

altura, ancho = 800, 800

ojox, ojoy, ojoz = 2, 2, 2

elapsedTime = 0
thisFrame = 0
lastFrame = 0
startTime = 0

totalTime = 1
fps = 60

velocidadAngularY = 30
rotacionY = 0

def cara(vertices, color):
    glColor(color[0], color[1], color[2], 1)
    if len(vertices) == 4:
        glBegin(GL_QUADS)
    elif len(vertices) == 3:
        glBegin(GL_TRIANGLES)
    else:
        return
    for v in vertices:
        glVertex3fv(v)
    glEnd()


def display():
    global ojox, ojoy, ojoz
    global elapsedTime, startTime, lastFrame, thisFrame, totalTime
    global fps
    global rotacionY

    viewMatrix = 0
    if startTime == 0:
        # Selecciona la matriz de proyección
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()  # Inicializar la matriz.

        # Ángulo, ratio, near, far
        gluPerspective(45, altura/ancho, 0.1, 10.0)

        # Seleccionar la matriz modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Desde, Hacia, Dirección arriba
        gluLookAt(ojox, ojoy, ojoz, 0, 0, 0, 0.0, 1.0, 0.0)

        startTime = time.time()
        lastFrame = startTime

    thisFrame = time.time()
    elapsedTime = thisFrame - lastFrame
    lastFrame = thisFrame

    totalTime += elapsedTime

    if totalTime >= 1.0 / fps:
        totalTime = 0

        rotacionY += velocidadAngularY / fps

        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        # glLoadIdentity()

        glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 0))
        # glTranslate(-0.05 * rotacionY, 0, 0)
        glRotate(rotacionY, 0, 1, 0)
        # print(rotacionY)
        glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
        glPopMatrix()


        glPushMatrix()
        # glLoadIdentity()
        # glTranslate(-0.05 * rotacionY, 0, 0)
        glRotate(rotacionY, 0, 1, 0)
        ejes()
        # Cube()
        # glRotate(rotacionY, 0, 1, 0)
        Star()
        glFlush()
        glPopMatrix()

    glutPostRedisplay()


def ejes():
    # Eje x
    largo = 2
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(largo, 0, 0)

    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, largo, 0)

    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, largo)

    glEnd()


def Star():
    ancho = 0.3
    y = 0
    dy = 0.2

    square = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
    )

    penta_low, penta_high = Pentagon(ancho, y, y + dy)
    star_low = [(2.618 * ancho * cos(2 * pi / 5 * (i + 1/2)), y, 2.618 * ancho * sin(2 * pi / 5 * (i + 1/2))) for i in range(5)]
    star_high = [(2.618 * ancho * cos(2 * pi / 5 * (i + 1/2)), y + dy, 2.618 * ancho * sin(2 * pi / 5 * (i + 1/2))) for i in range(5)]

    for i in range(5):
        cara([penta_low[i], penta_low[(i + 1) % 5], star_low[i]], (1, 1, 0))
        cara([penta_high[i], penta_high[(i + 1) % 5], star_high[i]], (1, 1, 0))

        cara([penta_low[i], penta_high[i], star_high[i], star_low[i]], (0.8, 0.8, 0))
        cara([penta_low[(i + 1) % 5], penta_high[(i + 1) % 5], star_high[i], star_low[i]], (0.6, 0.6, 0))
        pass

    glFlush()

def Pentagon(ancho, y, y2):
    vertices = []

    centro = (0, y, 0);
    vertices = [(ancho * cos(2 * pi / 5 * i), y, ancho * sin(2 * pi / 5 * i)) for i in range(5)]
    centro_high = (0, y2, 0);
    vertices_high = [(ancho * cos(2 * pi / 5 * i), y2, ancho * sin(2 * pi / 5 * i)) for i in range(5)]

    glPushMatrix()
    for i in range(5):
        cara([vertices[i], centro, vertices[(i + 1) % 5]], (1, 1, 1))
        cara([vertices_high[i], centro_high, vertices_high[(i + 1) % 5]], (1, 1, 0))
        
        # cara([vertices[i], vertices[(i + 1) % 5], vertices_high[(i + 1) % 5], vertices_high[i]], (0.7, 0.7, 0.7))
    glPopMatrix()

    return vertices, vertices_high


def buttons(key, x, y):
    global ojox
    print(f'key={key}')
    
    if key == b'a':
        ojox += 0.1


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glDepthFunc(GL_LESS)
    glutInitWindowSize(altura, ancho)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutCreateWindow("Estrella 3D")
    glutDisplayFunc(display)
    glutKeyboardFunc(buttons)
    glutMainLoop()


main()
