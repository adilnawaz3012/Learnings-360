class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:

        def mergeSortHelper(left, right):
            sorted_arr = []
            i, j = 0, 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    sorted_arr.append(left[i])
                    i += 1
                else:
                    sorted_arr.append(right[j])
                    j += 1
            while i < len(left):
                sorted_arr.append(left[i])
                i += 1

            while j < len(right):
                sorted_arr.append(right[j])
                j += 1
            
            return sorted_arr

        def mergeSort(nums):
            if len(nums) <= 1:
                return nums

            mid = len(nums) // 2
            left = mergeSort(nums[:mid])
            right = mergeSort(nums[mid:])
            return mergeSortHelper(left, right)
        return mergeSort(nums)

        """
                    [38, 27, 43, 3, 9, 82, 10]
                /                     \
        [38, 27, 43]               [3, 9, 82, 10]
            /         \               /          \
        [38, 27]    [43]         [3, 9]       [82, 10]
        /     \                 /    \        /     \
        [38]   [27]             [3]    [9]    [82]   [10]

        """