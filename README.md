# Dragon

[![Build status](https://travis-ci.org/nightblade9/dragon.svg?branch=master)](https://travis-ci.org/nightblade9/dragon/)

Dragon is a *universal Python translater*. It achieves this by transpiling Python to [Haxe](http://haxe.org), which can then be transpiled and compiled to various platforms and languages (C++, Javascript, Java, C#, Ruby, Python, Lua, etc. for browser/web, desktop, Android, iOS, etc.)

# Usage

- Create some Python code
- Create a file like `compiler.py`
- Add the import `from dragon.transpiler.python_to_haxe_transpiler import PythonToHaxeTranspiler`
- Invoke `PythonToHaxeTranspiler(source_path, files).transpile()` passing in the directory root of the source files (important for package names!) and a list of files to transpile (eg. `os.glob.glob("**/*.py"))`).
- Check the outputted Haxe code. Invoke the Haxe compiler as usual.
- Profit

For constructs that don't exist in Python (eg. `override`, `@:...`), add them to your Python code and prefix them with `@haxe:`.

# Caveats
- When importing Haxe code, use the Haxe-style `from package.subpackage import ClassName`

----

Currently, Dragon is in a very early stage of development. We're using Lark to generate the parse tree, and then generate the resulting Haxe code. 

Our roadmap:

- [X] Transpile the default HaxeFlixel "hello world" template (v0.1)
- [ ] Transpile a more complicated HaxeFlixel template
- [ ] Transpile an actual HaxeFlixel game
- [ ] Transpile one of the Kha game tutorials
    
Once we achieve these goals, we plan to release the `v1.0` version of Dragon.

You may also be interested in [Mars](https://github.com/nightblade9/mars), our companion project which handles generating, compiling, and running Python-based HaxeFlixel projects (via Dragon).
