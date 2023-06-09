from Game.board import *
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import *


class Actions:

    def __init__(self, screen):
        self._init()
        self.screen = screen
        self.selected = None
        self.valid_moves = {}

    def update(self):
        if self.board is not None:
            self.board.draw(self.screen)
            self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def winner(self):
        return self.board.winner()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLUE
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            output_pos = self._move(row, col)
            if not output_pos:  # handler if move is invalid
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

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

    def check_for_draw(self):
        pieces = self.board.get_all_pieces(self.turn)
        possible_moves = []
        for piece in pieces:
            possible_moves.append(self.board.get_valid_moves(piece))

        if not any(possible_moves):
            self.chk_winner("Draw")
            print(f"The game ended in a draw because {self.turn} has no moves left.")
            pygame.quit()
            exit()

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)

        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove_piece(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                    row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE

    def get_board(self):
        return self.board

    def update_board(self, board):
        self.board = board
        self.change_turn()
