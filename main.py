from random import randint
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import *

from play import play

palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.black)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)

palette_red = QPalette()
palette_red.setColor(QPalette.WindowText, Qt.red)

palette_blue = QPalette()
palette_blue.setColor(QPalette.WindowText, Qt.blue)

############################################################################################################################
import pygame
from Game.actions import Actions
from Game.board import *
from Algorithms import minimax, alpha_beta, random_move


def get_pos_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


############################################################################################################################


class CheckersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.WindowIcon = QIcon('Checker_Icon.png')
        self.setWindowTitle("Checkers Game")
        self.setWindowIcon(self.WindowIcon)
        self.setFixedSize(1200, 600)

        # -----------------------player 1------------------------------------------------------------------
        self.p1_icon = QPixmap('robot.png')
        self.p1_icon.setDevicePixelRatio(2.5)

        self.label_icon_p1 = QLabel()
        self.label_icon_p1.setAlignment(Qt.AlignCenter)
        self.label_icon_p1.setText('Player 1')
        self.label_icon_p1.setPixmap(self.p1_icon)

        self.label_p1 = QLabel()
        self.label_p1.setAlignment(Qt.AlignCenter)
        self.label_p1.setText('Player 1')
        self.label_p1.setPalette(palette_red)
        self.label_p1_font = self.label_p1.font()
        self.label_p1_font.setPointSize(15)
        self.label_p1_font.setBold(True)
        self.label_p1.setFont(self.label_p1_font)

        self.drop_p1_algorithm = QComboBox()
        drop_p1_algorithm_font = self.drop_p1_algorithm.font()
        drop_p1_algorithm_font.setPointSize(9)
        self.drop_p1_algorithm.setFont(drop_p1_algorithm_font)
        self.drop_p1_algorithm.addItems(["Random", "MiniMax", "Alpha-Beta Pruning"])

        self.drop_p1_difficulty = QComboBox()
        drop_p1_difficulty_font = self.drop_p1_difficulty.font()
        drop_p1_difficulty_font.setPointSize(9)
        self.drop_p1_difficulty.setFont(drop_p1_difficulty_font)
        self.drop_p1_difficulty.addItems(["Easy", "Medium", "Hard"])

        # Create a QVBoxLayout instance
        self.layout_p1 = QVBoxLayout()

        # Add widgets to the layout
        self.layout_p1.addWidget(self.label_icon_p1, 1)
        self.layout_p1.addWidget(self.label_p1, 1)
        self.layout_p1.addWidget(self.drop_p1_algorithm, 1)
        self.layout_p1.addWidget(self.drop_p1_difficulty, 1)

        # -----------------------player 1------------------------------------------------------------------

        # -----------------------player 2------------------------------------------------------------------
        self.p2_icon = QPixmap('robot.png')
        self.p2_icon.setDevicePixelRatio(2.5)

        self.label_icon_p2 = QLabel()
        self.label_icon_p2.setAlignment(Qt.AlignCenter)
        self.label_icon_p2.setText('Player 2')
        self.label_icon_p2.setPixmap(self.p2_icon)

        self.label_p2 = QLabel()
        self.label_p2.setAlignment(Qt.AlignCenter)
        self.label_p2.setText('Player 2')
        self.label_p2.setPalette(palette_blue)
        self.label_p2_font = self.label_p2.font()
        self.label_p2_font.setPointSize(15)
        self.label_p2_font.setBold(True)
        self.label_p2.setFont(self.label_p2_font)

        self.drop_p2_algorithm = QComboBox()
        drop_p2_algorithm_font = self.drop_p2_algorithm.font()
        drop_p2_algorithm_font.setPointSize(9)
        self.drop_p2_algorithm.setFont(drop_p2_algorithm_font)
        self.drop_p2_algorithm.addItems(["Random", "Human", "MiniMax", "Alpha-Beta Pruning"])

        self.drop_p2_difficulty = QComboBox()
        drop_p2_difficulty_font = self.drop_p2_difficulty.font()
        drop_p2_difficulty_font.setPointSize(9)
        self.drop_p2_difficulty.setFont(drop_p2_difficulty_font)
        self.drop_p2_difficulty.addItems(["Easy", "Medium", "Hard", "None"])

        # Create a QVBoxLayout instance
        self.layout_p2 = QVBoxLayout()

        # Add widgets to the layout
        self.layout_p2.addWidget(self.label_icon_p2, 1)
        self.layout_p2.addWidget(self.label_p2, 1)
        self.layout_p2.addWidget(self.drop_p2_algorithm, 1)
        self.layout_p2.addWidget(self.drop_p2_difficulty, 1)
        # -----------------------player 2------------------------------------------------------------------

        # -----------------------Layout Format-------------------------------------------------------------
        layout_p1_p2 = QHBoxLayout()
        layout_p1_p2.addLayout(self.layout_p1)
        layout_p1_p2.addLayout(self.layout_p2)

        label_title = QLabel()
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setText('Checkers')
        label_title_font = label_title.font()
        label_title_font.setPointSize(20)
        label_title_font.setBold(True)
        label_title.setFont(label_title_font)

        button_play = QPushButton()
        button_play.setText("Play")
        button_play_font = button_play.font()
        button_play_font.setPointSize(14)
        button_play.setFont(button_play_font)
        button_play.setFixedHeight(80)

        layout_Main = QVBoxLayout()
        layout_Main.addWidget(label_title)
        layout_Main.addLayout(layout_p1_p2)
        layout_Main.addWidget(button_play, 1)

        # -----------------------Layout Format-------------------------------------------------------------
        # Set the layout on the application's window
        self.setLayout(layout_Main)

        button_play.clicked.connect(self.on_button_clicked)

        self.warning = QMessageBox()
        self.warning.setWindowTitle("Warning!!")
        self.warning.setText("Setting the 2 players to be AI will probably lead to a draw or infinite playing")
        self.warning.setIcon(QMessageBox.Warning)

        self.error = QMessageBox()
        self.error.setWindowTitle("Error!!")
        self.error.setText("Difficulty in Human must be set to None")
        self.error.setIcon(QMessageBox.Critical)

        self.error2 = QMessageBox()
        self.error2.setWindowTitle("Error!!")
        self.error2.setText("Difficulty in AI can not be set to None")
        self.error2.setIcon(QMessageBox.Critical)

        # -----------------------Layout Format-------------------------------------------------------------

    def on_button_clicked(self):
        p1_algorithm = str(self.drop_p1_algorithm.currentText())
        p1_difficulty = str(self.drop_p1_difficulty.currentText())

        p2_algorithm = str(self.drop_p2_algorithm.currentText())
        p2_difficulty = str(self.drop_p2_difficulty.currentText())

        if ((p2_algorithm == 'Human' and p2_difficulty != 'None')):
            error_box = self.error.exec_()
        else:
            if (p2_algorithm in ("Random", "MiniMax", "Alpha-Beta Pruning") and p2_difficulty == 'None'):
                error2_box = self.error2.exec_()
            else:
                if (p1_algorithm in ("Random", "MiniMax", "Alpha-Beta Pruning") and p2_algorithm in (
                        "Random", "MiniMax", "Alpha-Beta Pruning")):
                    warning_box = self.warning.exec_()

            if p2_algorithm == 'Human':
                p2_depth = 0

            if (p1_difficulty == "Easy"):
                p1_depth = randint(1, 2)
            elif (p1_difficulty == "Medium"):
                p1_depth = randint(3, 4)
            elif (p1_difficulty == "Hard"):
                p1_depth = randint(4, 5)

            if (p2_difficulty == "Easy"):
                p2_depth = randint(1, 2)
            elif (p2_difficulty == "Medium"):
                p2_depth = randint(3, 4)
            elif (p2_difficulty == "Hard"):
                p2_depth = randint(4, 5)

            print("Player 1\nAlgorithm: ", p1_algorithm, " - Difficulty: ", p1_difficulty, " - Depth: ", p1_depth,
                  "\nPlayer 2\nAlgorithm: ", p2_algorithm, " - Difficulty: ", p2_difficulty, " - Depth: ", p2_depth)

            # self.close()
            ############################################################################################################################
            if (p2_algorithm != 'Human'):
                win = play(p1_algorithm, p2_algorithm, p1_depth, p2_depth)
            else:
                FPS = 240
                WIN = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Checkers")
                clock = pygame.time.Clock()
                run = True
                actions = Actions(WIN)
                board = Board()

                while run:
                    clock.tick(FPS)

                    if p1_algorithm == "MiniMax":
                        if actions.turn == RED:
                            value, new_board = minimax(actions.get_board(), p1_depth, True, actions)
                            actions.update_board(new_board)
                            pygame.time.delay(500)
                    elif p1_algorithm == "Random":
                        if actions.turn == RED:
                            value, new_board = random_move(actions.get_board(), RED, actions)
                            actions.update_board(new_board)
                            pygame.time.delay(500)
                    elif p1_algorithm == "Alpha-Beta Pruning":
                        if actions.turn == RED:
                            value, new_board = alpha_beta(actions.get_board(), p1_depth, float('-inf'), float('inf'), True,
                                                          actions)
                            actions.update_board(new_board)
                            pygame.time.delay(500)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            row, col = get_pos_from_mouse(pos)
                            if actions.turn:
                                actions.select(row, col)

                    actions.check_for_draw()
                    actions.update()


############################################################################################################################


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setPalette(palette)
    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")

    window = CheckersWindow()
    window.show()
    sys.exit(app.exec_())
