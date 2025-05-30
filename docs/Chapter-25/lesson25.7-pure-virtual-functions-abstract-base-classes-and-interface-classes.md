25.7 — 纯虚函数、抽象基类与接口类  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年2月13日下午4:09（首次发布）  
2024年10月1日（最后更新）  

**纯虚（抽象）函数与抽象基类**  
到目前为止，我们编写的所有虚函数都包含函数体（定义）。然而，C++允许创建一种特殊的虚函数——**纯虚函数（pure virtual function）**（或称**抽象函数（abstract function）**），这种函数完全没有函数体！纯虚函数仅作为占位符存在，其目的是由派生类重新定义。

要创建纯虚函数，只需将函数赋值为0（而非定义函数体）：
```cpp
#include <string_view>

class Base
{
public:
    std::string_view sayHi() const { return "Hi"; } // 普通非虚函数    

    virtual std::string_view getName() const { return "Base"; } // 普通虚函数

    virtual int getValue() const = 0; // 纯虚函数

    int doSomething() = 0; // 编译错误：不能将非虚函数设为0
};
```
当我们向类添加纯虚函数时，实际上是在声明"该函数由派生类实现"。

使用纯虚函数会带来两个主要影响：
1. 包含一个或多个纯虚函数的类成为**抽象基类（abstract base class）**，这意味着无法实例化该类的对象！试想若允许创建Base实例会发生什么：
```cpp
int main()
{
    Base base {}; // 假设允许实例化抽象基类（实际不可行）
    base.getValue(); // 此处将如何执行？

    return 0;
}
```
由于getValue()没有定义，base.getValue()将无法解析。

2. 任何派生类必须为该函数提供实现，否则该派生类也将被视为抽象基类。

**纯虚函数示例**  
让我们通过示例理解纯虚函数的应用。在前面的课程中，我们编写了简单的Animal基类，并派生出Cat和Dog类。以下是当时的代码：
```cpp
#include <string>
#include <string_view>

class Animal
{
protected:
    std::string m_name {};

    // 将构造函数设为protected以禁止直接创建Animal实例
    // 但仍允许派生类使用该构造函数
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

public:
    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const { return "???"; }
    
    virtual ~Animal() = default;
};

class Cat: public Animal
{
public:
    Cat(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const override { return "Meow"; }
};

class Dog: public Animal
{
public:
    Dog(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const override { return "Woof"; }
};
```
我们通过protected构造函数防止直接创建Animal实例。然而，仍然可能创建未重定义speak()的派生类：
```cpp
#include <iostream>
#include <string>
#include <string_view>

class Animal
{
protected:
    std::string m_name {};

    Animal(std::string_view name)
        : m_name{ name }
    {
    }

public:
    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const { return "???"; }
    
    virtual ~Animal() = default;
};

class Cow : public Animal
{
public:
    Cow(std::string_view name)
        : Animal{ name }
    {
    }

    // 忘记重定义speak函数
};

int main()
{
    Cow cow{"Betsy"};
    std::cout << cow.getName() << " says " << cow.speak() << '\n';

    return 0;
}
```
输出结果：
```
Betsy says ???
```
更好的解决方案是使用纯虚函数：
```cpp
#include <string>
#include <string_view>

class Animal // 现在Animal是抽象基类
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const = 0; // 注意speak现在是纯虚函数
    
    virtual ~Animal() = default;
};
```
需要注意两点：首先，speak()成为纯虚函数使Animal成为抽象基类，因此不再需要protected构造函数（尽管保留无害）。其次，由于Cow类派生自Animal但未定义Cow::speak()，Cow也成为了抽象基类。编译以下代码时：
```cpp
#include <iostream>
#include <string>
#include <string_view>

class Animal // 抽象基类
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const = 0; // 纯虚函数
    
    virtual ~Animal() = default;
};

class Cow: public Animal
{
public:
    Cow(std::string_view name)
        : Animal{ name }
    {
    }

    // 忘记重定义speak
};

int main()
{
    Cow cow{ "Betsy" };
    std::cout << cow.getName() << " says " << cow.speak() << '\n';

    return 0;
}
```
编译器将报错：
```
prog.cc:35:9: 错误: 'Cow'类型变量是抽象类
   35 |     Cow cow{ "Betsy" };
      |         ^
prog.cc:17:30: 注意: 'Cow'类中未实现的纯虚方法'speak'
   17 |     virtual std::string_view speak() const = 0;
      |                              ^
```
只有为Cow类实现speak()后才能实例化：
```cpp
class Cow: public Animal
{
public:
    Cow(std::string_view name)
        : Animal(name)
    {
    }

    std::string_view speak() const override { return "Moo"; }
};

int main()
{
    Cow cow{ "Betsy" };
    std::cout << cow.getName() << " says " << cow.speak() << '\n';

    return 0;
}
```
现在程序输出：
```
Betsy says Moo
```
纯虚函数适用于需要将函数声明在基类但具体实现由派生类决定的情形。纯虚函数强制派生类必须实现该函数，否则无法实例化，从而避免遗漏实现。

通过基类引用（或指针）可以调用纯虚函数：
```cpp
int main()
{
    Cow cow{ "Betsy" };
    Animal& a{ cow };

    std::cout << a.speak(); // 虚函数解析至Cow::speak()，输出"Moo"

    return 0;
}
```
重要提醒：包含纯虚函数的类必须同时拥有虚析构函数。

**带定义的纯虚函数**  
实际上，可以为纯虚函数提供定义：
```cpp
#include <string>
#include <string_view>

class Animal // 抽象基类
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() { return m_name; }
    virtual std::string_view speak() const = 0; // =0表示纯虚函数
    
    virtual ~Animal() = default;
};

std::string_view Animal::speak() const  // 尽管有定义
{
    return "buzz";
}
```
此时speak()仍被视为纯虚函数（因有=0标记），Animal仍是抽象基类。派生类必须提供自己的speak()定义，否则仍为抽象基类。纯虚函数的定义必须单独提供（不能内联）。

对于Visual Studio用户：  
VS允许纯虚函数声明包含内联定义：
```cpp
virtual std::string_view speak() const = 0
{
  return "buzz";
}
```
此行为不符合C++标准且无法禁用。

该模式适用于希望基类提供默认实现，同时强制派生类自行实现的情况。若派生类满意基类实现，可直接调用基类版本：
```cpp
#include <iostream>
#include <string>
#include <string_view>

class Animal // 抽象基类
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name(name)
    {
    }

    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const = 0; // 纯虚函数
    
    virtual ~Animal() = default;
};

std::string_view Animal::speak() const
{
    return "buzz"; // 默认实现
}

class Dragonfly: public Animal
{
public:
    Dragonfly(std::string_view name)
        : Animal{name}
    {
    }

    std::string_view speak() const override // 已定义函数，不再是抽象类
    {
        return Animal::speak(); // 使用基类实现
    }
};

int main()
{
    Dragonfly dfly{"Sally"};
    std::cout << dfly.getName() << " says " << dfly.speak() << '\n';

    return 0;
}
```
输出：
```
Sally says buzz
```
此功能使用频率较低。析构函数可设为纯虚函数，但必须提供定义以便派生对象析构时调用。

**接口类**  
**接口类（interface class）**是指没有成员变量且所有函数均为纯虚函数的类！接口类用于定义派生类必须实现的功能，具体实现方式完全由派生类决定。

接口类通常以"I"开头命名。示例：
```cpp
#include <string_view>

class IErrorLog
{
public:
    virtual bool openLog(std::string_view filename) = 0;
    virtual bool closeLog() = 0;

    virtual bool writeError(std::string_view errorMessage) = 0;

    virtual ~IErrorLog() {} // 虚析构函数确保删除IErrorLog指针时正确调用派生类析构函数
};
```
继承自IErrorLog的类必须实现所有三个函数才能实例化。例如：
- FileErrorLog：openLog()打开磁盘文件，closeLog()关闭文件，writeError()写入消息
- ScreenErrorLog：openLog()和closeLog()无操作，writeError()在屏幕弹出窗口显示消息

使用接口类提升代码灵活性。比较以下两种实现方式：
```cpp
// 强制使用FileErrorLog
double mySqrt(double value, FileErrorLog& log)
{
    if (value < 0.0)
    {
        log.writeError("尝试对负数开平方");
        return 0.0;
    }
    return std::sqrt(value);
}

// 使用IErrorLog接口
double mySqrt(double value, IErrorLog& log)
{
    if (value < 0.0)
    {
        log.writeError("尝试对负数开平方");
        return 0.0;
    }
    return std::sqrt(value);
}
```
第二种实现允许调用者传递任何符合IErrorLog接口的类实例，极大提升灵活性和扩展性。接口类应包含虚析构函数以保证正确析构。

接口类因其易用性、可扩展性和可维护性而广受欢迎。Java和C#等现代语言专门提供了"interface"关键字来定义接口类，并支持多接口继承（尽管普通类不支持多继承）。

**纯虚函数与虚表（virtual table）**  
为保持一致性，抽象类仍拥有虚表。抽象类的构造函数或析构函数调用虚函数时，会正确解析到当前类的实现（此时派生类尚未构造或已被销毁）。

含纯虚函数的类的虚表条目通常包含空指针或指向打印错误信息的通用函数（有时名为__purecall）。

[下一课 25.8 虚基类](Chapter-25/lesson25.8-virtual-base-classes.md)  
[返回主页](/)  
[上一课 25.6 虚表](Chapter-25/lesson25.6-the-virtual-table.md)