class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        seen = set()
        for idx in range(n):
            _remainder = target - nums[idx]
            if _remainder in seen:
                return [nums.index(_remainder), idx]
            else:
                seen.add(nums[idx])
        return []