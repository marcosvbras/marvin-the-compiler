# Marvin: The Compiler

<p align="center">
  <img src="images/the-martian.gif" alt="Marvin The Martian gif"/>
</p>

## What is this?

This project consists in a Compiler program written entirely in **Python** for the Compilers subject in my undergraduate degree. 

The compiler was made for a programming language called **Mars** that doesn't exist (yet). **Mars** is extremely simple and has just the limited functions that its grammar allows to do.

The compiler's name is an acronym for my name (**MAR**cos **VIN**ícius) and it really means nothing beyond that. However, since this name remembers the [Looney Tunes' character "Marvin: The Martian"](https://en.wikipedia.org/wiki/Marvin_the_Martian), the project name was quite inspired in this one.

## About Mars

As I said, Mars is a simple programming language and it counts with the following features:

- Allows the four base math operations: addition, subtraction, multiplication and division
- One-line and multi-line comments
- It's not *case-sensitive*

## About the compiler

The compiler consists in 3 parts: 
- **Lexical Analyser**: It's the first phase of every compiler. The lexer takes a source code from language preprocessors that are written in the form of sentences. The lexer then breaks the syntaxes into a series of tokens (language keywords), by removing any whitespace or comments in the source code. If the lexer finds an invalid token during its running, it throws an error for user. In Marvin, it will just prints a simple Syntax Error message with the corresponding line and column of the error. The lexer uses the **Panic mode** approach as error catcher: when it encounters an error anywhere in the statement, it ignores the rest of the statement by not processing input from erroneous input to delimiter, such as semi-colon. This is the easiest way of error-recovery and also, it prevents the parser from developing infinite loops.
- **Syntax Analyser**: It's the second phase of a compiler. This is roughly the equivalent of checking that some ordinary text written in some language. It takes the recognized token from the lexer and then check the order according to the grammer. Marvin also uses **Panic Mode** by checking *Synch* on Preditive table.
- **[In Progress]** Semantic Analyser


