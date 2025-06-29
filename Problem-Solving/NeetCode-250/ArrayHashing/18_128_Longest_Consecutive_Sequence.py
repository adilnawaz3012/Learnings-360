from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # as to make it increasing, same elements cannot help in making an acending list
        unique_nums = set(nums)
        max_len = 0
        
        for ele in unique_nums:
            """
                We'll proceed only if prev element is not there, it means it's a fresh start.
                Also if num - 1 element is there, we'll skip as all the previous elements would have 
                been taken care
            """
            if ele - 1 not in unique_nums:
                curr_streak = 1
                curr_ele = ele
                while curr_ele + 1 in unique_nums:
                    curr_streak += 1
                    curr_ele += 1
                max_len = max(max_len, curr_streak)
        return max_len