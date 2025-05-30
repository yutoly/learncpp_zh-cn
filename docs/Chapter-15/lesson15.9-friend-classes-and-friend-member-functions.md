15.9 — 友元类与友元成员函数  
==================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日（更新于2024年4月30日）  

友元类  
----------------  

**友元类（friend class）**是指能够访问另一个类的私有（private）和受保护（protected）成员的类。示例：  

```cpp
#include <iostream>

class Storage
{
private:
    int m_nValue {};
    double m_dValue {};
public:
    Storage(int nValue, double dValue)
       : m_nValue { nValue }, m_dValue { dValue }
    { }

    // 将Display类声明为Storage的友元
    friend class Display;
};

class Display
{
private:
    bool m_displayIntFirst {};

public:
    Display(bool displayIntFirst)
         : m_displayIntFirst { displayIntFirst }
    {
    }

    // 因Display是Storage的友元，可访问其私有成员
    void displayStorage(const Storage& storage)
    {
        if (m_displayIntFirst)
            std::cout << storage.m_nValue << ' ' << storage.m_dValue << '\n';
        else // 先显示double
            std::cout << storage.m_dValue << ' ' << storage.m_nValue << '\n';
    }

    void setDisplayIntFirst(bool b)
    {
         m_displayIntFirst = b;
    }
};

int main()
{
    Storage storage { 5, 6.7 };
    Display display { false };

    display.displayStorage(storage);

    display.setDisplayIntFirst(true);
    display.displayStorage(storage);

    return 0;
}
```  

由于`Display`是`Storage`的友元类，`Display`的成员可访问任何`Storage`对象的私有成员。程序输出：  
```
6.7 5
5 6.7
```  

关于友元类的补充说明：  
1. 即使`Display`是`Storage`的友元，`Display`也无法访问`Storage`对象的`*this`指针（因`*this`本质是函数参数）  
2. 友元关系不具有互惠性：`Display`是`Storage`的友元，不代表`Storage`自动成为`Display`的友元。若需双向友元关系，双方必须显式声明  
3. 友元关系不可传递：若A是B的友元，B是C的友元，并不意味A是C的友元  

> **进阶阅读**  
> 友元关系也不可继承：若A将B设为友元，B的派生类不会成为A的友元。  

友元类声明同时充当被友元类的前向声明（forward declaration）。例如上例中`friend class Display`既声明友元关系，又前向声明了`Display`类。  

友元成员函数  
----------------  

可单独声明某个成员函数为友元，而非整个类。方法与友元非成员函数类似，但需指定成员函数名。实际应用中需注意以下问题：  

尝试将`Display::displayStorage`设为友元成员函数时：  
```cpp
#include <iostream>

class Display; // Display类前向声明

class Storage
{
// ... 其他代码
    friend void Display::displayStorage(const Storage& storage); // 错误：Storage尚未看到Display完整定义
};
```  

此时编译器报错，因`Storage`类声明时尚未获得`Display`的完整定义。解决方法是将`Display`类定义移至`Storage`之前：  

```cpp
#include <iostream>

class Display
{
public:
    void displayStorage(const Storage& storage); // 错误：Storage未定义
};

class Storage
{
    friend void Display::displayStorage(const Storage& storage);
};
```  

但此时`Display::displayStorage()`使用`Storage`引用参数，而`Storage`定义在后。解决方案：  
1. 为`Storage`添加前向声明  
2. 将`Display::displayStorage()`的定义移至`Storage`类之后  

最终正确版本：  
```cpp
#include <iostream>

class Storage; // Storage前向声明

class Display
{
public:
    void displayStorage(const Storage& storage); // 声明
};

class Storage
{
    friend void Display::displayStorage(const Storage& storage);
};

// 成员函数定义在Storage类之后
void Display::displayStorage(const Storage& storage)
{
    // 访问Storage成员
}
```  

关键点：  
- 类前向声明满足引用需求  
- 访问类成员需完整类定义  

> **最佳实践**  
> 将类定义分别置于头文件中，成员函数定义置于对应.cpp文件，可避免代码顺序问题。  

测验  
----------------  

**问题1**  
几何学中，点（Point）表示空间位置，向量（Vector）表示方向与长度。实现`Point3d::moveByVector()`函数，使`Point3d`成为`Vector3d`的友元类。  

解决方案：  
```cpp
// Vector3d类中添加友元声明
friend class Point3d;

// Point3d类中实现
void moveByVector(const Vector3d& v)
{
    m_x += v.m_x;
    // ... 其他坐标同理
}
```  

**问题2**  
改为仅声明`Point3d::moveByVector`为友元成员函数：  
```cpp
// Vector3d类中添加
friend void Point3d::moveByVector(const Vector3d& v);

// 需要前向声明和正确代码顺序
```  

**问题3**  
使用5个文件重构方案：  
- Point3d.h：类声明  
- Point3d.cpp：成员函数定义  
- Vector3d.h：类声明（包含友元声明）  
- Vector3d.cpp：成员函数定义  
- main.cpp：主程序  

头文件使用包含保护（include guard），函数定义分离到.cpp文件。  

[下一课 15.10 — 引用限定符](Chapter-15/lesson15.10-ref-qualifiers.md)  
[返回主页](/)  
[上一课 15.8 — 友元非成员函数](Chapter-15/lesson15.8-friend-non-member-functions.md)