






1\.1 — Statements and the structure of a program
================================================





[*Alex*](https://www.learncpp.com/author/Alex/ "View all posts by Alex")




 May 30, 2007, 7:10 am PDT 
March 17, 2025





 






Chapter introduction


Welcome to the first primary chapter of these C\+\+ tutorials!


In this chapter, we’ll take a first look at a number of topics that are essential to every C\+\+ program. Because there are quite a few topics to cover, we’ll cover most at a fairly shallow level (just enough to get by). The goal of this chapter is to help you understand how basic C\+\+ programs are constructed. By the end of the chapter, you will be able to write your own simple programs.


In future chapters, we’ll revisit the majority of these topics and explore them in more detail. We’ll also introduce new concepts that build on top of these.


In order to keep the lesson lengths manageable, topics may be split over several subsequent lessons. If you feel like some important concept isn’t covered in a lesson, or you have a question that isn’t answered in the current lesson, it’s possible that it’s covered in the next lesson.


Statements


A computer program is a sequence of instructions that tell the computer what to do. A **statement** is a type of instruction that causes the program to *perform some action*.


 
Statements are by far the most common type of instruction in a C\+\+ program. This is because they are the smallest independent unit of computation in the C\+\+ language. In that regard, they act much like sentences do in natural language. When we want to convey an idea to another person, we typically write or speak in sentences (not in random words or syllables). In C\+\+, when we want to have our program do something, we typically write statements.


Most (but not all) statements in C\+\+ end in a semicolon. If you see a line that ends in a semicolon, it’s probably a statement.


In a high\-level language such as C\+\+, a single statement may compile into many machine language instructions.



For advanced readers


There are many different kinds of statements in C\+\+:


* Declaration statements
* Jump statements
* Expression statements
* Compound statements
* Selection statements (conditionals)
* Iteration statements (loops)
* Try blocks


By the time you’re through with this tutorial series, you’ll understand what all of these are!



Functions and the `main` function


In C\+\+, statements are typically grouped into units called functions. A **function** is a collection of statements that get executed sequentially (in order, from top to bottom). As you learn to write your own programs, you’ll be able to create your own functions and mix and match statements in any way you please (we’ll show how in a future lesson).


 

Rule


Every C\+\+ program must have a special function named **main** (all lower case letters).



When the program is run, the statements inside of `main` are executed in sequential order.


Programs typically terminate (finish running) after the last statement inside function `main` has been executed (though programs may abort early in some circumstances, or do some cleanup afterwards).


Functions are typically written to do a specific job or perform some useful action. For example, a function named `max` might contain statements that figures out which of two numbers is larger. A function named `calculateGrade` might calculate a student’s grade from a set of test scores. A function named `printEmployee` might print an employee’s information to the console. We will talk a lot more about functions soon, as they are the most commonly used organizing tool in a program.



Nomenclature


When discussing functions, it’s fairly common shorthand to append a pair of parenthesis to the end of the function’s name. For example, if you see the term `main()` or `doSomething()`, this is shorthand for functions named `main` or `doSomething` respectively. This helps differentiate functions from other things with names (such as variables) without having to write the word “function” each time.



In programming, the name of a function (or object, type, template, etc…) is called its **identifier**.


Characters and text


The earliest computers were designed primarily for mathematical calculations and data processing. As hardware improved, networking became accessible, and consumer software evolved, computers also became valuable tools for written communication.


 
In written language, the most basic unit of communication is the character. To simplify slightly, a **character** is a written symbol or mark, such as a letter, digit, punctuation mark, or mathematical symbol. When we tap an alphabetic or numeric key on our keyboard, a character is produced as a result, which can then be displayed on the screen. The following are all characters: `a`, `2`, `$`, and `=`.


In many cases, such as when writing words or sentences, we want to make use of more than one character. A sequence of characters is called **text** (also called a **string** in programming contexts).



Nomenclature


Conventionally, the term “text” is also used to mean **plain text**, which is text that contains only characters that appear on a standard keyboard, with no special formatting or styling. For example, plain text cannot represent bold words, as that requires styling.


Our C\+\+ programs are written as plain text.




For advanced readers


Computers have an additional type of character, called a “control character”. These are characters that have special meaning to the computer system, but either aren’t intended to be displayed, or display as something other than a single visible symbol. Examples of well\-known control characters include “escape” (which doesn’t display anything), “tab” (which displays as some number of spaces), and “backspace” (which erases the previous character).




Related content


We discuss the outputting of characters and text in lesson [1\.5 \-\- Introduction to iostream: cout, cin, and endl](https://www.learncpp.com/cpp-tutorial/introduction-to-iostream-cout-cin-and-endl/).  

We discuss characters (including control characters) in more detail in lesson [4\.11 \-\- Chars](https://www.learncpp.com/cpp-tutorial/chars/).



Dissecting Hello world!


Now that you have a brief understanding of what statements and functions are, let’s return to our “Hello world” program and take a high\-level look at what each line does in more detail.



```
#include <iostream>

int main()
{
   std::cout << "Hello world!";
   return 0;
}
```

Line 1 is a special type of line called a preprocessor directive. This `#include` preprocessor directive indicates that we would like to use the contents of the `iostream` library, which is the part of the C\+\+ standard library that allows us to read and write text from/to the console. We need this line in order to use `std::cout` on line 5\. Excluding this line would result in a compile error on line 5, as the compiler wouldn’t otherwise know what `std::cout` is.


Line 2 is blank, and is ignored by the compiler. This line exists only to help make the program more readable to humans (by separating the `#include` preprocessor directive and the subsequent parts of the program).


 
Line 3 tells the compiler that we’re going to write (define) a function whose name (identifier) is `main`. As you learned above, every C\+\+ program must have a `main` function or it will fail to link. This function will produce a value whose type is `int` (an integer).


Lines 4 and 7 tell the compiler which lines are part of the *main* function. Everything between the opening curly brace on line 4 and the closing curly brace on line 7 is considered part of the `main` function. This is called the function body.


Line 5 is the first statement within function `main`, and is the first statement that will execute when we run our program. `std::cout` (which stands for “character output”) and the `<<` operator allow us to display information on the console. In this case, we’re displaying the text `Hello world!`. This statement creates the visible output of the program.


Line 6 is a return statement. When an executable program finishes running, the program sends a value back to the operating system in order to indicate whether it ran successfully or not. This particular return statement returns the integer value `0` to the operating system, which means “everything went okay!”. This is the last statement in the program that executes.


All of the programs we write will follow this general template, or a variation on it.


 

Author’s note


If parts (or all) of the above explanation are confusing, that’s to be expected at this point. This was just to provide a quick overview. Subsequent lessons will dig into all of the above topics, with plenty of additional explanation and examples.



You can compile and run this program yourself, and you will see that it outputs the following to the console:



```
Hello world!

```

If you run into issues compiling or executing this program, check out lesson [0\.8 \-\- A few common C\+\+ problems](https://www.learncpp.com/cpp-tutorial/a-few-common-cpp-problems/).


Syntax and syntax errors


In the English language, sentences are constructed according to specific grammatical rules that you probably learned in English class in school. For example, in writing, normal sentences end in a period. The set of rules that describe how specific words (and punctuation) can be arranged to form valid sentences in a language is called **syntax**. For example, “My house painted is blue” is a syntax error, because the ordering of the words is unconventional. “All your base are belong to us!” is another notable one.


The C\+\+ programming language also has a syntax, which describes how the elements of your program must be written and arranged in order for the program to be considered valid. When you compile your program, the compiler is responsible for making sure your program follows these syntactical rules. If your program does something that deviates from the syntax of the language, the compiler will halt compilation and issue a *\_syntax error*.


Unlike the English language, which allows for a lot of ambiguity, the syntax rules of C\+\+ are strictly defined and upheld. Syntax errors are common. Fortunately, such errors are typically straightforward to find and fix, as the compiler will generally point you right at them. Compilation of a program will only complete once all syntax errors are resolved.


 
Since the syntax for most statements requires those statements to end in a semicolon, let’s see what happens if we omit the semicolon on line 5 of the “Hello world” program, like this:



```
#include <iostream>

int main()
{
   std::cout << "Hello world!"
   return 0;
}
```

Feel free to compile this ill\-formed program yourself.


When compiled using Clang, the following error message is generated:



```
prog.cc:5:31: error: expected ';' after expression

```

Clang is telling us that on line 5 at the 31st character, the syntax rules require a semicolon, but we did not provide one. Therefore, compilation was halted with an error.


When compiled with Visual Studio instead, the compiler produces this compilation error:


 

```
c:\vcprojects\hello.cpp(6): error C2143: syntax error : missing ';' before 'return'

```

Note that Visual Studio says the error was encountered on line 6 (instead of on line 5\). So who is right? Both are, in a way.


Clang knows we conventionally put semicolons at the end of statements, so it is reporting that the error is on line 5 based on the assumption that we will do so. Visual Studio is opting to report the line it was compiling when it determined that the error occurred (on line 6, when it encountered `return` instead of the expected semicolon).



Key insight


Compilers will sometimes report that an error has occurred on the line after the one where we’d conventionally fix the issue. If you can’t find the error on the line indicated, check the prior line.



To see other different error messages, experiment with deleting characters or even whole lines from the “Hello world” program. Also try restoring the missing semicolon at the end of line 5, and then deleting lines 1, 3, or 4 to see what happens.


Quiz time


The following quiz is meant to reinforce your understanding of the material presented above.


Question \#1


What is a statement?


[Show Solution](javascript:void(0))



A statement is an instruction in a computer program that tells the computer to perform an action.



Question \#2


What is a function?


[Show Solution](javascript:void(0))



A function is a collection of statements that executes sequentially.



Question \#3


What is the name of the function that all programs must have?


[Show Solution](javascript:void(0))



main



Question \#4


What happens when the program is run?


[Show Solution](javascript:void(0))



The statements inside `main()` are executed in sequential order.



Question \#5


What symbol are statements in C\+\+ often ended with?


[Show Solution](javascript:void(0))



A semicolon (`;`)



Question \#6


What is a syntax error?


[Show Solution](javascript:void(0))



A syntax error occurs when your program violates the grammar rules of the C\+\+ language.



Question \#7


What is the C\+\+ Standard Library?


[Show Hint](javascript:void(0))


Hint: Review lesson [0\.5 \-\- Introduction to the compiler, linker, and libraries](https://www.learncpp.com/cpp-tutorial/introduction-to-the-compiler-linker-and-libraries/)
[Show Solution](javascript:void(0))



A library file is a collection of precompiled code that has been “packaged up” for reuse in other programs. The C\+\+ Standard Library is a library that ships with C\+\+. It contains additional functionality to use in your programs.




[Next lesson

1\.2Comments](https://www.learncpp.com/cpp-tutorial/comments/)
[Back to table of contents](/)
[Previous lesson

0\.13What language standard is my compiler using?](https://www.learncpp.com/cpp-tutorial/what-language-standard-is-my-compiler-using/)


 
















 