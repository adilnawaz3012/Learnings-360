from typing import List
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
            Keep storing those value which does not match val and keep incrementing
            the counter to store next set of values.
        """
        k = 0
        n = len(nums)
        for idx, num in enumerate(nums):
            if num != val:
                nums[k] = num
                k += 1
        return k