class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        """
            Basic Logic:
                1. we need to pair the min and max weight to at a time
                2. if weight is more, take the max weight person alone and proceed with other
        """
        n = len(people)
        people.sort()
        min_boats_req = 0
        i, j = 0, n -1
        while i <= j:
            weight_sum = people[i] + people[j]
            if weight_sum <= limit:
                i +=1 
                j -= 1
                min_boats_req += 1
            else:
                min_boats_req += 1
                j -= 1
        return min_boats_req
