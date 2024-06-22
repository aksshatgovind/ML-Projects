class DotsAndBoxes:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.horizontal_lines = [[False] * (cols - 1) for _ in range(rows)]
        self.vertical_lines = [[False] * cols for _ in range(rows - 1)]
        self.boxes = [[None] * (cols - 1) for _ in range(rows - 1)]
        self.current_player = 1 
        self.num_players = 2
        self.scores = [0] * self.num_players

    def print_board(self):
        print("Current Board:")
        print("  " + "   ".join(str(i) for i in range(self.cols)))
        for r in range(self.rows):
            if r > 0:
                print("  " + "+".join("---" for _ in range(self.cols)))
            row = []
            for c in range(self.cols):
                if c > 0 and r < self.rows - 1:
                    if self.vertical_lines[r][c - 1]:
                        row.append("|")
                    else:
                        row.append(" ")
                row.append(" ")
                if r < self.rows - 1 and c < self.cols - 1:
                    if self.boxes[r][c] is None:
                        row.append("   ")
                    else:
                        row.append(f" {self.boxes[r][c]} ")
            print(f"{r} " + "".join(row))


    def is_valid_line(self, line_type, row, col):
        if line_type == 'h':
            return 0 <= row < self.rows and 0 <= col < self.cols - 1 and not self.horizontal_lines[row][col]
        elif line_type == 'v':
            return 0 <= row < self.rows - 1 and 0 <= col < self.cols and not self.vertical_lines[row][col]
        else:
            return False

    def draw_line(self, line_type, row, col):
        if line_type == 'h':
            self.horizontal_lines[row][col] = True
        elif line_type == 'v':
            self.vertical_lines[row][col] = True
        else:
            return False

        box_completed = False
        if line_type == 'h' and row > 0:
            if self.horizontal_lines[row - 1][col] and self.vertical_lines[row - 1][col] and self.vertical_lines[row - 1][col + 1]:
                self.boxes[row - 1][col] = self.current_player
                self.scores[self.current_player - 1] += 1
                box_completed = True
        elif line_type == 'v' and col > 0:
            if self.vertical_lines[row][col - 1] and self.horizontal_lines[row][col - 1] and self.horizontal_lines[row + 1][col - 1]:
                self.boxes[row][col - 1] = self.current_player
                self.scores[self.current_player - 1] += 1
                box_completed = True


        if not box_completed:
            self.current_player = 3 - self.current_player  

        return True

    def is_game_over(self):
        total_lines = (self.rows * (self.cols - 1) + (self.rows - 1) * self.cols)
        return all(self.horizontal_lines[i][j] for i in range(self.rows) for j in range(self.cols - 1)) and \
               all(self.vertical_lines[i][j] for i in range(self.rows - 1) for j in range(self.cols))

    def get_winner(self):
        if not self.is_game_over():
            return None
        max_score = max(self.scores)
        if self.scores.count(max_score) == 1:
            return self.scores.index(max_score) + 1
        else:
            return 0  

    def play(self):
        while not self.is_game_over():
            self.print_board()
            print(f"Player {self.current_player}'s turn")
            line_type = input("Enter line type ('h' for horizontal, 'v' for vertical): ").strip().lower()
            if line_type not in ['h', 'v']:
                print("Invalid input. Please enter 'h' or 'v'.")
                continue
            try:
                row = int(input("Enter row number: "))
                col = int(input("Enter column number: "))
                if not self.is_valid_line(line_type, row, col):
                    print("Invalid move. Try again.")
                    continue
                self.draw_line(line_type, row, col)
            except ValueError:
                print("Invalid input. Please enter valid row and column numbers.")
                continue

        self.print_board()
        winner = self.get_winner()
        if winner == 0:
            print("It's a draw!")
        else:
            print(f"Player {winner} wins!")


# if __name__ == "__main__":
#     rows = int(input("Enter number of rows: "))
#     cols = int(input("Enter number of columns: "))
#     game = DotsAndBoxes(rows, cols)
#     game.play()
