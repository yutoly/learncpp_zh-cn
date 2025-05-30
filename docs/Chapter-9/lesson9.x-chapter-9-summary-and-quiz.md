9.x — 第9章总结与测验  
=================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看Alex的所有文章")  
2023年12月28日，太平洋标准时间下午2:45  
2024年12月1日  

章节回顾  
----------------  
**范围蔓延（Scope creep）**发生在项目能力超出初始规划时。  
**软件验证（Software verification）**是测试软件在所有场景下是否符合预期的过程。  
**单元测试（Unit test）**指隔离测试小段代码（通常为函数或调用）以确保特定行为符合预期。  
**单元测试框架（Unit test frameworks）**可协助组织单元测试。  
**集成测试（Integration testing）**测试多个单元组合以确保其协同工作。  
**代码覆盖率（Code coverage）**指测试中执行的源代码比例。  
**语句覆盖率（Statement coverage）**指测试覆盖的程序语句百分比。  
**分支覆盖率（Branch coverage）**指测试覆盖的分支百分比。  
**循环覆盖率（Loop coverage）**（亦称**0、1、2测试（0, 1, 2 test）**）要求循环在迭代0次、1次和2次时均能正常工作。  
**快乐路径（Happy path）**指无错误发生的执行流程。  
**悲伤路径（Sad path）**指出现错误或失败状态的执行流程。  
**不可恢复错误（Non-recoverable error）**（或称**致命错误（Fatal error）**）指严重到程序无法继续运行的错误。  
能妥善处理错误情况的程序具有**健壮性（Robust）**。  
**缓冲区（Buffer）**是为临时存储传输数据而预留的内存区域。  
检查用户输入是否符合程序预期的过程称为**输入验证（Input validation）**。  
**std::cerr**是专用于错误消息的输出流（类似`std::cout`）。  
**前置条件（Precondition）**指代码段执行前必须恒真的条件。  
**不变式（Invariant）**指组件执行期间必须恒真的条件。  
**后置条件（Postcondition）**指代码段执行后必须恒真的条件。  
**断言（Assertion）**是程序中除非存在缺陷否则恒真的表达式。C++运行时断言通常通过**assert**预处理宏实现，非调试代码中通常禁用断言。  
**static_assert**是编译时评估的断言。  
断言应用于记录逻辑上不可能发生的情况，错误处理应用于处理可能发生的情况。  

测验时间  
----------------  
**问题 #1**  
在课程[8.x — 第8章总结与测验](Chapter-8/lesson8.x-chapter-8-summary-and-quiz.md)的测验中，我们实现了猜数字游戏（Hi-Lo）。  
更新您的解决方案以处理无效猜测（如'x'）、越界猜测（如`0`或`101`）或含额外字符的有效猜测（如`43x`）。同时处理游戏询问是否重玩时用户输入的多余字符。  
提示：编写独立函数处理用户猜测输入及相关错误处理。  
  
```
#include <iostream>
#include <limits>   // for std::numeric_limits
#include "Random.h" // global-random-numbers-random-h/

int getGuess(int count, int min, int max)
{
	while (true) // 循环直至用户输入有效值
	{
		std::cout << "Guess #" << count << ": ";

		int guess {};
		std::cin >> guess;

		bool success { std::cin };
		std::cin.clear(); // 恢复至正常操作模式（如需要）
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // 清除额外输入

		// 若未提取数据或猜测越界，则重试
		if (!success || guess < min || guess > max)
			continue;

		return guess;
	}
}

// 用户获胜返回true，失败返回false
bool playHiLo(int guesses, int min, int max)
{
	std::cout << "Let's play a game. I'm thinking of a number between " << min << " and " << max << ". You have " << guesses << " tries to guess what it is.\n";
	int number{ Random::get(min, max) }; // 用户需猜测的数字

	// 遍历所有猜测机会
	for (int count{ 1 }; count <= guesses; ++count)
	{
		int guess{ getGuess(count, min, max) };

		if (guess > number)
			std::cout << "Your guess is too high.\n";
		else if (guess < number)
			std::cout << "Your guess is too low.\n";
		else // 猜中数字，用户获胜
		{
			std::cout << "Correct! You win!\n";
			return true;
		}
	}

	// 用户失败
	std::cout << "Sorry, you lose. The correct number was " << number << '\n';
	return false;
}

bool playAgain()
{
	// 循环询问用户是否重玩直至输入y或n
	while (true)
	{
		char ch{};
		std::cout << "Would you like to play again (y/n)? ";
		std::cin >> ch;

		// 清除额外输入
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        
		switch (ch)
		{
		case 'y': return true;
		case 'n': return false;
		}
	}
}

int main()
{
	constexpr int guesses { 7 }; // 用户猜测次数
	constexpr int min     { 1 };
	constexpr int max     { 100 };

	do
	{
		playHiLo(guesses, min, max);
	} while (playAgain());

	std::cout << "Thank you for playing.\n";

	return 0;
}
```
[下一课 10.1 隐式类型转换](Chapter-10/lesson10.1-implicit-type-conversion.md)  
[返回主页](/)  
[上一课 9.6 assert与static_assert](Chapter-9/lesson9.6-assert-and-static_assert.md)