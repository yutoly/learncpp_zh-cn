21.7 — 比较运算符的重载  
============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年10月4日下午5:10（太平洋夏令时）  
2024年2月7日  

在课程[6.7 — 关系运算符与浮点数比较](Chapter-6/lesson6.7-relational-operators-and-floating-point-comparisons.md)中，我们探讨了六种比较运算符。重载这些运算符相对简单（注意到双关了吗？），因为它们遵循与其他运算符重载相同的模式。

由于比较运算符都是不修改左操作数的二元运算符，我们将重载的比较运算符设为友元函数（friend function）。

以下Car类示例重载了operator==和operator!=：

```cpp
#include <iostream>
#include <string>
#include <string_view>

class Car
{
private:
    std::string m_make;   // 厂商
    std::string m_model;  // 车型

public:
    Car(std::string_view make, std::string_view model)
        : m_make{ make }, m_model{ model }
    {
    }

    friend bool operator== (const Car& c1, const Car& c2);
    friend bool operator!= (const Car& c1, const Car& c2);
};

bool operator== (const Car& c1, const Car& c2)
{
    return (c1.m_make == c2.m_make &&
            c1.m_model == c2.m_model);
}

bool operator!= (const Car& c1, const Car& c2)
{
    return (c1.m_make != c2.m_make ||
            c1.m_model != c2.m_model);
}

int main()
{
    Car corolla{ "Toyota", "Corolla" };
    Car camry{ "Toyota", "Camry" };

    if (corolla == camry)
        std::cout << "Corolla与Camry相同\n";

    if (corolla != camry)
        std::cout << "Corolla与Camry不同\n";

    return 0;
}
```
此处的代码逻辑应清晰明了。

那么operator<和operator>呢？如何定义汽车"大于"或"小于"另一辆汽车？这通常不符合直观认知。由于operator<和operator>的结果缺乏直接意义，最好不定义这些运算符。

> **最佳实践**  
> 仅重载符合类语义直觉的运算符。

但存在一个常见例外：若需对Car列表排序，可能需要重载比较运算符以返回最可能用于排序的成员。例如，Car的operator<可基于厂商（make）和车型（model）按字母顺序排序。

标准库中的部分容器类（用于存储其他类的集合）要求重载operator<以保持元素有序。

以下是重载全部6个逻辑比较运算符的不同示例：

```cpp
#include <iostream>

class Cents // 美分类
{
private:
    int m_cents; // 美分数值
 
public:
    Cents(int cents)
	: m_cents{ cents }
	{}
 
    friend bool operator== (const Cents& c1, const Cents& c2);
    friend bool operator!= (const Cents& c1, const Cents& c2);

    friend bool operator< (const Cents& c1, const Cents& c2);
    friend bool operator> (const Cents& c1, const Cents& c2);

    friend bool operator<= (const Cents& c1, const Cents& c2);
    friend bool operator>= (const Cents& c1, const Cents& c2);
};

bool operator== (const Cents& c1, const Cents& c2)
{
    return c1.m_cents == c2.m_cents;
}

// 其他运算符实现类似...
```
此实现同样较为直接。

### 减少比较冗余  
注意上例中重载比较运算符的实现高度相似。重载比较运算符通常存在大量冗余，实现越复杂，冗余越多。

幸运的是，许多比较运算符可通过其他运算符实现：
* operator!= 可实现为 !(operator==)
* operator> 可调用operator<并交换参数顺序
* operator>= 可实现为 !(operator<)
* operator<= 可实现为 !(operator>)

这意味着只需实现operator==和operator<的逻辑，其余四个比较运算符可基于这两者定义！更新后的Cents示例如下：

```cpp
#include <iostream>

class Cents
{
private:
    int m_cents;

public:
    Cents(int cents)
        : m_cents{ cents }
    {}

    friend bool operator== (const Cents& c1, const Cents& c2) { return c1.m_cents == c2.m_cents; }
    friend bool operator!= (const Cents& c1, const Cents& c2) { return !(operator==(c1, c2)); }

    friend bool operator< (const Cents& c1, const Cents& c2) { return c1.m_cents < c2.m_cents; }
    friend bool operator> (const Cents& c1, const Cents& c2) { return operator<(c2, c1); }

    friend bool operator<= (const Cents& c1, const Cents& c2) { return !(operator>(c1, c2)); }
    friend bool operator>= (const Cents& c1, const Cents& c2) { return !(operator<(c1, c2)); }
};
```
此方式下，任何修改只需更新operator==和operator<，无需改动全部六个比较运算符！

### C++20的三路比较运算符（operator<=>）  
C++20引入的三路比较运算符（`operator<=>`）可将需编写的比较函数减少至最多两个，有时仅需一个！

> **作者注**  
> 我们将尽快新增相关课程。在此之前，请将此视为兴趣引子——更多内容需参考外部资源。

**测验时间**  
1. 为Fraction类添加六个比较运算符，使以下程序通过编译：
```cpp
#include <iostream>
#include <numeric> // 用于std::gcd

class Fraction // 分数类
{
private:
	int m_numerator{};   // 分子
	int m_denominator{}; // 分母

public:
	Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }, m_denominator{ denominator }
	{
		reduce(); // 在构造函数中约分确保新分数最简
	}

	void reduce() // 约分函数
	{
		int gcd{ std::gcd(m_numerator, m_denominator) };
		if (gcd)
		{
			m_numerator /= gcd;
			m_denominator /= gcd;
		}
	}

    // 比较运算符声明...
	friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);
};

// 实现示例（部分）：
bool operator< (const Fraction& f1, const Fraction& f2)
{
    return (f1.m_numerator * f2.m_denominator < f2.m_numerator * f1.m_denominator);
}
```

2. 为本课顶部的Car类添加重载operator<<和operator<，使以下程序通过编译：
```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main()
{
  std::vector<Car> cars{
    { "Toyota", "Corolla" },
    { "Honda", "Accord" },
    { "Toyota", "Camry" },
    { "Honda", "Civic" }
  };

  std::sort(cars.begin(), cars.end()); // 需重载operator<

  for (const auto& car : cars)
    std::cout << car << '\n'; // 需重载operator<<

  return 0;
}
```
程序应输出：
```
(Honda, Accord)
(Honda, Civic)
(Toyota, Camry)
(Toyota, Corolla)
```

[下一课 21.8 自增与自减运算符的重载](Chapter-21/lesson21.8-overloading-the-increment-and-decrement-operators.md)  
[返回主页](/)  
[上一课 21.6 一元运算符+, -和!的重载](Chapter-21/lesson21.6-overloading-unary-operators.md)