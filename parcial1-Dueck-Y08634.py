'''
Parcial 1
Giovanni Dueck
Matricula Y08634

Controles:
    x: Mover +X
    Shift+x: Mover -X

    y: Toggle rotacion alrededor del eje Y

    r: Toggle rotacion alrededor de la primera arista

    m: Aumentar cantidad de triangulos (inicialmente 4)
    n: Disminuir cantidad de triangulos (minimo 2)
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
from math import atan, pi

altura, ancho = 800, 800

ojox, ojoy, ojoz = 2, 2, 2

elapsedTime = 0
thisFrame = 0
lastFrame = 0
startTime = 0

totalTime = 1
fps = 60

offsetX = 0
xIncrement = 0.1

angularSpeed = 60
doRotate = False
rotation = 0
doRotateY = False
rotationY = 0

triangleCount = 4
b, h = 0.2, 0.6

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
    global rotation, rotationY
    global doRotate, doRotateY
    global offsetX
    global b, h

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

        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Desde, Hacia, Dirección arriba
        gluLookAt(ojox, ojoy, ojoz, 0, 0, 0, 0.0, 1.0, 0.0)

        startTime = time.time()
        lastFrame = startTime

    # Manejo del tiempo para una velocidad de simulacion constante sin importar
    # la cantidad de recursos que tiene disponibles el programa
    thisFrame = time.time()
    elapsedTime = thisFrame - lastFrame
    lastFrame = thisFrame

    totalTime += elapsedTime

    # Una vez cada frame
    if totalTime >= 1.0 / fps:
        totalTime = 0

        if doRotate:
            rotation += angularSpeed / fps
        if doRotateY:
            rotationY += angularSpeed / fps

        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        ejes()

        # Rotacion y traslacion con respecto a los ejes es simple
        glRotate(rotationY, 0, 1, 0)
        glTranslate(offsetX, 0, 0)
        
        # Angulo de b con hipotenusa: phi = atan(h/b)
        # Ya que cos(phi) = cateto opuesto / cateto adyacente
        # Convertido a grados y rotado con respecto al origen por 90 grados en sentido horario
        angle = atan(h/b) * 180 / pi - 90

        # 1. Transladar recta al origen
        # 2. Rotar en Y, ya esta alineada en X y Z
        # 3. Rotar alrededor de la recta, ahora alineada con el eje Y
        # 4. Deshacer transformaciones en orden inverso

        glTranslate(b, 0, 0)        # 4.1
        glRotate(-angle, 0, 0, 1)   # 4.2
        glRotate(rotation, 0, 1, 0) # 3.
        glRotate(angle, 0, 0, 1)    # 2.
        glTranslate(-b, 0, 0)       # 1.

        Piramide()

        glFlush()
        glPopMatrix()

    # Llama otra vez la funcion display
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


def Piramide():
    global triangleCount
    global b, h

    vertices = [(0, 0, 0), (b, 0, 0), (0, h, 0)]

    angle = 360 / triangleCount

    glPushMatrix()
    # Redibujar la cara cada angle grados, rotada y con un color parametrico dependiente de su indice
    for i in range(triangleCount):
        glRotate(angle, 0, 1, 0)
        cara(vertices, (0, 1 / (triangleCount - 1) * i, 1 - 1 / (triangleCount - 1) * i))
    glPopMatrix()


def buttons(key, x, y):
    global offsetX, xIncrement
    global doRotate
    global doRotateY
    global triangleCount

    # print(f'key={key}')
    
    if key == b'x':
        offsetX += xIncrement
    if key == b'X':
        offsetX -= xIncrement
    
    if key == b'y':
        doRotateY = not doRotateY
    if key == b'r':
        doRotate = not doRotate
    
    if key == b'm':
        triangleCount += 1
    if key == b'n':
        triangleCount -= 1
        if triangleCount < 2:
            triangleCount = 2


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
