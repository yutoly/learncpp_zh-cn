23.6 — 容器类  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月30日（首次发布于2007年12月14日）  

现实世界中，我们时刻在使用容器。早餐麦片装在盒子里，书籍页面通过封面和装订组合，车库中各种物品也存储在容器里。若没有容器，处理这些物品将变得极其不便。试想阅读没有装订的散页书籍，或者不使用碗直接食用无包装的麦片，场面必定混乱。容器的核心价值在于其组织和存储物品的能力。  

类似地，**容器类（container class）**是用于保存和组织其他类型（可以是其他类或基础类型）多个实例的类。存在多种不同容器类，各自在使用中具有不同的优势、局限和约束。迄今为止编程中最常用的容器是数组（array），您已见过多个示例。尽管C++内置了数组功能，程序员通常更倾向于使用数组容器类（如std::array或std::vector），因为它们提供了额外优势。与内置数组不同，数组容器类通常支持动态调整大小（增删元素时）、在传递到函数时记录自身尺寸，并进行边界检查。这不仅使数组容器类比普通数组更方便，也更安全。  

容器类通常实现一组标准化的基础功能。定义良好的容器通常包含以下功能：  
* 创建空容器（通过构造函数）  
* 插入新对象到容器  
* 从容器移除对象  
* 报告当前容器内对象数量  
* 清空容器内所有对象  
* 提供存储对象的访问方式  
* 元素排序（可选功能）  

某些容器类可能省略部分功能。例如，数组容器类常省略插入和移除函数，因这些操作效率较低且类设计者不希望鼓励其使用。  

容器类实现成员归属关系。例如，数组元素属于（从属于）数组。注意此处"成员归属"是常规语义，而非C++类成员的特定含义。  

**容器类型**  
容器类通常分为两种形式。**值容器（value containers）**是组合关系，存储所持有对象的副本（因而负责这些副本的创建和销毁）。**引用容器（reference containers）**是聚合关系，存储指向其他对象的指针或引用（因而不负责这些对象的创建和销毁）。  

与现实世界容器可容纳任意类型不同，C++容器通常只存储单一数据类型。例如整型数组仅保存整数。与某些语言不同，多数C++容器不允许随意混合类型。若需同时保存整数和双精度数，通常需要编写两个独立容器（或使用模板——C++高级特性）。尽管存在使用限制，容器仍然极其有用，它们使编程更简单、安全和高效。  

**数组容器类示例**  
本例将从头编写实现多数容器基础功能的整型数组类。该数组类为值容器，保存所组织元素的副本。如其名称所示，该容器将保存整型数组，类似于`std::vector<int>`。  

首先创建IntArray.h文件：
```cpp
#ifndef INTARRAY_H
#define INTARRAY_H

class IntArray
{
};

#endif
```
IntArray需要跟踪两个值：数据本身和数组长度。由于需要动态调整大小，必须使用指针存储数据：
```cpp
#ifndef INTARRAY_H
#define INTARRAY_H

#include <cassert>   // 用于assert()
#include <cstddef>   // 用于std::size_t

class IntArray
{
private:
    int m_length{};
    int* m_data{};

public:
    IntArray() = default;

    IntArray(int length):
        m_length{ length }
    {
        assert(length >= 0);

        if (length > 0)
            m_data = new int[static_cast<std::size_t>(length)]{};
    }
};
#endif
```
添加清理功能。首先编写析构函数，其次定义erase()函数：
```cpp
    ~IntArray()
    {
        delete[] m_data;
        // 无需在此置空m_data或m_length，对象将立即销毁
    }

    void erase()
    {
        delete[] m_data;
        m_data = nullptr;  // 必须置空，避免悬垂指针
        m_length = 0;
    }
```
重载[]运算符并添加长度访问函数：
```cpp
    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }

    int getLength() const { return m_length; }
```
添加调整大小功能：
```cpp
#include <algorithm> // 用于std::copy_n

    // 快速调整大小，销毁原有元素
    void reallocate(int newLength)
    {
        erase();
        if (newLength <= 0) return;
        m_data = new int[static_cast<std::size_t>(newLength)];
        m_length = newLength;
    }

    // 保留原有元素的调整大小
    void resize(int newLength)
    {
        if (newLength == m_length) return;
        if (newLength <= 0) return erase();

        int* data{ new int[static_cast<std::size_t>(newLength)] };
        if (m_length > 0) {
            int elementsToCopy = (newLength > m_length) ? m_length : newLength;
            std::copy_n(m_data, elementsToCopy, data);
        }
        delete[] m_data;
        m_data = data;
        m_length = newLength;
    }
```
添加拷贝控制：
```cpp
    IntArray(const IntArray& a): IntArray(a.getLength())
    {
        std::copy_n(a.m_data, m_length, m_data);
    }

    IntArray& operator=(const IntArray& a)
    {
        if (&a == this) return *this;
        reallocate(a.getLength());
        std::copy_n(a.m_data, m_length, m_data);
        return *this;
    }
```
实现插入删除功能：
```cpp
    void insertBefore(int value, int index)
    {
        assert(index >= 0 && index <= m_length);
        int* data{ new int[static_cast<std::size_t>(m_length+1)] };
        std::copy_n(m_data, index, data);
        data[index] = value;
        std::copy_n(m_data + index, m_length - index, data + index + 1);
        delete[] m_data;
        m_data = data;
        ++m_length;
    }

    void remove(int index)
    {
        assert(index >= 0 && index < m_length);
        if (m_length == 1) return erase();
        int* data{ new int[static_cast<std::size_t>(m_length-1)] };
        std::copy_n(m_data, index, data);
        std::copy_n(m_data + index + 1, m_length - index - 1, data + index);
        delete[] m_data;
        m_data = data;
        --m_length;
    }
```
完整IntArray.h代码参见原文。测试代码：
```cpp
#include <iostream>
#include "IntArray.h"

int main()
{
    IntArray array(10);
    for (int i{0}; i<10; ++i) array[i] = i+1;
    array.resize(8);
    array.insertBefore(20, 5);
    array.remove(3);
    array.insertAtEnd(30);
    array.insertAtBeginning(40);
    // 拷贝测试
    {
        IntArray b{ array };
        b = array;
    }
    for (int i{0}; i<array.getLength(); ++i)
        std::cout << array[i] << ' ';
    std::cout << '\n';
    return 0;
}
```
输出结果：
```
40 1 2 3 5 20 6 7 8 30
```
改进建议：  
* 模板化以支持多类型  
* 添加const成员函数重载  
* 支持移动语义  
* 异常安全优化  

**重要提示**：标准库容器（如`std::vector`）已通过充分测试，应优先使用。仅在需要特殊功能时自行实现容器类。  

[下一课 23.7 — std::initializer_list](Chapter-23/lesson23.7-stdinitializer_list.md)  
[返回主页](/)  
[上一课 23.5 — 依赖关系](Chapter-23/lesson23.5-dependencies.md)