import torch
import random
import numpy as np
from collections import deque
from snake import SnakeGameAI, Direction, Point
from modele import Linear_QNet, QTrainer

Max_Memory = 100_000
Batch_Size = 1000
Learning_Rate = 0.001

class Agent: 

    #Init
    def __init__(self):
        self.number_games = 0
        self.randomness = 0 #pour les random moves
        self.discount_rate = 0.9
        self.memory = deque(maxlen=Max_Memory) #SI on dépasse la mémoire, on supprime les données du début. (Garde les + récentes)

        #Size of states , , nombre d'action
        self.model = Linear_QNet(11, 256 ,3)
        self.trainer = QTrainer(self.model, learning_rate=Learning_Rate, discount_rate=self.discount_rate)

    #Connaitre l'état du jeu
    def get_state(self, game):

        head_snake= game.snake[0]
        #Les points autour de la tete dans toutes les directions
        point_left = Point(head_snake.x -20, head_snake.y)
        point_right = Point(head_snake.x +20, head_snake.y)
        point_under = Point(head_snake.x, head_snake.y - 20)
        point_over = Point(head_snake.x, head_snake.y + 20)

        #Les direction actuelles, en binaire. Donc comme on en a forcement 1 vrai, les autres sont faux (donc 0)
        direction_left = game.direction == Direction.LEFT
        direction_right = game.direction == Direction.RIGHT
        direction_under = game.direction == Direction.DOWN
        direction_over = game.direction == Direction.UP

        #On a 11 valeurs d'états de notre snake :  
        #[Danger devant, Danger Droite, Danger Gauche,
        #Direction LEFT, Direction DROITE, Direction UP, Direction DOWN
        #Pomme à Gauche, Pomme à Droite, Pomme Up, Pomme Down]

        state = [
            #Danger devant
            (direction_left and game.is_collision(point_left)) or
            (direction_right and game.is_collision(point_right)) or
            (direction_over and game.is_collision(point_over)) or
            (point_under and game.is_collision(point_under)),

            #Danger à droite
            (direction_left and game.is_collision(point_over)) or
            (direction_right and game.is_collision(point_under)) or
            (direction_over and game.is_collision(point_right)) or
            (point_under and game.is_collision(point_left)),

            #Danger à gauche
            (direction_left and game.is_collision(point_under)) or
            (direction_right and game.is_collision(point_over)) or
            (direction_over and game.is_collision(point_left)) or
            (point_under and game.is_collision(point_right)),

            #Directions
            direction_left, 
            direction_right, 
            direction_over, 
            direction_under,

            #Pomme à gauche
            game.apple.x < game.head.x,
            #Pomme à droite
            game.apple.x > game.head.x,
            #Pomme en haut
            game.apple.y < game.head.y,
            #Pomme en bas
            game.apple.y > game.head.y

        ]

        return np.array(state, dtype=int)



    #Rappel des paramètres
    def remember(self, state, action, reward, next_state, gameover):
        #Si on dépasse max memory
        self.memory.append((state, action, reward, next_state, gameover))


    def train_long_memory(self):
        #Si on a plus que la valeur de base, on prend un sample
        if len(self.memory) > Batch_Size: 
            mini_sample = random.sample(self.memory, Batch_Size)
        #Sinon on prend tout
        else:
            mini_sample = self.memory

        #on va regrouper chaque éléments de la meme catégorie dans de nouveaux tuples (States, actions, etc...)
        states, actions, rewards, next_states, gameovers = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, gameovers)
    


    def train_short_memory(self, state, action, reward, next_state, gameover):
        self.trainer.train_step(state, action, reward, next_state, gameover)


    #Random moves : on va faire de lexploration et de l'exploitation
    def get_action(self, state):
        #Determine le nombre de parties pour savoir si IA va jouer aléatoireement. Plus on joue, meilleur on est
        self.randomness = max(10, 80 - self.number_games)
        final_move = [0,0,0]
        #Si on est en dessous de notre nombre
        if random.randint(0,200) < self.randomness:

            #On choisi entre 0,1,2
            move = random.randint(0,2)
            #On donne a la valeur 0,1,2 dans le tableau, la valeur 1. Etc [1,0,0] si la valeur choisie avant est 0
            final_move[move] = 1
        else: #Si on ne veut plus d'aléatoire
            #Me sort un % de chance en fonction du state : [0.1,0.8,0.1]
            state_init = torch.tensor(state, dtype=torch.float)
            #Modele de prédiction
            prediction = self.model(state_init)
            #Renvoie la plus haute prédiction
            move = torch.argmax(prediction).item()
            #On donne a la valeur 0,1,2 dans le tableau, la valeur 1. Etc [1,0,0] si la valeur choisie avant est 0
            final_move[move] = 1

        return final_move


#Training fonction
def train():

    best_score = 0
    agent = Agent()
    game = SnakeGameAI()

    #On veut boucler au max
    print(f"dans la boucle de jeu {agent.number_games}")
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
        agent.remember(last_state, last_move, reward, new_state, game_over)

        if game_over:
            print(f"Perdu Game {agent.number_games}")
            #Si on perd, on veut entrainer la mémoire à long terme
            game.reset_ai_game()
            agent.number_games += 1
            agent.train_long_memory()

            if score > best_score:
                best_score = score
                agent.model.save()
            print(f"Score: {score}")


            #Faire liste affichage



if __name__ == '__main__':
    train()
