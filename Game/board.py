from Game.piece import Piece
import pygame
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import *

WIDTH, HEIGHT = 800, 800
NUM_ROWS, NUM_COLS = 8, 8
SQUARE_SIZE = WIDTH // NUM_COLS

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CROWN = pygame.transform.scale(pygame.image.load('crown.png'), (44, 25))





class Board:

    def __init__(self):
        self.board = []
        self.blue_left = self.red_left = 12
        self.blue_kings = self.red_kings = 0
        self.create_board()
        self.run = True

    def chk_winner(self, winner):
        if (winner == "Red"):
            self.WindowIcon = QIcon('Checker_Icon.png')
            self.winner_red = QMessageBox()
            self.winner_red.setWindowTitle("WINNER")
            self.winner_red.setText("Winner is RED")
            self.winner_red.setIcon(QMessageBox.Information)
            self.winner_red.setWindowIcon(self.WindowIcon)
            self.winner_red.exec()

        elif (winner == "Blue"):
            self.WindowIcon = QIcon('Checker_Icon.png')
            self.winner_blue = QMessageBox()
            self.winner_blue.setWindowTitle("WINNER")
            self.winner_blue.setText("Winner is blue")
            self.winner_blue.setWindowIcon(self.WindowIcon)
            self.winner_blue.setIcon(QMessageBox.Information)
            self.winner_blue.exec()

        elif (winner == "Draw"):
            self.WindowIcon = QIcon('Checker_Icon.png')
            self.winner_draw = QMessageBox()
            self.winner_draw.setWindowTitle("WINNER")
            self.winner_draw.setText("NO WINNER!!\nIt's a Draw")
            self.winner_draw.setWindowIcon(self.WindowIcon)
            self.winner_draw.setIcon(QMessageBox.Information)
            self.winner_draw.exec()

    def draw_grid(self, screen):
        screen.fill(BLACK)
        for row in range(HEIGHT):
            for col in range(row % 2, NUM_ROWS, 2):
                pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == 0 or row == NUM_ROWS - 1:
            if piece.color == RED and not piece.king:
                self.red_kings += 1
                piece.make_king()
            if piece.color == BLUE and not piece.king:
                self.blue_kings += 1
                piece.make_king()

    def evaluate(self):
        score = 0
        score += 4 * (self.red_kings - self.blue_kings)
        score += len(self.get_all_pieces(RED)) - len(self.get_all_pieces(BLUE))
        return score

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)

        return pieces

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(NUM_ROWS):
            self.board.append([])
            for col in range(NUM_COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLUE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, screen):
        self.draw_grid(screen)
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen)

    def remove_piece(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLUE:
                    self.blue_left -= 1
                else:
                    self.red_left -= 1

                print(self.blue_left, self.red_left)
                if self.winner() is not None:
                    print("The winner is: " + str(self.winner()))
                    self.chk_winner(str(self.winner()))
                    pygame.quit()
                    exit()

    def winner(self):
        if self.blue_left == 0:
            return "Red"
        elif self.red_left == 0:
            return "Blue"
        else:
            return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if  piece.color == BLUE:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == RED :
            moves.update(self._traverse_left(row + 1, min(row + 3, NUM_ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, NUM_ROWS), 1, piece.color, right))

        if piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
            moves.update(self._traverse_left(row + 1, min(row + 3,  NUM_ROWS - 1), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3,  NUM_ROWS - 1), 1, piece.color, right))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            potential_move = self.board[r][left]
            if potential_move == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last  # If checks are passed, add the move to dict of valid moves

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, NUM_ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break

            elif potential_move.color == color:
                break
            else:
                last = [potential_move]  # if after one jump we can still jump, adjust the last list
            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= NUM_COLS:
                break

            potential_move = self.board[r][right]
            if potential_move == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last  # If checks are passed, add the move to dict of valid moves

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, NUM_ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break

            elif potential_move.color == color:
                break
            else:
                last = [potential_move]  # if after one jump we can still jump, adjust the last list
            right += 1

        return moves