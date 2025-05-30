21.5 — 使用成员函数重载运算符  
====================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2023年10月30日（首次发布于2007年10月11日）  

在课程[21.2 — 使用友元函数重载算术运算符](Chapter-21/lesson21.2-overloading-the-arithmetic-operators-using-friend-functions.md)中，我们学习了如何通过友元函数重载算术运算符。此外还了解到运算符也可以作为普通函数进行重载。但许多运算符可以通过另一种方式重载：作为成员函数（member function）。  

使用成员函数重载运算符与使用友元函数（friend function）的方法非常相似。当使用成员函数重载运算符时：  

* 重载的运算符必须作为左操作数的成员函数添加  
* 左操作数成为隐式*this对象  
* 其他操作数成为函数参数  

回忆一下之前使用友元函数重载operator+的例子：  

```cpp
#include <iostream>

class Cents
{
private:
    int m_cents {};

public:
    Cents(int cents)
        : m_cents { cents } { }

    // 重载Cents + int
    friend Cents operator+(const Cents& cents, int value);

    int getCents() const { return m_cents; }
};

// 注意：此函数不是成员函数！
Cents operator+(const Cents& cents, int value)
{
    return Cents(cents.m_cents + value);
}

int main()
{
	const Cents cents1 { 6 };
	const Cents cents2 { cents1 + 2 };
	std::cout << "I have " << cents2.getCents() << " cents.\n";
 
	return 0;
}
```  

将友元重载运算符转换为成员重载运算符的步骤：  

1. 将重载运算符定义为成员函数而非友元（使用Cents::operator+代替friend operator+）  
2. 移除左参数，因为该参数现在成为隐式*this对象  
3. 在函数体内，所有对左参数的引用需改为访问成员变量（例如cents.m_cents改为m_cents）  

以下是使用成员函数方法重载的相同运算符：  

```cpp
#include <iostream>

class Cents
{
private:
    int m_cents {};

public:
    Cents(int cents)
        : m_cents { cents } { }

    // 重载Cents + int
    Cents operator+(int value) const;

    int getCents() const { return m_cents; }
};

// 注意：此函数是成员函数！
// 友元版本中的cents参数现在成为隐式*this参数
Cents Cents::operator+ (int value) const
{
    return Cents { m_cents + value };
}

int main()
{
	const Cents cents1 { 6 };
	const Cents cents2 { cents1 + 2 };
	std::cout << "I have " << cents2.getCents() << " cents.\n";
 
	return 0;
}
```  

注意运算符的使用方式保持不变（都是`cents1 + 2`），我们只是以不同方式定义了函数。原来的双参数友元函数变成了单参数成员函数，友元版本中最左侧参数（cents）在成员函数版本中成为隐式*this参数。  

让我们仔细分析表达式`cents1 + 2`的求值过程：  

* 在友元函数版本中，表达式转换为函数调用operator+(cents1, 2)，包含两个参数  
* 在成员函数版本中，表达式转换为函数调用cents1.operator+(2)。由于编译器会将对象前缀转换为隐式左参数*this，实际调用等价于operator+(&cents1, 2)  

两种方式最终产生相同结果，只是实现路径不同。  

## 选择友元函数还是成员函数  

**不能作为友元函数重载的情况**  
赋值（=）、下标（[]）、函数调用（()）和成员选择（->）运算符必须作为成员函数重载，这是语言规范要求的。  

**不能作为成员函数重载的情况**  
在课程[21.4 — 重载I/O运算符](Chapter-21/lesson21.4-overloading-the-io-operators.md)中，我们使用友元函数方法为Point类重载了operator<<。此时无法使用成员函数，因为左操作数是std::ostream类型，而我们不能修改标准库中的类定义。  

同理，虽然可以将operator+(Cents, int)重载为成员函数，但不能将operator+(int, Cents)作为成员函数，因为int不是可添加成员函数的类。  

**何时使用普通函数/友元函数/成员函数重载**  
大多数情况下，语言允许自由选择重载形式，但通常某种方式会更合适：  

* 对于不修改左操作数的二元运算符（如operator+），优先选择普通函数或友元函数，因为它们适用于所有参数类型（包括左操作数不可修改的情况），且保持参数对称性  
* 对于会修改左操作数的二元运算符（如operator+=），优先选择成员函数。此时左操作数始终是类类型，使用*this指代被修改对象更自然  
* 一元运算符通常作为成员函数重载，因为成员版本无需参数  

经验法则：  

1. 重载赋值（=）、下标（[]）、函数调用（()）、成员选择（->）时，必须使用成员函数  
2. 重载一元运算符时，使用成员函数  
3. 重载不修改左操作数的二元运算符时，优先使用普通函数或友元函数  
4. 重载修改左操作数的二元运算符但无法修改左操作数类定义时（如operator<<），使用普通函数或友元函数  
5. 重载修改左操作数的二元运算符且可修改左操作数类定义时（如operator+=），使用成员函数  

[下一课 21.6 重载一元运算符+, -, 和!](Chapter-21/lesson21.6-overloading-unary-operators.md)  
[返回主页](/)  
[上一课 21.4 重载I/O运算符](Chapter-21/lesson21.4-overloading-the-io-operators.md)