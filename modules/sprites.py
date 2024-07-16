import pygame

from config import Config
from utils.utils import to_tl_x, to_tl_y

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
class Element(pygame.sprite.Sprite):

    def __init__(self, init_mb_coordinates, screen):
        super().__init__()
        self.config = Config
        self.size = self.config.SIZE

        # State properties : x, y and velocity_y        
        self.velocity_y = 0
        self._x = init_mb_coordinates[0] - self.size / 2
        @property
        def x(self):
            return self._x
        
        @x.setter
        def x(self, value):
            corrected_value = value - self.size / 2
            print('x setter called.')
            self.update(x=corrected_value)
            self._x = corrected_value        
        
        self._y = init_mb_coordinates[1] + self.size
        @property
        def y(self):
            return self._y
        
        @y.setter
        def y(self, value):
            corrected_value = value + self.size
            print('y setter called.')
            self.update(y=corrected_value)
            self._y = corrected_value

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
        self.rect.x = int(to_tl_x(self.x))
        self.rect.y = int(to_tl_y(self.y))

        # Actions
        self.is_jumping = False

    def setterTest(self, key):
        print('Setter test started.')
        match key:
            case 'x':
                print('x setter should be called…')
                self.x = 0
            case 'y':
                print('y setter should be called…')
                self.y = 0
        print('Setter test finished.')

    def jump(self, jump_direction):
        if not self.is_jumping:
            self.is_jumping = True
            target_x = None
            direction_x = 0
            match str(jump_direction):
                case 'left':
                    target_x = self.x - self.size
                    direction_x = -1
                case 'right':
                    target_x = self.x + self.size
                    direction_x = 1

            if target_x is not None:

                while self.x != target_x:
                    self.velocity_y += self.config.GRAVITY
                    self.y += self.velocity_y
                    self.x += direction_x * 1

                self.is_jumping = False
                #print(self.state['x'], self.state['y'])
                self.velocity_y = 0

    def update(self, *arg, **kwargs):
        # Affections effects
        if 'scroll' in self.affected_by:
            self.y -= self.config.SCROLLSPEED

        # Position update
        match len(kwargs.items()):
            case 0:  # If no specific coordinate is passed
                self.rect.x = int(to_tl_x(self.x))
                self.rect.y = int(to_tl_y(self.y))

            case _:  # If x and/or y coordinate is passed
                for key, value in kwargs.items():
                    match key:
                        case 'x':
                            self.rect.x = int(to_tl_x(value))
                        case 'y':
                            self.rect.y = int(to_tl_y(value))

    def draw(self):
        self.screen.blit(self.image, self.rect)
