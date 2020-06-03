from copy import deepcopy
import random

ORIGINAL_DEPTH = 20
def play(state, move, player):
    #print(move)
    state[move[0]][move[1]] = 0
    playerscore = 0
    #print(move)
    ##Check for if move is horizontal
    if move[0] == 0:
        ##if the position - n of the move is above 0, then we can check the upper box.
        if ((move[1] - 5) > 0):
            if (state[0][move[1]-6] != 99) and (state[1][move[1]-6] !=99) and (state[1][move[1]-5] != 99):
                ##If upper left, uper right and upper straight are not empy, it means that I filled a spot with this move
                playerscore = (playerscore + 1) if player == 1 else (playerscore-1)
        #if the position +n of the move is below len(state), then we can check the lower box
        if ((move[1] + 5) < 28):
            if (state[0][move[1]+6] != 99) and (state[1][move[1]+6] !=99) and (state[1][move[1]+5] != 99):
                ##If upper left, uper right and upper straight are not empy, it means that I filled a spot with this move
                playerscore = (playerscore + 1) if player == 1 else (playerscore-1)
        state[move[0]][move[1]] = playerscore
        #print(playerscore)
        return state, playerscore
    ##Check for if move is vertical
    elif move[0] == 1:
        if ((move[1] - 5) > 0):
            if (state[1][move[1]-6] != 99) and (state[0][move[1]-6] !=99) and (state[0][move[1]-5] != 99):
                ##If left up, left down and left straight are not empy, it means that I filled a spot with this move
                playerscore = (playerscore + 1) if player == 1 else (playerscore-1)
        #if the position +n of the move is below len(state), then we can check the left box
        if ((move[1] + 5) < 28):
            if (state[1][move[1]+6] != 99) and (state[0][move[1]+6] !=99) and (state[0][move[1]+5] != 99):
                ##If right up, right down and right straight are not empy, it means that I filled a spot with this move
                playerscore = (playerscore + 1) if player == 1 else (playerscore-1)
        state[move[0]][move[1]] = playerscore
        #print(playerscore)
        #print(state)
        return state, playerscore


# # print(board)
# # move = (0,0)

def checkOpens(board):
    i = 0
    openspots = []
    for spot in board[0]:
        if spot == 99:
            openspots.append((0, i))
        i=i+1
    i = 0
    for spot in board[1]:
        if spot == 99:
            openspots.append((1, i))
        i=i+1
    return openspots


def minimax(state, possibleplays, depth, max_state, myTurnID, alpha, beta, heuristic_list):
    #print(depth)

    ##Inicializamos los costos de la corrida.
    if max_state is True:
        bestMove = (-1000, None)
    else:
        bestMove = (1000, None)

    if depth == 0 or len(possibleplays) == 0:
        ##Obtener nuestro costo si llegamos al tope de nuestra profundidad o si ya no quedan mas movimientos por hacer.
        cost = eval(state, myTurnID, depth, heuristic_list)
        return (cost, None)

    for i in range(0, len(possibleplays)):
        #Quitamos el movimiento que haremos, copiamos la lista de movimientos posibles posterior a este movimiento, y regresamos el movimiento a la lista original;
        # Si no regresamos el movimiento a la lista original, no tenemos una forma real de compararlos.

        #hacemos deepcopy del possible plays y el state para poder hacer las pruebas sin afectar el estado actual.
        move = possibleplays.pop()
        pplayscopy = deepcopy(possibleplays)
        possibleplays.insert(0,move)

        ## Copiamos el board y realizamos nuestro movimiento para determinar el siguiente estado. 
        board_copy = deepcopy(state)
        board_copy, movescore = play(board_copy, move, myTurnID)

        # Evaluamos nuestro punteo; si el punteo es mayor a la condicion beta, o menor a la condicion alpha, hacemos la 'poda' al arbol de lo contrario, 
        # asignamos un nuevo valor a alpha y a beta. Por default, nuestro alpha y beta son numeros muy altos.
        cost = eval(board_copy, myTurnID, depth, heuristic_list, movescore)
        if max_state:
            if cost >= beta:
                return (cost, move)
            else:
                alpha = max(alpha, cost)
        else:
            if cost <= alpha:
                return (cost, move)
            else:
                beta = min(beta, cost)
        ##Si en los pasos anteriores obtuvimos un H mejor al alpha/beta (Dependiendo si era min o max), ese movimiento es el mejor para la rama del arbol en la que estamos, 
        # por lo que ya no es necesario seguir. De lo contrario, seguimos realizando pruebas para rama.
        next_scenario = minimax(board_copy, pplayscopy, depth - 1, not max_state, myTurnID, alpha, beta, heuristic_list)

        # Si el mejor valor obtenido para la rama siguiente es mejor que el valor obtenido que para la rama en la que estamos, enviamos como mejor rama a la siguiente. 
        # De lo contrario nuestro mejor movimiento sigue siendo el mismo que se calculo en el paso anterior.
        if max_state is True:
            # Si este paso es para max, el punteo debe ser mayor para ser mejor
            if next_scenario[0] > bestMove[0]:
                bestMove = (next_scenario[0], move)
        else:
            # Si este paso es para min, el punteo debe ser menor para ser mejor
            if next_scenario[0] < bestMove[0]:
                bestMove = (next_scenario[0], move)
    return bestMove



def difference_heuristic(mescore, otherscore):
    if max(mescore, otherscore) == 0:
        mescore, otherscore = 1, 1
    difference_multiplier = float((max(mescore, otherscore)-min(mescore,otherscore))/max(mescore,otherscore))
    return difference_multiplier

def efficiency_heuristic(mescore, current_depth):
    move_efficiency_multiplier = float(current_depth/ORIGINAL_DEPTH)
    #print(move_efficiency_multiplier)
    return (mescore * move_efficiency_multiplier)

def eval(state, myTurnID, current_depth, heuristic_list=[], movescore=0):
    #Funcion simple de evaluacion. 

    # Las heuristicas se pasan como una lista, en el orden en el que se quieren aplicar.
    meScore, otherScore = getPlayerScores(state, myTurnID)
    if len(heuristic_list) > 0 :
        for heuristic in heuristic_list:
            if heuristic == 'difference_heuristic':
                difference_multiplier = difference_heuristic(meScore, otherScore)
                if meScore > otherScore:
                    meScore = meScore+(meScore*difference_multiplier)
                elif otherScore > meScore:
                    otherScore = otherScore+(otherScore*difference_multiplier)
                elif meScore == otherScore:
                    pass
            if heuristic == 'efficiency_heuristic':
                meScore = efficiency_heuristic(meScore, current_depth)
    if movescore > 0:
        meScore = meScore  * movescore
    elif movescore < 0:
        otherScore = otherScore * movescore
        
    h = meScore + otherScore
    #print(meScore, otherScore, h)
    return h


def getPlayerScores(state, myTurnID):
    mescore = 0
    otherscore = 0
    for dim in state:
        for i in dim:
            if myTurnID == 1:
                if i == 99:
                    pass
                if (i == 1) or (i == 2):
                    mescore = mescore + i
                if (i == -1) or (i == -2):
                    otherscore = otherscore + i
            else:
                if i == 99:
                    pass
                if (i == 1) or (i == 2):
                    otherscore = otherscore - i
                if (i == -1) or (i == -2):
                    mescore = mescore - i
    return mescore, otherscore


# a = 0
# scores = []
# while a < 5:
#     board = [[99 for x in range(29)] for x in range(2)]
#     a = a+1
#     turns = 0
#     while turns < 58:
#         turns = turns + 1
#         #print("Turn", turns)
#         if (turns %2 == 0):
#             if(turns < 4):
#                 move = random.choice(checkOpens(board))
#             else:
#                 #move = minimax(board, checkOpens(board), 20, True, 2, -1000, 1000,['efficiency_heuristic','difference_heuristic'])[1]
#                 #print(move)
#                 move = random.choice(checkOpens(board))
#                 print(move)
#         else:
#             if(turns < 4):
#                move = random.choice(checkOpens(board))
#             else:
#                 #move = minimax(board, checkOpens(board), 20, True, 1, -1000, 1000,[])[1]
#                 #move = minimax(board, checkOpens(board), 20, True, 1, -1000, 1000,['difference_heuristic'])[1]
#                 move = minimax(board, checkOpens(board), 20, True, 1, -1000, 1000,['efficiency_heuristic'])[1]
#                 #move = minimax(board, checkOpens(board), 20, True, 1, -1000, 1000,['difference_heuristic','efficiency_heuristic'])[1]
#                 #move = minimax(board, checkOpens(board), 20, True, 1, -1000, 1000,['efficiency_heuristic','difference_heuristic'])[1]
                
#                 print(move)
#         board = play(board, move, (1 if (turns % 2 == 0) else 2))[0]
#         #print(board)

#     print(board)
#     randomscore, aiscore = getPlayerScores(board, 1)
#     scores.append((randomscore, aiscore))
# print(scores)