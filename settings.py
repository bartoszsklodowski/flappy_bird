from dataclasses import dataclass


@dataclass
class GameSettings:
    FPS: int = 60
    SCREEN_WIDTH: int = 864
    SCREEN_HEIGHT: int = 936
    SCROLL_SPEED: int = 4
    PIPE_GAP: int = 150
    PIPE_FREQUENCY: int = 1500  # milliseconds
