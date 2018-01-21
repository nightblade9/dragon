# Dragon

[![Build status](https://travis-ci.org/nightblade9/dragon.svg?branch=master)](https://travis-ci.org/nightblade9/dragon/)

Dragon transpiles Python 3 code to [Haxe](http://haxe.org), which can then be transpiled and compiled to various platforms and languages (C++, Javascript, Java, C#, Ruby, Python, Lua, etc. for browser/web, desktop, Android, iOS, etc.)

Dragon was created in order to be able to write HaxeFlixel games in Python. However, it can generically transpile Python code to Haxe code.

Dragon is still in the early stages of development and currently can only process a subset of Python 3 code.

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
- Make sure all Python files have a final empty line

----

    Currently, Dragon is in a very early stage of development. We're using Lark to generate the parse tree, and then generate the resulting Haxe code. 

    Our roadmap:

    - Transpile a very simple "hello world" HaxeFlixel project
    - Transpile a more complicated HaxeFlixel game
    - Transpile one of the Kha game tutorials
    
    Once we achieve these goals, we plan to release the `v1.0.0` version of Dragon.

    You may also be interested in [Mars](https://github.com/nightblade9/mars), our companion project which handles generating and compiling HaxeFlixel projects (via Dragon).