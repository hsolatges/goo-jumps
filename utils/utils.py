from config import Config

cfg = Config
'''Convert between middle-bottom and top-left coordinates, flipping y-axis'''


def to_tl_x(mb_x, width=cfg.SCREEN_WIDTH):
                      return float(mb_x + width / 2)


def to_tl_y(mb_y, height=cfg.SCREEN_HEIGHT):
                      return float(height - mb_y)
