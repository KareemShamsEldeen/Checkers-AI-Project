import pygame
from Game.actions import Actions
from Game.board import *
from Algorithms import minimax, alpha_beta, random_move
import time
import matplotlib.pyplot as plt


def get_pos_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col



def play(p1_algo,p2_algo,p1_dep,p2_dep):
    FPS = 240
    minimax_timesB = []
    minimax_timesR = []
    alpha_beta_timesB = []
    alpha_beta_timesR = []
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")

    clock = pygame.time.Clock()
    run = True
    actions = Actions(WIN)
    board = Board()

    while run:
        clock.tick(FPS)

        if actions.winner() != None:
            print(actions.winner())
            run = False


        if p2_algo == "MiniMax" or p1_algo == "MiniMax":
            if actions.turn == BLUE:
                start_timeBLUE = time.time()
                value, new_board = minimax(actions.get_board(), p2_dep, False, actions)
                minimax_time = time.time() - start_timeBLUE
                minimax_timesB.append(minimax_time)
                total_time=0
                for times in minimax_timesB:
                    total_time = total_time+times
                print("total_timeB= "+str(total_time)+"S --- Depth"+str(p2_dep))
                actions.update_board(new_board)
                pygame.time.delay(300)
            elif actions.turn == RED:
                start_timeRED = time.time()
                value, new_board = minimax(actions.get_board(), p1_dep, True, actions)
                minimax_time = time.time() - start_timeRED
                minimax_timesR.append(minimax_time)
                total_time=0
                for times in minimax_timesR:
                    total_time = total_time+times
                print("total_timeR= "+str(total_time)+"S --- Depth"+str(p1_dep))
                actions.update_board(new_board)
                pygame.time.delay(300)
        elif p1_algo == "Random" or p2_algo == "Random":
            if actions.turn == RED:
                value, new_board = random_move(actions.get_board(),RED,actions)
                actions.update_board(new_board)
            elif actions.turn == BLUE:
                value, new_board = random_move(actions.get_board(), BLUE, actions)
                actions.update_board(new_board)
                pygame.time.delay(300)
        elif p1_algo == "Alpha-Beta Pruning" or p2_algo == "Alpha-Beta Pruning":
            if actions.turn == RED:
                start_timeRED = time.time()
                value, new_board = alpha_beta(actions.get_board(), p1_dep, float('-inf'), float('inf'), True, actions)
                Alpha_Beta_time = time.time() - start_timeRED
                alpha_beta_timesR.append(Alpha_Beta_time)
                total_time = 0
                for times in alpha_beta_timesR:
                    total_time = total_time + times
                print("alpha_beta_total_timeR = " + str(total_time) + "S --- Depth" + str(p1_dep))
                actions.update_board(new_board)
                pygame.time.delay(300)
            elif actions.turn == BLUE:
                start_timeBLUE = time.time()
                value, new_board = alpha_beta(actions.get_board(), p2_dep, float('-inf'), float('inf'), False,actions)
                Alpha_Beta_time = time.time() - start_timeBLUE
                alpha_beta_timesB.append(Alpha_Beta_time)
                total_time = 0
                for times in alpha_beta_timesB:
                    total_time = total_time + times
                print("alpha_beta_total_timeB = " + str(total_time) + "S --- Depth" + str(p1_dep))
                actions.update_board(new_board)
                pygame.time.delay(300)
############################################################################################################################

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if actions.winner() is not None:
                    return str(actions.winner())
                else:
                    return "0"
                run = False

############################################################################################################################
        actions.check_for_draw()
        pygame.time.delay(300)
        actions.update()
