import pygame
import math

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
        self.status = dict(
            zip(('x', 'y', 'velocity', 'acceleration'), (0.0, 0.0, 0.0, 0.0)))

        # Position, velocity and accleration
        # are stored and updated in the status dictionary
        @property
        def status(self):
            return self._status

        @status.setter
        def status(self, **kwargs):
            for key, value in kwargs.items():
                if key in self._status:
                    match key:  # Apply coordinate system swap
                        case 'x':
                            self._status[key] = value - self.size / 2
                            self.update(self, x=self._status[key])
                        case 'y':
                            self._status[key] = value + self.size
                            self.update(self, y=self._status[key])
                        case _:
                            self._status[key] = value

        self.status['x'] = init_mb_coordinates[0] - self.size / 2
        self.status['y'] = init_mb_coordinates[1]
        self.status['velocity'] = self.config.VELOCITY

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
        self.rect.x = int(to_tl_x(self.status['x']))
        self.rect.y = int(to_tl_y(self.status['y']))

        # Actions
        self.is_jumping = False

    def jump(self, jump_direction):
        if not self.is_jumping:
            self.is_jumping = True
            target_x = None
            direction_x = 0
            match str(jump_direction):
                case 'left':
                    target_x = self.status['x'] - self.size
                    direction_x = -1
                case 'right':
                    target_x = self.status['x'] + self.size
                    direction_x = 1

            if target_x is not None:
                # Calculate jump parameters
                jump_height = ((7 / 3) * self.size)
                horizontal_displacement = self.size
                jump_duration = int(
                    2 * (jump_height / abs(self.config.GRAVITY))**0.5)

                # Calculate jump trajectory
                for t in range(jump_duration):
                    # Vertical displacement
                    vertical_displacement = 0.5 * self.config.GRAVITY * t**2
                    # Horizontal displacement
                    horizontal_displacement_t = (horizontal_displacement /
                                                 jump_duration) * t
                    # Update position
                    self.status['x'] += direction_x * horizontal_displacement_t
                    self.status['y'] += vertical_displacement

                self.is_jumping = False
                print(self.status['x'], self.status['y'], jump_duration)
                self.status['velocity'] = self.config.VELOCITY

    def update(self, *arg, **kwargs):
        # Affections effects
        if 'scroll' in self.affected_by:
            self.status['y'] -= self.config.SCROLLSPEED

        # Position update
        match len(kwargs.items()):
            case 0:  # If no specific coordinate is passed
                self.rect.x = int(to_tl_x(self.status['x']))
                self.rect.y = int(to_tl_y(self.status['y']))
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
