21.12 — 重载赋值运算符  
============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年7月22日（首次发布于2016年6月5日）  

**复制赋值运算符**（operator=）用于将值从一个对象复制到*已存在的另一个对象*。  

> **相关内容**  
> 自C++11起支持"移动赋值（Move assignment）"，详见课程[22.3 — 移动构造函数与移动赋值](Chapter-22/lesson22.3-move-constructors-and-move-assignment.md)。  

**复制赋值 vs 复制构造函数**  
复制构造函数与复制赋值运算符的功能几乎相同——都用于对象复制。但复制构造函数用于初始化新对象，而赋值运算符替换现有对象的内容。  

两者的区别常使新手困惑，但本质并不复杂：  
* 若需先创建新对象再进行复制，则使用复制构造函数（包括传值或返回对象时）  
* 若无需创建新对象即可完成复制，则使用赋值运算符  

**重载赋值运算符**  
重载复制赋值运算符（operator=）相对简单，但需注意特定注意事项。复制赋值运算符必须作为成员函数重载。  

```cpp
#include <cassert>
#include <iostream>

class Fraction
{
private:
	int m_numerator { 0 };
	int m_denominator { 1 };

public:
	// 默认构造函数
	Fraction(int numerator = 0, int denominator = 1 )
		: m_numerator { numerator }, m_denominator { denominator }
	{
		assert(denominator != 0);
	}

	// 复制构造函数
	Fraction(const Fraction& copy)
		: m_numerator { copy.m_numerator }, m_denominator { copy.m_denominator }
	{
		std::cout << "复制构造函数被调用\n";
	}

	// 重载赋值运算符
	Fraction& operator= (const Fraction& fraction);

	friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);
        
};

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
}

// 简易实现（下文将展示优化版本）
Fraction& Fraction::operator= (const Fraction& fraction)
{
    // 执行复制
    m_numerator = fraction.m_numerator;
    m_denominator = fraction.m_denominator;

    // 返回当前对象以支持链式调用
    return *this;
}

int main()
{
    Fraction fiveThirds { 5, 3 };
    Fraction f;
    f = fiveThirds; // 调用重载赋值运算符
    std::cout << f;

    return 0;
}
```  
输出：  
```
5/3
```  

重载的operator=返回\*this以支持链式赋值：  
```cpp
int main()
{
    Fraction f1 { 5, 3 };
    Fraction f2 { 7, 2 };
    Fraction f3 { 9, 5 };

    f1 = f2 = f3; // 链式赋值
    return 0;
}
```  

**自赋值问题**  
C++允许自赋值：  
```cpp
int main()
{
    Fraction f1 { 5, 3 };
    f1 = f1; // 自赋值
    return 0;
}
```  
在简易实现中，成员变量被赋给自身，虽无实际影响但浪费时间。但对于需要动态分配内存的类，自赋值可能引发危险：  

```cpp
#include <algorithm> 
#include <iostream>

class MyString
{
private:
	char* m_data {};
	int m_length {};

public:
	MyString(const char* data = nullptr, int length = 0 )
		: m_length { std::max(length, 0) }
	{
		if (length)
		{
			m_data = new char[static_cast<std::size_t>(length)];
			std::copy_n(data, length, m_data);
		}
	}
	~MyString()
	{
		delete[] m_data;
	}

	MyString(const MyString&) = default;

	// 重载赋值运算符
	MyString& operator= (const MyString& str);

	friend std::ostream& operator<<(std::ostream& out, const MyString& s);
};

std::ostream& operator<<(std::ostream& out, const MyString& s)
{
	out << s.m_data;
	return out;
}

// 有缺陷的实现（勿用）
MyString& MyString::operator= (const MyString& str)
{
	if (m_data) delete[] m_data;

	m_length = str.m_length;
	m_data = nullptr;

	if (m_length)
		m_data = new char[static_cast<std::size_t>(str.m_length)];

	std::copy_n(str.m_data, m_length, m_data);
	return *this;
}

int main()
{
	MyString alex("Alex", 5); 
	alex = alex; // 自赋值
	std::cout << alex; // 输出乱码
	return 0;
}
```  
当对象自我赋值时，m_data与str.m_data指向相同内存。删除m_data后，str.m_data成为悬垂指针（dangling pointer），导致后续复制无效数据。  

**检测与处理自赋值**  
优化后的实现增加自检机制：  
```cpp
MyString& MyString::operator= (const MyString& str)
{
	// 自赋值检查
	if (this == &str)
		return *this;

	if (m_data) delete[] m_data;

	m_length = str.m_length;
	m_data = nullptr;

	if (m_length)
		m_data = new char[static_cast<std::size_t>(str.m_length)];

	std::copy_n(str.m_data, m_length, m_data);
	return *this;
}
```  
通过检查对象地址，避免不必要的操作。此检查仅涉及指针比较，性能开销小。  

**无需处理自赋值的情况**  
1. 复制构造函数通常无需自检，因为新对象初始化时自我复制会触发编译器警告  
2. 能自然处理自赋值的类（如Fraction类），可省略自检：  
```cpp
Fraction& Fraction::operator= (const Fraction& fraction)
{
    // 即使无自检，下列赋值仍安全
    m_numerator = fraction.m_numerator; 
    m_denominator = fraction.m_denominator; 
    return *this;
}
```  

**拷贝和交换惯用法（Copy and swap idiom）**  
更优解决方案是使用拷贝和交换惯用法，详见[Stack Overflow详解](https://stackoverflow.com/questions/3279543/what-is-the-copy-and-swap-idiom)。  

**隐式复制赋值运算符**  
若未自定义赋值运算符，编译器会生成隐式公有版本，执行成员级赋值。可通过设为私有或使用delete禁用：  
```cpp
class Fraction
{
public:
	Fraction& operator= (const Fraction& fraction) = delete;
};

int main()
{
    Fraction f;
    f = fiveThirds; // 编译错误
    return 0;
}
```  
含const成员的类，编译器将隐式operator=设为delete。若需赋值，需显式重载并逐个赋值非const成员。  

[下一课 21.13 浅拷贝与深拷贝](Chapter-21/lesson21.13-shallow-vs-deep-copying.md)  
[返回主页](/)  
[上一课 21.11 重载类型转换](Chapter-21/lesson21.11-overloading-typecasts.md)