class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        n = len(nums)
        
        for i in range(0, n-2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue  # skip duplicates for i
            k = i + 1
            j = n - 1
            while k < j:
                triplet_sum = nums[i] + nums[j] + nums[k]
                if triplet_sum == 0:
                    result.append([nums[i], nums[j], nums[k]])
                    k += 1
                    j -= 1
                    while k < j and nums[k] == nums[k - 1]:
                        k += 1
                    while k < j and nums[j] == nums[j + 1]:
                        j -= 1
                elif triplet_sum < 0:
                    k += 1
                else:
                    j -= 1
        return result
