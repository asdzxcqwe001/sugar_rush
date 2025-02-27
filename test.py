import copy
import random


def eliminate_special_symbol(matrix, floor_multiple, this_rm_element):
    """
    如果出现了炸弹，则将其本身及其相邻的八个方向的元素都归零消除。
    :param matrix: 二维数组
    :param floor_multiple: 底板倍数数组
    :param this_rm_element: 本次消除的元素记录数组
    :return: 是否出现了炸弹
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    # 定义八个方向：上、下、左、右、左上、左下、右上、右下
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # 记录需要归零的位置
    to_zero = [[False for _ in range(cols)] for _ in range(rows)]
    is_bomb = False

    # 遍历数组，查找是否有炸弹
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 99:
                # 将炸弹本身消除处理
                to_zero[r][c] = True
                is_bomb = True

                # 将八个方向的相邻元素标记为需要归零
                for dx, dy in directions:
                    x = r + dx
                    y = c + dy
                    if 0 <= x < rows and 0 <= y < cols:
                        to_zero[x][y] = True

    # 将所有标记的位置归零
    for r in range(rows):
        for c in range(cols):
            if to_zero[r][c]: # 如果这个地方是True，则代表炸弹覆盖范围
                this_rm_element[r][c] = matrix[r][c]
                matrix[r][c] = 0
            # 炸弹爆炸后需要底板倍数乘倍
            if floor_multiple[r][c] == 0:
                floor_multiple[r][c] = 1
            elif floor_multiple[r][c] < 1024:
                floor_multiple[r][c] *= 2
    return is_bomb


def find_adjacent(matrix, r, c):
    """
    使用栈实现 DFS，找到所有与 (r, c) 相邻且值相同的元素。
    :param matrix: 二维数组
    :param r: 起始行
    :param c: 起始列
    :return: 所有相邻且值相同的点的列表
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    target = matrix[r][c]
    stack = [(r, c)]
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    path = []
    # 定义四个方向：上、下、左、右
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        x, y = stack.pop()
        if x < 0 or x >= rows or y < 0 or y >= cols:
            continue  # 超出边界
        if matrix[x][y] != target or visited[x][y]:
            continue  # 值不匹配或已经访问过
        if matrix[x][y] in [99, 92]:
            continue  # 炸弹图标或scatter图标不记录

        # 标记当前点为已访问，并加入路径
        visited[x][y] = True
        path.append((x, y))

        # 将四个方向的点加入栈
        for dx, dy in directions:
            stack.append((x + dx, y + dy))

    return path


def move_zero(matrix, add_new_element):
    """
    移动盘面中的零元素，为新元素加入做准备。
    :param matrix: 真实的7x7盘面
    :param add_new_element: 7x7全是0的增加里面的新元素
    :return: 无
    """

    for r in range(len(matrix)):
        for c in range(len(matrix[r]) - 1, -1, -1):
            if matrix[r][c] == 0:
                del matrix[r][c]
                del add_new_element[r][c]


def add_element(matrix, reel_lines, add_new_element):
    """
    为盘面添加新元素。
    :param matrix: 原始盘面
    :param reel_lines: 总线条数
    :param add_new_element: 记录新加入元素的数组
    :return: 无
    """
    for r in range(len(matrix)):
        now_lines = reel_lines - len(matrix[r])
        matrix[r] = [random.randint(1, 4) for _ in range(now_lines)] + matrix[r]
        add_new_element[r] = [random.randint(1, 4) for _ in range(now_lines)] + add_new_element[r]


def eliminate(matrix, floor_multiple, this_rm_element, total_win):
    """
    消除所有相邻相同且数量大于5的元素。
    :param matrix: 原始盘面
    :param floor_multiple: 底板倍数
    :param this_rm_element: 本次消除的元素盘面初始化
    :param total_win: 分数
    :return: 是否有元素被消除, 更新后的总分数
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    to_zero = [[False for _ in range(cols)] for _ in range(rows)]
    eliminated = False
    this_win = 0

    # 遍历每个元素
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 0 or to_zero[r][c]:
                continue  # 如果已经是 0 或已经标记过，跳过

            # 找到所有相邻且值相同的点
            path = find_adjacent(matrix, r, c)

            # 如果路径长度大于等于 5，标记需要归零
            if len(path) >= 5:
                eliminated = True
                this_floor_multiple = 0
                for x, y in path:
                    this_rm_element[x][y] = matrix[r][c]
                    to_zero[x][y] = True
                    if floor_multiple[x][y] == 0:
                        floor_multiple[x][y] = 1
                    elif floor_multiple[x][y] < 1024:
                        floor_multiple[x][y] *= 2
                    if floor_multiple[x][y] > 1:
                        this_floor_multiple += floor_multiple[x][y]
                if this_floor_multiple:
                    this_win += this_floor_multiple * 1
                else:
                    this_win += 1 * 1

    # 将标记的位置归零
    for i in range(rows):
        for j in range(cols):
            if to_zero[i][j]:
                matrix[i][j] = 0
    total_win += this_win
    print('本次消除分数是', total_win)
    return eliminated, total_win


# 调用函数
if __name__ == '__main__':
    # _matrix = [[random.randint(1, 4) for c in range(7)] for r in range(7)]
    _matrix = [
        [1, 1, 3, 3, 1, 1, 1],
        [2, 1, 3, 2, 2, 2, 2],
        [2, 1, 2, 4, 3, 1, 2],
        [1, 1, 3, 1, 3, 3, 1],
        [3, 4, 3, 3, 4, 4, 1],
        [4, 4, 3, 99, 3, 4, 3],
        [2, 4, 4, 2, 3, 2, 4]]
    print("初始化盘面")
    for item in _matrix:
        print(item)
    _total_win = 0
    total_info = []
    _floor_multiple = [[0 for _ in range(7)] for _ in range(7)]
    while True:
        this_dict = {}
        _this_rm_element = [[0 for _ in range(7)] for _ in range(7)]
        _add_new_element = [[0 for _ in range(7)] for _ in range(7)]
        is_eliminate, _total_win = eliminate(_matrix, _floor_multiple, _this_rm_element, _total_win)
        if not is_eliminate and not eliminate_special_symbol(_matrix, _floor_multiple, _this_rm_element):
            break

        new_matrix = copy.deepcopy(_matrix)
        this_dict['eliminate'] = new_matrix

        this_dict['this_rm_element'] = _this_rm_element

        move_zero(_matrix, _add_new_element)

        add_element(_matrix, 7, _add_new_element)
        this_dict['add_new_position'] = _add_new_element

        new_floor_multiple = copy.deepcopy(_floor_multiple)
        this_dict['floor_multiple'] = new_floor_multiple

        add_new_matrix = copy.deepcopy(_matrix)
        this_dict['add_new_array'] = add_new_matrix

        total_info.append(this_dict)
    if not total_info:
        print('没有消除')
    else:
        for item in total_info:
            print('========================================================')
            for k, v in item.items():
                if k == "eliminate":
                    print("消除盘面：")
                    for i in v:
                        print(i)
                elif k == "this_rm_element":
                    print("消除的元素：")
                    for i in v:
                        print(i)
                elif k == "add_new_position":
                    print("新加入的元素：")
                    for i in v:
                        print(i)
                elif k == "floor_multiple":
                    print("底板倍数：")
                    for i in v:
                        print(i)
                elif k == "add_new_array":
                    print("加入元素后的完整盘面：")
                    for i in v:
                        print(i)
    print('总分是', _total_win)
