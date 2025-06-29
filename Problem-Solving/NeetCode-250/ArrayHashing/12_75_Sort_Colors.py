from typing import List

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        i = 0
        j = n - 1
        k = 0
        while k <= j:
            if nums[k] == 0:
                # Move the 0 element to ith place
                nums[i] , nums[k] = nums[k], nums[i]
                i += 1
                k += 1
            elif nums[k] == 2:
                # Move the 2 element to jth place
                nums[k], nums[j] = nums[j], nums[k]
                j -= 1
            else:
                # keep moving
                k += 1