14.12 — 委托构造函数（Delegating Constructors）
================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年9月7日上午9:22（PDT）首次发布，2025年1月21日修订  

在可能的情况下，我们应当遵循DRY原则（Don’t Repeat Yourself）减少冗余代码。考虑以下函数示例：
```
void A()
{
    // 执行任务A的语句
}

void B()
{
    // 执行任务A的语句
    // 执行任务B的语句
}
```
两个函数都包含执行相同任务A的语句。此时可以通过重构消除冗余：
```
void A()
{
    // 执行任务A的语句
}

void B()
{
    A();
    // 执行任务B的语句
}
```
这种重构使得维护更加容易，修改只需在单处完成。  

当类包含多个构造函数时，各构造函数的代码往往存在大量重复。类似地，我们也希望消除这种冗余。考虑以下示例：
```
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name { "???" };
    int m_id { 0 };
    bool m_isManager { false };

public:
    Employee(std::string_view name, int id) // 必须提供姓名和ID
        : m_name{ name }, m_id { id }
    {
        std::cout << "Employee " << m_name << " created\n";
    }

    Employee(std::string_view name, int id, bool isManager) // 可选是否为经理
        : m_name{ name }, m_id{ id }, m_isManager { isManager }
    {
        std::cout << "Employee " << m_name << " created\n";
    }
};

int main()
{
    Employee e1{ "James", 7 };
    Employee e2{ "Dave", 42, true };
}
```
每个构造函数的输出语句完全相同。  

> **作者注**  
> 通常不建议在构造函数中进行输出（调试目的除外），因为这会导致不需要输出的场景无法使用该构造函数。本例仅为演示目的使用。  

构造函数允许调用其他函数（包括类的成员函数）。重构如下：
```
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name { "???" };
    int m_id{ 0 };
    bool m_isManager { false };

    void printCreated() const // 新增辅助函数
    {
        std::cout << "Employee " << m_name << " created\n";
    }

public:
    Employee(std::string_view name, int id)
        : m_name{ name }, m_id { id }
    {
        printCreated(); // 在此处调用
    }

    Employee(std::string_view name, int id, bool isManager)
        : m_name{ name }, m_id{ id }, m_isManager { isManager }
    {
        printCreated(); // 在此处调用
    }
};

int main()
{
    Employee e1{ "James", 7 };
    Employee e2{ "Dave", 42, true };
}
```
虽然优于前版（冗余语句替换为函数调用），但仍需引入新函数。且两个构造函数都初始化了`m_name`和`m_id`，理想情况应消除这些冗余。  

在函数体内调用构造函数会创建临时对象  
尝试在`Employee(std::string_view, int, bool)`构造函数体内调用`Employee(std::string_view, int)`：
```
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name { "???" };
    int m_id { 0 };
    bool m_isManager { false };

public:
    Employee(std::string_view name, int id)
        : m_name{ name }, m_id { id } // 初始化姓名和ID
    {
        std::cout << "Employee " << m_name << " created\n";
    }

    Employee(std::string_view name, int id, bool isManager)
        : m_isManager { isManager } // 初始化m_isManager
    {
        Employee(name, id); // 预期外的临时对象创建
    }

    const std::string& getName() const { return m_name; }
};

int main()
{
    Employee e2{ "Dave", 42, true };
    std::cout << "e2 has name: " << e2.getName() << "\n"; // 输出e2.m_name
}
```
输出结果：
```
Employee Dave created
e2 has name: ???
```
问题在于：构造函数体执行时，对象已完成初始化。此时调用构造函数会创建临时对象（临时对象打印信息后即被销毁），当前对象（`e2`）的`m_name`和`m_id`未被修改。  

> **最佳实践**  
> 不应从函数体内直接调用构造函数，这会导致编译错误或临时对象创建。  

委托构造函数（Delegating Constructors）  
构造函数可通过成员初始化列表将初始化任务委托给同类其他构造函数，这称为**构造函数链（constructor chaining）**或**委托构造函数（delegating constructors）**。示例：
```
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name { "???" };
    int m_id { 0 };

public:
    Employee(std::string_view name)
        : Employee{ name, 0 } // 委托给Employee(std::string_view, int)
    {
    }

    Employee(std::string_view name, int id)
        : m_name{ name }, m_id { id } // 实际初始化成员
    {
        std::cout << "Employee " << m_name << " created\n";
    }
};

int main()
{
    Employee e1{ "James" };
    Employee e2{ "Dave", 42 };
}
```
当初始化`e1 { "James" }`时，构造函数`Employee(std::string_view)`通过成员初始化列表委托给`Employee(std::string_view, int)`，传递`"James"`和`0`。  

> **注意**  
> - 委托构造函数不可自行初始化成员，只能选择委托或初始化  
> - 通常参数较少的构造函数委托给参数较多的构造函数  
> - 避免循环委托导致栈溢出  

使用默认参数简化构造函数  
通过给参数设置默认值，可将多个构造函数合并：
```
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{};
    int m_id{ 0 }; // 默认成员初始化值

public:
    Employee(std::string_view name, int id = 0) // id的默认参数
        : m_name{ name }, m_id{ id }
    {
        std::cout << "Employee " << m_name << " created\n";
    }
};

int main()
{
    Employee e1{ "James" };
    Employee e2{ "Dave", 42 };
}
```
> **最佳实践**  
> 必须初始化的成员应定义为构造函数左参数，可选成员作为右参数。  

初始化值重复问题  
上述方法导致`m_id`的默认值重复定义（默认成员初始化和默认参数各一次）。目前无法直接引用默认成员初始化值。  

> **高级技巧**  
> 使用`static constexpr`成员定义命名常量：
```
class Employee
{
private:
    static constexpr int default_id { 0 }; // 定义命名常量
    
    std::string m_name {};
    int m_id { default_id }; // 此处使用

public:
    Employee(std::string_view name, int id = default_id) // 此处使用
        : m_name { name }, m_id { id }
    {
        std::cout << "Employee " << m_name << " created\n";
    }
};
```
这种方法通过共享的静态成员减少重复，但会增加类复杂度。静态成员详见[15.6 — 静态成员变量](Chapter-15/lesson15.6-static-member-variables.md)。  

测验  
问题1：实现Ball类  
```
#include <iostream>
#include <string>
#include <string_view>

class Ball
{
private:
    std::string m_color{ "black" };
    double m_radius{ 10.0 };

public:
    Ball() { print(); }
    Ball(double radius) : m_radius{ radius } { print(); }
    Ball(std::string_view color) : m_color{ color } { print(); }
    Ball(std::string_view color, double radius) : m_color{ color }, m_radius{ radius } { print(); }

    void print() const { std::cout << "Ball(" << m_color << ", " << m_radius << ")\n"; }
};
```
问题2：使用默认参数和委托构造函数简化  
```
class Ball
{
private:
    std::string m_color{ "black" };
    double m_radius{ 10.0 };

public:
    Ball(double radius) : Ball{ "black", radius } {}
    Ball(std::string_view color = "black", double radius = 10.0) : m_color{ color }, m_radius{ radius } { print(); }

    void print() const { std::cout << "Ball(" << m_color << ", " << m_radius << ")\n"; }
};
```

[下一课 14.13 临时类对象](Chapter-14/lesson14.13-temporary-class-objects.md)  
[返回主页](/)  
[上一课 14.11 默认构造函数与默认参数](Chapter-14/lesson14.11-default-constructors-and-default-arguments.md)