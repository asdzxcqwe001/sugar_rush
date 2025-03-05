#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import random

from SlotCommon.game_check_line import MainGameCheckLine
from .CashKingInfo import GameInfo


# ======================================================================
class CashKingCheck(MainGameCheckLine):
    def _init_const(self):
        self.SpecReelIdx = 3
        # 特殊图标会替换成其他图标
        self.SpecialSymbolID = 99
        # 触发进入条件的图标
        self.ScatterSymbolID = 92
        # 炸弹图标
        self.BombSymbolID = 94
        # 普通图标列表
        self.CommonSymbolIdList = [1,2,3,4,5,6,7]
        # 免费游戏id
        self.FreeGameId = 1
        # 超级免费游戏id
        self.SuperFreeGameId = 2
        # 触发进入免费游戏的特殊图标最小次数
        self.TriggerFreeMinCount = 3
        # 在免费游戏中增加免费游戏次数的特殊图标出现数量最小次数
        self.TriggerAddMinCount = 2
        # 最大倍率
        self.MaxMulti = 1024
        # 满足相邻消除的个数
        self.RemoveCount = 5
        # 最大获取分数，大于则推出
        self.MaxWin = 10000

    def game_check(self, main_result, block_id, play_info, odds, special_odds, extra_odds, reel_length, reel_amount,
                   check_reel_length, check_reel_amount):
        """
        :param main_result: 這次spin的所有資訊
        :param feature_reel: main game命中的feature在哪一輪，若-1表示沒中
        :param play_info: 遊戲的押注、選線、特殊遊戲狀態
        :param odds: 賠率表
        :param special_odds: scatter中獎獲得的次數
        :param extra_odds: 其他機率相關的設定數值
        :param reel_length: 包含不可視的symbol，一輪有多少顆symbol
        :param reel_amount: 包含不可視的symbol，有多少輪
        :param check_reel_length: 不包含不可視的symbol，一輪有多少顆symbol
        :param check_reel_amount: 不包含不可視的symbol，有多少輪
        :return:
        """
        # note: local variable fast than class variable

        # ====================================================
        # show_reel: game log顯示的牌面, check_reel: 檢查各種獎項使用的牌面
        # 若有修改到show_reel，最後需要存回main_result
        fg_type = main_result.get_temp_special_game_data('fg_type')
        showReel = self.get_check_reel(main_result, block_id, reel_length, reel_amount, check_reel_length, check_reel_amount, transform=False)
        scatter_count = 0
        for row in range(check_reel_amount):
            for col in range(check_reel_length):
                amount_scatter_count = 0
                if showReel[row][col] == self.SpecialSymbolID:
                    scatter_weight = random.random()
                    if not play_info.is_special_game:
                        if scatter_weight < extra_odds['base_trigger_scatter'][scatter_count] and amount_scatter_count < 1:
                            showReel[row][col] = self.ScatterSymbolID
                            amount_scatter_count += 1
                            scatter_count += 1
                        else:
                            showReel[row][col] = random.choice(self.CommonSymbolIdList)
                    else:
                        current_win_times = main_result.get_temp_special_game_data("current_win_times")
                        if current_win_times <= 20:
                            add_scatter_by_weight = 20
                        elif current_win_times <= 30:
                            add_scatter_by_weight = 30
                        elif current_win_times <= 35:
                            add_scatter_by_weight = 35
                        elif current_win_times <= 38:
                            add_scatter_by_weight = 38
                        elif current_win_times <= 40:
                            add_scatter_by_weight = 40
                        elif current_win_times <= 45:
                            add_scatter_by_weight = 45
                        else:
                            add_scatter_by_weight = 50

                        if scatter_weight < extra_odds['free_trigger_scatter'][fg_type][str(add_scatter_by_weight)][scatter_count] and amount_scatter_count < 1:
                            showReel[row][col] = self.ScatterSymbolID
                            amount_scatter_count += 1
                            scatter_count += 1
                        else:
                            showReel[row][col] = random.choice(self.CommonSymbolIdList)
        checkReel = [[i for i in row] for row in showReel]
        main_result.set_extra_data('init__reel', copy.deepcopy(checkReel))
        if play_info.is_special_game and '客户端传过来的是：super':
            while True:
                r = random.randint(0,6)
                c = random.randint(0,6)
                if checkReel[r][c] not in [self.ScatterSymbolID,self.BombSymbolID]:
                    checkReel[r][c] = self.BombSymbolID
                    # mystery玩法更改炸弹之后的盘面
                    main_result.set_extra_data('mystery_reel', copy.deepcopy(checkReel))
                    break
        elif play_info.is_special_game and '客户端传过来的是：free':

            while True:
                r = random.randint(0,6)
                c = random.randint(0,6)
                num = random.random()
                if num < extra_odds['free_mystery'][fg_type]:
                    if checkReel[r][c] not in [self.ScatterSymbolID,self.BombSymbolID]:
                        checkReel[r][c] = self.BombSymbolID
                        # mystery玩法更改炸弹之后的盘面
                        main_result.set_extra_data('mystery_reel', copy.deepcopy(checkReel))
                        break
        elif play_info.is_special_game and '客户端传过来的是：by_bonus':
            while True:
                r = random.randint(0,6)
                c = random.randint(0,6)
                num = random.random()
                if num < extra_odds['free_mystery'][fg_type]:
                    if checkReel[r][c] not in [self.ScatterSymbolID,self.BombSymbolID]:
                        checkReel[r][c] = self.BombSymbolID
                        # mystery玩法更改炸弹之后的盘面
                        main_result.set_extra_data('mystery_reel', copy.deepcopy(checkReel))
                        break

        # main_result.set_temp_special_game_data("CheckReel", checkReel)
        self.free_game_symbol_check(main_result,block_id,play_info,extra_odds,checkReel,self.FreeGameId)

        combo_arr,total_win = self.main_win_check(main_result, block_id, play_info, odds, checkReel, showReel, check_reel_length,check_reel_amount,extra_odds)

        main_result.set_extra_data('combo_arr',combo_arr)



    def free_game_symbol_check(self, main_result, block_id, play_info, extra_odds, check_reel,
                               free_game_id):

        reel_info = main_result.get_reel_block_data(block_id)
        symbol_pos = [[-1 for row in range(len(check_reel[col]))] for col in range(len(check_reel))]
        scatter_count = 0
        for i in range(len(check_reel)):
            for j in range(len(check_reel[i])):
                if check_reel[i][j] == self.ScatterSymbolID:
                    scatter_count += 1
                    symbol_pos[i][j] = 1

        # 大于等于指定数量 概率触发免费 或增加免费次数
        if (play_info.is_special_game and scatter_count >= self.TriggerAddMinCount) or (not play_info.is_special_game and scatter_count >= self.TriggerFreeMinCount):
            key = "base_trigger_scatter" if not play_info.is_special_game else "free_re_trigger"
            # 赢到的次数
            win_times = extra_odds[key][scatter_count]
            reel_info.set_special_symbol_win_pos(free_game_id, symbol_pos)
            main_result.set_win_special_game(free_game_id, win_times)
            if not play_info.is_special_game:
                current_script = {
                    'main_reel': reel_info.reel_data,
                    'game_type': free_game_id,
                }
                self.set_win_special_symbol_info(main_result, block_id, free_game_id, self.ScatterSymbolID, symbol_pos,
                                                 win_times, current_script)
            else:
                main_result.set_temp_special_game_data("win_times", win_times)


        # # 特殊輪處理
        # feature, multiplier = self._CheckSpecReel(checkReel, SymbolIDMap, special_odds["SpecialReelSymbolMulti"], bet_level)
        # if multiplier is None:
        #     multiplier = 1
        # else:
        #     main_result.set_temp_special_game_data("Multiplier", multiplier)
        # # 檢查線獎贏分
        # self.main_win_check(main_result, block_id, play_info, odds, checkReel, showReel, check_reel_length, check_reel_amount,
        #                                  all_multiplier=multiplier, SymbolIDMap=SymbolIDMap, ReverseSymbolIDMap=ReverseSymbolIDMap, PlatRatio=PlatRatio)
        # if feature == "Bonus":
        #     main_result.set_temp_special_game_data("Bonus", True)
        # self.pre_win_check(main_result, block_id, 0, 0, checkReel, showReel, check_reel_length, check_reel_amount, is_pass_line=False)

    def main_win_check(self, main_result, block_id, play_info, odds, check_reel, show_reel, check_reel_length,check_reel_amount,extra_odds):
        """
        檢查線獎的贏分；scatter的贏分在scatter的check給
        :type main_result: MainGameResultEX
        :param is_two_way: 是不是雙邊對獎，預設單邊
        """
        count = 0 # 随时可删除

        total_win = 0
        combo_arr = []
        floor_multiple = [[0 for _ in range(check_reel_length)] for _ in range(check_reel_amount)]
        while True:
            count += 1# 随时可删除



            if not play_info.is_special_game:
                floor_multiple = [[0 for _ in range(check_reel_length)] for _ in range(check_reel_amount)]
            combo_info = {}
            this_rm_element = [[0 for _ in range(check_reel_length)] for _ in range(check_reel_amount)]
            add_new_element = [[0 for _ in range(check_reel_length)] for _ in range(check_reel_amount)]
            is_eliminate, this_win = self._eliminate(check_reel, floor_multiple, this_rm_element, total_win,odds)
            if (not is_eliminate and not self._eliminate_special_symbol(check_reel, floor_multiple, this_rm_element)) or total_win > self.MaxWin:
                break
            combo_info['this_eliminate_mark'] = this_win
            print('第%s次%s分'%(count,this_win))

            total_win += this_win

            combo_info['eliminate'] = copy.deepcopy(check_reel)

            combo_info['this_rm_element'] = this_rm_element

            self._move_zero(check_reel, add_new_element)
            # TODO 先用固定死主游戏卷轴，后续会改
            self._add_element(check_reel, add_new_element, GameInfo[0]["main_reels"]['100'],extra_odds)
            combo_info['add_new_position'] = add_new_element

            new_floor_multiple = copy.deepcopy(floor_multiple)
            combo_info['floor_multiple'] = new_floor_multiple

            add_new_matrix = copy.deepcopy(check_reel)
            combo_info['add_new_array'] = add_new_matrix

            combo_arr.append(combo_info)
        reel_info = main_result.get_reel_block_data(block_id)
        main_result.this_win += int(total_win)
        print('总分', total_win)
        return combo_arr, total_win

    def _add_element(self,reel,add_new_element,all_reel_data,extra_odds):
        scatter_count = 0 # 记录scatter初始数量
        for r in range(len(reel)):
            temp_show_reel = list()
            amount_scatter_count = 0 # 记录当前轮scatter数量
            if self.ScatterSymbolID in reel[r]:
                amount_scatter_count += 1
                scatter_count += 1
            lines_count = len(reel) - len(reel[r]) # 记录当前轮缺少几个元素
            now_reel_data = all_reel_data[str(r)] # 当前轮所用的盘面中，应该用到的轮
            now_reel_data_max_index = len(now_reel_data) - 1 # 当前轮所对应的配置轮中有多少个元素
            random_index = random.randint(0, now_reel_data_max_index)
             # 添加缺失的元素循环上面记录缺失的次数
            for c in range(random_index,random_index + lines_count):
                while c > now_reel_data_max_index:
                    c -= now_reel_data_max_index + 1
                temp_show_reel.append(now_reel_data[c])
            # 如果后生成的盘面中有特殊图标，则判断是否生成scatter 还是普通图标
            if self.SpecialSymbolID in temp_show_reel:
                # TODO 以后的base_trigger_scatter可能改成变量
                if random.random() < extra_odds['base_trigger_scatter'][scatter_count] and not amount_scatter_count:
                    temp_show_reel[temp_show_reel.index(self.SpecialSymbolID)] = self.ScatterSymbolID
                    amount_scatter_count += 1
                    scatter_count += 1
                else:
                    temp_show_reel[temp_show_reel.index(self.SpecialSymbolID)] = random.choice(self.CommonSymbolIdList)
            reel[r] = temp_show_reel + reel[r]
            add_new_element[r] = temp_show_reel + add_new_element[r]

        # pass

    def _eliminate(self,reel, floor_multiple, this_rm_element, total_win, odds):
        """
        消除所有相邻相同且数量大于5的元素。
        :param reel: 原始盘面
        :param floor_multiple: 底板倍数
        :param this_rm_element: 本次消除的元素盘面初始化
        :param total_win: 分数
        :param odds: 配置表对应分数
        :return: 是否有元素被消除, 更新后的总分数
        """
        rows = len(reel)
        cols = len(reel[0]) if rows > 0 else 0
        to_zero = [[False for _ in range(cols)] for _ in range(rows)]
        eliminated = False
        this_win = 0

        # 遍历每个元素
        for r in range(rows):
            for c in range(cols):
                if reel[r][c] == 0 or to_zero[r][c]:
                    continue  # 如果已经是 0 或已经标记过，跳过

                # 找到所有相邻且值相同的点
                path = self._find_adjacent(reel, r, c)

                # 如果路径长度大于等于 5，标记需要归零
                if len(path) >= self.RemoveCount:
                    eliminated = True
                    this_floor_multiple = 0
                    for x, y in path:
                        this_rm_element[x][y] = reel[r][c]
                        to_zero[x][y] = True
                        if floor_multiple[x][y] == 0:
                            floor_multiple[x][y] = 1
                        elif floor_multiple[x][y] < self.MaxMulti:
                            floor_multiple[x][y] *= 2
                        if floor_multiple[x][y] > 1:
                            this_floor_multiple += floor_multiple[x][y]
                    if this_floor_multiple:
                        this_win += this_floor_multiple * odds[str(reel[r][c])][len(path)]
                    else:
                        this_win += odds[str(reel[r][c])][len(path)]

        # 将标记的位置归零
        for i in range(rows):
            for j in range(cols):
                if to_zero[i][j]:
                    reel[i][j] = 0
        total_win += this_win
        return eliminated, this_win

    def _move_zero(self,reel, add_new_element):
        """
        移动盘面中的零元素，为新元素加入做准备。
        :param reel: 真实的7x7盘面
        :param add_new_element: 7x7全是0的增加里面的新元素
        :return: 无
        """

        for r in range(len(reel)):
            for c in range(len(reel[r]) - 1, -1, -1):
                if reel[r][c] == 0:
                    del reel[r][c]
                    del add_new_element[r][c]
    
    def _find_adjacent(self,reel, r, c):
        """
        使用栈实现 DFS，找到所有与 (r, c) 相邻且值相同的元素。
        :param reel: 二维数组
        :param r: 起始行
        :param c: 起始列
        :return: 所有相邻且值相同的点的列表
        """
        rows = len(reel)
        cols = len(reel[0]) if rows > 0 else 0
        target = reel[r][c]
        stack = [(r, c)]
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        path = []
        # 定义四个方向：上、下、左、右
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while stack:
            x, y = stack.pop()
            if x < 0 or x >= rows or y < 0 or y >= cols:
                continue  # 超出边界
            if reel[x][y] != target or visited[x][y]:
                continue  # 值不匹配或已经访问过
            if reel[x][y] in [94, 92]:
                continue  # 炸弹图标或scatter图标不记录

            # 标记当前点为已访问，并加入路径
            visited[x][y] = True
            path.append((x, y))

            # 将四个方向的点加入栈
            for dx, dy in directions:
                stack.append((x + dx, y + dy))

        return path

    def _eliminate_special_symbol(self,reel, floor_multiple, this_rm_element):
        """
        如果出现了炸弹，则将其本身及其相邻的八个方向的元素都归零消除。
        :param reel: 二维数组
        :param floor_multiple: 底板倍数数组
        :param this_rm_element: 本次消除的元素记录数组
        :return: 是否出现了炸弹
        """
        rows = len(reel)
        cols = len(reel[0]) if rows > 0 else 0
        # 定义八个方向：上、下、左、右、左上、左下、右上、右下
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # 记录需要归零的位置
        to_zero = [[False for _ in range(cols)] for _ in range(rows)]
        # 是否出现了炸弹
        is_bomb = False

        # 遍历数组，查找是否有炸弹
        for r in range(rows):
            for c in range(cols):
                if reel[r][c] == self.BombSymbolID:
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
                if to_zero[r][c]:  # 如果这个地方是True，则代表炸弹覆盖范围
                    this_rm_element[r][c] = reel[r][c]
                    reel[r][c] = 0
                # 炸弹爆炸后需要底板倍数乘倍
                if floor_multiple[r][c] == 0:
                    floor_multiple[r][c] = 1
                elif floor_multiple[r][c] < self.MaxMulti:
                    floor_multiple[r][c] *= 2
        return is_bomb

    # 計算贏倍 (skip_five_symbol=True代表要略過5連線的贏分)
    def check_line_win(self, reel_info, play_info, odds, check_reel, show_reel, line_id, line_data, check_reel_length,
                       check_reel_amount, is_from_left=True, skip_five_symbol=False, wild_multiplier=[], all_multiplier=1, SymbolIDMap=None, ReverseSymbolIDMap=None, PlatRatio=None):
        """
        計算線獎贏分
        :type reel_info: MainReelInfo
        """

        check_str = ""
        for i in range(check_reel_amount):
            check_str += SymbolIDMap[check_reel[i][line_data[i]]]

        if len(check_str) <= 0:
            return 0
        current_win = int(check_str)
        if current_win == 0:
            return 0

        all_multiplier /= PlatRatio
        if check_reel[check_reel_amount - 1][line_data[check_reel_amount - 1]] >= 100:
            all_multiplier /= 10 ** int((check_reel[check_reel_amount - 1][line_data[check_reel_amount - 1]])/100)   # 顯示數字有小數，預留多於一位的情況
        current_win *= all_multiplier

        assert current_win.is_integer()
        current_win = int(current_win)
        # print(current_win)

        return current_win


    def pre_win_check(self, main_result, block_id, check_symbol_id, check_symbol_limit, check_reel, show_reel, check_reel_length, check_reel_amount, is_pass_line=False, check_symbol_included_wild=tuple()):
        # 第二、三輪都有symbol就聽牌
        reel_info = main_result.get_reel_block_data(block_id)
        if check_reel[1][0] > 0 and check_reel[2][0] > 0:
            pre_win_info = [1, 0, 0, 0]
            reel_info.set_pre_win_info(pre_win_info)

    def _CheckSpecReel(self, reel, SymbolIDMap, awardMultiMap, bet_level):
        multiplier, feature = None, None
        spec_id = reel[self.SpecReelIdx][0]
        feature = SymbolIDMap.get(spec_id)
        if feature is None:
            return feature, multiplier
        if feature == "Bonus":
            return feature, multiplier
        multiplier = awardMultiMap.get(str(spec_id))
        return feature, multiplier

