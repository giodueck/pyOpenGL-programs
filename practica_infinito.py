from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
from math import pi, sin, cos, asin

altura, ancho = 800, 800

ojox, ojoy, ojoz = 0, 0, 3

elapsedTime = 0
thisFrame = 0
lastFrame = 0
startTime = 0

totalTime = 1
fps = 60

resolution = 36
width = 1

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
        # rotacionY += velocidadAngularY / fps

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
        # Cube()
        Infinity()
        glFlush()
        glPopMatrix()

    # glutPostRedisplay()


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


def Infinity():
    global resolution, width
    global debug

    scale = lambda t: 2 / (3 - cos(2 * t))
    xcoord = lambda t: scale(t) * cos(t)
    ycoord = lambda t: scale(t) * sin(2 * t) / 2

    vertices = []

    increment = 360 // resolution
    for i in range(0, 360, increment):
        rad = i / 180 * pi
        radinc = (i + increment) / 180 * pi

        point = (xcoord(rad), ycoord(rad), 0)
        next_point = (xcoord(radinc), ycoord(radinc), 0)
        normal_start = [(next_point[j] + point[j]) / 2 for j in range(3)]
        normal1_end = normal_start
        normal2_end = normal_start
        if next_point[0] - point[0] != 0:
            normal1_end = (- (next_point[1] - point[1]) * width / 2, (next_point[0] - point[0]) * width / 2, 0)
            normal1_end = [normal1_end[j] + normal_start[j] for j in range(3)]

            normal2_end = ((next_point[1] - point[1]) * width / 2, - (next_point[0] - point[0]) * width / 2, 0)
            normal2_end = [normal2_end[j] + normal_start[j] for j in range(3)]


        if debug:
            glBegin(GL_LINES)

            glColor3f(0, 1, 1)
            glVertex3f(point[0], point[1], point[2])
            glVertex3f(next_point[0], next_point[1], next_point[2])

            glColor3f(1, 1, 0)
            glVertex3f(normal_start[0], normal_start[1], normal_start[2])
            glVertex3f(normal1_end[0], normal1_end[1], normal1_end[2])

            glColor3f(1, 0, 1)
            glVertex3f(normal_start[0], normal_start[1], normal_start[2])
            glVertex3f(normal2_end[0], normal2_end[1], normal2_end[2])

            glEnd()

            glPushMatrix()
            glTranslate(normal_start[0], normal_start[1], normal_start[2])
            glutSolidSphere(0.01, 5, 5)
            glPopMatrix()

        vertices.append(normal1_end)
        vertices.append(normal2_end)

    glBegin(GL_TRIANGLE_STRIP)
    glColor3f(1, 1, 1)
    for v in vertices:
        glVertex3f(v[0], v[1], v[2])
    glVertex3f(vertices[0][0], vertices[0][1], vertices[0][2])
    glVertex3f(vertices[1][0], vertices[1][1], vertices[1][2])
    glEnd()


def buttons(key, x, y):
    global resolution, width, debug

    print(f'key={key}')
    glutPostRedisplay()
    
    if key == b'+':
        resolution *= 2
        width *= 2
        if resolution >= 288:
            resolution = 288
            width /= 2
        print(resolution)
    if key == b'-':
        resolution //= 2
        width /= 2
        if resolution <= 9:
            resolution = 9
            width *= 2
        print(resolution)
        
    if key == b'.':
        width += 0.2
    if key == b',':
        width -= 0.2
    
    if key == b'd':
        debug = not debug


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glDepthFunc(GL_LESS)
    glutInitWindowSize(altura, ancho)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutCreateWindow("Infinito")
    glutDisplayFunc(display)
    glutKeyboardFunc(buttons)
    glutMainLoop()


main()
