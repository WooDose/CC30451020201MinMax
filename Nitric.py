import socketio
import random 

from minimax import minimax, checkOpens

sio = socketio.Client()

TURN_COUNTER = 0

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)

@sio.on('connect')
def signin():
    sio.emit('signin', {'user_name': 'Diego Alvarez', 'tournament_id': 5000, 'user_role': 'player'})

@sio.on('ok_signin')
def print_oksignin():
    print('Signin Successful!')

@sio.on('finish')
def player_ready(data):
   game_id = data['game_id']
   playerTurnID = data['player_turn_id']
   board = data['board']
   sio.emit('player_ready',{
       'tournament_id': 5000,
       'player_turn_id' : playerTurnID,
       'game_id':game_id
   })
   print("I finished a game and I'm ready for the next.")

@sio.on('ready')
def get_ready_state(data):
    board = data['board']
    move = minimax(board, checkOpens(board), 20, True, data['player_turn_id'], -1000, 1000, ['efficiency_heuristic'])[1]
    sio.emit('play', {
        'tournament_id': 5000,
        'player_turn_id': data['player_turn_id'],
        'game_id': data['game_id'],
        'movement': move
    })


@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://3.12.129.126:5000/')
#sio.connect('http://localhost:4000/')
sio.wait()
