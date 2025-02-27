import random


def generate_matrix(rows, cols):
    """
    生成一个随机填充 1-7 的二维数组，其中 99 出现的概率很小。
    :param rows: 行数
    :param cols: 列数
    :return: 生成的二维数组
    """
    matrix = [[random.randint(1, 7) for _ in range(cols)] for _ in range(rows)]

    # 随机选择一个位置填充 99（概率为 1/(rows*cols)）
    if random.random() < 1 / (rows * cols):
        x = random.randint(0, rows - 1)
        y = random.randint(0, cols - 1)
        matrix[x][y] = 99

    return matrix


def eliminate_special_symbol(matrix):
    """
    如果出现了 99，则将其本身及其相邻的八个方向的元素都归零。
    :param matrix: 二维数组
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
                matrix[i][j] = 0
    return is_bomb


def print_matrix(matrix):
    """
    打印二维数组。
    :param matrix: 二维数组
    """
    for row in matrix:
        print(row)
    print()


# 生成一个 7x7 的随机二维数组
# matrix = generate_matrix(7, 7)
matrix = [  [1, 5, 1, 2, 7, 4, 1],
            [2, 5, 5, 3, 2, 3, 5],
            [7, 4, 7, 7, 1, 7, 2],
            [5, 4, 3, 7, 3, 7, 1],
            [1, 5, 1, 4, 3, 7, 6],
            [2, 4, 2, 4, 5, 99, 1],
            [1, 99, 7, 3, 5, 7, 4]]

# 打印初始数组
print("Initial Matrix:")
print_matrix(matrix)

# 处理特殊数字 99
eliminate_special_numbers(matrix)

# 打印处理后的数组
print("Matrix After Eliminating 99 and Adjacent Elements:")
print_matrix(matrix)