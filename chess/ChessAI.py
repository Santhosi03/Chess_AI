"""
Handling the AI moves.
"""
import random
import copy

counte = 0
piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4
s_map = {}

class state_D():

    def __init__(self, state, move):
        # self.is_over=check_gameover_S(state)
        self.state = state
        self.children = []
        self.minimax_val= None
        self.best_move_node = None
        self.prev_move = move
        self.cur_move = None
        # self.is_max= is_max

    def add_children(self, children):
        self.children= children


#dont think any changes need to be made
def build_tree_D(root,depth):
    # n = len(root.state)
    q = [root]
    cur_depth = 0
    keep_going = True
    # is_max = root.state.white_to_move
    while(cur_depth < depth and keep_going):
        size=len(q)
        # print("Size of queue: ", size,"    Is p1:", is_max,"    Current Depth: ",  cur_depth)
        keep_going = False
        for i in range(size):
            node=q[0]
            q.pop(0)
            # print("start " , node.state)
            if node.state.checkmate==False and node.state.stalemate==False:
                keep_going = True
                children = next_states_S(node.state)
                node.add_children(children)
                for child in children:
                    # print(child.state, child.is_max)
                    q.append(child)
        cur_depth+=1
        # is_max = not is_max
    return root

def next_states_S(pres_state):
    next_states=[]
    valid_moves = pres_state.getValidMoves()
    # children_player = not is_max
    for move in valid_moves:
                dup = copy.deepcopy(pres_state)
                dup.makeMove(move)
                if dup in s_map:
                    global counte
                    counte+=1
                    # print(1)
                    next_states.append(s_map[dup])
                else:
                    child=  state_D(dup, move)
                    s_map[dup] = child
                    next_states.append(child)
                # print(" after: ", pres_state)
                # dup.undoMove()
    # for s in next_states:
    #     print(s.state.board)
    return next_states

def findBestMove(game_state, valid_moves, return_queue):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    # if(game_state in s_map):
    #     node = s_map[game_state]
    #     return_queue.put(node.cur_move)
    # else:
    #     node = state_D(game_state, None)
    #     s_map[game_state] = node
    #     node = build_tree_D(node,DEPTH)
    #     K_depth_S(node, 0,DEPTH)
    #     print(counte, " nodes were repeated")
    #     print(len(s_map))
    #     return_queue.put(node.cur_move)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1)
    return_queue.put(next_move)


#K-depth approximation to the minimax approach using a static evaluation function
def K_depth_S(root,depth,k):
    if len(root.children)==0: 
        # root.minimax = root.is_over ##We have changed the meaning of minimax, now it represents the path
        # print(root.state, root.is_over)
        # if(root.is_over==-1):
        #     print(root.is_over)
        root.minimax_val = scoreBoard(root.state)
        return root
    if depth==k:
        root.minimax_val = scoreBoard(root.state)
        return root
    mini=root.children[0]
    maxi=root.children[0]
    for child in root.children:
        v = K_depth_S(child,depth+1, k)
        # print(type(v))
        if(mini.minimax_val > v.minimax_val):
            mini = v
        if(maxi.minimax_val < v.minimax_val):
            maxi = v
    if root.state.white_to_move:
        root.best_move_node=maxi
        root.cur_move = maxi.prev_move
        root.minimax_val = maxi.minimax_val
        # print(root.minimax_val, " white")
        return root
    root.best_move_node=mini
    root.cur_move = mini.prev_move
    root.minimax_val = mini.minimax_val
    # print(root.minimax_val, " black")
    return root
def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)
    # move ordering - implement later //TODO
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

    return score


def findRandomMove(valid_moves):
    """
    Picks and returns a random valid move.
    """
    return random.choice(valid_moves)
