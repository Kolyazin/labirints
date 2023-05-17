# This is a sample Python script.
import random


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Итак, нам нужна программа, которая
# 1. получит схему лабиринта в виде последовательности из семи строк
#   по семь символов в строке. Каждая входная строка представляет горизонталь лабиринта, а порядок строк соответствует
#   порядку горизонталей, считая сверху вниз. Элементы лабиринта (символы в строке) упорядочены слева направо.
#   "Пустой" элемент лабиринта (доступный для прохода) во входной строке обозначается точкой ("."),
#   а символ звездочка ("*") соответствует элементу со стеной (закрытому для прохода).
# 2. попробует найти кратчайший путь от крайнего верхнего левого узла до крайнего нижнего правого узла соблюдая
#   следующие условия: путь должен проходить только через "свободные" узлы и не может включать в себя один и тот же
#   узел более одного раза. "Соседними" узлами в пути могут быть узлы, смежные по вертикали или по горизонтали,
#   но не по диагонали.
# 3. выведет графическое представление пути, если путь найден. В противном случае выведет сообщение об отсутствии пути.
# 4. выведет схему лабиринта
#
#
#

# Получает с консоли семь строк содержащих по семь символов * или .
# если get_from_console = true, то ждем ввода лабиринта пользователем, если нет, то отдаем заданный по умолчанию.
def get_labyrinth(get_from_console: bool) -> []:
    # инициализирую массив из семи строк, точнее список, т.к. в питоне нет массивов
    s = ['..**..*',
         '..*..**',
         '.**.***',
         '....***',
         '**....*',
         '*..**.*',
         '*..**..']
    # если get_from_console не true, то возвращаю заданный по умолчанию лабиринт
    if not get_from_console:
        return s
    # вывожу подсказку
    print('Определите схему лабиринта (7 строк по 7 символов "•" или "*"):')
    # цикл от 0 до 6 включительно (как раз 7 раз сработает)
    for i in range(7):
        # бесконечный цикл выход из которого будет только тогда, когда пользователь введет корректную строку,
        # длиной в 7 символов и только точки или звездочки
        while True:
            # жду ввода пользователя
            s[i] = input('Строка %d:' % i)
            # проверяю, что строка длиной в 7 символов и только точки или звездочки
            # и если это так, то прерываю цикл while и перехожу к следующему значению for
            if (len(s[i]) == 7) and (s[i].count('.') + s[i].count('*') == 7):
                break
            # если дощли до сюда, значит предыдущее условие не сработало, значит в введенная строка не такая как надо
            # ругаюсь и откправляю вводить еще раз, цикл while не прерывается, i не меняется.
            print('Некорректный ввод, попробуйте еще раз.')
    # возвращаю полученный лабиринт
    return s


# так как для поска пути используются веса клеток, то преобразую исходный лабиринт состоящий из . и * в
# набор весов, где -1 это стенка, 0 это свободный узел, 1 начало пути.
def get_weights(str_lab: []) -> [[]]:
    # инициализирую двумерный массис, а точнее, для питона, список списков
    # row строк
    # elem элементов в каждой строке
    # row и elem вычисляются из входного массива
    row = len(str_lab)
    elem = len(str_lab[0])
    # можно так:
    # w = [0] * row
    # for i in range(row):
    #     w[i] = [0] * elem
    # а можно так:
    # w = []
    # for i in range(row):
    #     w.append([0] * elem)
    # а можно так:
    w = [[0] * elem for i in range(row)]
    # присваиваю веса
    # цикл по строкам
    for i in range(row):
        # цикл по элементам
        for j in range(elem):
            # можно так:
            # if str_lab[i][j] == '*':
            #     w[i][j] = -1
            # else:
            #     w[i][j] = 0
            # а можно так
            w[i][j] = -1 if str_lab[i][j] == '*' else 0
    # возвращаю веса
    return w


#
def colorize(w: [[]], start_point: (int, int)) -> [[]]:
    # вычисляю количество строк в исходном массиве с весами
    row = len(w)
    # вычисляю количество элементов в строке в исходном массиве с весами
    elem = len(w[0])
    # создаю новый двумерный массив с которым и буду работать и его возвращать,
    # это сделано для того, чтобы не портить исходный массив, т.к. он передается в функцию по ссылке
    c = [[0] * elem for i in range(row)]
    # так как функции копирования двумерных массивов в питон не встроено, а разбираться с функцией deepcopy
    # из пакета copy неохота, то тупо копирую поэлементно один массив в другой
    for i in range(row):
        for j in range(elem):
            c[i][j] = w[i][j]
    # делаю буфер fifo (первый пришел, первый ушел) на основе массива
    # в который будут складываться координаты соседних узлов, которые доступны из текущего узла и не являются стенкой
    # и которым будет присваиваться вес на единицу больше чем у текущего узла
    fifo = []
    # кладу координаты начального узла в буфер
    fifo.append(start_point)
    # координаты точки старта
    row, elem = start_point
    # вес первого узла = 1
    c[row][elem] = 1
    # цикл работает пока есть не обследованные узлы
    while len(fifo) != 0:
        # достаю узел из буфера, удаляя его оттуда
        row, elem = fifo.pop(0)
        # задаю вес соседей узла как вес самого узла + 1
        new_weight = c[row][elem] + 1
        # проверяю не вышел ли за границы массива, если бы добавил внешние стенки массиву,
        # то это условие можно было не добавлять
        if row + 1 < len(c):
            # проверяю, что нижний узел свободен для посещения и не является стенкой
            if c[row + 1][elem] == 0:
                # присваиваю ему вес
                c[row + 1][elem] = new_weight
                # и кладу его координаты в буфер, чтобы в дальнейшем обойти его соседей
                fifo.append((row + 1, elem))
        # проверяю не вышел ли за границы массива
        if row - 1 >= 0:
            # проверяю, что верхний узел свободен для посещения и не является стенкой
            if c[row - 1][elem] == 0:
                # присваиваю ему вес
                c[row - 1][elem] = new_weight
                # и кладу его координаты в буфер, чтобы в дальнейшем обойти его соседей
                fifo.append((row - 1, elem))
        # проверяю не вышел ли за границы массива
        if elem + 1 < len(c[row]):
            # проверяю, что правый узел свободен для посещения и не является стенкой
            if c[row][elem + 1] == 0:
                # присваиваю ему вес
                c[row][elem + 1] = new_weight
                # и кладу его координаты в буфер, чтобы в дальнейшем обойти его соседей
                fifo.append((row, elem + 1))
        # проверяю не вышел ли за границы массива
        if elem - 1 >= 0:
            # проверяю, что левый узел свободен для посещения и не является стенкой
            if c[row][elem - 1] == 0:
                # присваиваю ему вес
                c[row][elem - 1] = new_weight
                # и кладу его координаты в буфер, чтобы в дальнейшем обойти его соседей
                fifo.append((row, elem - 1))
    return c


# поиск пути в лабиринте, лабиринт в виде двумерного массива с весами
def find_path(w: [[]], end_point: (int, int)) -> []:
    # получаю координаты конечного узла
    row, elem = end_point
    # если конечный узел это стена или вес его равен 0, значит до него невозможно добраться из стартового узла
    if w[row][elem] == 0 or w[row][elem] == -1:
        # возвращаю пустой список как признак отсутствия пути
        return []
    # если путь есть, то количество шагов равно весу конечного узла, такого размера и формирую массив
    p = [(0, 0)] * w[row][elem]
    # работаю пока не достигну узла с весом 1 - это стартовый узел
    while w[row][elem] != 1:
        # ищу соседа с весом меньше на 1
        neighbour_weight = w[row][elem] - 1
        # добавляю в путь координаты очередного найденного узла, в самом начале это координаты конечного узла
        p[neighbour_weight] = (row, elem)
        # проверяю не вышел ли за границы массива
        if row + 1 < len(w):
            # проверяю вес соседа
            if w[row + 1][elem] == neighbour_weight:
                # если нашел такого соседа, то делаю его координаты текущими
                row = row + 1
                # прекращаю выполнение текущей итерации и перехожу к новой, чтобы не выполнялись условия ниже
                continue
        # проверяю не вышел ли за границы массива
        if row - 1 >= 0:
            # проверяю вес соседа
            if w[row - 1][elem] == neighbour_weight:
                # если нашел такого соседа, то делаю его координаты текущими
                row = row - 1
                # прекращаю выполнение текущей итерации и перехожу к новой, чтобы не выполнялись условия ниже
                continue
        # проверяю не вышел ли за границы массива
        if elem + 1 < len(w[row]):
            # проверяю вес соседа
            if w[row][elem + 1] == neighbour_weight:
                # если нашел такого соседа, то делаю его координаты текущими
                elem = elem + 1
                # прекращаю выполнение текущей итерации и перехожу к новой, чтобы не выполнялись условия ниже
                continue
        # проверяю не вышел ли за границы массива
        if elem - 1 >= 0:
            # проверяю вес соседа
            if w[row][elem - 1] == neighbour_weight:
                # если нашел такого соседа, то делаю его координаты текущими
                elem = elem - 1
                # прекращаю выполнение текущей итерации и перехожу к новой, чтобы не выполнялись условия ниже
                continue
    # заодно добавляю координаты узла старта в начало массива
    p[0] = (row, elem)
    # возвращаю путь
    return p


# генерация лабиринта методом прямого обхода графа в глубину
def generate_labyrinth(row: int, elem: int) -> [[]]:
    # создаю начальный лабиринт вида
    # -1 -1 -1 -1 -1
    # -1  1 -1  1 -1
    # -1 -1 -1 -1 -1
    # -1  1 -1  1 -1
    # -1 -1 -1 -1 -1
    # т.е. на местах с четными индексами стоит 1, на всех остальных -1
    w = [[0] * elem for i in range(row)]
    for i in range(row):
        for j in range(elem):
            if (i % 2 != 0 and j % 2 != 0) and (i < row and j < elem):
                w[i][j] = 1
            else:
                w[i][j] = -1
    # стэк для работы
    stack = []
    # прохожу по всему лабиринту и считаю сколько ячеек содержит единицу, это означает, что ячейка не посещенная
    unvisited_count = get_unvisited_count(w)
    # задаю с какой ячейки начать
    start_point = (1, 1)
    # работаю пока есть непосещенные ячейки
    while unvisited_count != 0:
        # собираю непосещенных соседей текущей ячейки
        nbc = get_neighbours(w, start_point)
        # если непочещенные соседи есть
        if len(nbc) != 0:
            # выбираю случайную ячейку из списка непосещенных соседей ячейки
            rand_num = random.randint(0, len(nbc) - 1)
            # достаю
            next_cell = nbc.pop(rand_num)
            # закидываю в стек
            stack.append(start_point)
            # удаляю стенку между ячейками
            remove_wall(w, start_point, next_cell)
            # уменьшаю количество непосещенных ячеек
            unvisited_count -= 1
            # делаю соседнюю текущей
            start_point = next_cell
            # получаю ее координаты
            row, elem = start_point
            # помечаю ее как посещенную
            w[row][elem] = 0
        elif len(stack) != 0:
            # если обошел всех соседей и они кончились, достаю из стека следующую ячейку
            start_point = stack.pop(0)
        else:
            # если и в стеке ячейки кончились, но в лабиринте остались непосещенные
            uvc = get_unvisited_cells(w)
            # выбираю случайную непосещенную
            rand_num = random.randint(0, len(uvc) - 1)
            # делаю текущей и продолжаю из нее строить лабиринт
            start_point = uvc[rand_num]
    return w


# возвращает список непосещенных ячеек, непосещенная ячейка имеет вес 1
def get_unvisited_cells(lab: [[]]) -> []:
    uvc = []
    for i in range(len(lab)):
        for j in range(len(lab[i])):
            if lab[i][j] == 1:
                uvc.append((i, j))
    return uvc


# возвращает список непосещенных соседей,
def get_neighbours(lab: [[]], cell: (int, int)) -> []:
    nb = []
    row, elem = cell
    if row + 2 < len(lab):
        if lab[row + 2][elem] == 1:
            nb.append((row + 2, elem))
    if row - 2 >= 0:
        if lab[row - 2][elem] == 1:
            nb.append((row - 2, elem))
    if elem + 2 < len(lab[row]):
        if lab[row][elem + 2] == 1:
            nb.append((row, elem + 2))
    if elem - 2 >= 0:
        if lab[row][elem - 2] == 1:
            nb.append((row, elem - 2))
    return nb


# возвращает количество непосещенных ячеек, непосещенная ячейка имеет вес 1
def get_unvisited_count(lab: [[]]) -> int:
    count = 0
    for row in lab:
        for elem in row:
            if elem == 1:
                count += 1
    return count


# удаляет стенку между двумя ячейками, т.е. ставит признак, что она посещенная
def remove_wall(lab: [[]], start_point: (int, int), end_point: (int, int)):
    statr_row, start_elem = start_point
    end_row, end_elem = end_point
    row_diff = end_row - statr_row
    elem_diff = end_elem - start_elem
    add_row = int(row_diff / abs(row_diff)) if row_diff != 0 else 0
    add_elem = int(elem_diff / abs(elem_diff)) if elem_diff != 0 else 0
    row_target = statr_row + add_row
    elem_target = start_elem + add_elem
    lab[row_target][elem_target] = 0


# генератор лабиринта методом Эллера
def generate_ellers_labyrinth(row: int, elem: int) -> [[]]:
    b = [-1] * elem
    w = [b.copy()]
    # строка для работы
    s = [0 for i in range(elem)]
    # стенки с краев
    s[0] = -1
    s[elem-1] = -1
    weight = 1
    bottom_borders = s.copy()
    # первая строка лабиринта, не стенка вокруг
    # каждой ячейке присваиваю свое уникальное множество
    for i in range(1, elem, 2):
        s[i] = weight
        weight += 1
    # по всем строкам лабиринта кроме 0й и последней
    # через две, т.к. одна строка это строка лабиринта, а вторая это ее нижняя граница
    for i in range(1, row-2, 2):
        # прохожу по каждой ячейке
        for j in range(1, elem-2, 2):
            # если ячейки принадлежат одному и тому же множеству, то ставлю между ними стенку
            # случайным образом определяю ставить стенку или нет
            # если ставить, то ставлю
            set_border = random.choice([True, False])
            if s[j] == s[j+2] or set_border:
                s[j+1] = -1
            # если нет, то объединяю ячейки в одно множество
            else:
                s[j+2] = s[j]
                s[j+1] = 0
        w.append(s.copy())
        # количество ячеек в одном множестве
        count = 1
        bottom_borders_count = 0
        for k in range(1, elem-2, 2):
            # случайным образом определяю ставить нижнюю границу или нет
            set_bottom_border = random.choice([True, False])
            # если дальше идет другое множество, то
            if s[k] != s[k + 2]:
                # если ячейка в множестве одна, или все кроме последней имеют нижнюю границу, то
                if count == 1 or bottom_borders_count == count-1:
                    # нижнюю границу не ставлю
                    set_bottom_border = False
                bottom_borders_count = 0
                count = 1
            else:
                count += 1
            # если ставлю нижнюю границу, то
            if set_bottom_border:
                bottom_borders[k] = -1
                bottom_borders_count += 1
            # если не ставлю нижнюю границу
            else:
                bottom_borders[k] = 0
            bottom_borders[k+1] = -1 if s[k+1] == -1 else 0
        w.append(bottom_borders.copy())
        for n in range(1, elem-2, 2):
            if bottom_borders[n] == -1:
                s[n] = weight
                weight += 1
    w.pop()
    w.append(b.copy())
    # очищаю лабиринт от весов
    for i in range(len(w)):
        for j in range(len(w[i])):
            if w[i][j] > 0:
                w[i][j] = 0
    return w


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # получаю в переменную лабиринт, заранее заданный (False) или с клавиатуры (True)
    src_lab = get_labyrinth(False)
    # вывожу его на экран построчно
    for row in src_lab:
        print(row)
    print('\n')

    # задаю стартовый узел
    start_point = (0, 0)
    # задаю конечный узел, т.к. отсчет начинается с 0, то 7й элемент будет иметь порядковый номер 6
    end_point = (6, 6)

    # создаю массив с весами элементов, где вместо . и * стоят -1 для стенки и 0 для пустого места
    weights = get_weights(src_lab)
    # вывожу полученные веса на экран
    # for row in weights:
    #     for elem in row:
    #         print('%2d' % elem, end=' ')
    #     print('\n')
    # print('\n')

    # проставляю веса узлов начиная от стартового
    weights = colorize(weights, start_point)
    # вывожу на экран
    # for row in weights:
    #     for elem in row:
    #         print('%2d' % elem, end=' ')
    #     print('\n')
    # print('\n')

    # получаю путь до него или пустой массив, если путь не найден
    path = find_path(weights, end_point)
    # print(path)

    if len(path) == 0:
        print('Путь не найден!')
    else:
        # прохожу по всем точкам пути
        for i in range(len(path)):
            # беру координаты
            row, elem = path[i]
            # можно так, но будет без буквы ё
            # по ним вставляю букву, беру код буквы а и прибавляю порядковый номер точки пути и
            # преобразую обратно в букву, а+1 будет б, +2 будет в и т.д.
            # i % 32 это я беру остаток от деления на 32, чтобы когда количество точек пути превысит количество
            # букв алфавита, то снова началось с начала алфавита, т.е. когда будет 34,35,36, то остаток
            # от деления будет 1,2,3 и к а будет прибавляться 1,2,3 и будет опять получаться б,в,г
            # а 32, а не 33 потому что буква ё в другом месте находится, не по порядку
            # src_lab[row] = src_lab[row][:elem] + chr(ord('а') + i % 32) + src_lab[row][elem + 1:]
            # а можно так, можно задать любой алфавит
            alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р',
                        'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'ъ', 'э', 'ю', 'я']
            src_lab[row] = src_lab[row][:elem] + alphabet[i % 33] + src_lab[row][elem + 1:]
        # вывожу на экран полученный лабиринт
        for row in src_lab:
            print(row)
        print('\n')

    # конец основного задания, дальше идет алгоритм генерации лабиринта прямым обходом графа в глубину
    # особенность в том, что нечетный размер должен быть
    # лабиринт генерирую сразу в виде весовых коэффициентов
    # лабиринт генерируется сразу с внешними стенками
    www = generate_labyrinth(21, 81)
#    www = generate_ellers_labyrinth(21, 81)
    # for row in www:
    #     for elem in row:
    #         print('\u2593\u2593' if elem == -1 else '  ', end='')
    #     print('')
    # print('')
    # for row in www:
    #     for elem in row:
    #         print('%2d' % elem, end=' ')
    #     print('\n')
    # print('\n')

    # задаю стартовый узел, верхняя левая свободная ячейка
    start_point = (1, 1)
    # задаю конечный узел, нижняя правая свободная ячейка
    end_point = (len(www) - 2, len(www[0]) - 2)
    #
    # проставляю веса узлов начиная от стартового
    weights = colorize(www, start_point)
    # вывожу на экран
    # for row in weights:
    #     for elem in row:
    #         print('%2d' % elem, end=' ')
    #     print('\n')
    # print('\n')

    # получаю путь до него или пустой массив, если путь не найден
    path = find_path(weights, end_point)
    # print(path)

    if len(path) == 0:
        print('''\033[33m
            ███╗░░██╗░█████╗░  ░██╗░░░░░░░██╗░█████╗░██╗░░░██╗██╗
            ████╗░██║██╔══██╗  ░██║░░██╗░░██║██╔══██╗╚██╗░██╔╝██║
            ██╔██╗██║██║░░██║  ░╚██╗████╗██╔╝███████║░╚████╔╝░██║
            ██║╚████║██║░░██║  ░░████╔═████║░██╔══██║░░╚██╔╝░░╚═╝
            ██║░╚███║╚█████╔╝  ░░╚██╔╝░╚██╔╝░██║░░██║░░░██║░░░██╗
            ╚═╝░░╚══╝░╚════╝░  ░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝░░░╚═╝░░░╚═╝
            \033[38m''')
    else:
        # прохожу по всем точкам пути
        for i in range(len(path)):
            # беру координаты
            row, elem = path[i]
            www[row][elem] = ord('а') + i % 32
    # вывожу на экран полученный лабиринт
    for row in www:
        for elem in row:
            if elem == -1:
                print('\u2593\u2593', end='')
            elif elem == 0:
                print('  ', end='')
            else:
                # print('\033[032m\u2593\u2593\033[038m', end='')
                print('\033[045m%2s\033[0m' % chr(elem), end='')
        print('')


