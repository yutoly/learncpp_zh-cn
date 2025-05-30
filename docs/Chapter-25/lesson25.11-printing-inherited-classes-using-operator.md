25.11 — 使用operator\<\<打印继承类  
======================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2016年11月23日 下午1:57（太平洋标准时间）  
2024年2月18日  

考虑以下使用虚函数（virtual function）的程序：  

```cpp
#include <iostream>

class Base
{
public:
    virtual void print() const { std::cout << "Base";  }
};

class Derived : public Base
{
public:
    void print() const override { std::cout << "Derived"; }
};

int main()
{
    Derived d{};
    Base& b{ d };
    b.print(); // 调用Derived::print()

    return 0;
}
```  

现在您应该理解`b.print()`会调用`Derived::print()`（因为b引用的是派生类对象，`Base::print()`是虚函数，`Derived::print()`是覆盖版本）。  

虽然通过成员函数输出是可行的，但这种风格与`std::cout`的配合不够优雅：  

```cpp
#include <iostream>

int main()
{
    Derived d{};
    Base& b{ d };

    std::cout << "b is a ";
    b.print(); // 需要中断输出语句来调用函数
    std::cout << '\n';

    return 0;
}
```  

本章将探讨如何为继承类重载（overload）operator\<\<，使其能像这样使用：  

```cpp
std::cout << "b is a " << b << '\n'; // 更优雅
```  

operator\<\<的挑战  
----------------  

首先按常规方式重载operator\<\<：  

```cpp
#include <iostream>

class Base
{
public:
    virtual void print() const { std::cout << "Base"; }

    friend std::ostream& operator<<(std::ostream& out, const Base& b)
    {
        out << "Base";
        return out;
    }
};

class Derived : public Base
{
public:
    void print() const override { std::cout << "Derived"; }

    friend std::ostream& operator<<(std::ostream& out, const Derived& d)
    {
        out << "Derived";
        return out;
    }
};

int main()
{
    Base b{};
    std::cout << b << '\n';

    Derived d{};
    std::cout << d << '\n';

    return 0;
}
```  

由于此处不需要虚函数解析（virtual function resolution），程序按预期输出：  

```
Base
Derived
```  

考虑以下main函数：  

```cpp
int main()
{
    Derived d{};
    Base& bref{ d };
    std::cout << bref << '\n';
    
    return 0;
}
```  

该程序输出：  

```
Base
```  

这是因为处理Base对象的operator\<\<版本不是虚函数，因此调用的是Base版本的operator\<\<。  

operator\<\<能否设为虚函数？  
----------------  

简短回答是否定的，主要原因如下：  

1. 只有成员函数（member function）可以是虚函数，而operator\<\<通常作为友元（friend）实现  
2. 即使可以设为虚函数，Base和Derived版本的operator\<\<参数不同（分别接受Base和Derived参数），Derived版本不会被视作覆盖（override）  

解决方案  
----------------  

通过一个简单的技巧实现：  

1. 在基类中按常规方式将operator\<\<设为友元  
2. 让operator\<\<调用可被虚化的普通成员函数  

第一个解决方案中，虚成员函数`identify()`返回`std::string`：  

```cpp
#include <iostream>

class Base
{
public:
    friend std::ostream& operator<<(std::ostream& out, const Base& b)
    {
        out << b.identify();
        return out;
    }

    virtual std::string identify() const
    {
        return "Base";
    }
};

class Derived : public Base
{
public:
    std::string identify() const override
    {
        return "Derived";
    }
};

int main()
{
    Base b{};
    std::cout << b << '\n';

    Derived d{};
    std::cout << d << '\n'; // 即使没有处理Derived的operator<<也能工作

    Base& bref{ d };
    std::cout << bref << '\n';

    return 0;
}
```  

输出预期结果：  

```
Base
Derived
Derived
```  

更灵活的解决方案  
----------------  

改进方案定义虚成员函数`print()`，直接将打印任务委托给它：  

```cpp
#include <iostream>

class Base
{
public:
    friend std::ostream& operator<<(std::ostream& out, const Base& b)
    {
        return b.print(out);
    }

    virtual std::ostream& print(std::ostream& out) const
    {
        out << "Base";
        return out;
    }
};

struct Employee
{
    std::string name{};
    int id{};

    friend std::ostream& operator<<(std::ostream& out, const Employee& e)
    {
        out << "Employee(" << e.name << ", " << e.id << ")";
        return out;
    }
};

class Derived : public Base
{
private:
    Employee m_e{};

public:
    Derived(const Employee& e)
        : m_e{ e }
    {
    }

    std::ostream& print(std::ostream& out) const override
    {
        out << "Derived: ";
        out << m_e;
        return out;
    }
};

int main()
{
    Base b{};
    std::cout << b << '\n';

    Derived d{ Employee{"Jim", 4}};
    std::cout << d << '\n';

    Base& bref{ d };
    std::cout << bref << '\n';

    return 0;
}
```  

输出：  

```
Base
Derived: Employee(Jim, 4)
Derived: Employee(Jim, 4)
```  

此版本中，`Derived::print()`可以使用流对象调用`Employee::operator<<`打印成员变量。  

[下一课 25.x — 第25章总结与测验](Chapter-25/lesson25.x-chapter-25-summary-and-quiz.md)  
[返回主页](/)  
[上一课 25.10 — 动态转型](Chapter-25/lesson25.10-dynamic-casting.md)