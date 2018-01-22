import flixel.FlxGame;
import openfl.display.Sprite;
import PlayState;
class Main extends Sprite {
function new() {
trace("Starting Main");
super();
this.addChild(new FlxGame(0, 0, PlayState));
}
}