24.4 — 派生类的构造函数与初始化  
==========================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年1月9日 下午2:36（首次发布）  
2023年9月11日（更新）  

前两节课我们探讨了C++继承基础与派生类初始化顺序。本节将深入分析构造函数在派生类初始化中的作用。我们将继续使用前文开发的Base和Derived类：  
```
class Base
{
public:
    int m_id {};
 
    Base(int id=0)
        : m_id{ id }
    {
    }
 
    int getId() const { return m_id; }
};
 
class Derived: public Base
{
public:
    double m_cost {};
 
    Derived(double cost=0.0)
        : m_cost{ cost }
    {
    }
 
    double getCost() const { return m_cost; }
};
```  

**非派生类的构造过程**  
对于非派生类（如Base），构造过程如下：  
```
int main()
{
    Base base{ 5 }; // 调用Base(int)构造函数
    return 0;
}
```  
实例化base时实际发生：  
1. 分配内存  
2. 调用Base构造函数  
3. 成员初始化列表初始化变量  
4. 执行构造函数体  
5. 返回控制权  

**派生类的构造过程**  
```
int main()
{
    Derived derived{ 1.3 }; // 调用Derived(double)构造函数
    return 0;
}
```  
实例化derived时实际发生：  
1. 分配内存（包含基类和派生类部分）  
2. 调用Derived构造函数  
3. **首先使用基类构造函数构造Base对象**（若未指定则使用默认构造函数）  
4. 成员初始化列表初始化变量  
5. 执行构造函数体  
6. 返回控制权  

与非继承情况的唯一区别在于：派生类构造函数执行主体前会先调用基类构造函数。基类构造函数完成基类部分的构造后，控制权返回派生类构造函数继续执行。  

**基类成员初始化问题**  
当前Derived类的缺陷在于创建对象时无法初始化基类成员m_id。若需要同时设置m_cost（派生类）和m_id（基类），新手常尝试：  
```
class Derived: public Base
{
public:
    double m_cost{};

    Derived(double cost=0.0, int id=0)
        : m_cost{ cost }
        , m_id{ id } // 无效！
    {
    }
};
```  
C++禁止在成员初始化列表中初始化继承成员。原因：  
- 若成员是const或引用类型，必须在创建时初始化  
- 基类构造函数已初始化成员，派生类再次修改会导致重复初始化  

另一种错误尝试：  
```
class Derived: public Base
{
public:
    Derived(double cost=0.0, int id=0)
        : m_cost{ cost }
    {
        m_id = id; // 可行但不推荐
    }
};
```  
此方法：  
- 对const/引用成员无效  
- 效率低下（m_id被赋值两次）  
- 基类构造时无法访问该值  

**正确初始化方法**  
通过成员初始化列表显式调用基类构造函数：  
```
class Derived: public Base
{
public:
    double m_cost{};

    Derived(double cost=0.0, int id=0)
        : Base{ id } // 调用Base(int)
        , m_cost{ cost }
    {
    }
};
```  
使用示例：  
```
int main()
{
    Derived derived{ 1.3, 5 };
    std::cout << "Id: " << derived.getId() << '\n'; // 5
    std::cout << "Cost: " << derived.getCost() << '\n'; // 1.3
    return 0;
}
```  
详细执行流程：  
1. 分配内存  
2. 调用Derived构造函数  
3. 调用Base(int)初始化m_id=5  
4. Base构造完成  
5. 初始化m_cost=1.3  
6. Derived构造完成  

**成员私有化**  
将成员设为private并通过访问函数访问：  
```
class Base
{
private:
    int m_id{};
public:
    Base(int id=0) : m_id{ id } {}
    int getId() const { return m_id; }
};

class Derived: public Base
{
private:
    double m_cost{};
public:
    Derived(double cost=0.0, int id=0)
        : Base{ id }, m_cost{ cost } {}
    double getCost() const { return m_cost; }
};
```  

**继承链示例**  
```
class A
{
public:
    A(int a) { std::cout << "A: " << a << '\n'; }
};

class B: public A
{
public:
    B(int a, double b) : A{ a } { std::cout << "B: " << b << '\n'; }
};

class C: public B
{
public:
    C(int a, double b, char c) : B{ a, b } { std::cout << "C: " << c << '\n'; }
};

int main()
{
    C c{ 5, 4.3, 'R' }; // 输出顺序：A → B → C
    return 0;
}
```  
执行顺序：  
1. C构造函数调用B构造函数  
2. B构造函数调用A构造函数  
3. 构造顺序：A → B → C  
4. 析构顺序：C → B → A  

**总结**  
- 派生类构造函数负责指定基类构造函数（默认使用无参构造）  
- 构造顺序：从最基类到最派生类  
- 析构顺序相反  

**测验**  
实现水果继承示例：  
```
#include <iostream>
#include <string>
#include <string_view>

class Fruit
{
private:
    std::string m_name;
    std::string m_color;
public:
    Fruit(std::string_view n, std::string_view c) : m_name{n}, m_color{c} {}
    const std::string& getName() const { return m_name; }
    const std::string& getColor() const { return m_color; }
};

class Apple : public Fruit
{
    double m_fiber;
public:
    Apple(std::string_view n, std::string_view c, double f)
        : Fruit{n,c}, m_fiber{f} {}
    double getFiber() const { return m_fiber; }
};

std::ostream& operator<<(std::ostream& os, const Apple& a) {
    os << "Apple(" << a.getName() << ", " << a.getColor() << ", " << a.getFiber() << ')';
    return os;
}

class Banana : public Fruit
{
public:
    Banana(std::string_view n, std::string_view c) : Fruit{n,c} {}
};

std::ostream& operator<<(std::ostream& os, const Banana& b) {
    os << "Banana(" << b.getName() << ", " << b.getColor() << ')';
    return os;
}
```  

[下一课 24.5 继承与访问说明符](Chapter-24/lesson24.5-inheritance-and-access-specifiers.md)  
[返回主页](/)  
[上一课 24.3 派生类的构造顺序](Chapter-24/lesson24.3-order-of-construction-of-derived-classes.md)