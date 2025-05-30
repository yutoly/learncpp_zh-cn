24.6 — 向派生类添加新功能  
===================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年1月17日下午4:06（太平洋标准时间）  
2023年9月11日更新  

在[继承入门](111-introduction-to-inheritance/)课程中，我们提到使用派生类（derived class）的最大优势之一是可重用现有代码。您可以通过继承基类（base class）功能，然后添加新功能、修改现有功能或隐藏不需要的功能。接下来的课程将详细讲解这些操作的具体实现。  

首先，我们从一个简单基类开始：  
```
#include <iostream>

class Base
{
protected:
    int m_value {};

public:
    Base(int value)
        : m_value { value }
    {
    }

    void identify() const { std::cout << "I am a Base\n"; }
};
```  
接下来创建继承自Base的派生类。为了让派生类对象在实例化时能够设置m_value的值，我们让派生类构造函数（constructor）在初始化列表中调用基类构造函数：  
```
class Derived: public Base
{
public:
    Derived(int value)
        : Base { value }
    {
    }
};
```  

**向派生类添加新功能**  
上述示例中，由于我们可以访问基类的源代码，可以直接向Base类添加功能。但有时我们可能拥有基类访问权限却不想修改它。例如：当您从第三方购买代码库但需要扩展功能时，直接修改原始代码并非最佳方案——更新时可能导致修改被覆盖，或需要手动迁移改动。  

另一种情况是基类不可修改（如标准库中的类）。这时可以通过继承创建派生类，并在派生类中添加所需功能。Base类中一个明显的缺失是未提供公有访问m_value的方式。虽然可以通过在基类添加访问函数解决，但本例选择在派生类中添加。由于m_value在基类中声明为protected，派生类可以直接访问它。  

要为派生类添加新功能，只需像常规类一样声明：  
```
class Derived: public Base
{
public:
    Derived(int value)
        : Base { value }
    {
    }

    int getValue() const { return m_value; }
};
```  
现在，公有成员可以通过调用派生类对象的getValue()访问m_value：  
```
int main()
{
    Derived derived { 5 };
    std::cout << "derived has value " << derived.getValue() << '\n';

    return 0;
}
```  
输出结果：  
```
derived has value 5
```  

需要注意的是，基类对象无法访问派生类中的getValue()函数。以下代码无法工作：  
```
int main()
{
    Base base { 5 };
    std::cout << "base has value " << base.getValue() << '\n';

    return 0;
}
```  
因为基类中不存在getValue()函数，该函数属于派生类。派生类可以访问基类成员，但基类不能访问派生类成员。  

[下一课 24.7 调用继承函数与重写行为](Chapter-24/lesson24.7-calling-inherited-functions-and-overriding-behavior.md)  
[返回主页](/)  
[上一课 24.5 继承与访问说明符](Chapter-24/lesson24.5-inheritance-and-access-specifiers.md)