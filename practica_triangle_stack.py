from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
from math import pi, sin, cos, asin, sqrt

altura, ancho = 800, 800

ojox, ojoy, ojoz = 0, 0, 2

elapsedTime = 0
thisFrame = 0
lastFrame = 0
startTime = 0

totalTime = 1
fps = 60

side = 0.1
N = 1

debug = False

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
    global N

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

        glPushMatrix()
        glTranslate(- side * N / 2, - side * N * sqrt(3) / 4, 0)
        TriangleStack(N)
        glPopMatrix()

        glFlush()
        glPopMatrix()

    # glutPostRedisplay()


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


def TriangleStack(n):
    global side

    if n <= 0:
        return

    vertices = [(0, 0, 0), (side, 0, 0), (side / 2, sqrt(3) / 2 * side, 0)]
    # print(vertices)
    # cara(vertices, (0, 1, 1))

    glPushMatrix()
    for i in range(n):
        cara(vertices, (i / n, 0.2, 1))
        glTranslate(side, 0, 0)
    glPopMatrix()
    
    glTranslate(vertices[2][0], vertices[2][1], 0)
    TriangleStack(n - 1)


def buttons(key, x, y):
    global debug
    global N

    print(f'key={key}')
    glutPostRedisplay()
    
    if key == b'd':
        debug = not debug

    if key == b'+':
        N += 1
    
    if key == b'-':
        N -= 1
        if N < 1:
            N = 1


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glDepthFunc(GL_LESS)
    glutInitWindowSize(altura, ancho)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutCreateWindow("Triangle Stack")
    glutDisplayFunc(display)
    glutKeyboardFunc(buttons)
    glutMainLoop()


main()
