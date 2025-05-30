14.8 — 数据隐藏（封装）的优势  
===================================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2025年2月20日  
2023年9月11日 PDT 中午12:18  

 

在之前的课程（[14.5 — 公有成员与私有成员及访问说明符](Chapter-14/lesson14.5-public-and-private-members-and-access-specifiers.md)）中，我们提到类的成员变量通常应设为私有。初学类的程序员往往难以理解这种做法的意义。毕竟，将变量设为私有意味着外界无法直接访问。最理想情况下，这不过是编写类时需要多费些功夫；最糟糕时，这种做法似乎毫无意义（尤其当我们提供公共访问函数来操作私有成员数据时）。  

这个问题的答案至关重要，因此我们将用整节课来深入探讨！  

让我们从一个类比开始。  

现代生活中，我们使用各种机械或电子设备。您用遥控器开关电视，踩油门让汽车前进，拨动开关开启电灯。这些设备都有一个共同点：它们提供简单的用户界面（一组按钮、踏板、开关等）来执行关键操作。  

这些设备的实际运作原理对您来说是隐藏的。按下遥控器按钮时，您无需知道遥控器如何与电视通信；踩下汽车油门时，您无需了解内燃机如何驱动车轮；拍照时，您不用明白传感器如何采集光线并转换为像素图像。  

这种接口（interface）与实现（implementation）的分离极为有用，因为它允许我们无需理解对象的工作原理即可使用它们——只需知道如何与之交互。这极大降低了使用复杂度，并提升了我们可操作对象的数量。  

类类型中的接口与实现  
----------------  

基于类似原因，接口与实现的分离在编程中同样重要。但首先，我们需要明确类类型中接口与实现的定义。  

类类型的**接口（interface）**（或称**类接口（class interface）**）定义了用户如何与类对象交互。由于只有公有成员能从类外部访问，类的公有成员构成了其接口。因此，由公有成员组成的接口有时被称为**公共接口（public interface）**。  

接口是类作者与用户之间的隐式契约。若现有接口发生变更，任何使用它的代码都可能崩溃。因此，确保类接口设计良好且稳定（不频繁改动）至关重要。  

类类型的**实现（implementation）**包含真正使类按预期运行的代码。这包括存储数据的成员变量，以及包含程序逻辑和操作成员变量的成员函数体。  

数据隐藏  
----------------  

在编程中，**数据隐藏（data hiding）**（亦称**信息隐藏（information hiding）**或**数据抽象（data abstraction）**）是通过隐藏（使不可访问）程序定义数据类型的实现细节，来强制实现接口与实现分离的技术。  

在C++类类型中实施数据隐藏十分简单。首先，确保类的数据成员为私有（用户无法直接访问）。成员函数体内的语句本身已无法直接访问，因此无需额外处理。其次，确保成员函数为公有，以便用户调用。  

遵循这些规则后，我们强制类的用户通过公共接口操作对象，并阻止其直接访问实现细节。  

C++中定义的类应使用数据隐藏。实际上，标准库提供的所有类都遵循这一原则。而结构体（struct）则不应使用数据隐藏，因为非公有成员会阻碍其作为聚合类型使用。  

这种类定义方式需要类作者付出额外工作。要求用户通过公共接口操作看似比直接公开成员变量更繁琐，但这能带来诸多优势，有助于提升类的可重用性和可维护性。本节余下部分将讨论这些优势。  

术语说明  
----------------  

在编程中，**封装（encapsulation）**通常指以下两种情形之一：  
* 将一项或多项内容封装至某种容器中  
* 将数据与操作该数据的函数捆绑  

在C++中，包含数据和创建/操作对象的公共接口的类类型即被封装。由于封装是数据隐藏的前提，且数据隐藏是重要技术，传统上"封装"一词通常也包含数据隐藏。  

本系列教程中，我们默认所有封装类都实现数据隐藏。  

数据隐藏使类更易用并降低复杂度  
----------------  

使用封装类时，无需了解其实现细节。只需理解其接口：可用的公有成员函数、参数要求及返回值。  

例如：  
```cpp
#include <iostream>
#include <string_view>

int main()
{
    std::string_view sv{ "Hello, world!" };
    std::cout << sv.length();
    return 0;
}
```  

在此简短程序中，`std::string_view`的实现细节未向我们暴露。我们不知道`std::string_view`有多少数据成员、其名称或类型，也不清楚`length()`成员函数如何返回字符串长度。  

最妙的是我们无需知道！程序即可运行。只需了解如何初始化`std::string_view`对象及`length()`的返回值。  

无需关注这些细节能极大降低程序复杂度，从而减少错误。这是封装的最大优势。  

试想若必须理解`std::string`、`std::vector`或`std::cout`的实现才能使用，C++将变得何等复杂！  

数据隐藏便于维护不变式  
----------------  

在类介绍课程（[14.2 — 类简介](Chapter-14/lesson14.2-introduction-to-classes.md)）中，我们提到过*类不变式（class invariants）*的概念——这是对象生命周期中必须保持为真的条件，以确保对象处于有效状态。  

考虑以下程序：  
```cpp
#include <iostream>
#include <string>

struct Employee // 默认公有成员
{
    std::string name{ "John" };
    char firstInitial{ 'J' }; // 应与name首字母匹配

    void print() const
    {
        std::cout << "Employee " << name << " has first initial " << firstInitial << '\n';
    }
};

int main()
{
    Employee e{}; // 默认"John"和'J'
    e.print();

    e.name = "Mark"; // 修改员工名为"Mark"
    e.print(); // 打印错误首字母
    return 0;
}
```  

该程序输出：  
```
John has first initial J
Mark has first initial J
```  

我们的`Employee`结构体存在类不变式：`firstInitial`应始终等于`name`的首字符。若此条件不成立，`print()`函数将出错。  

由于`name`成员为公有，`main()`中的代码能将`e.name`设为`"Mark"`，而`firstInitial`未更新。不变式被破坏，第二次`print()`调用结果异常。  

当用户可直接访问类实现时，他们需负责维护所有不变式——而这可能无法正确完成。将这一负担加诸用户会增加大量复杂度。  

重写此程序，将成员变量设为私有，并通过成员函数设置姓名：  
```cpp
#include <iostream>
#include <string>
#include <string_view>

class Employee // 默认私有成员
{
    std::string m_name{};
    char m_firstInitial{};

public:
    void setName(std::string_view name)
    {
        m_name = name;
        m_firstInitial = name.front(); // 使用std::string::front()获取首字母
    }

    void print() const
    {
        std::cout << "Employee " << m_name << " has first initial " << m_firstInitial << '\n';
    }
};

int main()
{
    Employee e{};
    e.setName("John");
    e.print();

    e.setName("Mark");
    e.print();
    return 0;
}
```  

现在程序按预期工作：  
```
John has first initial J
Mark has first initial M
```  

用户视角的唯一变化是：不再直接赋值`name`，而是调用`setName()`来设置`m_name`和`m_firstInitial`。用户从此不必负责维护该不变式！  

数据隐藏支持更好的错误检测（与处理）  
----------------  

在上述程序中，`m_firstInitial`需匹配`m_name`首字母的不变式存在，是因为`m_firstInitial`独立于`m_name`存储。我们可通过将数据成员`m_firstInitial`替换为返回首字母的成员函数来消除该不变式：  
```cpp
#include <iostream>
#include <string>

class Employee
{
    std::string m_name{ "John" };

public:
    void setName(std::string_view name)
    {
        m_name = name;
    }

    // 使用std::string::front()获取m_name首字母
    char firstInitial() const { return m_name.front(); }

    void print() const
    {
        std::cout << "Employee " << m_name << " has first initial " << firstInitial() << '\n';
    }
};

int main()
{
    Employee e{}; // 默认"John"
    e.setName("Mark");
    e.print();
    return 0;
}
```  

但此程序仍有类不变式。请花时间找出它。我们将在此观看干油漆...  

答案是`m_name`不应为空字符串（因每位员工都应有姓名）。若`m_name`设为空字符串，虽不会立即出错，但调用`firstInitial()`时，`std::string`的`front()`将尝试获取空字符串首字母，导致未定义行为。  

理想情况下，我们希望阻止`m_name`被设为空。  

若用户能公开访问`m_name`成员，他们可直接设置`m_name = ""`，而我们无法阻止。  

但通过强制用户通过公共接口函数`setName()`设置`m_name`，我们可让`setName()`验证输入是否有效。若姓名非空，则赋值给`m_name`；若为空，可采取以下任一措施：  
* 忽略空值请求并返回  
* 触发断言  
* 抛出异常  
* 跳个舞（这个不算）  

关键点在于我们能检测误用，并以最合适方式处理。如何有效处理这类情况是后续课程主题。  

数据隐藏允许变更实现细节而不破坏现有程序  
----------------  

考虑简单示例：  
```cpp
#include <iostream>

struct Something
{
    int value1 {};
    int value2 {};
    int value3 {};
};

int main()
{
    Something something;
    something.value1 = 5;
    std::cout << something.value1 << '\n';
}
```  

此程序运行正常，但若变更类实现如下：  
```cpp
#include <iostream>

struct Something
{
    int value[3] {}; // 使用含3个值的数组
};

int main()
{
    Something something;
    something.value1 = 5;
    std::cout << something.value1 << '\n';
}
```  

由于尚未讲解数组，但重点在于程序不再编译，因为名为`value1`的成员已不存在，而`main()`中仍在使用该标识符。  

数据隐藏使我们能更改类实现而不破坏使用它们的程序。  

原始类的封装版本通过函数访问`m_value1`：  
```cpp
#include <iostream>

class Something
{
private:
    int m_value1 {};
    int m_value2 {};
    int m_value3 {};

public:
    void setValue1(int value) { m_value1 = value; }
    int getValue1() const { return m_value1; }
};

int main()
{
    Something something;
    something.setValue1(5);
    std::cout << something.getValue1() << '\n';
}
```  

现在将类实现改回数组：  
```cpp
#include <iostream>

class Something
{
private:
    int m_value[3]; // 注意：我们改变了类实现！

public:
    // 需更新成员函数以反映新实现
    void setValue1(int value) { m_value[0] = value; }
    int getValue1() const { return m_value[0]; }
};

int main()
{
    // 使用该类的程序无需修改！
    Something something;
    something.setValue1(5);
    std::cout << something.getValue1() << '\n';
}
```  

由于未改变公共接口，使用该接口的程序无需任何修改，仍可正常运行。  

类比来说，若小精灵夜间将电视遥控器内部更换为不同（但兼容）技术，您可能浑然不觉！  

带接口的类更易调试  
----------------  

最后，封装能帮助调试程序。当程序出错时，常因某成员变量被赋予错误值。若所有代码都可直接修改成员变量，追踪实际修改者将十分困难——可能需要为每个修改语句设置断点，而这类语句可能很多。  

但若成员只能通过单一成员函数修改，您只需在该函数设置断点，观察各调用者如何修改值。这极大简化了问题定位。  

优先选择非成员函数而非成员函数  
----------------  

在C++中，若函数能合理实现为非成员函数，应优先选择非成员函数而非成员函数。  

这带来诸多优势：  
* 非成员函数不属于类接口，使接口更简洁易懂  
* 非成员函数强制封装，因其必须通过类公共接口操作，避免因便利直接访问实现  
* 修改类实现时无需考虑非成员函数（只要接口未不兼容变更）  
* 非成员函数通常更易调试  
* 包含应用特定数据和逻辑的非成员函数可与类的可重用部分分离  

若有现代OOP语言（如Java或C#）经验，此实践可能令人惊讶。这些语言以类为核心，推崇成员函数（甚至不支持非成员函数）。  

最佳实践  
----------------  

**最佳实践**  
尽可能实现非成员函数（特别含应用特定数据或逻辑的函数）。  

小贴士  
----------------  

以下是函数设为成员或非成员的简化指南：  
* **必须时**使用成员函数：C++要求某些函数必须定义为成员。下节课讨论构造函数时可见一例，其他包括析构函数、虚函数及某些运算符  
* **需要访问不应暴露的私有（或受保护）数据时**使用成员函数  
* **否则优先非成员函数**（特别是不修改对象状态的函数）  

后两者有例外——将在相关主题中介绍。  

常见挑战案例出现在优先选择非成员函数需添加访问函数时。此时需权衡利弊：  
* 添加访问函数需创建新成员函数（getter及可能的setter），增加类接口复杂度。除非能在多处使用新访问函数，否则可能不值得  
* 不应为不应直接访问的数据添加访问函数（如内部状态），或允许用户破坏类不变式  

相关内容  
----------------  

Scott Meyers的文章[《非成员函数如何提升封装》](https://embeddedartistry.com/fieldatlas/how-non-member-functions-improve-encapsulation/)深入探讨了优先非成员函数的理念。  

通过三个相似示例说明（从最差到最优）：  

**最差版本**：  
```cpp
class Yogurt {
    std::string m_flavor{ "vanilla" };
public:
    // ...其他成员...
    void print() const {
        std::cout << "The yogurt has flavor " << m_flavor << '\n'; // 直接访问成员
    }
};
```  

**较优版本**：  
```cpp
class Yogurt {
    // ...同上...
    void print(std::string_view prefix) const {
        std::cout << prefix << ' ' << getFlavor() << '\n'; // 通过getter访问
    }
};
```  

**最优版本**：  
```cpp
class Yogurt { /*...*/ };
// 非成员函数
void print(const Yogurt& y) {
    std::cout << "The yogurt has flavor " << y.getFlavor() << '\n';
}
```  

类成员声明顺序  
----------------  

编写类外部代码时，需先声明变量和函数才能使用。但在类内部无此限制。如[14.3 — 成员函数](Chapter-14/lesson14.3-member-functions.md)所述，成员可按任意顺序排列。  

如何排序？存在两种观点：  
1. **私有成员在前**：遵循传统的"先声明后使用"风格，便于阅读实现细节  
2. **公有成员在前**：用户关注公共接口，将实现细节（次要）置后  

现代C++更推荐第二种方法（公有成员在前），尤其对需共享的代码。  

最佳实践  
----------------  

**最佳实践**  
按以下顺序声明成员：公有成员在前，受保护成员次之，私有成员最后。这能突出公共接口并弱化实现细节。  

作者注  
----------------  

本站多数示例采用与推荐相反的声明顺序，部分出于历史原因，但也因学习语言机制时关注实现细节更直观。  

高级阅读  
----------------  

[Google C++风格指南](https://google.github.io/styleguide/cppguide.html#Declaration_Order)推荐以下顺序：  
1. 类型与类型别名（typedef、using、enum、嵌套结构体/类、友元类型）  
2. 静态常量  
3. 工厂函数  
4. 构造函数与赋值运算符  
5. 析构函数  
6. 其他所有函数（静态/非静态成员函数、友元函数）  
7. 数据成员（静态/非静态）  

[下一课 14.9 — 构造函数简介](Chapter-14/lesson14.9-introduction-to-constructors.md)  
[返回主页](/)  
[上一课 14.7 — 返回数据成员引用的成员函数](Chapter-14/lesson14.7-member-functions-returning-references-to-data-members.md)