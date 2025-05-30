8.15 — 全局随机数（Random.h）  
========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月29日（首次发布于2023年12月28日）  

当需要在多个函数或文件中使用随机数生成器时，如何实现？一种方法是在`main()`函数中创建（并播种）PRNG（伪随机数生成器），然后将其传递到所有需要的地方。但对于可能零散使用的功能来说，这种传递方式过于繁琐。让每个需要随机数的函数定义静态局部`std::mt19937`变量（静态以保证仅播种一次）也不理想——既冗余又可能影响生成质量。  

理想方案是创建一个全局共享的PRNG对象（置于命名空间中）。虽然通常不推荐使用非常量全局变量，但这是例外情况。以下是可包含在任何需要随机数功能的代码文件中的头文件解决方案：  

Random.h内容：  
```
#ifndef RANDOM_MT_H
#define RANDOM_MT_H

#include <chrono>
#include <random>

// 此头文件专用命名空间实现自播种梅森旋转算法（Mersenne Twister）
// 需C++17或更新标准
// 可被多个代码文件包含（inline关键字避免ODR违规）
namespace Random
{
	// 返回已播种的梅森旋转生成器
	// 注：优先返回std::seed_seq（用于初始化std::mt19937），但因不可复制故改用函数返回
	inline std::mt19937 generate()
	{
		std::random_device rd{};

		// 使用系统时钟和7个随机设备数创建种子序列
		std::seed_seq ss{
			static_cast<std::seed_seq::result_type>(std::chrono::steady_clock::now().time_since_epoch().count()),
				rd(), rd(), rd(), rd(), rd(), rd(), rd() };

		return std::mt19937{ ss };
	}

	// 全局std::mt19937对象
	// inline关键字确保整个程序仅有一个实例
	inline std::mt19937 mt{ generate() }; // 生成播种后的生成器并复制到全局对象

	// 生成[min, max]区间（含端点）的随机整数
        // * 处理参数类型不同但可转换为int的情况
	inline int get(int min, int max)
	{
		return std::uniform_int_distribution{min, max}(mt);
	}

	// 以下模板函数处理其他类型的随机数生成

	// 生成[min, max]区间（含端点）的随机值
	// * min与max必须同类型
	// * 返回值类型与参数相同
	// * 支持类型：
	// *    short、int、long、long long
	// *    unsigned short、unsigned int、unsigned long、unsigned long long
	template <typename T>
	T get(T min, T max)
	{
		return std::uniform_int_distribution<T>{min, max}(mt);
	}

	// 生成[min, max]区间（含端点）的随机值
	// * min与max可类型不同
        // * 必须显式指定返回类型为模板参数
	// * 参数将被转换为返回类型
	template <typename R, typename S, typename T>
	R get(S min, T max)
	{
		return get<R>(static_cast<R>(min), static_cast<R>(max));
	}
}

#endif
```  

使用步骤：  
1. 创建`Random.h`文件并添加上述代码  
2. 在需要随机数的.cpp文件中`#include "Random.h"`  
3. 调用`Random::get(min, max)`生成随机数（无需初始化）  

示例程序：  
```
#include "Random.h" 
#include <cstddef> 
#include <iostream>

int main()
{
	std::cout << Random::get(1, 6) << '\n';   // 生成1-6的int
	std::cout << Random::get(1u, 6u) << '\n'; // 生成1-6的unsigned int

	std::cout << Random::get<std::size_t>(1, 6u) << '\n'; // 显式指定返回类型

	// 直接使用全局生成器
	std::uniform_int_distribution die6{ 1, 6 }; // C++14需使用<> 
	for (int count{ 1 }; count <= 10; ++count)
	{
		std::cout << die6(Random::mt) << '\t'; 
	}

	std::cout << '\n';
	return 0;
}
```  

实现要点：  
- 通过`inline`关键字避免头文件多次包含导致的ODR（单一定义规则）违规  
- `generate()`函数整合系统时钟和随机设备生成种子序列，确保全局生成器的自播种特性  
- 模板函数提供灵活的类型支持，包括显式指定返回类型的功能  

相关课程：  
- 内联函数与变量：[7.9 — 内联函数与变量](Chapter-7/lesson7.9-inline-functions-and-variables.md)  

[下一课 8.x — 第八章总结与测验](Chapter-8/lesson8.x-chapter-8-summary-and-quiz.md)  
[返回主页](/)  
[上一课 8.14 — 使用梅森旋转算法生成随机数](Chapter-8/lesson8.14-generating-random-numbers-using-mersenne-twister.md)