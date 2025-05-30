14.16 — 转换构造函数与explicit关键字  
=========================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月1日（首次发布于2016年6月5日）  

在课程[10.1 — 隐式类型转换](Chapter-10/lesson10.1-implicit-type-conversion.md)中，我们介绍了类型转换和隐式类型转换的概念。当需要时，编译器会将一种类型的值隐式转换为另一种类型（前提是存在这样的转换）。例如：  
```
#include <iostream>

void printDouble(double d) // 参数为double类型
{
    std::cout << d;
}

int main()
{
    printDouble(5); // 传入int类型参数

    return 0;
}
```  
上例中，`printDouble`函数的参数是`double`类型，但我们传入的是`int`类型参数。由于参数类型不匹配，编译器会尝试将`int`值`5`隐式转换为`double`值`5.0`。  

用户定义转换  
----------------  

考虑以下类似示例：  
```
#include <iostream>

class Foo
{
private:
    int m_x{};
public:
    Foo(int x)
        : m_x{ x }
    {
    }

    int getX() const { return m_x; }
};

void printFoo(Foo f) // 参数为Foo类型
{
    std::cout << f.getX();
}

int main()
{
    printFoo(5); // 传入int类型参数

    return 0;
}
```  
本例中，`printFoo`的参数是`Foo`类型但传入的是`int`类型。编译器需要将`int`值`5`隐式转换为`Foo`对象才能调用函数。这种转换称为**用户定义转换（user-defined conversion）**。  

转换构造函数  
----------------  

编译器通过查找`Foo(int)`构造函数来完成上述转换。这种用于隐式转换的构造函数称为**转换构造函数（converting constructor）**。默认情况下，所有构造函数都是转换构造函数。  

用户定义转换规则限制  
----------------  

考虑以下示例：  
```
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{};

public:
    Employee(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() const { return m_name; }
};

void printEmployee(Employee e) // 参数为Employee类型
{
    std::cout << e.getName();
}

int main()
{
    printEmployee("Joe"); // 传入C风格字符串字面量

    return 0;
}
```  
此例需要两次用户定义转换：  
1. C风格字符串 → `std::string_view`  
2. `std::string_view` → `Employee`  

由于C++只允许单次用户定义转换，因此编译失败。解决方法：  
1. 使用`std::string_view`字面量：  
```cpp
    printEmployee("Joe"sv); // 使用sv后缀
```  
2. 显式构造`Employee`对象：  
```cpp
    printEmployee(Employee{ "Joe" });
```  

关键洞察  
----------------  
通过直接列表初始化（direct list initialization）可以将隐式转换显式化。  

转换构造函数的潜在问题  
----------------  
考虑以下程序：  
```
#include <iostream>

class Dollars
{
private:
    int m_dollars{};

public:
    Dollars(int d)
        : m_dollars{ d }
    {
    }

    int getDollars() const { return m_dollars; }
};

void print(Dollars d)
{
    std::cout << "$" << d.getDollars();
}

int main()
{
    print(5); // 隐式转换为Dollars

    return 0;
}
```  
输出：  
```
$5
```  
这种隐式转换可能导致意外行为，例如调用者可能期望输出`5`而非`$5`。  

explicit关键字  
----------------  
使用**explicit**关键字可禁用构造函数的隐式转换功能：  
```cpp
class Dollars
{
public:
    explicit Dollars(int d) // 显式构造函数
        : m_dollars{ d }
    {
    }
    // ...
};

int main()
{
    print(5); // 编译错误：无法隐式转换
    print(Dollars{5}); // 正确：显式构造
    return 0;
}
```  

显式构造函数特性：  
* 不能用于拷贝初始化或拷贝列表初始化  
* 不能用于隐式转换  

返回值与显式构造函数  
----------------  
函数返回值时，若类型不匹配会尝试隐式转换，但不会使用显式构造函数：  
```cpp
class Foo
{
public:
    explicit Foo(int x) {}
};

Foo getFoo()
{
    return 5;        // 错误：无法隐式转换
    return Foo{5};   // 正确
}
```  

最佳实践  
----------------  
* **默认**将接受单个参数的构造函数设为`explicit`  
* **不要**为拷贝/移动构造函数添加`explicit`  
* **通常不**需要为以下构造函数添加`explicit`：  
  - 无参默认构造函数  
  - 接受多个参数的构造函数  

例外情况：当类型转换语义等价且高效时，可考虑允许隐式转换。例如`std::string_view`的C字符串构造函数未标记`explicit`。  

最佳实践建议：  
默认将接受单个参数的构造函数设为显式。如果隐式转换在语义上等价且高效，可考虑设为非显式。  

[下一课14.17 — constexpr聚合与类](Chapter-14/lesson14.17-constexpr-aggregates-and-classes.md)  
[返回主页](/)  
[上一课14.15 — 类初始化与拷贝省略](Chapter-14/lesson14.15-class-initialization-and-copy-elision.md)