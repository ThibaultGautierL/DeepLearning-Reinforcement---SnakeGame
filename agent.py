import torch
import random
import numpy as np
from collections import deque
from snake import SnakeGameAI, Direction, Point

Max_Memory = 100_000
Batch_Size = 1000
Learning_Rate = 0.001

class Agent: 

    #Init
    def __init__(self):
        self.number_games = 0
        self.randomness = 0
        self.discount_rate = 0
        self.memory = deque(maxlen=Max_Memory) #SI on dépasse la mémoire, on supprime les données du début. (Garde les + récentes)

    #Connaitre l'état du jeu
    def get_state(self, game):

        head_snake= game.snake[0]
        #Les points autour de la tete dans toutes les directions
        point_left = Point(head_snake.x -20, head_snake.y)
        point_right = Point(head_snake.x +20, head_snake.y)
        point_under = Point(head_snake.x, head_snake.y - 20)
        point_over = Point(head_snake.x, head_snake.y + 20)

        

        pass

    #Rappel des paramètres
    def remember(self, state, action, reward, next_state, gameover):
        pass


    def train_long_memory(self):
        pass
    
    def train_short_memory(self, state, action, reward, next_state, gameover):
        pass

    def get_action(self):
        pass

#Training fonction
def train():
    list_scores = []
    list_moyen_score = []
    total_score = 0
    best_score = 0
    agent = Agent()
    game = SnakeGameAI()

    #On veut boucler au max
    print(f"dans la boucle de jeu" + {agent.number_games})
    while True:
        #On récupère l'ancien état
        last_state = agent.get_state(game)
        #On récupère l'ancienne action en fonction de l'ancien état
        last_move = agent.get_action(last_state)
        #On donne la valeur à nos 3 variables en fonction de cette dernière action (Si on a gagné des points, si on a perdu, quel est notre score)
        reward, game_over, score = game.play_step(last_move)

        #On défini notre nouvel état
        new_state = agent.get_state(game)

        #Appel fonction entrainement court terme (donc tant qu'on a pas perdu)
        agent.train_short_memory(last_state, last_move, reward, new_state, game_over)

        #Appel fonction de remember
        agent.memory(last_state, last_move, reward, new_state, game_over)

        if game_over:
            print(f"Perdu Game" + {agent.number_games})
            #Si on perd, on veut entrainer la mémoire à long terme
            game.reset_ai_game()
            agent.number_games += 1
            agent.train_long_memory()

            if score > best_score:
                best_score = score
                #Là on save le modèle
            print(f"Score:" + {score})

if __name__ == '__main__':
    train()
