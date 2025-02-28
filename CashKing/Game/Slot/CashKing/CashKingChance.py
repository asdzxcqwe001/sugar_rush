#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SlotCommon.game_chance import MainGameChance
from SlotCommon.slot_status_code import *
from SlotCommon.main_game_result import *


# ======================================================================
class CashKingChance(MainGameChance):

    def get_init_reel(self, reel_data, reel_length, reel_amount):
        main_result = MainGameResult([0])
        reel_info = main_result.get_reel_block_data(0)
        reel_info.set_one_reel_data(0, [11, 0, 11, 0, 11, 0, 11])
        reel_info.set_one_reel_data(0, [11, 0, 10, 0, 11, 0, 10])
        reel_info.set_one_reel_data(0, [10, 0, 10, 0, 10, 0, 10])
        reel_info.set_one_reel_data(0, [2, 0, 3, 0, 2, 0, 3])

        # self._get_spin_result_from_reel(reel_info, reel_data[str(0)], reel_length, reel_amount)
        return reel_info.reel_data

    def get_result_reels(self, main_result, block_id, real_weight_data, fake_weight_data, reel_length, reel_amount, dev_mode):
        if dev_mode != DevMode.NONE:
            real_weight_data = self.dev_change_reel_weight_data(real_weight_data, dev_mode)

        reel_info = main_result.get_reel_block_data(block_id)
        EmptySymbolID = 0
        MiddleSymbolIndex = reel_length // 2

        check_reel_result = self.transform_get_result_by_weight(real_weight_data)
        # print(f"check_reel_result: {check_reel_result}")
        if type(check_reel_result) is str:
            check_reel_result = tuple(int(i) for i in check_reel_result.split(","))
        for reel_no in range(reel_amount):
            temp_reel = [self.transform_get_result_by_weight(fake_weight_data[str(reel_no)]) for _ in range(reel_length)]
            # print(f"temp_reel[{reel_no}]: {temp_reel}")
            # 有效symbol
            temp_reel[MiddleSymbolIndex] = check_reel_result[reel_no]
            # print(f"temp_reel[{reel_no}]: {temp_reel}")
            # "bool(A) != bool(B)" means "A xor B"
            #                  有效symbol
            #              空白symbol 一般symbol
            #  有效 | 奇       1          0
            #  位置 | 偶       0          1
            empty_symbol_start_pos = 1 if (temp_reel[MiddleSymbolIndex] == EmptySymbolID) != (
                        MiddleSymbolIndex % 2 == 0) else 0
            for row in range(empty_symbol_start_pos, reel_length, 2):
                temp_reel[row] = EmptySymbolID
            # print(f"temp_reel[{reel_no}]: {temp_reel}")
            reel_info.set_one_reel_data(reel_no, temp_reel)

    def transform_get_result_by_weight(self, weight_data):
        transformed_weight_data = {"Result": [item["Result"] for item in weight_data], "Weight": [item["Weight"] for item in weight_data]}
        _, result = self.randomer.get_result_by_weight(transformed_weight_data["Result"], transformed_weight_data["Weight"])
        return result


    DEV_MODE_RESULT_TABLE = {
        1: (0, 0, 0, 2),
        3: (0, 11, 0, 3),
        4: (0, 11, 0, 4),
        5: (0, 11, 0, 5),
        6: (0, 11, 0, 6),
        7: (0, 11, 0, 7),

        20: (0, 10, 10, 2),
        21: (30, 20, 10, 2),
        22: (31, 30, 101, 0),
        23: (25, 21, 105, 0),
        24: (15, 20, 11, 0),
        25: (0, 12, 10, 0),

        100: (0, 11, 0, 2),
        101: (0, 11, 0, 2),
        102: (0, 11, 0, 2),
        103: (0, 11, 0, 2),
        104: (0, 11, 0, 2),
        105: (0, 11, 0, 2),
        106: (0, 11, 0, 2),
        107: (0, 11, 0, 2),
        108: (0, 11, 0, 2),
        109: (0, 11, 0, 2),
        110: (0, 11, 0, 2),
        111: (0, 11, 0, 2),

        211: (21, 21, 15, 2),
        212: (21, 21, 15, 3),

        2011: (25, 30, 20, 2),
        2012: (25, 30, 20, 3),
    }
    def dev_change_reel_weight_data(self, real_weight_data, dev_mode):
        if type(dev_mode) is int:
            pass
        elif dev_mode.isdigit():
            dev_mode = int(dev_mode)
        else:
            raise ValueError(f"dev_mode: {dev_mode} is not a valid value.")

        if dev_mode not in self.DEV_MODE_RESULT_TABLE:
            return real_weight_data
        return [{"Result": self.DEV_MODE_RESULT_TABLE[dev_mode], "Weight":1}]


# if __name__ == "__main__":
#     from SlotCommon.IgsRandomer import IgsRandomer
#     randomer = IgsRandomer()
#     chance = CashKingChance(randomer=randomer)
#     main_result = MainGameResult([0])
#     fake_weight_data = {
#                     "0": [
#                         {
#                             "Result": 11,
#                             "Weight": 10
#                         },
#                         {
#                             "Result": 15,
#                             "Weight": 10
#                         }
#                     ],
#                     "1": [
#                         {
#                             "Result": 10,
#                             "Weight": 10
#                         },
#                         {
#                             "Result": 11,
#                             "Weight": 10
#                         },
#                         {
#                             "Result": 15,
#                             "Weight": 10
#                         }
#                     ],
#                     "2": [
#                         {
#                             "Result": 10,
#                             "Weight": 10
#                         },
#                         {
#                             "Result": 101,
#                             "Weight": 10
#                         },
#                         {
#                             "Result": 105,
#                             "Weight": 10
#                         }
#                     ],
#                     "3": [
#                         {
#                             "Result": 2,
#                             "Weight": 10
#                         },
#                         {
#                             "Result": 3,
#                             "Weight": 10
#                         }
#                     ]
#                 }
#     real_weight_data = [
#                 {
#                     "Result": "(0, 0, 0, 0)",
#                     "Weight": 10
#                 },
#                 {
#                     "Result": "(11, 0, 0, 0)",
#                     "Weight": 10
#                 },
#                 {
#                     "Result": "(0, 11, 0, 3)",
#                     "Weight": 10
#                 },
#                 {
#                     "Result": "(0, 0, 11, 0)",
#                     "Weight": 10
#                 },
#                 {
#                     "Result": "(0, 0, 0, 2)",
#                     "Weight": 5
#                 }
#             ]
    # chance.get_result_reels(main_result, 0, real_weight_data, fake_weight_data, 7, 4, 3)
    # print(main_result.get_reel_block_data(0).reel_data)
