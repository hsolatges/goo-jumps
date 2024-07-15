import math


class Config:
  TITLE = 'Goo jumps! – The game'
  FPS = 60
  SCREEN_WIDTH = 240
  SCREEN_HEIGHT = 400
  SIZE = 41
  GRAVITY = 1
  SCROLLSPEED = 1
  VELOCITY = 1
  JUMP_DATA = {
      'velocity': 1,
      'angle': 10 * math.pi / 180,
      'max_height': 7 / 3 * SIZE,
  }
