from typing import List

class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        m = len(matrix)
        n = len(matrix[0])
        # Increse the size by 1 for both row and col to handle substraction
        """
            if i need first row and col, then prev val will be zero. so to handle edge case, we need one extra row and col
        """
        self.prefix = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                # same logic as below to calculate the sum
                self.prefix[i + 1][j + 1] =  matrix[i][j] + self.prefix[i + 1][j] + self.prefix[i][j + 1] - self.prefix[i][j]

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        """
            +----------------------------+
            | A (prefix[row1][col1])     | B (prefix[row1][col2+1] - prefix[row1][col1])    |
            |                            |                                                  |
            +----------------------------+--------------------------------------------------+
            | C (prefix[row2+1][col1] - prefix[row1][col1]) | D (desired rectangle)                  |
            |                            |                                                  |
            +----------------------------+--------------------------------------------------+

        """
        return (
            self.prefix[row2+1][col2+1] - self.prefix[row1][col2+1] - self.prefix[row2 + 1][col1] + self.prefix[row1][col1]
        )


# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)