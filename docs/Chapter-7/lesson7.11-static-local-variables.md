7.11 — 静态局部变量  
==============================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月19日首次发布，2024年12月26日更新  

`static`（静态）是C++中最易混淆的术语之一，主要原因在于它在不同上下文中有不同含义。在先前课程中，我们了解到全局变量具有静态存储期（static duration），即它们在程序启动时创建，程序终止时销毁。我们还讨论了`static`关键字如何赋予全局标识符内部链接（internal-linkage），使其仅能在定义文件中使用。  

本课程将探讨`static`关键字应用于局部变量时的用法。  

静态局部变量  
----------------  

在课程[2.5 — 局部作用域简介](Chapter-2/lesson2.5-introduction-to-local-scope.md)中，我们学习到局部变量默认具有自动存储期（automatic duration），即在定义时创建，离开作用域时销毁。对局部变量使用`static`关键字可将其存储期从自动改为静态，此时变量将在程序启动时创建，程序终止时销毁（类似全局变量）。因此静态局部变量在离开作用域后仍能保持其值！  

通过示例可以清晰展示自动存储期与静态存储期局部变量的区别：  

自动存储期（默认）：  
```cpp
#include <iostream>

void incrementAndPrint()
{
    int value{ 1 }; // 默认自动存储期
    ++value;
    std::cout << value << '\n';
} // value在此处销毁

int main()
{
    incrementAndPrint();
    incrementAndPrint();
    incrementAndPrint();

    return 0;
}
```  

每次调用`incrementAndPrint()`时，都会创建初始化为`1`的value变量。函数将其增至`2`后输出。函数执行完毕变量即被销毁。因此程序输出：  
```
2
2
2
```  

静态存储期（使用static关键字）：  
```cpp
#include <iostream>

void incrementAndPrint()
{
    static int s_value{ 1 }; // 通过static关键字实现静态存储期。此初始化器仅执行一次
    ++s_value;
    std::cout << s_value << '\n';
} // s_value不在此销毁，但因离开作用域而不可访问

int main()
{
    incrementAndPrint();
    incrementAndPrint();
    incrementAndPrint();

    return 0;
}
```  

此程序中，`s_value`被声明为`static`，故在程序启动时创建：  
- 具有零初始化或constexpr初始化器的静态局部变量可在程序启动时初始化  
- 无初始化器或非constexpr初始化器的静态局部变量会在程序启动时零初始化，非constexpr初始化器在首次遇到变量定义时重新初始化，后续调用将跳过初始化  
- 未显式初始化的静态局部变量默认进行零初始化  

由于`s_value`具有constexpr初始化器`1`，它将在程序启动时初始化。当函数结束时`s_value`离开作用域但不销毁，每次调用函数时其值保持上次结果。因此程序输出：  
```
2
3
4
```  

关键见解  
----------------  
静态局部变量适用于需要跨函数调用保持值的场景。  

最佳实践  
----------------  
始终初始化静态局部变量。静态局部变量仅在首次执行时初始化，后续调用不再初始化。  

技巧  
----------------  
类似使用"g_"前缀表示全局变量，常用"s_"前缀表示静态局部变量。  

ID生成  
----------------  
静态存储期局部变量最常见的用途之一是生成唯一ID。设想需要为多个相似对象（如僵尸攻击游戏或三角形模拟）赋予唯一标识符以便调试：  
```cpp
int generateID()
{
    static int s_itemID{ 0 };
    return s_itemID++; // 复制s_itemID当前值，递增实际值，返回复制的值
}
```  
首次调用返回`0`，第二次返回`1`，依此类推。这些数字可作为对象的唯一ID。由于`s_itemID`是局部变量，其他函数无法篡改。  

关键见解  
----------------  
静态局部变量具有类似局部变量的块作用域，但生命周期与全局变量相同，持续到程序结束。  

静态局部常量  
----------------  
静态局部变量可声明为const或constexpr。典型应用场景是函数需要频繁使用初始化成本高的常量（如从数据库读取值）。使用普通局部变量时，每次调用都需创建并初始化对象，而const/constexpr静态局部变量只需初始化一次即可重复使用。  

关键见解  
----------------  
静态局部变量最适合用于避免函数每次调用时的昂贵对象初始化。  

避免使用静态局部变量改变流程  
----------------  
考虑以下代码：  
```cpp
#include <iostream>

int getInteger()
{
	static bool s_isFirstCall{ true };

	if (s_isFirstCall)
	{
		std::cout << "Enter an integer: ";
		s_isFirstCall = false;
	}
	else
	{
		std::cout << "Enter another integer: ";
	}

	int i{};
	std::cin >> i;
	return i;
}
```  
此代码虽能运行，但静态局部变量使代码更难理解。若仅阅读`main()`中的调用而不查看`getInteger()`实现，无法察觉两次调用的差异。这类似于微波炉+1按钮有时加1分钟有时加1秒的迷惑行为。  

假设要为计算器添加减法功能：  
```cpp
int main()
{
  std::cout << "Addition\n";
  int a{ getInteger() };
  int b{ getInteger() };

  std::cout << "Subtraction\n";
  int c{ getInteger() };
  int d{ getInteger() };
}
```  
此时第三次调用`getInteger()`会显示"Enter another integer"而非预期提示，因为函数内部状态`s_isFirstCall`无法重置。  

改进方案是将`s_isFirstCall`作为参数传递，允许调用方控制提示：  
```cpp
#include <iostream>

constexpr bool g_firstCall { true }; // 定义符号常量

int getInteger(bool bFirstCall)
{
	if (bFirstCall)
		std::cout << "Enter an integer: ";
	else
		std::cout << "Enter another integer: ";

	int i{};
	std::cin >> i;
	return i;
}
```  

最佳实践  
----------------  
- const静态局部变量通常可以安全使用  
- 非const静态局部变量应尽量避免。若必须使用，确保变量无需重置且不用于改变程序流程  

技巧  
----------------  
更通用的解决方案是将`bool`参数改为`std::string_view`，允许调用方自定义提示文本。  

高级阅读  
----------------  
需要多个具有记忆功能变量的场景（如多个ID生成器），函数对象（functor）是良好解决方案（参见课程[21.10 — 重载括号运算符](Chapter-21/lesson21.10-overloading-the-parenthesis-operator.md)）。  

测验时间  
----------------  
问题1  
`static`关键字对全局变量和局部变量分别有何影响？  
  
<details><summary>答案</summary>对全局变量：定义为内部链接，不可被其他文件使用。对局部变量：定义为静态存储期，仅创建一次，程序结束时销毁。</details>  

[下一课 7.12 — 作用域、存储期与链接性总结](Chapter-7/lesson7.12-scope-duration-and-linkage-summary.md)  
[返回主页](/)  
[上一课 7.10 — 跨文件共享全局常量（使用内联变量）](Chapter-7/lesson7.10-sharing-global-constants-across-multiple-files-using-inline-variables.md)