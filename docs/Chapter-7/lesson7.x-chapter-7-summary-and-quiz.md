7.x — 第7章总结与测验  
=================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月2日（首次发布于2015年5月9日）  

本章回顾  
----------------  

本章涵盖了大量内容。做得好，您表现非常出色！  

**复合语句（compound statement）**或**块（block）**是由零条或多条语句组成的代码组，编译器将其视为单条语句。块以`{`符号开始，以`}`符号结束，执行语句位于两者之间。块可用于任何允许单条语句的位置。块末尾不需要分号。块常与`if语句`配合使用以执行多条语句。  

**用户自定义命名空间（user-defined namespaces）**是您为自己声明定义的命名空间。C++提供的命名空间（如`全局命名空间（global namespace）`）或库提供的命名空间（如`命名空间std（namespace std）`）不属于用户自定义命名空间。  

可以通过**作用域解析运算符（scope resolution operator）(::)**访问命名空间中的声明。该运算符告诉编译器应在左操作数指定的作用域中查找右操作数标识符。若未提供左操作数，则默认使用全局命名空间。  

局部变量是在函数内定义的变量（包括函数参数）。局部变量具有**块作用域（block scope）**，即从定义点开始到所在块结束均有效。局部变量具有**自动存储期（automatic storage duration）**，即定义时创建，所在块结束时销毁。  

在嵌套块中声明的名称可能**遮蔽（shadow）**或**隐藏（name hide）**外部块中的同名变量。应避免这种情况。  

全局变量是在函数外定义的变量。全局变量具有**文件作用域（file scope）**，即从声明点开始到文件末尾均可见。全局变量具有**静态存储期（static duration）**，即程序启动时创建，程序终止时销毁。尽可能避免静态变量的动态初始化。  

标识符的**链接属性（linkage）**决定不同声明是否指向同一实体。局部变量无链接属性。具有**内部链接（internal linkage）**的标识符可在单文件内使用，但不能在其他文件中访问。具有**外部链接（external linkage）**的标识符可在定义文件和其他代码文件（通过前向声明）中使用。  

尽可能避免使用非常量全局变量。常量全局变量通常可接受。若编译器支持C++17，请使用**内联变量（inline variables）**作为全局常量。  

可通过**static**关键字赋予局部变量静态存储期。  

**限定名称（qualified name）**包含关联作用域（如`std::string`）。**非限定名称（unqualified name）**不包含作用域限定符（如`string`）。  

**using声明（using declarations）**与**using指令（using directives）**可用于避免显式限定命名空间。**using声明**允许使用非限定名称作为限定名称的别名。**using指令**将命名空间所有标识符导入当前作用域。通常应避免使用这两种方式。  

**内联展开（inline expansion）**是将函数调用替换为函数定义代码的过程。使用`inline`关键字声明的函数称为**内联函数（inline function）**。  

内联函数和变量有两个主要要求：  
* 编译器必须在每个使用该函数/变量的翻译单元中看到完整定义（仅前向声明不够）。若提供前向声明，定义可出现在使用点之后  
* 所有内联函数/变量的定义必须完全相同，否则会导致未定义行为  

在现代C++中，inline术语演变为"允许多重定义"。因此，内联函数允许在多个文件中定义。C++17引入**内联变量（inline variables）**，允许在多个文件中定义。  

内联函数和变量对**纯头文件库（header-only libraries）**特别有用，这类库完全由头文件实现功能（不含.cpp文件）。  

最后，C++支持**未命名命名空间（unnamed namespaces）**，隐式将其内容视为具有内部链接。C++还支持**内联命名空间（inline namespaces）**，为命名空间提供基础版本控制功能。  

测验时间  
----------------  

**问题1**  
修复以下程序：  
```cpp
#include <iostream>

int main()
{
	std::cout << "Enter a positive number: ";
	int num{};
	std::cin >> num;


	if (num < 0)
		std::cout << "Negative number entered.  Making positive.\n";
		num = -num;

	std::cout << "You entered: " << num;

	return 0;
}
```  
  
<details><summary>答案</summary>  
```cpp
#include <iostream>

int main()
{
	std::cout << "Enter a positive number: ";
	int num{};
	std::cin >> num;


	if (num < 0)
	{ // 需要代码块来确保num<0时执行两条语句
		std::cout << "Negative number entered.  Making positive.\n";
		num = -num;
	}

	std::cout << "You entered: " << num;

	return 0;
}
```  
</details>  

**问题2**  
编写名为constants.h的文件使以下程序运行。若编译器支持C++17，使用内联constexpr变量，否则使用普通constexpr变量。`maxClassSize`值应为`35`。  
main.cpp：  
```cpp
#include "constants.h"
#include <iostream>

int main()
{
	std::cout << "How many students are in your class? ";
	int students{};
	std::cin >> students;


	if (students > Constants::maxClassSize)
		std::cout << "There are too many students in this class";
	else
		std::cout << "This class isn't too large";

	return 0;
}
```  
  
<details><summary>答案</summary>  
constants.h：  
```cpp
#ifndef CONSTANTS_H
#define CONSTANTS_H

namespace Constants
{
	inline constexpr int maxClassSize{ 35 }; // 不支持C++17时移除inline
}
#endif
```  
main.cpp：  
```cpp
#include "constants.h"
#include <iostream>

int main()
{
	std::cout << "How many students are in your class? ";
	int students{};
	std::cin >> students;


	if (students > Constants::maxClassSize)
		std::cout << "There are too many students in this class";
	else
		std::cout << "This class isn't too large";

	return 0;
}
```  
</details>  

**问题3**  
编写函数`int accumulate(int x)`，返回所有传入x值的累加和。  
[查看提示](javascript:void(0))  
<details><summary>提示</summary>使用静态局部变量存储总和</details>  
  
<details><summary>答案</summary>  
```cpp
#include <iostream>

int accumulate(int x)
{
    static int sum{ 0 }; // 程序启动时初始化sum为0
    sum += x;
    return sum;
}

int main()
{
    std::cout << accumulate(4) << '\n'; // 输出4
    std::cout << accumulate(3) << '\n'; // 输出7
    std::cout << accumulate(2) << '\n'; // 输出9
    std::cout << accumulate(1) << '\n'; // 输出10

    return 0;
}
```  
</details>  

**问题3b** 附加题：上述`accumulate()`函数有哪两个缺点？  
  
<details><summary>答案</summary>  
1. 没有常规方法在不重启程序的情况下重置累加器  
2. 没有常规方法运行多个累加器  

高级读者可通过函数对象（[21.10 — 重载括号运算符](Chapter-21/lesson21.10-overloading-the-parenthesis-operator.md)）替代静态局部变量解决这些问题。  
</details>  

[下一课 8.1 控制流简介](Chapter-8/lesson8.1-control-flow-introduction.md)  
[返回主页](/)  
[上一课 7.14 未命名与内联命名空间](Chapter-7/lesson7.14-unnamed-and-inline-namespaces.md)