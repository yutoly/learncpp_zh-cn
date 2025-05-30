8.4 — constexpr if语句  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年5月30日 PDT下午5:18  
2024年3月5日  

 

常规情况下，if语句的条件表达式会在运行时求值。

但考虑以下条件表达式为常量表达式的情况：

```cpp
#include <iostream>

int main()
{
	constexpr double gravity{ 9.8 };

	// 提醒：相同类型的低精度浮点数字面量可进行相等性测试
	if (gravity == 9.8) // 常量表达式，始终为真
		std::cout << "地球重力正常。\n";   // 该语句始终执行
	else
		std::cout << "当前不在地球环境。\n"; // 该语句永不执行

	return 0;
}
```

由于`gravity`是constexpr变量且初始化为`9.8`，条件表达式`gravity == 9.8`必然求值为`true`。因此else语句永远不会执行。

在运行时计算constexpr条件表达式是冗余的（因为结果不会变化），同时将永远不会执行的代码编译进可执行文件也是资源浪费。

C++17的constexpr if语句  
---------------- 

C++17引入了**constexpr if语句（constexpr if statement）**，其条件表达式必须是常量表达式。constexpr if语句的条件将在编译时求值。

若constexpr条件求值为`true`，整个if-else结构将替换为true分支语句。若求值为`false`，则替换为else分支语句（若存在）或不做任何处理（若无else分支）。

使用constexpr if语句时，需在`if`关键字后添加`constexpr`限定符：

```cpp
#include <iostream>

int main()
{
	constexpr double gravity{ 9.8 };

	if constexpr (gravity == 9.8) // 现在使用constexpr if
		std::cout << "地球重力正常。\n";
	else
		std::cout << "当前不在地球环境。\n";

	return 0;
}
```

上述代码编译时，编译器将在编译阶段求值条件表达式，判断其始终为`true`，因此仅保留`std::cout << "地球重力正常。\n";`语句。

最终生成的代码等效于：

```cpp
int main()
{
	constexpr double gravity{ 9.8 };

	std::cout << "地球重力正常。\n";

	return 0;
}
```

最佳实践  
---------------- 

当条件表达式为常量表达式时，优先选用constexpr if语句而非非constexpr if语句。

现代编译器与含constexpr条件的if语句（C++17）  
---------------- 

出于优化目的，现代编译器通常会将含有constexpr条件表达式的非constexpr if语句视作constexpr if语句处理。但此行为并非语言标准强制要求。

编译器在遇到含constexpr条件的非constexpr if语句时，可能发出警告提示改用`if constexpr`。这能确保编译时求值必然发生（即使关闭优化选项）。

[下一课 8.5 — switch语句基础](Chapter-8/lesson8.5-switch-statement-basics.md)  
[返回主页](/)  
[上一课 8.3 — 常见if语句问题](Chapter-8/lesson8.3-common-if-statement-problems.md)