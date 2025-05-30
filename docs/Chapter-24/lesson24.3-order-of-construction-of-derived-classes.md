24.3 — 派生类的构造顺序  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年1月7日（太平洋标准时间下午4:18）  
2024年4月30日  

 

在[基础继承](112-basic-inheritance-in-c/)课程中，我们学习了类如何从其他类继承成员和函数。本章将深入探讨派生类（derived class）实例化时的构造顺序。


首先引入新类来阐述关键概念：



```
class Base
{
public:
    int m_id {};

    Base(int id=0)
        : m_id { id }
    {
    }

    int getId() const { return m_id; }
};

class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0)
        : m_cost { cost }
    {
    }

    double getCost() const { return m_cost; }
};
```

此例中，Derived类继承自Base类。


![](https://www.learncpp.com/images/CppTutorial/Section11/DerivedBase.gif)


虽然Derived继承Base的成员，但并非简单复制成员。实际上，Derived类可视为由两部分组成：Derived部分和Base部分。


![](https://www.learncpp.com/images/CppTutorial/Section11/DerivedBaseCombined.gif)


普通类（非派生类）的实例化过程：



```
int main()
{
    Base base;

    return 0;
}
```

Base作为非派生类，其构造过程为：分配内存后调用默认构造函数（default constructor）进行初始化。


现在观察派生类的实例化：



```
int main()
{
    Derived derived;

    return 0;
}
```

表面看似与普通类实例化无异，但实际执行过程不同。Derived类由Base部分和Derived部分组成，C++构造派生对象时采用分阶段策略：首先构造最基类（继承树顶端），然后按继承顺序依次构造子类，直到完成最底层派生类的构造。


因此Derived实例化时，首先构造Base部分（调用Base默认构造函数），随后构造Derived部分（调用Derived默认构造函数）。此时无更多派生类，构造完成。


通过代码示例可直观演示该过程：



```
#include <iostream>

class Base
{
public:
    int m_id {};

    Base(int id=0)
        : m_id { id }
    {
        std::cout << "Base\n";
    }

    int getId() const { return m_id; }
};

class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0)
        : m_cost { cost }
    {
        std::cout << "Derived\n";
    }

    double getCost() const { return m_cost; }
};

int main()
{
    std::cout << "Instantiating Base\n";
    Base base;

    std::cout << "Instantiating Derived\n";
    Derived derived;

    return 0;
}
```

程序输出：



```
Instantiating Base
Base
Instantiating Derived
Base
Derived

```

可见构造Derived时，其Base部分首先被构造。这符合逻辑：子类不能脱离父类独立存在。从安全角度考虑，子类常使用父类成员，而父类对子类一无所知。优先构造父类可确保派生类构造时这些成员已初始化完毕。


**继承链的构造顺序**


多层继承的情况：



```
#include <iostream>

class A
{
public:
    A()
    {
        std::cout << "A\n";
    }
};

class B: public A
{
public:
    B()
    {
        std::cout << "B\n";
    }
};

class C: public B
{
public:
    C()
    {
        std::cout << "C\n";
    }
};

class D: public C
{
public:
    D()
    {
        std::cout << "D\n";
    }
};
```

C++始终优先构造最基类（继承树顶端），然后按继承顺序依次构造每个派生类。


演示程序：



```
int main()
{
    std::cout << "Constructing A: \n";
    A a;

    std::cout << "Constructing B: \n";
    B b;

    std::cout << "Constructing C: \n";
    C c;

    std::cout << "Constructing D: \n";
    D d;
}
```

输出结果：



```
Constructing A:
A
Constructing B:
A
B
Constructing C:
A
B
C
Constructing D:
A
B
C
D

```

**结论**


C++采用分阶段构造策略：从最基类（继承树顶端）开始，到最底层派生类（继承树末端）结束。每个类构造时调用其对应的构造函数完成初始化。


本节的示例类均使用基类默认构造函数（为简化说明）。下节课将深入探讨构造函数在派生类构造过程中的作用，包括如何显式选择基类构造函数。


[下一课 24.4 派生类的构造函数与初始化](Chapter-24/lesson24.4-constructors-and-initialization-of-derived-classes.md)  
[返回主页](/)  
[上一课 24.2 C++中的基础继承](Chapter-24/lesson24.2-basic-inheritance-in-c.md)