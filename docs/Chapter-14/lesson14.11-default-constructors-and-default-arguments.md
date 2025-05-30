14.11 — 默认构造函数与默认参数  
===================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年9月16日（首次发布于2023年9月11日）  

**默认构造函数（default constructor）**是不接受任何参数的构造函数。通常指没有参数的用户定义构造函数。以下示例类包含默认构造函数：  
```
#include <iostream>

class Foo
{
public:
    Foo() // 默认构造函数
    {
        std::cout << "Foo 默认构造\n";
    }
};

int main()
{
    Foo foo{}; // 无初始化值，调用 Foo 的默认构造函数

    return 0;
}
```
程序运行时，创建`Foo`类型对象。由于未提供初始化值，调用默认构造函数`Foo()`，输出：  
```
Foo 默认构造

```  

类类型的值初始化与默认初始化对比  
----------------  
若类类型具有默认构造函数，值初始化（value initialization）和默认初始化（default initialization）都会调用该构造函数。因此对于上述`Foo`类，以下两种方式等效：  
```
    Foo foo{};  // 值初始化，调用 Foo() 默认构造函数
    Foo foo2;   // 默认初始化，调用 Foo() 默认构造函数
```  
但如[13.9 — 默认成员初始化](Chapter-13/lesson13.9-default-member-initialization.md)所述，值初始化对聚合类（aggregate）更安全。由于判断类是否为聚合类较为困难，对所有类类型使用值初始化更为稳妥。  

**最佳实践**  
对所有类类型优先使用值初始化。  

带默认参数的构造函数  
----------------  
与其他函数类似，构造函数最右侧参数可设置默认参数。  

**相关内容**  
我们已在课程[11.5 — 默认参数](Chapter-11/lesson11.5-default-arguments.md)中讨论默认参数。  

示例：  
```
#include <iostream>

class Foo
{
private:
    int m_x { };
    int m_y { };

public:
    Foo(int x=0, int y=0) // 含默认参数
        : m_x { x }
        , m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") 构造\n";
    }
};

int main()
{
    Foo foo1{};     // 使用默认参数调用 Foo(int, int)
    Foo foo2{6, 7}; // 调用 Foo(int, int)

    return 0;
}
```  
输出：  
```
Foo(0, 0) 构造
Foo(6, 7) 构造

```  
若构造函数所有参数都有默认值，则该构造函数即为默认构造函数（因可不传参数调用）。下节课[14.12 — 委托构造函数](Chapter-14/lesson14.12-delegating-constructors.md)将展示其应用场景。  

构造函数重载  
----------------  
构造函数支持重载（overloaded），即通过不同方式构造对象：  
```
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo() // 默认构造函数
    {
        std::cout << "Foo 构造\n";
    }

    Foo(int x, int y) // 非默认构造函数
        : m_x { x }, m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") 构造\n";
    }
};

int main()
{
    Foo foo1{};     // 调用 Foo()
    Foo foo2{6, 7}; // 调用 Foo(int, int)

    return 0;
}
```  
推论：类只能有一个默认构造函数。若存在多个默认构造函数，编译器无法确定使用哪个：  
```
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo() // 默认构造函数
    {
        std::cout << "Foo 构造\n";
    }

    Foo(int x=1, int y=2) // 默认构造函数
        : m_x { x }, m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") 构造\n";
    }
};

int main()
{
    Foo foo{}; // 编译错误：构造函数调用歧义

    return 0;
}
```  
编译器发现两个默认构造函数后，将产生歧义错误。  

隐式默认构造函数  
----------------  
非聚合类（non-aggregate）若无用户声明构造函数，编译器会生成公共默认构造函数（以便进行值或默认初始化），称为**隐式默认构造函数（implicit default constructor）**。示例：  
```
#include <iostream>

class Foo
{
private:
    int m_x{};
    int m_y{};

    // 注意：未声明构造函数
};

int main()
{
    Foo foo{};

    return 0;
}
```  
编译器生成的隐式默认构造函数等效于无参数、无成员初始化列表、无函数体的构造函数。即生成：  
```
public:
    Foo() // 隐式生成的默认构造函数
    {
    }
```  
隐式默认构造函数主要适用于无数据成员的类。若类含数据成员，通常需要用户提供初始化值，此时隐式默认构造函数无法满足需求。  

使用`= default`生成显式默认构造函数  
----------------  
当需要与隐式默认构造函数等效的默认构造函数时，可使用`= default`语法让编译器生成，称为**显式默认构造函数（explicitly defaulted default constructor）**：  
```
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo() = default; // 生成显式默认构造函数

    Foo(int x, int y)
        : m_x { x }, m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") 构造\n";
    }
};

int main()
{
    Foo foo{}; // 调用 Foo() 默认构造函数

    return 0;
}
```  
由于已声明`Foo(int, int)`构造函数，编译器通常不会生成隐式默认构造函数。但通过`= default`显式要求后，编译器会生成默认构造函数。  

**最佳实践**  
优先使用显式默认构造函数（`= default`）而非空函数体的默认构造函数。  

显式默认构造函数 vs 空用户定义构造函数  
----------------  
显式默认构造函数与空用户定义构造函数在以下两种情况下表现不同：  
1. **值初始化时**：  
   - 用户定义默认构造函数 → 对象默认初始化  
   - 非用户提供默认构造函数（隐式定义或`= default`） → 对象先零初始化（zero-initialized）再默认初始化  

```
#include <iostream>

class User
{
private:
    int m_a; // 注意：无默认初始化值
    int m_b {};

public:
    User() {} // 用户定义空构造函数

    int a() const { return m_a; }
    int b() const { return m_b; }
};

class Default
{
private:
    int m_a; // 注意：无默认初始化值
    int m_b {};

public:
    Default() = default; // 显式默认构造函数

    int a() const { return m_a; }
    int b() const { return m_b; }
};

class Implicit
{
private:
    int m_a; // 注意：无默认初始化值
    int m_b {};

public:
    // 隐式默认构造函数

    int a() const { return m_a; }
    int b() const { return m_b; }
};

int main()
{
    User user{}; // 默认初始化
    std::cout << user.a() << ' ' << user.b() << '\n';

    Default def{}; // 先零初始化，再默认初始化
    std::cout << def.a() << ' ' << def.b() << '\n';

    Implicit imp{}; // 先零初始化，再默认初始化
    std::cout << imp.a() << ' ' << imp.b() << '\n';

    return 0;
}
```  
作者机器输出：  
```
782510864 0
0 0
0 0

```  
`user.a`未进行零初始化，保持未初始化状态。  

**提示**  
应为所有数据成员提供默认成员初始值！  

**性能提示**  
对于无用户提供默认构造函数的类：  
- 值初始化会先进行零初始化  
- 默认初始化不会  

若需优化大量此类对象的初始化性能，可考虑改用默认初始化。或为类添加空函数体的默认构造函数以避免零初始化，但可能影响其他优化。  

2. **C++20之前**：  
   - 用户定义默认构造函数 → 类变为非聚合类  
   - 显式默认构造函数 → 类保持聚合类  

C++20起，两者均使类变为非聚合类。  

合理使用默认构造函数  
----------------  
默认构造函数允许用户无初始化值创建非聚合类对象。因此，仅当类对象适合使用默认值创建时才应提供默认构造函数。  

示例：  
```
#include <iostream>

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    Fraction() = default;
    Fraction(int numerator, int denominator)
        : m_numerator{ numerator }
        , m_denominator{ denominator }
    {
    }

    void print() const
    {
        std::cout << "分数(" << m_numerator << "/" << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f1 {3, 5};
    f1.print();

    Fraction f2 {}; // 得到 0/1
    f2.print();

    return 0;
}
```  
对于分数类，允许创建默认分数（0/1）是合理的。  

反例：  
```
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{ };
    int m_id{ };

public:
    Employee(std::string_view name, int id)
        : m_name{ name }
        , m_id{ id }
    {
    }

    void print() const
    {
        std::cout << "员工(" << m_name << ", ID:" << m_id << ")\n";
    }
};

int main()
{
    Employee e1 { "张三", 1 };
    e1.print();

    Employee e2 {}; // 编译错误：无匹配构造函数
    e2.print();

    return 0;
}
```  
员工类不应允许创建无名员工，故不提供默认构造函数。  

[下一课 14.12 委托构造函数](Chapter-14/lesson14.12-delegating-constructors.md)  
[返回主页](/)  
[上一课 14.10 构造函数成员初始化列表](Chapter-14/lesson14.10-constructor-member-initializer-lists.md)