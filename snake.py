import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 30)


#Direction de notre Snake
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

#Couleurs In Game
# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
RED2 = (200,100,0)
GREEN1 = (0, 255, 0)
GREEN2 = (100, 200, 0)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 10

class SnakeGameAI:

    #Initialiser l'instance di jeu snake
    def __init__(self, w=600, h=400):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('SnakeAI')
        self.clock = pygame.time.Clock()
        self.reset_ai_game()


    #Fonction d'initialisation et reinitialisation de l'IA après chaque partie
    def reset_ai_game(self):
         #Partie initialisation 
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.apple = None
        self._place_apple()

        #Pour savoir le nombre d'itération que l'on a pour éviter qu'il tourne en boucle
        self.frame_iteration = 0


    def _place_apple(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.apple = Point(x, y)
        if self.apple in self.snake:
            self._place_apple()

    #Fonction à appeler pour l'IA
    def play_step(self, action):

        self.frame_iteration += 1


        #R2cupérer les évènement du user ou de l'IA
        for event in pygame.event.get():
            #Arreter l'instance
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # #Cliquer sur une direction
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
            #         self.direction = Direction.LEFT
            #     elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
            #         self.direction = Direction.RIGHT
            #     elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
            #         self.direction = Direction.UP
            #     elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
            #         self.direction = Direction.DOWN

        # Met a jours la poistion pour déplacer le snake
        self._move(action)  # Toujours tout droit avec la direction définie par les touches
        self.snake.insert(0, self.head)
        reward = 0

        #Vérifier sic'est Game Over
        game_over = False
        if self.is_collision():
            game_over = True
            reward = -100
            return reward, game_over, self.score
    

        #On ajoute cette fonction pour punir le modèl s'il tourne en rond pendant trop longtemps
        if self.frame_iteration > 100*len(self.snake):
            reward = -10
            return reward, game_over, self.score
        

        # Gestion de la nourriture, avec un bonus si on la mange
        if self.head == self.apple:
            self.score += 1
            reward = 10
            self._place_apple()
        else:
            self.snake.pop()

        #Mise à jour de la fenêtre et de l'horloge
        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    #Vérifier les collisions
    def is_collision(self, point=None):

        if point is None: 
            point = self.head

        # Mange le mur
        if point.x > self.w - BLOCK_SIZE or point.x < 0 or point.y > self.h - BLOCK_SIZE or point.y < 0:
            return True
        #Mange sa queue
        if point in self.snake[1:]:
            return True

        return False

    #Ppour mettre à jour l'interface User 
    def _update_ui(self):
        self.display.fill(BLACK)

        #Dessin du snake
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        #Dessin de la pomme
        pygame.draw.rect(self.display, RED, pygame.Rect(self.apple.x, self.apple.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, RED2, pygame.Rect(self.apple.x+4, self.apple.y+4, 12, 12))

        #Afficher le score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):

        # [Devant , à droite, à gauche]
        possible_direction = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        #Direction actuelle du snake
        idx = possible_direction.index(self.direction)

        #
        if np.array_equal(action, [1,0,0]) : 
            #Récupère la direction actuelle
            new_direction = possible_direction[idx] # On va devant (donc pas de changement)
        elif np.array_equal(action, [0,1,0]): #On va à droite
            #Donc si on est à RIGHT, on passe à Down, etc... et si on est à UP, on revient à right
            next_idx = (idx + 1) % 4
            new_direction = possible_direction[next_idx] 
        else: #On va à gauche
            #Donc si on est à RIGHT, on passe à UP, etc... et si on est à UP, on revient à Left
            next_idx = (idx - 1) % 4
            new_direction = possible_direction[next_idx] 

        self.direction = new_direction

        #Calcul de la nouvelle position
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)



# if __name__ == '__main__':
#     game = SnakeGameAI()

#     while True:

#         game_over, score = game.play_step()

#         if game_over:
#             print(f'Game over! Score: {score}')
#             break

#     pygame.quit()