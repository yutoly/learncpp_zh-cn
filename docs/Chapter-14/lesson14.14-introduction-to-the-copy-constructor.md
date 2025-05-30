14.14 — 拷贝构造函数简介  
=============================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月19日（首次发布于2007年11月4日）  

考虑以下程序：  
```
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // 默认构造函数（Default constructor）
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };  // 调用 Fraction(int, int) 构造函数
    Fraction fCopy { f }; // 这里调用什么构造函数？

    f.print();
    fCopy.print();

    return 0;
}
```  
您可能会惊讶地发现这个程序能正常编译，并产生以下结果：  
```
Fraction(5, 3)
Fraction(5, 3)
```  

让我们仔细分析这个程序的工作原理。变量`f`的初始化是标准的大括号初始化，调用了`Fraction(int, int)`构造函数。但下一行呢？变量`fCopy`的初始化显然也是初始化操作，而您知道构造函数用于初始化类对象。那么这行代码调用了哪个构造函数？  

答案是：**拷贝构造函数（copy constructor）**。  

拷贝构造函数  
----------------  
**拷贝构造函数**是用于通过同类型现有对象来初始化新对象的构造函数。拷贝构造函数执行后，新创建的对象应该是传入初始化对象的副本。  

隐式拷贝构造函数  
----------------  
如果未为类提供拷贝构造函数，C++会自动生成一个公共的**隐式拷贝构造函数（implicit copy constructor）**。在上例中，语句`Fraction fCopy { f };`正是通过隐式拷贝构造函数用`f`来初始化`fCopy`。  

默认情况下，隐式拷贝构造函数会执行**成员级初始化（memberwise initialization）**。这意味着每个成员都将使用传入初始化对象对应的成员进行初始化。在上例中，`fCopy.m_numerator`使用`f.m_numerator`（值为`5`）初始化，`fCopy.m_denominator`使用`f.m_denominator`（值为`3`）初始化。  

拷贝构造函数执行后，`f`和`fCopy`的成员具有相同值，因此`fCopy`是`f`的副本。因此对两者调用`print()`会得到相同结果。  

定义自定义拷贝构造函数  
----------------  
我们也可以显式定义自己的拷贝构造函数。本节中，我们将让拷贝构造函数打印消息以证明其确实在执行拷贝操作。  

拷贝构造函数的定义形式如下：  
```
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // 默认构造函数
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    // 拷贝构造函数（copy constructor）
    Fraction(const Fraction& fraction)
        // 使用参数对象的对应成员初始化当前成员
        : m_numerator{ fraction.m_numerator }
        , m_denominator{ fraction.m_denominator }
    {
        std::cout << "拷贝构造函数被调用\n"; // 用于验证执行
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };  // 调用 Fraction(int, int) 构造函数
    Fraction fCopy { f }; // 调用 Fraction(const Fraction&) 拷贝构造函数

    f.print();
    fCopy.print();

    return 0;
}
```  
运行该程序将输出：  
```
拷贝构造函数被调用
Fraction(5, 3)
Fraction(5, 3)
```  

上述自定义拷贝构造函数在功能上与默认生成的版本等效，只是添加了输出语句以验证拷贝构造函数的调用。当用`f`初始化`fCopy`时会调用该拷贝构造函数。  

访问权限提示  
----------------  
访问控制以类为单位（而非对象）。这意味着类的成员函数可以访问任何同类对象的私有成员（而不仅是隐式对象）。  

我们在上述`Fraction`类的拷贝构造函数中利用了这一特性，直接访问参数`fraction`的私有成员。否则我们将无法直接访问这些成员（除非添加访问函数，这可能并非我们所愿）。  

拷贝构造函数的职责范围  
----------------  
拷贝构造函数不应执行除拷贝对象之外的操作。这是因为编译器在某些情况下可能优化掉拷贝构造函数的调用。如果依赖拷贝构造函数实现拷贝之外的行为，该行为可能无法保证执行。我们将在课程[14.15 — 类初始化与拷贝省略](Chapter-14/lesson14.15-class-initialization-and-copy-elision.md)中进一步讨论。  

最佳实践  
----------------  
拷贝构造函数除执行拷贝外不应产生副作用。  

优先使用隐式拷贝构造函数  
----------------  
与隐式默认构造函数（通常不符合需求）不同，隐式拷贝构造函数执行的成员级初始化通常正是我们需要的。因此在多数情况下，使用隐式拷贝构造函数完全合适。  

最佳实践  
----------------  
除非有特殊需求，否则优先使用隐式拷贝构造函数。  

动态内存分配案例  
----------------  
在讨论动态内存分配时（参见课程[21.13 — 浅拷贝与深拷贝](Chapter-21/lesson21.13-shallow-vs-deep-copying.md)），我们将看到需要重写拷贝构造函数的情形。  

拷贝构造函数的参数要求  
----------------  
拷贝构造函数的参数必须是左值引用或常量左值引用。由于拷贝构造函数不应修改参数，建议使用常量左值引用。  

最佳实践  
----------------  
编写自定义拷贝构造函数时，参数应使用常量左值引用。  

传值与拷贝构造函数  
----------------  
当对象按值传递时，实参会被拷贝到形参。当实参与形参为同类类型时，拷贝操作通过隐式调用拷贝构造函数完成。  

以下示例说明该过程：  
```
#include <iostream>

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    // 默认构造函数
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }, m_denominator{ denominator }
    {
    }

    // 拷贝构造函数
    Fraction(const Fraction& fraction)
        : m_numerator{ fraction.m_numerator }
        , m_denominator{ fraction.m_denominator }
    {
        std::cout << "拷贝构造函数被调用\n";
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

void printFraction(Fraction f) // f 为传值参数
{
    f.print();
}

int main()
{
    Fraction f{ 5, 3 };

    printFraction(f); // 通过拷贝构造函数将 f 拷贝到函数参数

    return 0;
}
```  
作者机器上该示例输出：  
```
拷贝构造函数被调用
Fraction(5, 3)
```  

上例中，`printFraction(f)`的调用按值传递`f`。拷贝构造函数被调用来将`main`中的`f`拷贝到函数`printFraction()`的参数`f`中。  

返回值与拷贝构造函数  
----------------  
在课程[2.5 — 局部作用域简介](Chapter-2/lesson2.5-introduction-to-local-scope.md)中我们提到，按值返回会创建传递给调用者的临时对象（保存返回值拷贝）。当返回类型与返回值同类时，临时对象通过隐式调用拷贝构造函数初始化。  

例如：  
```
#include <iostream>

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    // 默认构造函数
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }, m_denominator{ denominator }
    {
    }

    // 拷贝构造函数
    Fraction(const Fraction& fraction)
        : m_numerator{ fraction.m_numerator }
        , m_denominator{ fraction.m_denominator }
    {
        std::cout << "拷贝构造函数被调用\n";
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

void printFraction(Fraction f) // f 为传值参数
{
    f.print();
}

Fraction generateFraction(int n, int d)
{
    Fraction f{ n, d };
    return f;
}

int main()
{
    Fraction f2 { generateFraction(1, 2) }; // 使用拷贝构造函数返回 Fraction

    printFraction(f2); // 使用拷贝构造函数将 f2 拷贝到函数参数

    return 0;
}
```  
当`generateFraction`向`main`返回`Fraction`时，使用拷贝构造函数创建并初始化临时`Fraction`对象。由于该临时对象用于初始化`Fraction f2`，这会再次调用拷贝构造函数将临时对象拷贝到`f2`。当`f2`被传递给`printFraction()`时，第三次调用拷贝构造函数。  

在作者机器上，该示例输出：  
```
拷贝构造函数被调用
拷贝构造函数被调用
拷贝构造函数被调用
Fraction(1, 2)
```  

如果编译并执行该示例，您可能发现只发生两次拷贝构造函数调用。这是称为*拷贝省略（copy elision）*的编译器优化。我们将在课程[14.15 — 类初始化与拷贝省略](Chapter-14/lesson14.15-class-initialization-and-copy-elision.md)中进一步讨论。  

使用`= default`生成默认拷贝构造函数  
----------------  
如果类没有拷贝构造函数，编译器会隐式生成。我们也可以使用`= default`语法显式要求编译器生成默认拷贝构造函数：  
```
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // 默认构造函数
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    // 显式请求生成默认拷贝构造函数
    Fraction(const Fraction& fraction) = default;

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };
    Fraction fCopy { f };

    f.print();
    fCopy.print();

    return 0;
}
```  

使用`= delete`禁止拷贝  
----------------  
有时我们希望禁止特定类的对象拷贝。可以通过`= delete`语法将拷贝构造函数标记为已删除来实现：  
```
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // 默认构造函数
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    // 删除拷贝构造函数以禁止拷贝
    Fraction(const Fraction& fraction) = delete;

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };
    Fraction fCopy { f }; // 编译错误：拷贝构造函数已被删除

    return 0;
}
```  
在此示例中，当编译器寻找用于通过`f`初始化`fCopy`的构造函数时，会发现拷贝构造函数已被删除，导致编译错误。  

附注  
----------------  
也可以通过将拷贝构造函数设为私有来禁止公开拷贝（私有函数无法被公开使用）。但私有拷贝构造函数仍可被类其他成员使用，因此除非有此需求，否则不建议采用此方案。  

高阶阅读  
----------------  
**三法则（rule of three）**是C++的著名原则，指出若类需要用户定义的拷贝构造函数、析构函数或拷贝赋值运算符，则可能三者皆需。在C++11中，该原则扩展为**五法则（rule of five）**，新增移动构造函数和移动赋值运算符。  

不遵循三法则/五法则可能导致代码故障。我们将在讨论动态内存分配时重提这些原则。析构函数相关内容见课程[15.4 — 析构函数简介](Chapter-15/lesson15.4-introduction-to-destructors.md)和[19.3 — 析构函数](Chapter-15/lesson15.4-introduction-to-destructors.md)，拷贝赋值运算符见课程[21.12 — 重载赋值运算符](Chapter-21/lesson21.12-overloading-the-assignment-operator.md)。  

测验时间  
----------------  
**问题1**  
上文提到拷贝构造函数的参数必须为（const）引用。为何不允许使用传值方式？  
[查看提示](javascript:void(0))  
<details><summary>提示</summary>思考按值传递类类型参数时的过程。</details>  
  
<details><summary>答案</summary>按值传递类类型参数时，会隐式调用拷贝构造函数将实参拷贝到形参。若拷贝构造函数使用传值方式，拷贝构造函数需要调用自身来拷贝初始化参数，导致无限递归调用。</details>  

[下一课14.15 类初始化与拷贝省略](Chapter-14/lesson14.15-class-initialization-and-copy-elision.md)  
[返回主页](/)  
[上一课14.13 临时类对象](Chapter-14/lesson14.13-temporary-class-objects.md)