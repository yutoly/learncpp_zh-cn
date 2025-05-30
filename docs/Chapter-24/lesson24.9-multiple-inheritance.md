24.9 — 多重继承  
============================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年1月24日（太平洋标准时间下午3:39）  
2024年7月11日更新  

到目前为止，我们展示的所有继承案例都是单继承——即每个派生类只有一个父类。然而，C++提供了多重继承的能力。**多重继承（multiple inheritance）**允许派生类从多个父类继承成员。

假设我们要编写程序来管理教师信息。教师是人（Person），同时也是雇员（Employee）（如果是自由职业者则自己是雇主）。多重继承可用于创建同时继承Person和Employee属性的Teacher类。使用多重继承时，只需用逗号分隔每个基类（类似于单继承语法）。  

![](https://www.learncpp.com/images/CppTutorial/Section11/PersonTeacher.gif)  
```cpp
#include <string>
#include <string_view>

class Person
{
private:
    std::string m_name{};
    int m_age{};

public:
    Person(std::string_view name, int age)
        : m_name{ name }, m_age{ age }
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }
};

class Employee
{
private:
    std::string m_employer{};
    double m_wage{};

public:
    Employee(std::string_view employer, double wage)
        : m_employer{ employer }, m_wage{ wage }
    {
    }

    const std::string& getEmployer() const { return m_employer; }
    double getWage() const { return m_wage; }
};

// Teacher 公有继承 Person 和 Employee
class Teacher : public Person, public Employee
{
private:
    int m_teachesGrade{};

public:
    Teacher(std::string_view name, int age, std::string_view employer, double wage, int teachesGrade)
        : Person{ name, age }, Employee{ employer, wage }, m_teachesGrade{ teachesGrade }
    {
    }
};

int main()
{
    Teacher t{ "Mary", 45, "Boo", 14.3, 8 };

    return 0;
}
```

混合类（Mixins）  
----------------  

**混合类（mixin）**（也拼作"mix-in"）是通过继承为类添加属性的小型类。其名称表明该类用于混合到其他类中，而不是独立实例化。

以下示例中，Box、Label和Tooltip类都是混合类，通过继承创建新的Button类：  
```cpp
// 感谢读者 Waldo 提供此示例
#include <string>

struct Point2D
{
	int x{};
	int y{};
};

class Box // 混合类 Box
{
public:
	void setTopLeft(Point2D point) { m_topLeft = point; }
	void setBottomRight(Point2D point) { m_bottomRight = point; }
private:
	Point2D m_topLeft{};
	Point2D m_bottomRight{};
};

class Label // 混合类 Label
{
public:
	void setText(const std::string_view str) { m_text = str; }
	void setFontSize(int fontSize) { m_fontSize = fontSize; }
private:
	std::string m_text{};
	int m_fontSize{};
};

class Tooltip // 混合类 Tooltip
{
public:
	void setText(const std::string_view str) { m_text = str; }
private:
	std::string m_text{};
};

class Button : public Box, public Label, public Tooltip {}; // 使用三个混合类的 Button

int main()
{
	Button button{};
	button.Box::setTopLeft({ 1, 1 });
	button.Box::setBottomRight({ 10, 10 });
	button.Label::setText("Submit");
	button.Label::setFontSize(6);
	button.Tooltip::setText("将表单提交至服务器");
}
```

可能有人会疑惑为何需要显式使用`Box::`、`Label::`和`Tooltip::`作用域解析前缀：  
1. `Label::setText()`与`Tooltip::setText()`函数原型相同。若调用`button.setText()`，编译器会产生函数调用歧义错误。此时必须使用前缀消除歧义  
2. 在非歧义情况下，使用混合类名称可明确函数调用所属的混合类，增强代码可读性  
3. 非歧义情况在新增混合类后可能变为歧义，显式前缀可预防此类问题  

> **进阶阅读**  
> 由于混合类旨在为派生类添加功能而非提供接口，通常不使用虚函数（下章讨论）。若需定制混合类，通常采用模板。因此混合类常被模板化。  

有趣的是，派生类可以通过**奇异递归模板模式（Curiously Recurring Template Pattern，CRTP）**将自身作为模板参数继承混合类：  
```cpp
// 奇异递归模板模式（CRTP）

template <class T>
class Mixin
{
    // Mixin<T> 可通过 (static_cast<T*>(this)) 访问派生类成员
};

class Derived : public Mixin<Derived>
{
};
```  
简单示例可参考[cppreference CRTP说明](https://en.cppreference.com/w/cpp/language/crtp)。

多重继承的问题  
----------------  

虽然多重继承看似是单继承的简单扩展，但它引入了许多显著增加程序复杂度和维护难度的问题。  

首先，当多个基类包含同名函数时会产生歧义：  
```cpp
#include <iostream>

class USBDevice
{
private:
    long m_id {};

public:
    USBDevice(long id)
        : m_id { id }
    {
    }

    long getID() const { return m_id; }
};

class NetworkDevice
{
private:
    long m_id {};

public:
    NetworkDevice(long id)
        : m_id { id }
    {
    }

    long getID() const { return m_id; }
};

class WirelessAdapter: public USBDevice, public NetworkDevice
{
public:
    WirelessAdapter(long usbId, long networkId)
        : USBDevice { usbId }, NetworkDevice { networkId }
    {
    }
};

int main()
{
    WirelessAdapter c54G { 5442, 181742 };
    std::cout << c54G.getID(); // 调用哪个getID()？

    return 0;
}
```  
当编译`c54G.getID()`时，编译器发现WirelessAdapter包含两个getID()函数：分别继承自USBDevice和NetworkDevice。此时函数调用产生歧义，将导致编译错误。  

可通过显式指定版本来解决：  
```cpp
int main()
{
    WirelessAdapter c54G { 5442, 181742 };
    std::cout << c54G.USBDevice::getID();

    return 0;
}
```  
当类继承四到六个基类时，命名冲突的可能性将指数级增长，每个冲突都需要显式解决。  

其次更严重的是[菱形问题（diamond problem）](https://en.wikipedia.org/wiki/Diamond_problem)（作者称为"毁灭菱形"），当类多重继承自两个共同继承单一基类的类时，形成菱形继承结构：  
```cpp
class PoweredDevice
{
};

class Scanner: public PoweredDevice
{
};

class Printer: public PoweredDevice
{
};

class Copier: public Scanner, public Printer
{
};
```  
![](https://www.learncpp.com/images/CppTutorial/Section11/PoweredDevice.gif)  
扫描仪和打印机都是用电设备，故继承PoweredDevice。但复印机同时具备扫描和打印功能。  

这将导致诸多问题，包括Copier应包含几个PoweredDevice副本，以及如何解析某些类型的歧义引用。虽然多数问题可通过显式作用域解决，但为处理复杂性增加的维护成本将显著上升。下章将讨论解决方案（见[25.8 — 虚基类](Chapter-25/lesson25.8-virtual-base-classes.md)）。  

多重继承是否弊大于利？  
----------------  

事实证明，多数多重继承能解决的问题也可通过单继承实现。许多面向对象语言（如Smalltalk、PHP）根本不支持多重继承。Java、C#等现代语言限制普通类的单继承，但允许接口类的多重继承（后续讨论）。这些语言认为多重继承会使语言过于复杂，最终弊大于利。  

许多作者和经验丰富的程序员认为C++多重继承应完全避免。但本文作者认为某些情况下多重继承仍是最佳选择，只是需极度谨慎使用。  

有趣的是，您早已在使用通过多重继承实现的类：标准库中的std::cin和std::cout对象正是通过多重继承实现的！  

> **最佳实践**  
> 除非其他方案会导致更大复杂性，否则应避免多重继承。  

[下一课 24.x — 第24章总结与测验](Chapter-24/lesson24.x-chapter-24-summary-and-quiz.md)  
[返回主页](/)  
[上一课 24.8 — 隐藏继承功能](Chapter-24/lesson24.8-hiding-inherited-functionality.md)