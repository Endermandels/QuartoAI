from __future__ import annotations
from global_defs.state import State, Winner, Action, PiecePlace, PieceGive
from global_defs.stats import Stats
from collections import defaultdict
from model import Model
from view import View
from random import choice, random
import math

"""
- **Goal:** learn Q(s,a), the expected total future reward of taking action a in state s and then playing well afterward.
- **Update rule:** Q(s,a) ← Q(s,a) + α · [r + γ · max Q(s',a') − Q(s,a)]. You move your estimate toward a target built from the reward plus your best estimate of the next state.
- **Bootstrapping:** the target uses your own current estimates, so you learn from guesses of guesses. Values propagate backward from rewards (e.g., a win) over many episodes.
- **Off-policy:** it learns the value of the greedy policy (the max) even while you act with an exploratory one.
- **Exploration vs. exploitation:** epsilon-greedy balances trying new actions against using what you know. Decay ε over training.
- **Hyperparameters:** α (learning rate), γ (discount), ε (exploration rate).
- **Terminal states:** no future, so the target is just r.
- **Sparse rewards:** with only win/loss at the end, learning is slow early on because most updates have nothing to propagate yet.
- **Tabular limits:** a table only works when the state space is small enough to visit repeatedly. This is why DQN replaces the table with a neural network that generalizes.
- **Convergence:** it provably converges to the optimal Q-values if every state-action pair is visited enough and α decays appropriately. In practice you use a fixed small α.
- **Opponent matters:** in a game, the opponent is part of the environment, so what the agent learns is tuned to the opponent it trained against.
"""

class Agent:
    def __init__(self, is_p1: bool, stats: Stats):
        self.is_p1: bool = is_p1
        self.stats: Stats = stats

    def query_give_piece(self, mdl: Model) -> Action | None:
        return None

    def query_place_piece(self, mdl: Model) -> Action | None:
        return None
    
    def update_stats(self, mdl: Model) -> None:
        """ Called at the end of the game """
        if (mdl.winner == Winner.PLAYER_1 and self.is_p1) or (mdl.winner == Winner.PLAYER_2 and not self.is_p1):
            self.stats.games_won += 1
        elif (mdl.winner == Winner.PLAYER_2 and self.is_p1) or (mdl.winner == Winner.PLAYER_1 and not self.is_p1):
            self.stats.games_lost += 1
        else:
            self.stats.games_tied += 1
            
        self.stats.games_played += 1

class HumanAgent(Agent):
    def __init__(self, is_p1: bool, stats: Stats, vw: View):
        super().__init__(is_p1, stats)
        self.vw: View = vw
    
    def query_give_piece(self, mdl: Model) -> Action | None:
        return self.vw.query_give_piece(mdl)

    def query_place_piece(self, mdl: Model) -> Action | None:
        return self.vw.query_place_piece(mdl)

class RandomAgent(Agent):
    def __init__(self, is_p1: bool, stats: Stats):
        super().__init__(is_p1, stats)
    
    def query_give_piece(self, mdl: Model) -> Action | None:
        return Action(piece=choice(mdl.legal_give_actions(mdl.state)))

    def query_place_piece(self, mdl: Model) -> Action | None:
        return Action(board_coords=choice(mdl.legal_place_actions(mdl.state)))

class HeuristicAgent(Agent):
    def __init__(self, is_p1: bool, stats: Stats):
        super().__init__(is_p1, stats)
    
    def query_give_piece(self, mdl: Model) -> Action | None:
        # Never give a winning piece, if possible
        
        # For each piece left,
        #  check if any spot on the board having that piece will result in a win for the opponent
        #  if there are any spots, don't give that piece
        # If after searching no pieces are left that won't result in defeat, choose a random piece
        
        legal_pieces: list[int] = mdl.legal_give_actions(mdl.state)
        good_pieces: list[int] = []
        
        for piece in legal_pieces:
            bad_piece: bool = False
            piece_place: int = PiecePlace[PieceGive(piece).name].value
            
            for r in range(len(mdl.state.board)):
                for c in range(len(mdl.state.board[r])):
                    if mdl.check_winner(mdl.state, r, c, piece_place) == (Winner.PLAYER_2 if self.is_p1 else Winner.PLAYER_1):
                        bad_piece = True
                        break
            
            if not bad_piece:
                good_pieces.append(piece)
            
        return Action(piece=choice(good_pieces if len(good_pieces) > 0 else legal_pieces)) 

    def query_place_piece(self, mdl: Model) -> Action | None:
        # Always place piece in a winning spot, if possible
        
        # For each place,
        #  check if placing the piece results in a win
        #  if there are any spots, place it there
        # Otherwise, place it randomly
        
        legal_spaces: list[tuple[int, int]] = mdl.legal_place_actions(mdl.state)
        winning_space: tuple[int, int] | None = None
        piece_place: int = PiecePlace[PieceGive(mdl.state.given_piece).name].value
        
        for space in legal_spaces:
            if mdl.check_winner(mdl.state, space[0], space[1], piece_place) == (Winner.PLAYER_1 if self.is_p1 else Winner.PLAYER_2):
                winning_space = space
                break
        
        return Action(board_coords=(winning_space if winning_space != None else choice(legal_spaces)))
    
class QLearnAgent(Agent):
    # store q values: {(state, action): -> q}
    # store epsilon (exploration rate)
    # store alpha (learning rate)
    # store gamma (discount)
    
    # update q values: Q(s, a) = Q(s, a) + alpha * (R(s) + gamma * max(Q(s', a')) - Q(s, a))
    # where Q(s', a') is the q value of the next state given the next action
    # the update rule uses back propogation, so the next state is actually the current state
    
    def __init__(self, is_p1, stats, epsilon: int = 0.7, alpha: int = 0.1, gamma: int = 1.0, epsilon_decay_rate: float = 0):
        super().__init__(is_p1, stats)
        
        # Exploration rate of making random moves
        self.epsilon: int = epsilon
        self.epsilon_decay_rate: float = epsilon_decay_rate

        # Learning rate of q values
        self.alpha: int = alpha
        
        # Discount rate of future rewards
        self.gamma: int = gamma
        
        # Usefulness of each action at a given state
        self.q_table: dict[State, Action] = defaultdict(float) # default q of 0; populate q as agent encounters state, action pairs
        
        # Remember previous move for updating
        self.prev_move: tuple[State, Action] = (None, None)
        
        # Debugging stats
        self.hit_rate = 0
        self.lookups = 0
    
    def update_stats(self, mdl: Model) -> None:
        """ Called at the end of the game """
        super().update_stats(mdl)
        self._learn(self.prev_move[0], self.prev_move[1], mdl.final_reward(self.is_p1), 0.0)
        self.prev_move = (None, None)
        self._decay_epsilon()
    
    def _decay_epsilon(self) -> float:
        if self.epsilon > 0.05:
            self.epsilon = max(self.epsilon - self.epsilon_decay_rate, 0.05)
    
    def _learn(self, state: State, action: Action, r: float, max_q: float) -> None:
        future_r: float = self.gamma * max_q
        self.q_table[state, action] += self.alpha * (r + future_r - self.q_table[state, action])
    
    def _get_best_action_q(self, mdl: Model, legal_actions: list[Action]) -> tuple[float, Action]:
        best_action: Action = legal_actions[0]
        best_q: float = -9999999
                
        for a in legal_actions:
            self.lookups += 1
            if (mdl.state, a) in self.q_table:
                self.hit_rate += 1
            q = self.q_table[mdl.state, a]
            if q > best_q:
                best_q = q
                best_action = a
        
        return best_q, best_action

    def query_give_piece(self, mdl: Model) -> Action | None:
        legal_actions: list[Action] = [Action(piece=p) for p in mdl.legal_give_actions(mdl.state)]
        q, best_action = self._get_best_action_q(mdl, legal_actions)
        action: Action = choice(legal_actions) if random() <= self.epsilon else best_action
        
        self._learn(self.prev_move[0], self.prev_move[1], 0, q)
        self.prev_move = (mdl.state, action)

        return action
    
    def query_place_piece(self, mdl: Model) -> Action | None:
        legal_actions: list[Action] = [Action(board_coords=s) for s in mdl.legal_place_actions(mdl.state)]
        q, best_action = self._get_best_action_q(mdl, legal_actions)
        action: Action = choice(legal_actions) if random() <= self.epsilon else best_action
                
        self._learn(self.prev_move[0], self.prev_move[1], 0, q)
        self.prev_move = (mdl.state, action)

        return action