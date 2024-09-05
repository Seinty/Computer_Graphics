import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Размер окна
width,height = 600,600
#window_titles = ["Задание 1", "Задание 2", "Задание 3"]

# Вершины многоугольника Θ (включая однородную координату)
vertices = np.array([
    [300, 330],
    [270,290],
    [340, 300]
], dtype=int)

# Прямая Λ, проходящая через точки K и L
K = np.array([240, 240], dtype=float)
L = np.array([420, 250], dtype=float)

Light = np.array([300,420],dtype = float)
def to_homogeneous(coords: np.ndarray) -> np.ndarray:
    """
    Преобразование массива точек из обычных координат в однородные.

    :param coords: Массив точек в обычных координатах, размерностью (n, 2).
    :return: Массив точек в однородных координатах, размерностью (n, 3).
    """
    if coords.shape[1] != 2:
        raise ValueError("Input coordinates must have shape (n, 2)")

    # Добавляем третий компонент со значением 1 для каждой точки
    ones = np.ones((coords.shape[0], 1))
    homogeneous_coords = np.hstack((coords, ones))
    return homogeneous_coords


def to_cartesian(homogeneous_coords: np.ndarray) -> np.ndarray:
    """
    Преобразование массива точек из однородных координат в обычные.

    :param homogeneous_coords: Массив точек в однородных координатах, размерностью (n, 3).
    :return: Массив точек в обычных координатах, размерностью (n, 2).
    """
    if homogeneous_coords.shape[1] != 3:
        raise ValueError("Input coordinates must have shape (n, 3)")

    # Делим первые два компонента на третий для получения обычных координат
    cartesian_coords = homogeneous_coords[:, :2] / homogeneous_coords[:, 2][:, np.newaxis]
    return cartesian_coords

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Рисуем исходную фигуру
    draw_polygon(vertices, color=(0, 1, 0))

    # Рисуем прямую
    draw_line(K, L, color=(0, 0, 1))

    draw_light(Light, color=(1,0,0))

    proj_vert = projections(vertices,K,L)
    draw_proj(proj_vert,color=(1,0,0))
    # Выполняем отражение
    reflected_vertices = reflect(vertices, K, L)

    # Рисуем отраженную фигуру
    draw_polygon(reflected_vertices[:, :2], color=(1, 0, 0))

    glfw.swap_buffers(window)


def draw_proj(vertices,color):
    glColor3f(*color)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    for vertex in vertices:
        glVertex2f(vertex[0], vertex[1])
    glEnd()
def draw_polygon(vertices, color):
    glColor3f(*color)
    glBegin(GL_POLYGON)
    for vertex in vertices:
        glVertex2f(vertex[0], vertex[1])
    glEnd()

def draw_line(K, L, color):
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex2f(K[0], K[1])
    glVertex2f(L[0], L[1])
    glEnd()

def draw_light(Light,color):
    glColor3f(*color)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    glVertex2f(Light[0], Light[1])
    glEnd()

def line_eq(K,L):
    return (L[1]-K[1],K[0]-L[0],L[0]*K[1]-K[0]*L[1])

def reflect(vertices, K, L):

    teta = np.arctan((L[1]-K[1])/(L[0]-K[0]))
    # Матрица отражения в однородных координатах
    M_reflect = np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])

    # Смещение вершин так, чтобы прямая проходила через начало координат
    T1 = np.eye(3)
    T1[:2, 2] = -K

    Rp = np.array([
        [np.cos(teta),np.sin(teta),0],
        [-np.sin(teta),np.cos(teta),0],
        [0,         0,          1]
    ])

    Rm = np.array([
        [np.cos(teta), -np.sin(teta), 0],
        [np.sin(teta), np.cos(teta), 0],
        [0, 0, 1]
    ])

    # Обратное смещение после отражения
    T2 = np.eye(3)
    T2[:2, 2] = K

    # Полная матрица преобразования
    M = T2@Rm@M_reflect@Rp@T1

    # Применение матрицы отражения к каждой вершине
    od_vertices = to_homogeneous(vertices)
    reflected_vertices = od_vertices @ M.T
    return to_cartesian(reflected_vertices)

def projections(vertices,K,L):
    vert = to_homogeneous(vertices)
    l_v = np.array([1,-1])
    matrix = np.eye(len(vert))
    A,B,C = line_eq(K,L)
    temp = np.array((A,B,C)) / (np.array((A, B)) @ l_v)
    temp = np.tile(temp, (2, 1))
    temp = (temp.T * np.array((0, -1))).T
    matrix[:2] -= temp

    projection = vert@matrix.T

    return to_cartesian(projection)




def main():
    if not glfw.init():
        return

    global window
    window = glfw.create_window(width, height, "OpenGL Reflection Example", None, None)
    if not window:
       glfw.terminate()
       return

    glfw.make_context_current(window)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, width, 0, height)

    while not glfw.window_should_close(window):
        display()
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()