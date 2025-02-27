import copy
import random

# 定义四个方向：上、下、左、右
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def eliminate_special_symbol(matrix,floor_multiple,this_rm_element):
    """
    如果出现了 99，则将其本身及其相邻的八个方向的元素都归零。
    :param matrix: 二维数组
    :param floor_multiple
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    # 定义八个方向：上、下、左、右、左上、左下、右上、右下
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # 记录需要归零的位置
    to_zero = [[False for _ in range(cols)] for _ in range(rows)]
    is_bomb = False

    # 遍历数组，查找所有 99
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 99:
                # 将 99 本身标记为需要归零
                to_zero[i][j] = True
                is_bomb = True

                # 将八个方向的相邻元素标记为需要归零
                for dx, dy in directions:
                    x = i + dx
                    y = j + dy
                    if 0 <= x < rows and 0 <= y < cols:
                        to_zero[x][y] = True

    # 将所有标记的位置归零
    for i in range(rows):
        for j in range(cols):
            if to_zero[i][j]:
                this_rm_element[i][j] = matrix[i][j]
                matrix[i][j] = 0
            if floor_multiple[i][j] == 0:
                floor_multiple[i][j] = 1
            elif floor_multiple[i][j] < 1024:
                floor_multiple[i][j] *= 2
    return is_bomb

def find_adjacent(matrix, i, j):
    """
    使用栈实现 DFS，找到所有与 (i, j) 相邻且值相同的元素。
    :param matrix: 二维数组
    :param i: 起始行
    :param j: 起始列
    :return: 所有相邻且值相同的点的列表
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    target = matrix[i][j]
    stack = [(i, j)]
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    path = []

    while stack:
        x, y = stack.pop()
        if x < 0 or x >= rows or y < 0 or y >= cols:
            continue  # 超出边界
        if matrix[x][y] != target or visited[x][y]:
            continue  # 值不匹配或已经访问过
        if matrix[x][y] in [99,92]:
            continue  # 炸弹图标或scatter图标不记录

        # 标记当前点为已访问，并加入路径
        visited[x][y] = True
        path.append((x, y))

        # 将四个方向的点加入栈
        for dx, dy in DIRECTIONS:
            stack.append((x + dx, y + dy))

    return path


def move_zero(matrix,add_new_element):
    """

    :param matrix: 真实的7x7盘面
    :param add_new_element: 7x7全是0的增加里面的新元素
    :return:
    """

    for r in range(len(matrix)):
        for c in range(len(matrix[r])-1,-1,-1):
            if matrix[r][c] == 0:
                del matrix[r][c]
                del add_new_element[r][c]

def add_element(matrix,reel_lines,add_new_element):
    for r in range(len(matrix)):
        now_lines = reel_lines-len(matrix[r])
        matrix[r] = [random.randint(1,4) for _ in range(now_lines)] + matrix[r]
        add_new_element[r] = [random.randint(1,4) for _ in range(now_lines)] + add_new_element[r]

def eliminate(matrix,floor_multiple,this_rm_element):
    """
    消除所有相邻且相同且数量大于等于 5 的元素。
    :param matrix: 二维数组
    :return: 是否进行了消除操作
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    to_zero = [[False for _ in range(cols)] for _ in range(rows)]
    eliminated = False

    # 遍历每个元素
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 0 or to_zero[i][j]:
                continue  # 如果已经是 0 或已经标记过，跳过

            # 找到所有相邻且值相同的点
            path = find_adjacent(matrix, i, j)


            # 如果路径长度大于等于 5，标记需要归零
            if len(path) >= 5:
                eliminated = True
                for x, y in path:
                    this_rm_element[x][y] = matrix[i][j]
                    to_zero[x][y] = True
                    if floor_multiple[x][y] == 0:
                        floor_multiple[x][y] = 1
                    elif floor_multiple[x][y] < 1024:
                        floor_multiple[x][y] *= 2

    # 将标记的位置归零
    for i in range(rows):
        for j in range(cols):
            if to_zero[i][j]:
                matrix[i][j] = 0

    return eliminated


# 调用函数

if __name__ == '__main__':
    # matrix = [[random.randint(1, 4) for c in range(7)] for r in range(7)]
    matrix = [  [1, 1, 3, 3, 1, 1, 1],
                [2, 1, 3, 2, 2, 2, 2],
                [2, 1, 2, 4, 3, 1, 2],
                [1, 1, 3, 1, 3, 3, 1],
                [3, 4, 3, 3, 4, 4, 1],
                [4, 4, 3, 1, 3, 4, 3],
                [2, 4, 4, 2, 3, 2, 99]]
    print("初始化盘面")
    for item in matrix:
        print(item)
    count = 0
    total_win = 0
    total_info = []
    floor_multiple = [[0 for _ in range(7)]for _ in range(7)]
    while True:
        count += 1
        this_dict = {}
        this_rm_element = [[0 for _ in range(7)] for _ in range(7)]
        add_new_element = [[0 for _ in range(7)] for _ in range(7)]
        if not eliminate(matrix,floor_multiple,this_rm_element) and not eliminate_special_symbol(matrix,floor_multiple,this_rm_element):
            break

        new_matrix = copy.deepcopy(matrix)
        this_dict['eliminate'] = new_matrix

        this_dict['this_rm_element'] = this_rm_element

        move_zero(matrix,add_new_element)

        add_element(matrix,7,add_new_element)
        this_dict['add_new_position'] = add_new_element

        new_floor_multiple = copy.deepcopy(floor_multiple)
        this_dict['floor_multiple'] = new_floor_multiple

        add_new_matrix = copy.deepcopy(matrix)
        this_dict['add_new_array'] = add_new_matrix

        total_info.append(this_dict)
    if not total_info:
        print('没有消除')
    else:
        for item in total_info:
            print('========================================================')
            for k,v in item.items():
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
                    print("新加入的盘面：")
                    for i in v:
                        print(i)