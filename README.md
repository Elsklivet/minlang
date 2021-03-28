# Minlang

Minlang is an [esoteric programming language](https://en.wikipedia.org/wiki/Esoteric_programming_language) based on the language [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck). It is based on a single-dimensional array of integer values that can be altered and accessed with single-character commands.

## The Table

The table is a single-dimension list of integers, which is allocated based on the first line of any `.mini` file, which should be of the form
`[size]` where `size` is the integer size of the table. The default is 256.

## Commands

 `+` Increment current cell

 `-` Decrement current cell

 `*` Multiply current cell by 2

 `/` Divide current cell by 2

 `>` Move one cell right

 `<` Move one cell left (note: these do not wrap, they simply stop at ends)

 `.` Print the integer in this cell

 `{` Start a loop

 `}` End loop if the current cell is either 0 (default) or a value parameterized: `}(num)`. 

 `[` Start definition.

 `]` Finish definition. (Current cell is equal to num between `[` and `]`, e.g. `[3]` sets current cell to 3)

 `?` Execute if cell holds parameterized value (e.g. `?(2)...;`).

 `@` Goto cell in parameter (e.g. `@(0)` goes to cell 0).

 `$` Save the current cell location (can be used in `@` or `?`).

 `&` Print the ascii value determined by the integer in the cell.

 `=` Copy the current cell's value to the parameterized cell.

 `%` Set current cell to its value modulo 2.

 `:` Define a function with parameterized ID. (`(0): ... ;` defines a function which can be called by `^(0)`).

 `^` Run a function. 

 `_` Print a newline.

 `;` End statement.

## Issues

 Currently, loops and functions are a big issue, probably because I have a very primitive/un-intuitive way of managing a "PC register." You cannot nest loops, recurse function calls, call functions inside loops, or use loops inside functions, because of the fact that the `charNum` pointer doesn't return control to the correct place in the code. A call-stack might be a good idea...

 Additionally, inside functions, `?` statements need to end the function if they are used, because the function searches for the first `;` it finds and ends the function definition there. This shouldn't be a super hard fix, though.

 Other than those, the code is just generally messy, and could use some cleaning up. I threw the whole thing together in eight hours tops so I could encode the lyrics to Never Gonna Give You Up into it (see [buildmini.py](/src/python/buildmini.py)).
 
## Using
 The [buildmini.py](/src/python/buildmini.py) file is an example of creating a file that will encode a string message to be printed by the language if it were to be run through the interpreter.

 As for running the code, the [interpreter.py](/src/python/interpreter.py) file can be run in the command line **with a file to be run as its first parameter**. I am trying to make this more user-friendly but right now it will demand a file to run or else it defaults to a REPL mode, similar to the python interpreter. You can also use `-sr` or `--show-registers` to print out the table of cells for debugging as a flag on the interpreter. 

## Contributing/Goals

 Other than resolving the above issues, I hoped to also make a few changes:

 - Make it so that `"comments inside quotation marks"` are escaped entirely (this should be pretty easy, I figure a single boolean flag and a `continue` will do the trick), because right now if a comment says `wow this comment has punctuation.` the `.` will be run as a command. It's semi annoying to type out "negative" every time. 

 - Write the interpreter in other languages, namely Java, JavaScript (web interpreters anyone?), C#, or C++. Any languages really. It would just be fun to do.

 - Make the language a hybrid interpreted/compiled language by making the interpreter create a file with equivalent code that can be compiled once and then is ready to run instantly thereafter, instead of needing to be interpreted again each and every time. (Python interpreter that makes a Java file and runs `javac`? _Java_ file that makes a Java file and runs `javac`??)

 I'm happy to review any pull requests or issues whenever I have time, as this is a just-for-fun project. 

If you'd like to cooperate more closely, add me on Discord (tag in profile). I'll have a website to put here at some point but it isn't done right now, so my Github profile has most of my other projects. Thanks for taking the time to check this out! :)