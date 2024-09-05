import glfw
from OpenGL.GL import *
import numpy as np

# Инициализация GLFW
if not glfw.init():
    raise Exception("GLFW can't be initialized")

# Создание окон
window_size = (600,600)
window_titles = ["Задание 1: Отражение относительно прямой", "Задание 2", "Задание 3"]

windows = []
for title in window_titles:
    window = glfw.create_window(*window_size, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception(f"GLFW window {title} can't be created")
        # Устанавливаем ортографическую проекцию для текущего окна
    glfw.make_context_current(window)
    glMatrixMode(GL_PROJECTION)
    glOrtho(0, window_size[0], 0, window_size[1],1,-1)
    glMatrixMode(GL_MODELVIEW)

    windows.append(window)

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


# Функция для задания 1 (Отражение относительно прямой)
def task_1(window):
    # Вершины многоугольника Θ (включая однородную координату)
    vertices = np.array([
        [300, 330],
        [270, 290],
        [340, 300]
    ], dtype=int)

    # Прямая Λ, проходящая через точки K и L
    K = np.array([240, 240], dtype=float)
    L = np.array([420, 250], dtype=float)

    glClear(GL_COLOR_BUFFER_BIT)
    draw_polygon(vertices, color=(0, 1, 0))
    draw_line(K, L, color=(0, 0, 1))
    reflected_vertices = reflect(vertices, K, L)
    draw_polygon(reflected_vertices, color=(1, 0, 0))
    glfw.swap_buffers(window)


# Функция для задания 2 (например, рисование квадрата)
def task_2(window):
    glClear(GL_COLOR_BUFFER_BIT)
    vertices = np.array([
        [-0.5, -0.5],
        [0.5, -0.5],
        [0.5, 0.5],
        [-0.5, 0.5]
    ])
    draw_polygon(vertices, color=(0, 0, 1))
    glfw.swap_buffers(window)


# Функция для задания 3 (например, рисование круга)
def task_3(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POLYGON)
    for i in range(100):
        angle = 2 * np.pi * i / 100
        glColor3f(1.0, i / 100.0, 0.0)
        glVertex2f(np.cos(angle) * 0.5, np.sin(angle) * 0.5)
    glEnd()
    glfw.swap_buffers(window)

# Основной цикл
while not any(glfw.window_should_close(win) for win in windows):
    glfw.poll_events()
    # Выполняем задачи в каждом окне
    for i, win in enumerate(windows):
        glfw.make_context_current(win)
        if i == 0:
            task_1(win)
        elif i == 1:
            task_2(win)
        elif i == 2:
            task_3(win)

# Завершаем работу и закрываем окна
for win in windows:
    glfw.destroy_window(win)
glfw.terminate()