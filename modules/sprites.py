import pygame

from config import Config
from utils.utils import to_tl_x, to_tl_y

from collections.abc import MutableMapping

class Axe(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.config = Config

        self.screen = screen
        self.image = pygame.Surface((1, self.config.SCREEN_HEIGHT))
        self.image.fill((255, 0, 0))
        pygame.draw.rect(self.image, (255, 0, 0),
                         (0, 0, 1, self.config.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = int(to_tl_x(0))
        self.rect.y = 0

    def update(self, *args, **kwargs):
        self.rect.x = int(to_tl_x(0))
        self.rect.y = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)

class State(MutableMapping, dict):

    def __setitem__(self, key, value):
        print('Setter got call…')
        match key:  # Apply coordinate system swap
            case 'x':
                print('x key has been updated. \o/')
                dict.__setitem__(self,key,value - self.size / 2)
                self.update(self, x=self.state[key])
            case 'y':
                print('y key has been updated. \o/')
                self.state[key] = value + self.size
                dict.__setitem__(self,key,value + self.size) 
                self.update(self, y=self.state[key])
            case _:
                print(key + ' key has been updated.')
                self.state[key] = value

class Element(pygame.sprite.Sprite):

    def __init__(self, init_mb_coordinates, screen):
        super().__init__()
        self.config = Config
        self.size = self.config.SIZE
        
        self.state = dict(
            zip(('x', 'y', 'velocity', 'acceleration'), (0.0, 0.0, 0.0, 0.0)))

        self.state = State(self.state)

        self.state['x'] = init_mb_coordinates[0] - self.size / 2
        self.state['y'] = init_mb_coordinates[1]
        self.state['velocity'] = self.config.VELOCITY

        # Affections collection
        # scroll, fire, gravity, wind…
        self.affected_by = []

        # Apparence
        self.screen = screen
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 0, 0))
        pygame.draw.rect(self.image, (0, 255, 0),
                         (5, 5, self.size - 10, self.size - 10))
        self.rect = self.image.get_rect()
        self.rect.x = int(to_tl_x(self.state['x']))
        self.rect.y = int(to_tl_y(self.state['y']))

        # Actions
        self.is_jumping = False

    def setterTest(self, key):
        print('Setter test started.')
        match key:
            case 'x':
                print('Should print Hello.')
                self.state['x'] = 0
            case 'y':
                print('Should print Bye.')
                self.state['y'] = 0
        print('Setter test finished.')

    def jump(self, jump_direction):
        if not self.is_jumping:
            self.is_jumping = True
            target_x = None
            direction_x = 0
            match str(jump_direction):
                case 'left':
                    target_x = self.state['x'] - self.size
                    direction_x = -1
                case 'right':
                    target_x = self.state['x'] + self.size
                    direction_x = 1

            if target_x is not None:

                while self.state['x'] != target_x:
                    self.state['velocity'] += self.config.GRAVITY
                    self.state['y'] += self.state['velocity']
                    self.state['x'] += direction_x * 1
                    self.state['velocity'] = self.config.VELOCITY

                self.is_jumping = False
                #print(self.state['x'], self.state['y'])
                self.state['velocity'] = self.config.VELOCITY

    def update(self, *arg, **kwargs):
        # Affections effects
        if 'scroll' in self.affected_by:
            self.state['y'] -= self.config.SCROLLSPEED

        # Position update
        match len(kwargs.items()):
            case 0:  # If no specific coordinate is passed
                self.rect.x = int(to_tl_x(self.state['x']))
                self.rect.y = int(to_tl_y(self.state['y']))
                #print('Both x and y coordinates updated.')

            case _:  # If x and/or y coordinate is passed
                for key, value in kwargs.items():
                    match key:
                        case 'x':
                            self.rect.x = int(to_tl_x(value))
                        case 'y':
                            self.rect.y = int(to_tl_y(value))

    def draw(self):
        self.screen.blit(self.image, self.rect)
