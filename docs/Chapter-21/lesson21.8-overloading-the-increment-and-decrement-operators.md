21.8 — 递增与递减运算符的重载  
=========================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2007年10月15日 PDT上午8:19  
2023年11月25日  

重载递增（`++`）与递减（`--`）运算符的过程相对直观，但存在一个特殊细节。这两个运算符实际包含两种版本：前缀递增/递减（如`++x; --y;`）与后缀递增/递减（如`x++; y--;`）。  

由于递增和递减运算符均为一元运算符且会修改操作数，它们最适合以成员函数形式重载。我们将首先处理前缀版本，因为它们的实现最为直接。  

**重载前缀递增与递减运算符**  
----------------  

前缀递增和递减运算符的重载方式与常规一元运算符完全相同。通过示例进行说明：  

```cpp  
#include <iostream>

class Digit
{
private:
    int m_digit{};
public:
    Digit(int digit=0)
        : m_digit{digit}
    {
    }

    Digit& operator++();    // 前缀递增
    Digit& operator--();    // 前缀递减

    friend std::ostream& operator<< (std::ostream& out, const Digit& d);
};

Digit& Digit::operator++()
{
    // 若数字已达9，循环回0
    if (m_digit == 9)
        m_digit = 0;
    // 否则正常递增
    else
        ++m_digit;

    return *this;
}

Digit& Digit::operator--()
{
    // 若数字已达0，循环至9
    if (m_digit == 0)
        m_digit = 9;
    // 否则正常递减
    else
        --m_digit;

    return *this;
}

std::ostream& operator<< (std::ostream& out, const Digit& d)
{
	out << d.m_digit;
	return out;
}

int main()
{
    Digit digit { 8 };

    std::cout << digit;
    std::cout << ++digit;
    std::cout << ++digit;
    std::cout << --digit;
    std::cout << --digit;

    return 0;
}
```  

这个`Digit`类存储0-9之间的数字。我们通过重载运算符实现了循环递增/递减功能。  

该程序输出：  
```
89098  
```  

注意我们返回了`*this`。重载的递增递减运算符返回当前对象本身，从而支持运算符链式调用。  

**重载后缀递增与递减运算符**  
----------------  

通常，函数重载要求参数数量或类型不同。但对于前缀和后缀版本的运算符，两者名称相同（如`operator++`）、均为一元运算符且参数类型相同。C++语言规范为此提供了特殊解决方案：若重载运算符包含int类型参数，则视为后缀版本；若无参数则为前缀版本。  

以下是包含前后缀重载的完整`Digit`类：  

```cpp  
class Digit
{
private:
    int m_digit{};
public:
    Digit(int digit=0)
        : m_digit{digit}
    {
    }

    Digit& operator++();    // 前缀版本无参数
    Digit& operator--();    // 前缀版本无参数

    Digit operator++(int);  // 后缀版本带int参数（哑元）
    Digit operator--(int);  // 后缀版本带int参数（哑元）

    friend std::ostream& operator<< (std::ostream& out, const Digit& d);
};

// 前缀递增实现
Digit& Digit::operator++()
{
    if (m_digit == 9)
        m_digit = 0;
    else
        ++m_digit;

    return *this;
}

// 前缀递减实现
Digit& Digit::operator--()
{
    if (m_digit == 0)
        m_digit = 9;
    else
        --m_digit;

    return *this;
}

// 后缀递增实现（int参数为哑元）
Digit Digit::operator++(int)
{
    Digit temp{*this};  // 保存当前状态
    ++(*this);          // 应用前缀递增
    return temp;        // 返回保存的旧状态
}

// 后缀递减实现（int参数为哑元）
Digit Digit::operator--(int)
{
    Digit temp{*this};  // 保存当前状态
    --(*this);          // 应用前缀递减
    return temp;        // 返回保存的旧状态
}

std::ostream& operator<< (std::ostream& out, const Digit& d)
{
	out << d.m_digit;
	return out;
}

int main()
{
    Digit digit { 5 };

    std::cout << digit;
    std::cout << ++digit;   // 调用前缀递增
    std::cout << digit++;   // 调用后缀递增
    std::cout << digit;
    std::cout << --digit;   // 调用前缀递减
    std::cout << digit--;   // 调用后缀递减
    std::cout << digit;

    return 0;
}
```  

该程序输出：  
```
5667665  
```  

关键点说明：  
1. 通过int哑元参数区分后缀版本  
2. 后缀版本需返回修改前的状态，因此创建临时变量保存旧值  
3. 后缀操作通过调用前缀操作实现，减少代码重复  
4. 后缀版本返回非引用类型（不能返回局部变量的引用）  
5. 后缀操作效率低于前缀操作（涉及临时对象构造与值返回）  

[下一课 21.9 下标运算符的重载](Chapter-21/lesson21.9-overloading-the-subscript-operator.md)  
[返回主页](/)  
[上一课 21.7 比较运算符的重载](Chapter-21/lesson21.7-overloading-the-comparison-operators.md)