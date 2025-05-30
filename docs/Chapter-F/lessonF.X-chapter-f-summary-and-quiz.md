F.X — 章节F总结与测验  
================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月2日  

**constexpr函数（constexpr function）**是允许在常量表达式中调用的函数。将函数声明为constexpr只需在返回类型前添加`constexpr`关键字。当用于需要常量表达式的上下文中时，constexpr函数保证在编译期求值；否则可能在编译期（若符合条件）或运行期求值。constexpr函数隐式内联（inline），编译器需看到其完整定义才能在编译期调用。  

**consteval函数（consteval function）**是必须在编译期求值的函数，其他规则与constexpr函数相同。  

测验时间  
----------------  

**问题1**  
为以下程序添加`const`和/或`constexpr`修饰符：  

```cpp
#include <iostream>

// 从用户获取塔高并返回
double getTowerHeight()
{
	std::cout << "输入塔的高度（米）：";
	double towerHeight{};
	std::cin >> towerHeight;
	return towerHeight;
}

// 计算"seconds"秒后球的离地高度
double calculateBallHeight(double towerHeight, int seconds)
{
	double gravity{ 9.8 };

	double distanceFallen{ (gravity * (seconds * seconds)) / 2.0 };
	double currentHeight{ towerHeight - distanceFallen };

	return currentHeight;
}

// 打印球的当前高度
void printBallHeight(double ballHeight, int seconds)
{
	if (ballHeight > 0.0)
		std::cout << seconds << "秒时，球的高度：" << ballHeight << "米\n";
	else
		std::cout << seconds << "秒时，球已落地\n";
}

// 辅助函数：计算并打印球的高度
void printCalculatedBallHeight(double towerHeight, int seconds)
{
	double ballHeight{ calculateBallHeight(towerHeight, seconds) };
	printBallHeight(ballHeight, seconds);
}

int main()
{
	double towerHeight{ getTowerHeight() };

	printCalculatedBallHeight(towerHeight, 0);
	printCalculatedBallHeight(towerHeight, 1);
	printCalculatedBallHeight(towerHeight, 2);
	printCalculatedBallHeight(towerHeight, 3);
	printCalculatedBallHeight(towerHeight, 4);
	printCalculatedBallHeight(towerHeight, 5);

	return 0;
}
```  

<details><summary>参考答案</summary>  

```cpp
#include <iostream>

// 此函数不应设为constexpr，因输入输出仅支持运行时
double getTowerHeight()
{
	std::cout << "输入塔的高度（米）：";
	double towerHeight{};
	std::cin >> towerHeight;
	return towerHeight;
}

// 声明为constexpr：仅通过输入参数进行计算
// 注意：函数参数本身不是constexpr，但函数可被编译期调用
constexpr double calculateBallHeight(double towerHeight, int seconds)
{
	constexpr double gravity{ 9.8 }; // 编译期常量

	const double distanceFallen{ (gravity * (seconds * seconds)) / 2.0 };
	const double currentHeight{ towerHeight - distanceFallen };

	return currentHeight;
}

// 保持非constexpr：涉及输出操作
void printBallHeight(double ballHeight, int seconds)
{
	if (ballHeight > 0.0)
		std::cout << seconds << "秒时，球的高度：" << ballHeight << "米\n";
	else
		std::cout << seconds << "秒时，球已落地\n";
}

// 保持非constexpr：调用非constexpr函数
void printCalculatedBallHeight(double towerHeight, int seconds)
{
	const double ballHeight{ calculateBallHeight(towerHeight, seconds) };
	printBallHeight(ballHeight, seconds);
}

int main()
{
	const double towerHeight{ getTowerHeight() }; // 运行期常量

	printCalculatedBallHeight(towerHeight, 0);
	// ...其余调用保持不变...
	return 0;
}
```  
</details>  

[下一课 12.1 — 复合数据类型简介](Chapter-12/lesson12.1-introduction-to-compound-data-types.md)  
[返回主页](/)    
[上一课 F.4 — Constexpr函数（第四部分）](Chapter-F/lessonF.4-constexpr-functions-part-4.md)