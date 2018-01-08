from flixel import FlxGame
from openfl.display import Sprite
import PlayState

class Main(Sprite):
    def __init__(self):
        super(Sprite, self).__init__()
        self.addChild(FlxGame(0, 0, PlayState))
