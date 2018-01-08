from flixel.flx_game import FlxGame
from openfl.display.sprite import Sprite
from play_state import PlayState

class Main(Sprite):
    def __init__(self):
        super(Sprite, self).__init__()
        self.addChild(FlxGame(0, 0, PlayState))
