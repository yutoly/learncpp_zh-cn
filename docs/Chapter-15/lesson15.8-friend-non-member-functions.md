15.8 — 友元非成员函数
====================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年9月20日，下午2:04（太平洋夏令时）  
2024年5月8日

在本章及前一章的大部分内容中，我们一直在强调访问控制（access controls）的优势，它提供了一种机制来控制谁可以访问类的各个成员。私有成员（private members）仅能被类的其他成员访问，而公有成员（public members）可被所有人访问。在课程[14.6 — 访问函数](Chapter-14/lesson14.6-access-functions.md)中，我们讨论了保持数据私有化（private）并通过公有接口（public interface）供非成员使用的优点。

然而，在某些情况下，这种安排可能不够充分或不够理想。

例如，考虑一个专注于管理数据集的存储类（storage class）。假设您还需要显示这些数据，但处理显示的代码包含大量选项且较为复杂。您可以将存储管理函数和显示管理函数都放在同一个类中，但这会使类变得臃肿并导致接口复杂化。另一种方案是将它们分离：存储类负责管理存储，而另一个显示类（display class）负责所有显示功能。这实现了良好的职责分离（separation of responsibility）。但显示类将无法访问存储类的私有成员，可能无法完成其工作。

此外，有时在语法上我们可能更倾向于使用非成员函数（non-member function）而非成员函数（member function）（下文将给出示例）。在重载运算符（overloading operators）时这种情况尤为常见（我们将在后续课程讨论该主题）。但非成员函数存在同样的问题——它们无法访问类的私有成员。

若访问函数（access functions）（或其他公有成员函数）已存在且能满足所需功能，那么直接使用它们即可（且应当如此）。但某些情况下这些函数并不存在。此时该怎么办？

一种方案是向类添加新的成员函数，以允许其他类或非成员函数执行原本无法完成的任务。但我们可能不希望公开访问这些函数——或许这些函数高度依赖实现细节（implementation dependent）或容易被误用（prone to misuse）。

我们真正需要的是在特定情况下绕过访问控制系统的方法。

友元机制（Friendship）的魔力
----------------

解决方案就是友元（friendship）。

在类主体内部，可通过**友元声明**（friend declaration）（使用`friend`关键字）告知编译器其他类或函数成为友元。在C++中，**友元**（friend）是被授予完全访问另一个类私有（private）和保护（protected）成员权限的类或函数（成员或非成员）。通过这种方式，类可以有选择地授权其他类或函数完全访问其成员，而不影响其他部分。

> **关键洞察**  
> 友元关系始终由被访问成员的类授予（而非由需要访问的类或函数授予）。通过访问控制和授予友元关系，类始终保留对其成员访问权限的控制权。

例如，若存储类将显示类设为友元，则显示类将能直接访问存储类的所有成员。显示类可利用此直接访问实现存储类的显示功能，同时保持结构分离。

友元声明不受访问控制影响，因此其在类主体内的位置无关紧要。

了解友元概念后，我们将通过具体示例展示如何向非成员函数、成员函数及其他类授予友元关系。本节讨论**友元非成员函数**（friend non-member functions），下节课[15.9 — 友元类与友元成员函数](Chapter-15/lesson15.9-friend-classes-and-friend-member-functions.md)将介绍友元类（friend classes）和友元成员函数（friend member functions）。

友元非成员函数
----------------

**友元函数**（friend function）是可像类成员一样访问类私有和保护成员的函数（成员或非成员）。在其他所有方面，友元函数都是普通函数。

以下示例展示了一个简单类如何将非成员函数设为友元：

```cpp
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 };

public:
    void add(int value) { m_value += value; }

    // 此友元声明使非成员函数 void print(const Accumulator& accumulator) 成为 Accumulator 的友元
    friend void print(const Accumulator& accumulator);
};

void print(const Accumulator& accumulator)
{
    // 因 print() 是 Accumulator 的友元
    // 故可访问其私有成员
    std::cout << accumulator.m_value;
}

int main()
{
    Accumulator acc{};
    acc.add(5); // 累加器增加5

    print(acc); // 调用非成员函数 print()

    return 0;
}
```

本例中，我们声明了接受`Accumulator`类对象的非成员函数`print()`。由于`print()`不是Accumulator类的成员，通常无法访问私有成员`m_value`。但Accumulator类通过友元声明使`print(const Accumulator& accumulator)`成为友元，因此该访问被允许。

注意：因`print()`是非成员函数（故无隐式对象），必须显式传递`Accumulator`对象给`print()`以供操作。

在类内部定义友元非成员函数
----------------

与成员函数类似，友元非成员函数也可在类内部定义。下例在`Accumulator`类内部定义友元非成员函数`print()`：

```cpp
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 };

public:
    void add(int value) { m_value += value; }

    // 类内定义的友元函数属于非成员函数
    friend void print(const Accumulator& accumulator)
    {
        // 因 print() 是 Accumulator 的友元
        // 故可访问其私有成员
        std::cout << accumulator.m_value;
    }
};

int main()
{
    Accumulator acc{};
    acc.add(5); // 累加器增加5

    print(acc); // 调用非成员函数 print()

    return 0;
}
```

尽管`print()`定义在`Accumulator`内部，您可能认为它是成员函数，但事实并非如此。由于`print()`被定义为友元，它被视为非成员函数（如同定义在`Accumulator`外部）。

语法上更倾向友元非成员函数的情况
----------------

在本课引言中，我们提到有时可能更倾向于使用非成员函数而非成员函数。以下示例说明这种情况：

```cpp
#include <iostream>

class Value
{
private:
    int m_value{};

public:
    explicit Value(int v): m_value { v }  { }

    bool isEqualToMember(const Value& v) const;
    friend bool isEqualToNonmember(const Value& v1, const Value& v2);
};

bool Value::isEqualToMember(const Value& v) const
{
    return m_value == v.m_value;
}

bool isEqualToNonmember(const Value& v1, const Value& v2)
{
    return v1.m_value == v2.m_value;
}

int main()
{
    Value v1 { 5 };
    Value v2 { 6 };

    std::cout << v1.isEqualToMember(v2) << '\n';
    std::cout << isEqualToNonmember(v1, v2) << '\n';

    return 0;
}
```

本例定义了两个检查`Value`对象是否相等的相似函数。`isEqualToMember()`是成员函数，`isEqualToNonmember()`是非成员函数。重点观察它们的实现方式。

在`isEqualToMember()`中，我们隐式传递一个对象，显式传递另一个对象。函数实现反映了这一点：需在思维中区分`m_value`属于隐式对象，而`v.m_value`属于显式参数。

在`isEqualToNonmember()`中，两个对象均显式传递。这使函数实现更具对称性：`m_value`成员始终显式地通过参数前缀访问。

您可能仍偏爱调用语法`v1.isEqualToMember(v2)`而非`isEqualToNonmember(v1, v2)`。但在讨论运算符重载时，我们将再次涉及此主题。

多重友元关系
----------------

一个函数可同时成为多个类的友元。例如：

```cpp
#include <iostream>

class Humidity; // Humidity 的前向声明

class Temperature
{
private:
    int m_temp { 0 };
public:
    explicit Temperature(int temp) : m_temp { temp } { }

    friend void printWeather(const Temperature& temperature, const Humidity& humidity); // 此行需要前向声明
};

class Humidity
{
private:
    int m_humidity { 0 };
public:
    explicit Humidity(int humidity) : m_humidity { humidity } {  }

    friend void printWeather(const Temperature& temperature, const Humidity& humidity);
};

void printWeather(const Temperature& temperature, const Humidity& humidity)
{
    std::cout << "温度为 " << temperature.m_temp << 
        "，湿度为 " << humidity.m_humidity << '\n';
}

int main()
{
    Humidity hum { 10 };
    Temperature temp { 12 };

    printWeather(temp, hum);

    return 0;
}
```

此示例有三点值得注意：首先，因`printWeather()`同等使用`Humidity`和`Temperature`，将其作为任何一方的成员都不合理，非成员函数更合适；其次，因`printWeather()`是`Humidity`和`Temperature`的共同友元，可访问两类对象的私有数据；最后，注意示例顶部的声明：

```cpp
class Humidity;
```

这是`class Humidity`的前向声明（forward declaration）。类前向声明的作用与函数前向声明类似——告知编译器稍后将定义的标识符。但不同于函数，类无返回类型或参数，故类前向声明始终为`class ClassName`形式（类模板除外）。

若无此行，编译器在解析`Temperature`内部的友元声明时将因无法识别`Humidity`而报错。

友元是否违反数据隐藏原则？
----------------

否。友元关系由实施数据隐藏的类主动授予，且预期友元将访问其私有成员。可将友元视为类自身的扩展，拥有完全相同的访问权限。因此，这种访问是预期行为而非违规。

正确使用时，友元机制可通过设计层面的功能分离提升程序可维护性（而非因访问控制被迫保持功能集中）。或在语法上使用非成员函数比成员函数更合理时发挥作用。

但需注意：由于友元能直接访问类的实现细节，类实现的变更通常也会导致其友元需要相应修改。若类拥有大量友元（或友元拥有其他友元），可能引发连锁反应（ripple effect）。

实现友元函数时，应优先使用公有接口（public interface）而非直接访问成员。这有助于隔离友元函数与未来实现变更，减少后续需修改和/或重测的代码量。

> **最佳实践**  
> 友元函数应尽可能优先使用类接口而非直接访问成员。

优先选择非友元函数
----------------

在课程[14.8 — 数据隐藏（封装）的优势](Chapter-14/lesson14.8-the-benefits-of-data-hiding-encapsulation.md)中，我们提到应优先选择非成员函数而非成员函数。基于同样理由，应优先选择非友元函数（non-friend functions）而非友元函数。

例如下例中，若`Accumulator`的实现变更（如重命名`m_value`），则`print()`的实现也需同步修改：

```cpp
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 }; // 若重命名此成员

public:
    void add(int value) { m_value += value; } // 需修改此处

    friend void print(const Accumulator& accumulator);
};

void print(const Accumulator& accumulator)
{
    std::cout << accumulator.m_value; // 也需修改此处
}

int main()
{
    Accumulator acc{};
    acc.add(5); // 累加器增加5

    print(acc); // 调用非成员函数 print()

    return 0;
}
```

更佳方案如下：

```cpp
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 };

public:
    void add(int value) { m_value += value; }
    int value() const { return m_value; } // 添加合理的访问函数
};

void print(const Accumulator& accumulator) // 不再是 Accumulator 的友元
{
    std::cout << accumulator.value(); // 使用访问函数替代直接访问
}

int main()
{
    Accumulator acc{};
    acc.add(5); // 累加器增加5

    print(acc); // 调用非成员函数 print()

    return 0;
}
```

此例中，`print()`通过访问函数`value()`获取`m_value`值而非直接访问。现在若`Accumulator`的实现变更，`print()`无需更新。

> **最佳实践**  
> 在可能且合理的情况下，优先将函数实现为非友元形式。

为现有类的公有接口添加新成员时需谨慎，因为每个函数（即使是简单函数）都会增加一定程度的复杂性和冗余。对于上述`Accumulator`类，提供获取当前累加值的访问函数完全合理。但在更复杂场景中，相较于向类接口添加大量新访问函数，使用友元可能更可取。

[下一课 15.9 友元类与友元成员函数](Chapter-15/lesson15.9-friend-classes-and-friend-member-functions.md)  
[返回主页](/)  
[上一课 15.7 静态成员函数](Chapter-15/lesson15.7-static-member-functions.md)