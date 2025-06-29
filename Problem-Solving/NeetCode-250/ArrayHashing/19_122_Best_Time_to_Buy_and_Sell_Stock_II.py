from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)

        def r(idx: int, buy: bool) -> int:
            if idx == n:
                return 0
            profit = float('-inf')
            if buy:
                can_buy = -prices[idx] + r(idx + 1, not buy)
                not_buy = 0 + r(idx + 1, buy)
                profit = max(can_buy, not_buy)
            else:
                can_sell = prices[idx] + r(idx + 1, not buy)
                not_sell = 0 + r(idx + 1, buy)
                profit = max(can_sell, not_sell)
            return profit

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def m(idx, buy):
            if idx == n:
                return 0
            if buy:
                can_buy = -prices[idx] + m(idx + 1, not buy)
                not_buy = 0 + m(idx + 1, buy)
                profit = max(can_buy, not_buy)
            else:
                can_sell = prices[idx] + m(idx + 1, not buy)
                not_sell = 0 + m(idx + 1, buy)
                profit = max(can_sell, not_sell)
            return profit

        def t():
            dp = [[0] * 2 for _ in range(n + 1)]
            for idx in range(n - 1, -1, -1):
                for buy in [0, 1]:
                    if buy:
                        can_buy = -prices[idx] + dp[idx + 1][not buy]
                        not_buy = 0 + dp[idx + 1][buy]
                        profit = max(can_buy, not_buy)
                    else:
                        can_sell = prices[idx] + dp[idx + 1][not buy]
                        not_sell = 0 + dp[idx + 1][buy]
                        profit = max(can_sell, not_sell)
                    dp[idx][buy] = profit
            return dp[0][1]


        def t_op():
            """
                if we see the t(), i.e dp code, we only care about the previous val, so don't need to 
                keep storing all the values
            """
            prev, curr = [0, 0], [0, 0]
            for idx in range(n - 1, -1, -1):
                for buy in [0, 1]:
                    if buy:
                        can_buy = -prices[idx] + prev[not buy]
                        not_buy = 0 + prev[buy]
                        profit = max(can_buy, not_buy)
                    else:
                        can_sell = prices[idx] + prev[not buy]
                        not_sell = 0 + prev[buy]
                        profit = max(can_sell, not_sell)
                    curr[buy] = profit
                prev = curr
            return prev[1]

        # return r(0, 1)
        # return m(0, 1)

        # return t()

        return t_op()