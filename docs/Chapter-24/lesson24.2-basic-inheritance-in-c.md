24.2 — C++中的基础继承  
==================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日（首次发布于2008年1月4日）  

理解继承的抽象概念后，我们探讨其在C++中的具体实现。C++的继承关系发生在类之间。在继承（is-a）关系中，被继承的类称为**父类（parent class）**、**基类（base class）**或**超类（superclass）**，实施继承的类称为**子类（child class）**、**派生类（derived class）**或**派生类（subclass）**。![](http://learncpp.com/images/CppTutorial/Section11/FruitInheritance.gif)上图中，Fruit是父类，Apple和Banana是子类。![](http://learncpp.com/images/CppTutorial/Section11/ShapesInheritance.gif)此例中，Triangle既是子类（继承自Shape）又是父类（被Right Triangle继承）。  

子类从父类继承行为（成员函数）和属性（成员变量）（具体访问限制将在后续课程讨论）。这些变量和函数成为派生类的成员。由于子类是完全独立的类，它们可以拥有专属的特定成员（稍后示例说明）。  

**Person类**  
以下是表示通用人员的简单类：  
```cpp
#include <string>
#include <string_view>

class Person
{
// 本例为简化将成员设为公有
public: 
    std::string m_name{};
    int m_age{};

    Person(std::string_view name = "", int age = 0)
        : m_name{ name }, m_age{ age }
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }
};
```  
由于Person类代表通用人员，仅定义各类人员共有的成员。所有人（无论性别、职业等）都具备姓名和年龄，因此包含这些属性。注意本例将成员设为公有仅为简化示例，通常应将变量设为私有。访问控制与继承的交互将在本章后续讨论。  

**BaseballPlayer类**  
假设需编写记录棒球运动员信息的程序。棒球运动员需要特定属性——例如击球率（batting average）和本垒打次数。以下是未完成的棒球运动员类：  
```cpp
class BaseballPlayer
{
// 本例为简化将成员设为公有
public:
    double m_battingAverage{};
    int m_homeRuns{};

    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0)
       : m_battingAverage{battingAverage}, m_homeRuns{homeRuns}
    {
    }
};
```  
现在需添加姓名和年龄属性，而这些已存在于Person类。此时有三种选择：  
1. 直接添加至BaseballPlayer类：最差方案，造成与Person类的代码重复，任何Person的更新都需同步至BaseballPlayer  
2. 通过组合（composition）将Person作为成员：需判断"棒球运动员是否拥有人"？答案否定，故不适用  
3. 通过继承获取属性：继承反映is-a关系，棒球运动员是人，故选择继承  

**实现BaseballPlayer派生类**  
使BaseballPlayer继承Person类的语法简明：在`class BaseballPlayer`声明后使用冒号、`public`关键字和基类名，这称为*公有继承（public inheritance）*（后续课程详述公有继承含义）。  
```cpp
// BaseballPlayer 公有继承 Person
class BaseballPlayer : public Person
{
public:
    double m_battingAverage{};
    int m_homeRuns{};

    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0)
       : m_battingAverage{battingAverage}, m_homeRuns{homeRuns}
    {
    }
};
```  
继承关系图示：![](https://www.learncpp.com/images/CppTutorial/Section11/BaseballPlayerInheritance.gif)  
BaseballPlayer继承Person后，获得其成员函数和变量，并新增m_battingAverage和m_homeRuns成员。因此BaseballPlayer对象将包含4个成员变量：来自基类的m_name、m_age，以及自身的两个属性。  

验证示例：  
```cpp
#include <iostream>
#include <string>
#include <string_view>

class Person
{
public:
    std::string m_name{};
    int m_age{};

    Person(std::string_view name = "", int age = 0)
        : m_name{name}, m_age{age}
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }
};

// BaseballPlayer 公有继承 Person
class BaseballPlayer : public Person
{
public:
    double m_battingAverage{};
    int m_homeRuns{};

    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0)
       : m_battingAverage{battingAverage}, m_homeRuns{homeRuns}
    {
    }
};

int main()
{
    // 创建BaseballPlayer对象
    BaseballPlayer joe{};
    // 直接赋值公有成员m_name
    joe.m_name = "Joe";
    // 输出姓名
    std::cout << joe.getName() << '\n'; // 使用从Person继承的getName()

    return 0;
}
```  
输出：  
```
Joe
```  
程序通过编译运行，因为joe作为BaseballPlayer对象，继承了Person类的m_name成员变量和getName()成员函数。  

**Employee派生类**  
创建另一个继承自Person的Employee类。雇员是人，适用继承：  
```cpp
// Employee 公有继承 Person
class Employee: public Person
{
public:
    double m_hourlySalary{};
    long m_employeeID{};

    Employee(double hourlySalary = 0.0, long employeeID = 0)
        : m_hourlySalary{hourlySalary}, m_employeeID{employeeID}
    {
    }

    void printNameAndSalary() const
    {
        std::cout << m_name << ": " << m_hourlySalary << '\n';
    }
};
```  
Employee继承Person的m_name、m_age和访问函数，新增两个成员变量和一个成员函数。注意printNameAndSalary()同时使用本类（Employee::m_hourlySalary）和父类（Person::m_name）的成员。继承关系图示：![](https://www.learncpp.com/images/CppTutorial/Section11/EmployeeInheritance.gif)  

完整示例：  
```cpp
#include <iostream>
#include <string>
#include <string_view>

class Person
{
public:
    std::string m_name{};
    int m_age{};

    Person(std::string_view name = "", int age = 0)
        : m_name{name}, m_age{age}
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }
};

// Employee 公有继承 Person
class Employee: public Person
{
public:
    double m_hourlySalary{};
    long m_employeeID{};

    Employee(double hourlySalary = 0.0, long employeeID = 0)
        : m_hourlySalary{hourlySalary}, m_employeeID{employeeID}
    {
    }

    void printNameAndSalary() const
    {
        std::cout << m_name << ": " << m_hourlySalary << '\n';
    }
};

int main()
{
    Employee frank{20.25, 12345};
    frank.m_name = "Frank"; // 因m_name为公有成员

    frank.printNameAndSalary();
    
    return 0;
}
```  
输出：  
```
Frank: 20.25
```  

**继承链**  
可以从派生类继续派生子类，形成继承链。例如创建Supervisor类：主管（Supervisor）是雇员（Employee），雇员是人（Person）。继承关系图示：![](https://www.learncpp.com/images/CppTutorial/Section11/SupervisorInheritance.gif)  
Supervisor对象继承Employee和Person的成员，并新增m_overseesIDs成员变量。通过构建此类继承链，可创建从通用（顶层）到具体（底层）的可重用类层次。  

**继承的优势**  
继承基类意味着无需在派生类中重复定义基类成员，自动通过继承获得基类成员，只需添加新成员即可。这不仅减少工作量，还确保基类更新（如新增函数或修复错误）时，所有派生类自动继承变更。例如：  
- 为Person添加新函数，Employee、Supervisor和BaseballPlayer自动获得  
- 为Employee新增变量，Supervisor也会继承  
这种机制使得类构建更直观、易维护。  

**总结**  
继承通过派生类复用基类成员。后续课程将继续探讨其工作机制。  

[下一课 24.3 派生类的构造顺序](Chapter-24/lesson24.3-order-of-construction-of-derived-classes.md)  
[返回主页](/)  
[上一课 24.1 继承简介](Chapter-24/lesson24.1-introduction-to-inheritance.md)