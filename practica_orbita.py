from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
from math import pi, sin, cos, asin

altura, ancho = 800, 800

ojox, ojoy, ojoz = 4, 6, 4

elapsedTime = 0
thisFrame = 0
lastFrame = 0
startTime = 0

totalTime = 1
fps = 60

orbit_a = 5
orbit_b = 10
orbit_scale = 0.2
speed = 1
rotation = 0

debug = True

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
    global debug
    global speed, rotation

    viewMatrix = 0
    if startTime == 0:
        # Selecciona la matriz de proyección
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()  # Inicializar la matriz.

        # Ángulo, ratio, near, far
        gluPerspective(45, altura/ancho, 0.1, 20.0)

        # Seleccionar la matriz modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Lighting
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        
        # glEnable(GL_COLOR_MATERIAL)
        # glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Desde, Hacia, Dirección arriba
        gluLookAt(ojox, ojoy, ojoz, 0, 0, 0, 0.0, 1.0, 0.0)

        startTime = time.time()
        lastFrame = startTime
        totalTime = 1

    thisFrame = time.time()
    elapsedTime = thisFrame - lastFrame
    lastFrame = thisFrame

    totalTime += elapsedTime

    if totalTime >= 1.0 / fps:
        totalTime = 0

        # print(".")
        rotation += speed / fps

        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # glPushMatrix()
        # glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 0))
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 0))
        # # glTranslate(-0.05 * rotacionY, 0, 0)
        # # glRotate(rotacionY, 0, 1, 0)
        # # print(rotacionY)
        # glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
        # glPopMatrix()


        glPushMatrix()
        # glLoadIdentity()
        # glTranslate(-0.05 * rotacionY, 0, 0)
        # glRotate(rotacionY, 0, 1, 0)
        if debug:
            ejes()

        Sistema(rotation)
        glFlush()
        glPopMatrix()

    glutPostRedisplay()


def ejes():
    # Eje x
    largo = 4
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


# t en radianes
def Sistema(t):
    global orbit_a, orbit_b, orbit_scale

    x, z = orbit_scale * orbit_a * cos(t), orbit_scale * orbit_b * sin(t)
    print((x, z))

    glPushMatrix()
    glColor3f(1, 1, 0)
    glTranslate(-0.05 * x, 0, -0.05 * z)
    glutSolidSphere(0.5, 20, 20)
    glPopMatrix()

    rot = -10 * t

    glPushMatrix()
    glTranslate(x, 0, z)
    glRotate(rot / pi * 180, 0, 1, 0)
    glColor3f(0, 0.2, 1)
    glutSolidSphere(0.2, 4, 3)
    glPopMatrix()


def buttons(key, x, y):
    global resolution, width, debug

    print(f'key={key}')
    # glutPostRedisplay()
    
    if key == b'd':
        debug = not debug


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glDepthFunc(GL_LESS)
    glutInitWindowSize(altura, ancho)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutCreateWindow("Orbita")
    glutDisplayFunc(display)
    glutKeyboardFunc(buttons)
    glutMainLoop()


main()
