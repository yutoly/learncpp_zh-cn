3.x — 第3章 总结与测验  
=================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2024年8月13日（首次发布于2019年2月1日）  

本章回顾  
----------------  

**语法错误（syntax error）**指违反C++语法规则的代码错误，编译器会捕获此类错误。  

**语义错误（semantic error）**指语法正确但不符合程序员预期的错误。  

**调试（debugging）**是发现并修复程序中错误的过程。  

可采用五步调试法：  
1. 定位根本原因  
2. 理解问题  
3. 确定修复方案  
4. 实施修复  
5. 重新测试  

定位错误通常是调试过程中最困难的环节。  

**静态分析工具（static analysis tools）**可分析代码并检测潜在的语义问题。  

可靠复现问题是调试的首要关键步骤。  

常用调试策略包括：  
* 注释代码段  
* 使用输出语句验证代码流程  
* 打印变量值  

使用打印语句调试时，建议改用*std::cerr*而非*std::cout*，但最好避免依赖打印调试。  

**日志文件（log file）**记录程序运行事件，**日志记录（logging）**是写入日志的过程。  

**重构（refactoring）**指在不改变程序行为的前提下重组代码，通常用于提高代码组织性、模块化或性能。  

**单元测试（unit testing）**通过测试代码单元确保其正确性。  

**防御性编程（defensive programming）**通过预判软件滥用场景来检测和缓解问题。  

**程序状态（program state）**包含变量值、函数调用记录和执行点等运行时信息。  

**调试器（debugger）**允许程序员控制执行流程并检查程序状态，**集成调试器（integrated debugger）**是集成在代码编辑器中的调试工具。  

**单步调试（stepping）**相关功能：  
* **逐语句（step into）**：执行下条语句，若含函数调用则跳入函数  
* **逐过程（step over）**：执行下条语句，若含函数调用则直接执行完函数  
* **跳出（step out）**：执行完当前函数剩余代码  
* **运行到光标处（run to cursor）**：执行至光标位置  

**继续（continue）**：运行至程序结束或断点  
**启动（start）**：从头开始继续执行  

**断点（breakpoint）**使调试器在指定位置暂停执行。  

**设置下条语句（set next statement）**可跳转执行点，用于跳过或重复代码。  

**监视变量（watching a variable）**允许在调试时检查变量值，**监视窗口（watch window）**显示变量或表达式的值。  

**调用栈（call stack）**记录执行路径上的活动函数，**调用栈窗口（call stack window）**显示该信息。  

测验时间  
----------------  

**问题1**  
以下加法程序存在缺陷，请使用调试器观察变量x的值并修复：  

```cpp
#include <iostream>

int readNumber(int x)
{
	std::cout << "请输入数字：";
	std::cin >> x;
	return x;
}

void writeAnswer(int x)
{
	std::cout << "和为：" << x << '\n';
}

int main()
{
	int x {};
	readNumber(x);
	x = x + readNumber(x);
	writeAnswer(x);

	return 0;
}
```  

  
<details><summary>答案</summary>main函数中未接收readNumber返回值，且readNumber应使用局部变量：</details>  

修复后代码：  
```cpp
#include <iostream>

int readNumber()
{
	std::cout << "请输入数字：";
	int x {};
	std::cin >> x;
	return x;
}

void writeAnswer(int x)
{
	std::cout << "和为：" << x << '\n';
}

int main()
{
	int x { readNumber() };
	x = x + readNumber();
	writeAnswer(x);

	return 0;
}
```  

**问题2**  
以下除法程序存在缺陷，输入8和4进行调试并修复：  

```cpp
#include <iostream>

int readNumber()
{
	std::cout << "请输入数字：";
	int x {};
	std::cin >> x;
	return x;
}

void writeAnswer(int x)
{
	std::cout << "商为：" << x << '\n';
}

int main()
{
	int x{ };
	int y{ };
	x = readNumber();
	x = readNumber();
	writeAnswer(x/y);

	return 0;
}
```  

  
<details><summary>答案</summary>第二个readNumber错误赋值给x导致除零错误：</details>  

修复后代码：  
```cpp
#include <iostream>

int readNumber()
{
	std::cout << "请输入数字：";
	int x {};
	std::cin >> x;
	return x;
}

void writeAnswer(int x)
{
	std::cout << "商为：" << x << '\n';
}

int main()
{
	int x{ readNumber() };
	int y{ readNumber() };
	writeAnswer(x/y);

	return 0;
}
```  

**问题3**  
当程序执行到d()函数内部时（第4行），调用栈顺序是？  

```cpp
void d() { }  // 执行点在此
void c() {}
void b() { c(); d(); }
void a() { b(); }
int main() { a(); return 0; }
```  

  
<details><summary>答案</summary>调用栈顺序：d → b → a → main</details>  

**问题4（附加题）**  
修复以下加法程序：  

```cpp
#include <iostream>

int readNumber()
{
    std::cout << "请输入数字：";
    char x{};
    std::cin >> x;    
    return x;
}

void writeAnswer(int x)
{
    std::cout << "和为：" << x << '\n';
}

int main()
{
    int x { readNumber() };
    int y { readNumber() };
    writeAnswer(x + y);

    return 0;
}
```  

  
<details><summary>答案</summary>readNumber中使用char导致ASCII值错误，应改为int：</details>  

修复后代码：  
```cpp
int readNumber()
{
    std::cout << "请输入数字：";
    int x{};  // 修改此处
    std::cin >> x;    
    return x;
}
```  

作者注  
----------------  
寻找简单程序中的非显式错误示例具有挑战性，欢迎读者提供建议。  

[下一课 4.1 基础数据类型简介](Chapter-4/lesson4.1-introduction-to-fundamental-data-types.md)  
[返回主页](/)  
[上一课 3.10 问题预防](Chapter-3/lesson3.10-finding-issues-before-they-become-problems.md)