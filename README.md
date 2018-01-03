# Dragon

[![Build status](https://travis-ci.org/nightblade9/dragon.svg?branch=master)](https://travis-ci.org/nightblade9/dragon/)

Dragon is a *universal Python translater*. It achieves this by transpiling Python to [Haxe](http://haxe.org), which can then be transpiled and compiled to various platforms and languages (C++, Javascript, Java, C#, Ruby, Python, Lua, etc. for browser/web, desktop, Android, iOS, etc.)

----

Currently, Dragon is a Python to Haxe transpiler, written in Python.

At this (very early MVP) stage, the goal is to transpile simple code from Haxe to Python in order to generate fully-runnable HaxeFlixel games.

Once I achieve this goal, I will add more generic functionality to Dragon.

# Limitations

Your Python code must obey the following rules. If this chafes you, feel free to open an issue (or better yet, a PR) to resolve the problem.

- Tabs and spaces are both okay
- import statements should always be of the form `from a.b.c import X`. Any other types of imports (eg. `import a.b.*`) are not supported.