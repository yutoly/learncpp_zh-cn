21.2 — 使用友元函数重载算术运算符  
===============================================

[*亚历克斯*](https://www.learncpp.com/author/Alex/ "查看亚历克斯的所有文章")  
2007年9月26日 PDT上午11:36（2024年10月21日更新）  

C++中最常用的运算符之一是算术运算符——即加号运算符（+）、减号运算符（-）、乘号运算符（*）和除号运算符（/）。这些算术运算符都是二元运算符，意味着它们需要两个操作数——运算符两侧各一个。这四个运算符的重载方式完全相同。

运算符重载有三种不同方式：成员函数方式、友元函数方式和普通函数方式。本章重点讲解友元函数方式（因其对多数二元运算符更直观），下一课讨论普通函数方式，后续课程将覆盖成员函数方式并详细总结各方法适用场景。

使用友元函数重载运算符  
----------------  

考虑以下类定义：
```
class Cents
{
private:
	int m_cents {};

public:
	Cents(int cents) : m_cents{ cents } { }
	int getCents() const { return m_cents; }
};
```
以下示例演示如何重载加号运算符实现两个Cents对象相加：
```
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	Cents(int cents) : m_cents{ cents } { }

	// 使用友元函数实现Cents + Cents
	friend Cents operator+(const Cents& c1, const Cents& c2);

	int getCents() const { return m_cents; }
};

// 注意：此函数不是成员函数！
Cents operator+(const Cents& c1, const Cents& c2)
{
	// 使用Cents构造函数和整型加法
	// 友元函数可直接访问私有成员
	return c1.m_cents + c2.m_cents;
}

int main()
{
	Cents cents1{ 6 };
	Cents cents2{ 8 };
	Cents centsSum{ cents1 + cents2 };
	std::cout << "我有 " << centsSum.getCents() << " 分.\n";

	return 0;
}
```
输出结果：
```
我有 14 分.

```
重载加号运算符只需声明名为operator+的函数，指定两个操作数类型并选择合适返回类型。对于Cents类，operator+的实现十分简单：参数类型为两个Cents对象，返回类型为Cents，函数体直接相加m_cents成员（友元函数可访问私有成员）。

减号运算符的重载方法类似：
```
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	explicit Cents(int cents) : m_cents{ cents } { }

	// 友元函数实现加法
	friend Cents operator+(const Cents& c1, const Cents& c2);

	// 友元函数实现减法
	friend Cents operator-(const Cents& c1, const Cents& c2);

	int getCents() const { return m_cents; }
};

Cents operator+(const Cents& c1, const Cents& c2)
{
	return Cents { c1.m_cents + c2.m_cents };
}

Cents operator-(const Cents& c1, const Cents& c2)
{
	return Cents { c1.m_cents - c2.m_cents };
}

int main()
{
	Cents cents1{ 6 };
	Cents cents2{ 2 };
	Cents centsSum{ cents1 - cents2 };
	std::cout << "我有 " << centsSum.getCents() << " 分.\n";

	return 0;
}
```
乘号（*）和除号（/）运算符的重载方式与上述示例相同。

在类内定义友元函数  
----------------  
友元函数即使定义在类内部也不属于类成员：
```
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	explicit Cents(int cents) : m_cents{ cents } { }

	// 类内定义的友元函数
	friend Cents operator+(const Cents& c1, const Cents& c2)
	{
		return Cents { c1.m_cents + c2.m_cents };
	}

	int getCents() const { return m_cents; }
};
```
这种方式适合实现简单的运算符重载。

不同类型操作数的运算符重载  
----------------  
当操作数类型不同时，需为每种组合编写重载函数。例如Cents(4) + 6调用operator+(Cents, int)，而6 + Cents(4)调用operator+(int, Cents)：
```
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	explicit Cents(int cents) : m_cents{ cents } { }

	// Cents + int
	friend Cents operator+(const Cents& c1, int value);

	// int + Cents
	friend Cents operator+(int value, const Cents& c1);

	int getCents() const { return m_cents; }
};

Cents operator+(const Cents& c1, int value)
{
	return Cents { c1.m_cents + value };
}

Cents operator+(int value, const Cents& c1)
{
	return Cents { c1.m_cents + value };
}

int main()
{
	Cents c1{ Cents{ 4 } + 6 };
	Cents c2{ 6 + Cents{ 4 } };

	std::cout << "我有 " << c1.getCents() << " 分.\n";
	std::cout << "我有 " << c2.getCents() << " 分.\n";

	return 0;
}
```

另一个示例：MinMax类  
----------------  
```
#include <iostream>

class MinMax
{
private:
	int m_min {}; // 当前最小值
	int m_max {}; // 当前最大值

public:
	MinMax(int min, int max) : m_min{ min }, m_max{ max } { }

	int getMin() const { return m_min; }
	int getMax() const { return m_max; }

	friend MinMax operator+(const MinMax& m1, const MinMax& m2);
	friend MinMax operator+(const MinMax& m, int value);
	friend MinMax operator+(int value, const MinMax& m);
};

MinMax operator+(const MinMax& m1, const MinMax& m2)
{
	int min = (m1.m_min < m2.m_min) ? m1.m_min : m2.m_min;
	int max = (m1.m_max > m2.m_max) ? m1.m_max : m2.m_max;
	return MinMax { min, max };
}

MinMax operator+(const MinMax& m, int value)
{
	int min = (m.m_min < value) ? m.m_min : value;
	int max = (m.m_max > value) ? m.m_max : value;
	return MinMax { min, max };
}

MinMax operator+(int value, const MinMax& m)
{
	return m + value; // 复用已有运算符
}

int main()
{
	MinMax mFinal{ m1 + m2 + 5 + 8 + m3 + 16 };
	std::cout << "结果: (" << mFinal.getMin() << ", " << mFinal.getMax() << ")\n";
	return 0;
}
```
输出结果：
```
结果: (3, 16)

```
该表达式从左至右求值，每次运算生成临时MinMax对象作为后续运算的左操作数。

通过其他运算符实现运算符  
----------------  
operator+(int, MinMax)通过调用operator+(MinMax, int)实现，减少代码冗余。建议在保持代码简洁的前提下复用现有运算符。

测验  
----------------  
**问题1a**  
编写Fraction类：
```
#include <iostream>

class Fraction
{
private:
	int m_numerator { 0 };
	int m_denominator { 1 };

public:
	explicit Fraction(int numerator, int denominator=1)
		: m_numerator{numerator}, m_denominator{denominator}
	{
	}

	void print() const
	{
		std::cout << m_numerator << '/' << m_denominator << '\n';
	}
};
```

**问题1b**  
添加乘法运算符重载：
```
friend Fraction operator*(const Fraction& f1, const Fraction& f2);
friend Fraction operator*(const Fraction& f1, int value);
friend Fraction operator*(int value, const Fraction& f1);

// 实现
Fraction operator*(const Fraction& f1, const Fraction& f2)
{
	return Fraction{ f1.m_numerator * f2.m_numerator, f1.m_denominator * f2.m_denominator };
}

Fraction operator*(int value, const Fraction& f1)
{
	return f1 * value;
}
```

**问题1c**  
若构造函数改为非explicit并移除整型乘法运算符，程序仍能工作，因为整型参数会隐式转换为Fraction对象。

**问题1d**  
非const引用参数无法绑定到临时对象，导致表达式`Fraction{1,2} * Fraction{2,3}`编译失败。

**问题1e**  
添加约分功能：
```
#include <numeric>

void reduce()
{
	int gcd = std::gcd(m_numerator, m_denominator);
	if (gcd) {
		m_numerator /= gcd;
		m_denominator /= gcd;
	}
}
```

[下一课 21.3 使用普通函数重载运算符](Chapter-21/lesson21.3-overloading-operators-using-normal-functions.md)  
[返回主页](/)  
[上一课 21.1 运算符重载简介](Chapter-21/lesson21.1-introduction-to-operator-overloading.md)