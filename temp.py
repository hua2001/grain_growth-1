for i in range(self.rows):
    for j in range(self.cols):
        if self.board[i][j].id != -1 and self.board[i][j].alive:
            cell_id = self.board[i][j].id
            # Cell on the right
            if j + 1 < self.cols and self.board[i][j + 1].id == -1:
                self.board[i][j + 1].id = cell_id
                self.board[i][j + 1].alive = True
            # Cell on the left
            if j - 1 >= 0 and self.board[i][j - 1].id == -1:
                self.board[i][j - 1].id = cell_id
                self.board[i][j - 1].alive = True
            # Cell on the top
            if i + 1 < self.rows and self.board[i + 1][j].id == -1:
                self.board[i + 1][j].id = cell_id
                self.board[i + 1][j].alive = True
            # Cell on the bottom
            if i - 1 >= 0 and self.board[i - 1][j].id == -1:
                self.board[i - 1][j].id = cell_id
                self.board[i - 1][j].alive = True
