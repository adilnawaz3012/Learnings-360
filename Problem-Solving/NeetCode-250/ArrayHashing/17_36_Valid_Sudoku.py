from typing import List

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        """
            Basic Logic:
                1. Is the row valid
                2. Is the col valid
                3. Is the square ( 3 x 3 ) valid

                If all 3 condition satisfied, then the complete board is valid
        """

        def is_row_valid(board):
            for row in board:
                # here row is also a sub board of length x and breadth 1
                if not is_valid(row):
                    return False
            return True
        
        def is_col_valid(board):
            """
                The * operator before board unpacks the list of rows into separate arguments. 
                So if board has rows [row1, row2, row3], then zip(*board) is equivalent to 
                zip(row1, row2, row3).

                The zip() function takes these rows and pairs elements with the same index 
                from each row together into tuples. Each tuple corresponds to one column of the matrix.

                Therefore, iterating over zip(*board) yields each column as a tuple.
            """
            for col in zip(*board):
                if not is_valid(col):
                    return False
            return True
    
        def is_square_valid(board):
            for i in (0, 3, 6):
                for j in (0, 3, 6):
                    all_element_of_square = []
                    for x in range(i, i + 3):
                        for y in range(j, j + 3):
                            all_element_of_square.append(board[x][y])
                    if not is_valid(all_element_of_square):
                        return False
            return True

        def is_valid(value):
            res = [i for i in value if i != '.']
            return len(res) == len(set(res))

        return is_row_valid(board) and is_col_valid(board) and is_square_valid(board)