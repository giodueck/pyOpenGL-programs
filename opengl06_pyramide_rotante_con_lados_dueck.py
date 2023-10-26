from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time

altura, ancho = 800, 800

ojox, ojoy, ojoz = 0.8, 0.8, 2

elapsedTime = 0
thisFrame = 0
lastFrame = 0
startTime = 0

totalTime = 1
fps = 60

velocidadAngularY = 90
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

    if startTime == 0:
        # Lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        # glLoadIdentity()
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 0, 0, 0))
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 0, 0))

        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Selecciona la matriz de proyección
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()  # Inicializar la matriz.

        # Ángulo, ratio, near, far
        gluPerspective(35, altura/ancho, 0.1, 10.0)

        # Seleccionar la matriz modelview
        glMatrixMode(GL_MODELVIEW)

        # Inicializar la matriz.
        glLoadIdentity()

        # Desde, Hacia, Dirección arriba
        ojox += 0.2
        gluLookAt(ojox, ojoy, ojoz, 0, 0, 0, 0.0, 1.0, 0.0)

        startTime = time.time()
        lastFrame = startTime


    thisFrame = time.time()
    elapsedTime = thisFrame - lastFrame
    lastFrame = thisFrame

    totalTime += elapsedTime
    # print(totalTime)

    if totalTime >= 1.0 / fps:
        totalTime -= 1.0 / fps

        rotacionY += velocidadAngularY / fps

        glPushMatrix()
        glLightfv(GL_LIGHT0, GL_AMBIENT, (1, 1, 1, 0))
        glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
        glPopMatrix()

        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ejes()

        glPushMatrix()
        # glRotate(elapsedTime // 50, 1, 0, 0)
        glRotate(rotacionY, 0, 1, 0)
        glTranslate(-0.15, 0, -0.15)
        # Cube()
        Pyramid()
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


def Cube():
    vertices = []
    ancho = 0.3
    z = 0
    # Inferior izquierdo
    vertices.append((0, 0, z))
    # Inferior derecho
    vertices.append((ancho, 0, z))
    # Superior derecho
    vertices.append((ancho, ancho, z))
    # Superior izquierdo
    vertices.append((0, ancho, z))

    square = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
    )

    # ejes()

    # Cara izquierda #rosada
    glPushMatrix()
    glRotate(-90, 0, 1, 0)
    cara(vertices, (0.8, 0.2, 0.5))
    glPopMatrix()

    # Cara inferior #amarillo
    glPushMatrix()
    glRotate(90, 1, 0, 0)
    cara(vertices, (0.7, 0.7, 0.1))
    glPopMatrix()

    # Cara derecha #celeste
    glPushMatrix()
    glTranslatef(ancho, 0, 0)
    glRotate(-90, 0, 1, 0)
    cara(vertices, (0.2, 0.4, 0.8))
    glPopMatrix()

    # Cara frontal #verde
    glPushMatrix()
    glTranslatef(0, 0, ancho)
    # cara(vertices, (0.1, 0.7, 0.2))
    glPopMatrix()

    # Cara superior #lila
    glPushMatrix()
    glTranslatef(0, ancho, 0)
    glRotate(90, 1, 0, 0)
    cara(vertices, (0.3, 0.1, 0.3))
    glPopMatrix()

    # Cara trasera #gris
    cara(vertices, (0.4, 0.4, 0.4))

    glFlush()


def Pyramid():
    vertices = []
    ancho = 0.3
    z = 0
    # Inferior izquierdo
    vertices.append((0, 0, z))
    # Inferior derecho
    vertices.append((ancho, 0, z))
    # Superior derecho
    vertices.append((ancho/2, ancho, z))

    # Cara trasera #gris
    glPushMatrix()
    glRotate(30, 1, 0, 0)
    cara(vertices, (0.4, 0.4, 0.4))
    glPopMatrix()

    # Cara izquierda #rosada
    glPushMatrix()
    glRotate(-30, 0, 0, 1)
    glRotate(-90, 0, 1, 0)
    cara(vertices, (0.8, 0.2, 0.5))
    glPopMatrix()

    # Cara izquierda #amarilla
    glPushMatrix()
    glTranslate(ancho, 0, 0)
    glRotate(30, 0, 0, 1)
    glRotate(-90, 0, 1, 0)
    cara(vertices, (0.8, 0.8, 0.0))
    glPopMatrix()

    # Cara frontal #blanco
    glPushMatrix()
    glTranslate(0, 0, ancho)
    glRotate(-30, 1, 0, 0)
    cara(vertices, (0.9, 0.9, 0.9))
    glPopMatrix()

    glFlush()


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
    glutCreateWindow("Cubo 3D con rotación de caras")
    glutDisplayFunc(display)
    glutKeyboardFunc(buttons)
    glutMainLoop()


main()
