15.1 — 隐藏的“this”指针与成员函数链式调用  
==============================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月29日（首次发布于2007年9月6日）

关于类（class），新程序员常问的问题是："当调用成员函数（member function）时，C++如何追踪调用该函数的对象？"

首先定义示例类。该类封装整数值并提供访问函数（access function）：

```cpp
#include <iostream>

class Simple
{
private:
    int m_id{};
 
public:
    Simple(int id)
        : m_id{ id }
    {
    }

    int getID() const { return m_id; }
    void setID(int id) { m_id = id; }

    void print() const { std::cout << m_id; }
};

int main()
{
    Simple simple{1};
    simple.setID(2);

    simple.print();

    return 0;
}
```

输出结果：

```
2
```

调用`simple.setID(2)`时，C++知道`setID()`应操作`simple`对象。其原理在于C++使用名为`this`的隐藏指针（pointer）！

隐藏的this指针  
----------------

每个成员函数内部，**this**关键字是保存当前隐式对象地址的常量指针（const pointer）。

示例显式使用`this`：

```cpp
void print() const { std::cout << this->m_id; } // 使用this指针访问成员
```

此代码与隐式版本等效：

```cpp
void print() const { std::cout << m_id; } // 隐式this
```

编译器会自动为隐式对象成员添加`this->`前缀。

关键点  
----------------

所有非静态（non-static）成员函数都有指向被操作对象的`this`常量指针。

this始终指向被操作对象  
----------------

每个成员函数的`this`参数指向隐式对象：

```cpp
Simple a{1}; // 构造函数中this = &a
Simple b{2}; // 构造函数中this = &b
a.setID(3);  // setID()中this = &a
b.setID(4);  // setID()中this = &b
```

显式使用this的场景  
----------------

1. **名称冲突消解**：当参数与成员同名时：

```cpp
struct Something
{
    int data;
    void setData(int data) { this->data = data; } // 使用this区分成员
};
```

2. **函数链式调用（function chaining）**：通过返回`*this`实现方法链（method chaining）：

```cpp
class Calc
{
public:
    Calc& add(int value) { m_value += value; return *this; }
    // 其他链式方法...
};

calc.add(5).sub(3).mult(4); // 链式调用
```

重置类到默认状态  
----------------

通过`reset()`成员函数实现：

```cpp
void reset() { *this = {}; } // 值初始化新对象并覆盖当前对象
```

this与const对象  
----------------

- 非const成员函数：`this`是const指针（指向非const对象）
- const成员函数：`this`是const指针（指向const对象）

在const对象上调用非const成员函数会导致编译错误：

```
error C2662: 无法将this指针从'const Something'转换为'Something &'
```

为何this是指针而非引用  
----------------

历史原因：C++加入`this`时引用（reference）尚未存在。现代语言如Java/C#的`this`实现为引用。

[下一课 15.2 — 类与头文件](Chapter-15/lesson15.2-classes-and-header-files.md)  
[返回主页](/)  
[上一课 14.x — 第14章总结与测验](Chapter-14/lesson14.x-chapter-14-summary-and-quiz.md)