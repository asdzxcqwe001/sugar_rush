#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SlotCommon.slot_calculator import *


class CashKing(DefaultSlotCalculator):
    SymbolIDMap = {
        0: "",
        2: "Bonus",
        3: "Multi",     # (Max)
        4: "Multi",     # (2nd)
        5: "Multi",     # (3rd)
        6: "Multi",     # (4th)
        7: "Multi",     # (5th)
        10: "0",
        20: "00",
        30: "000",
        101: "1",       # (.1)
        105: "5",       # (.5)
        225: "25",       # (.25)   # 目前規格沒有小數點下兩位數，但好像沒問題，再更多位可能就會GG
        11: "1",
        12: "2",
        15: "5",
        21: "10",
        25: "50",
        31: "100",
    }
    ReverseSymbolIDMap = None#{v: k for k, v in SymbolIDMap.items()}

    def _init_consts(self):
        self.FreeGameId = 1
        self.SuperFreeGameId = 2

    def get_init_reel_info(self, game_state):
        """
        START_GAME的時候需要取得初始牌面
        :return:
        """
        fake_reels = self._gameSetting['fake_main_reels']
        view_reels = game_state.last_main_reels.get('0', {})
        if len(view_reels) <= 0:
            view_reels = {str(reel_id): list(fake_reels.values())[0][str(reel_id)][:self.reel_length] for reel_id in range(self.reel_amount)}
        block_data = dict()

        ret = list()
        block_data.update({
            'id': 0,
            'init_wheels': view_reels,
            'fake_wheels': fake_reels,
        })
        ret.append(block_data)
        return ret

    # def get_spin_reel_data(self, gameInfo, is_extra_bet=False, reel_key="0"):
    #     reel_key = "extra_" + str(reel_key) if is_extra_bet else str(reel_key)
    #     return gameInfo['main_reels'][reel_key]

    def get_spin_reel_data(self, game_info, is_fever=False, reel_key="0"):
        if is_fever:
            return game_info['fever_reels'][reel_key]
        return game_info['main_reels'][reel_key]

    def spin(self, bet_value, bet_lines, game_state, gameInfo, dev_mode=DevMode.NONE, special_input_data=None, **kwargs):

        play_info = MainGamePlayInfo()
        play_info.set_is_fever_game(False)
        play_info.set_bet_info(bet_value, bet_lines)
        is_extra_bet = kwargs.get('extra_bet', False)
        bet_level = self._GetBetLevel(bet_value, is_extra_bet)
        play_info.set_extra_bet(is_extra_bet)
        extraOdds = gameInfo.get('extra_odds', {})
        PlatRatio = extraOdds['Ratio']

        block_id = 0
        result = MainGameResult([block_id])

        spin_reel_data = self.get_spin_reel_data(gameInfo,is_extra_bet, "100")
        # fake_reel_data = extraOdds['FakeReelWeight'][str(bet_level)]
        # self._chance.get_result_reels(result, block_id, spin_reel_data, fake_reel_data, self.reel_length, self.reel_amount, dev_mode)
        self._chance.get_spin_result(result, block_id, spin_reel_data, self.reel_length, self.reel_amount,self.check_reel_length, self.check_reel_amount, dev_mode)

        self._check.game_check(result, block_id, play_info, self._odds, self._special_odds, extraOdds,
                               self.reel_length, self.reel_amount, self.check_reel_length, self.check_reel_amount, bet_level=bet_level, SymbolIDMap=self.SymbolIDMap, ReverseSymbolIDMap=self.ReverseSymbolIDMap, PlatRatio=PlatRatio)
        main_win = result.this_win
        bonus_win = 0
        if result.get_temp_special_game_data("Bonus", False):
            bonus_win = self.bonus_win(result, play_info, extraOdds, bet_level, dev_mode)
            result.this_win += bonus_win

        # AnalysysLog
        result.set_log_custom("MainReels", result.get_temp_special_game_data("CheckReel"))
        result.set_log_custom("MainWin", main_win)
        result.set_log_custom("BonusWin", bonus_win)
        if result.get_temp_special_game_data("Multiplier", 1) > 1:
            result.set_log_custom("Multi", result.get_temp_special_game_data("Multiplier"))

        return result

    def next_fever(self, client_action, game_state, game_info, dev_mode=DevMode.NONE, **kwargs):
        """ 特殊遊戲處理 """

        print("[SugarRush][next_fever] client_action={}, game_state={}, game_info={}, dev_mode={}".format(
            client_action, game_state, game_info, dev_mode))

        special_game_id = game_state.current_sg_id  # 目前所在的特殊遊戲
        fever_result = FeverLevelResult(special_game_id)  # 最後要回傳的內容

        # 遊戲狀態非特殊遊戲
        if not game_state.is_special_game:
            self.logger.error("[SugarRush][next_fever] Not in special game, game:{}".format(self._game_id))
            fever_result.error = True
            return fever_result

        # sg_id 對不起來
        if client_action['client_sg_id'] != game_state.current_sg_id:
            self.logger.error("[SugarRush][next_fever] client_sg_id:{} != current_sg_id:{}".format(
                client_action['client_sg_id'], game_state.current_sg_id))
            fever_result.error = True
            return fever_result

        dev_mode = DevMode.NONE
        # 這邊依照遊戲自行設計
        if special_game_id == self.FreeGameId:
            self.free_game(fever_result, client_action, game_state, game_info, dev_mode)
        elif special_game_id == self.SuperFreeGameId:
            self.super_free_game(fever_result, client_action, game_state, game_info, dev_mode)
        else:
            # 未知的特殊遊戲
            raise Exception("[ERROR] Error Special Game id:{}, game:{}".format(special_game_id, self._game_id))

        return fever_result

    def free_game(self, fever_result, client_action, game_state, game_info, dev_mode):
        """ 特殊遊戲: FreeGame

        Args:
            fever_result (FeverLevelResult): 要回傳的結果
            client_action (dict): client 傳來的自訂資料，如果 client 需要作什麼選擇時會用到
            game_state (MainGameState): 遊戲狀態
            game_info (dict): 跟機率 (prod_id) 對應的 Info 資料
            dev_mode (DevMode): 測試模式 trigger
        """
        # 特殊遊戲基本資料
        special_game_id = game_state.current_sg_id  # 特殊遊戲ID
        special_game_state = game_state.current_special_game_data  # 該特殊遊戲的資料
        bet_lines = special_game_state['current_line']  # 押注線數
        bet_value = special_game_state['current_bet']  # 押注倍數
        current_level = special_game_state['current_level']  # 目前特殊遊戲的狀態
        current_script = special_game_state.get('current_script', {})  # 對應特殊遊戲的暫存內容 (自定義資料)
        is_extra_bet = special_game_state.get('is_extra_bet', False)  # 是否有額外押注
        extra_odds = game_info.get('extra_odds', {})
        block_id = 0

        # 準備 play_info
        play_info = MainGamePlayInfo()
        play_info.SpecialGame = special_game_id
        play_info.set_bet_info(bet_value, bet_lines)

        main_result = MainGameResult([block_id])
        if current_level == 1:
            fever_result.fever_map = FeverMap(1)
            spin_reel_data = self.get_spin_reel_data(game_info,True, "mid")
            self._check.get_spin_result(main_result,block_id,spin_reel_data,self.reel_length,self.reel_amount,self.check_reel_length,self.check_reel_amount,dev_mode)

            fever_result.fever_map.append("result",main_result.export_ex_wheel_block_result())
            fever_result.fever_map.append("total_times",special_game_state['current_script']['total_times'])
            special_game_state['current_level'] += 1
            _,fg_type = self.randomer.get_result_by_weight(
                extra_odds['fg_type']['result'],
                extra_odds['fg_type']['weight'],
            )
            special_game_state['fg_type'] = fg_type
        elif current_level == 2:
            result = MainGameResult([block_id])























            result.get_temp_special_game_data("win_times",0)


    def super_free_game(self, fever_result, client_action, game_state, game_info, dev_mode):
        pass

    def bonus_win(self, main_result, play_info, extra_odds, bet_level, dev_mode=DevMode.NONE):
        bonus_odds = [odds * play_info.total_bet for odds in extra_odds["Bonus"][str(play_info.GameLineBet)]["Odds"]]
        bonus_weight = extra_odds["Bonus"][str(play_info.GameLineBet)]["Weight"]
        if dev_mode >= 100 and dev_mode % 100 < 12:
            idx = dev_mode % 100
            win = bonus_odds[idx]
        else:
            idx, win = self.randomer.get_result_by_weight(bonus_odds, bonus_weight)
        bonus_odds.pop(idx)
        resultList = [win] + self.randomer.sample(bonus_odds, len(bonus_odds))
        reel_info = main_result.get_reel_block_data(block_id=0)
        reel_info.set_end_feature("Bill", {"Bill": resultList, "Win": win, "MainWin": main_result.this_win})

        return win

    def _GetBetLevel(self, nBetValue, bExtraBet=False):
        return str(int(nBetValue))


    def get_win_type(self, bet, win, gameState, result, winTypeInfo):
        # "NO_WIN": 0, "NORMAL_WIN": 1, "LIGHT_WIN": 2, "SMALL_WIN": 3, "BIG_WIN": 4,"MEGA_WIN": 5, "SUPER_WIN": 6
        type = 0
        if bet == 0 or win == 0 or bet is None or win is None:
            return 0
        win_bet_multiple = float(win) / bet
        for t, g in enumerate(winTypeInfo):
            if win_bet_multiple >= g:
                type = t
            else:
                break
        if type < 4 and result.get_temp_special_game_data("Bonus", False):   # less than BIG WIN and win Bonus
            return 7  # Bonus Special Win
        return type

    def build_result_log(self, ret_data, spin_result, jp_win, extra_bet=False):
        result_log = DefaultSlotCalculator.build_result_log(self, ret_data, spin_result, jp_win, extra_bet)
        # 需要顯示上下兩顆
        showReel = self._check.get_check_reel(spin_result, 0, self.reel_length, self.reel_amount, self.check_reel_length+2, self.reel_amount, transform=False)
        result_log['reel_info'] = [showReel]

        # 特殊輪的乘倍數字
        spec_reel_extra_info = [str(self._gameSetting['extra_info']['SpecialReelSymbolMulti'].get(str(symbol_id), "")) for symbol_id in showReel[3]]
        result_log['extra_info'] = [[[], [], [], spec_reel_extra_info]]
        return result_log

    def get_feature_win_log(self, spin_result):
        feature_win_log = []
        end_feature = spin_result.get_reel_block_data(0).end_feature
        main_win = end_feature.get("Main", 0)
        feature_win_log.append({'feature_id':0, "win": main_win})
        bonus_game = end_feature.get("Bill")
        if bonus_game:
            # feature_id 1: green bill, 2: golden bill(greatest bill)
            is_golden = bonus_game["Win"] == max(bonus_game["Bill"])
            feature_win_log.append({'feature_id': 2 if is_golden else 1, "win": bonus_game["Win"]})
        return feature_win_log




