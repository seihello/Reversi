from Common import Common
from Util import Util

from abc import ABC, abstractmethod
from enum import Enum, auto
import random

class StrategyType(Enum):
    PLAYER = auto()
    SIMPLE = auto()
    EVALUATION = auto()
    EVALUATION_RANDOM = auto()
    DECREACING_OPP_EVALUATION = auto()
    BALANCE_EVALUATION = auto()
    FLEXIBLE = auto()


# 駒配置アルゴリズムのインタフェース
class Strategy(ABC):
    def __init__(self, mass_type, strategy_type):
        self.mass_type = mass_type
        self.type = strategy_type

    @abstractmethod
    def put(self, board):
        pass

# 駒配置アルゴリズム
# 置けるところに置くだけ
class SimpleStrategy(Strategy):

    def __init__(self, mass_type):
        super().__init__(mass_type, StrategyType.SIMPLE)

    def put(self, mass_list):
        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, self.mass_type):
                    print(str(self.type) + ": " + str(i) + " " + str(j))
                    return i, j

# 駒配置アルゴリズム
# 評価値マップを使い、評価値が高いところに置く
class EvaluationStrategy(Strategy):

    def __init__(self, mass_type):
        super().__init__(mass_type, StrategyType.EVALUATION)
        self.evaluation = [[5, 1, 4, 4, 4, 4, 1, 5],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [5, 1, 4, 4, 4, 4, 1, 5]]

    def put(self, mass_list):

        max_value = 0
        x = 0
        y = 0
        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, self.mass_type):
                    if self.evaluation[i][j] > max_value:
                        max_value = self.evaluation[i][j]
                        x = i
                        y = j

        print(str(self.type) + ": " + str(x) + " " + str(y))
        return x, y

# 駒配置アルゴリズム
# 評価値マップを使い、評価値が高いところからランダムに選択して置く
class EvaluationRandomStrategy(Strategy):

    def __init__(self, mass_type):
        super().__init__(mass_type, StrategyType.EVALUATION_RANDOM)
        self.evaluation = [[5, 1, 4, 4, 4, 4, 1, 5],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [5, 1, 4, 4, 4, 4, 1, 5]]

        self.type = StrategyType.EVALUATION_RANDOM

    def put(self, mass_list):
        max_value = 0
        x = 0
        y = 0
        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, self.mass_type):
                    if self.evaluation[i][j] > max_value:
                        max_value = self.evaluation[i][j]
                        x = i
                        y = j
                    elif self.evaluation[i][j] == max_value:
                        if random.random() > 0.7:
                            max_value = self.evaluation[i][j]
                            x = i
                            y = j

        print(str(self.type) + ": " + str(x) + " " + str(y))
        return x, y


# 駒配置アルゴリズム
# 置いた結果、相手が置けるマスの最大評価値が最も低くなるように置く
class DecreasingOppEvaluation(Strategy):

    def __init__(self, mass_type):
        super().__init__(mass_type, StrategyType.DECREACING_OPP_EVALUATION)
        self.evaluation = [[5, 1, 4, 4, 4, 4, 1, 5],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [5, 1, 4, 4, 4, 4, 1, 5]]

    def put(self, mass_list):
        min_max_value = 5
        x = 0
        y = 0
        mass_list_origin = Util.copy_mass_list(mass_list)
        opp_mass_type = Util.get_opp_type(self.mass_type)

        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, self.mass_type):
                    new_mass_list = Util.copy_mass_list(mass_list)
                    max_value_this_time = 0

                    # 配置してひっくり返す
                    new_mass_list[i][j] = self.mass_type
                    new_mass_list = Util.reverse(new_mass_list, i, j, self.mass_type)

                    for s in range(Common.MASS_NUM):
                        for t in range(Common.MASS_NUM):
                            if Util.can_put(new_mass_list, s, t, opp_mass_type):
                                if max_value_this_time < self.evaluation[s][t]:
                                    max_value_this_time = self.evaluation[s][t]

                    if max_value_this_time <= min_max_value:
                        min_max_value = max_value_this_time
                        x = i
                        y = j

        print(str(self.type) + ": " + str(x) + " " + str(y))
        return x, y


# 駒配置アルゴリズム
# 自分が置くときの評価値から、自分が置いた結果相手が置けるマスの評価値を差し引きする
class BalanceEvaluation(Strategy):

    def __init__(self, mass_type):
        super().__init__(mass_type, StrategyType.BALANCE_EVALUATION)
        self.evaluation = [[5, 1, 4, 4, 4, 4, 1, 5],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [5, 1, 4, 4, 4, 4, 1, 5]]

    def put(self, mass_list):
        max_balance_value = -100
        x = 0
        y = 0
        mass_list_origin = Util.copy_mass_list(mass_list)
        opp_mass_type = Util.get_opp_type(self.mass_type)

        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, self.mass_type):
                    new_mass_list = Util.copy_mass_list(mass_list)
                    max_value_this_time = 0

                    # 配置してひっくり返す
                    new_mass_list[i][j] = self.mass_type
                    new_mass_list = Util.reverse(new_mass_list, i, j, self.mass_type)

                    for s in range(Common.MASS_NUM):
                        for t in range(Common.MASS_NUM):
                            if Util.can_put(new_mass_list, s, t, opp_mass_type):
                                if max_value_this_time < self.evaluation[s][t]:
                                    max_value_this_time = self.evaluation[s][t]

                    # 自分が置くときの評価値と、次相手が置くときの評価値を差し引き
                    balance_value = self.evaluation[i][j] - max_value_this_time

                    if max_balance_value < balance_value:
                        max_balance_value = balance_value
                        x = i
                        y = j

        print(str(self.type) + ": " + str(x) + " " + str(y))
        return x, y

# 駒配置アルゴリズム
#
class Flexible(Strategy):

    def __init__(self, mass_type):
        super().__init__(mass_type, StrategyType.FLEXIBLE)
        self.evaluation = [[5, 1, 4, 4, 4, 4, 1, 5],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [5, 1, 4, 4, 4, 4, 1, 5]]

    def put(self, mass_list):
        max_balance_value = -100
        x = 0
        y = 0
        mass_list_origin = Util.copy_mass_list(mass_list)
        opp_mass_type = Util.get_opp_type(self.mass_type)

        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, self.mass_type):

                    # 角が置けるなら必ず置く
                    if self.evaluation[i][j] == 5:
                        return i, j

                    new_mass_list = Util.copy_mass_list(mass_list)
                    max_value_this_time = 0

                    # 配置してひっくり返す
                    new_mass_list[i][j] = self.mass_type
                    new_mass_list = Util.reverse(new_mass_list, i, j, self.mass_type)

                    for s in range(Common.MASS_NUM):
                        for t in range(Common.MASS_NUM):
                            if Util.can_put(new_mass_list, s, t, opp_mass_type):
                                if max_value_this_time < self.evaluation[s][t]:
                                    max_value_this_time = self.evaluation[s][t]

                    # 自分が置くときの評価値と、次相手が置くときの評価値を差し引き
                    balance_value = self.evaluation[i][j] - max_value_this_time

                    if max_balance_value < balance_value:
                        max_balance_value = balance_value
                        x = i
                        y = j

        return x, y