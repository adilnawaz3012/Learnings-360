from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
            Area=width×height=(j−i)×min(height[i],height[j])
        """
        n = len(height)
        left = 0
        right = n - 1
        max_area = 0
        while left < right:
            width = right - left
            area = width * min(height[left], height[right])
            max_area = max(max_area, area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area