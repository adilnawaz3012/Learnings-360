from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:

        """
            Ref: https://www.youtube.com/watch?v=1_5VuquLbXg

            basic Logic:
                we need to see what is the max left height and max right height barrier for curren tbuilding to hold the water
                since min of left or right max will be able to hold the water
                but water will only be holded, if current building height is less than left or right min
        """
        n = len(height)
        left_max = [0] * n
        right_max = [0] * n
        for idx in range(1, n):
            left_max[idx] = max(left_max[idx - 1], height[idx - 1])
        for idx in range(n-2, -1, -1):
            right_max[idx] = max(right_max[idx + 1], height[idx + 1])
        
        water_stored = 0
        for idx in range(1, n - 1):
            if height[idx] < left_max[idx] and height[idx] < right_max[idx]:
                water_stored += min(left_max[idx], right_max[idx]) - height[idx]
        return water_stored