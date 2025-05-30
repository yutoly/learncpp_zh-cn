22.3 — 移动构造函数与移动赋值  
=============================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月26日（首次发布于2017年2月18日）  

 

在课程[22.1 — 智能指针与移动语义简介](Chapter-22/lesson22.1-introduction-to-smart-pointers-move-semantics.md)中，我们探讨了std::auto_ptr，讨论了移动语义的需求，并分析了为复制语义设计的函数（拷贝构造函数和拷贝赋值运算符）被重新定义以实现移动语义时可能产生的问题。


本课程将深入探讨C++11如何通过移动构造函数（move constructor）和移动赋值运算符（move assignment operator）解决这些问题。


回顾拷贝构造函数与拷贝赋值  
----------------  

首先回顾复制语义的基本概念。


拷贝构造函数（copy constructor）通过复制同类对象来初始化新对象。拷贝赋值运算符（copy assignment operator）用于将对象复制到已存在的对象。默认情况下，若未显式提供这些函数，C++将提供浅拷贝版本。处理动态内存的类应重写这些函数以实现深拷贝。


以本章首课的Auto_ptr智能指针类为例，以下是实现深拷贝的版本及测试程序：


```cpp
#include <iostream>

template<typename T>
class Auto_ptr3
{
    T* m_ptr {};
public:
    Auto_ptr3(T* ptr = nullptr) : m_ptr{ ptr } {}
    
    ~Auto_ptr3() { delete m_ptr; }

    // 深拷贝构造函数
    Auto_ptr3(const Auto_ptr3& a)
    {
        m_ptr = new T;
        *m_ptr = *a.m_ptr;
    }

    // 深拷贝赋值
    Auto_ptr3& operator=(const Auto_ptr3& a)
    {
        if (&a == this) return *this;
        delete m_ptr;
        m_ptr = new T;
        *m_ptr = *a.m_ptr;
        return *this;
    }

    T& operator*() const { return *m_ptr; }
    T* operator->() const { return m_ptr; }
    bool isNull() const { return m_ptr == nullptr; }
};

class Resource
{
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; }
};

Auto_ptr3<Resource> generateResource()
{
    Auto_ptr3<Resource> res{new Resource};
    return res; // 触发拷贝构造函数
}

int main()
{
    Auto_ptr3<Resource> mainres;
    mainres = generateResource(); // 触发拷贝赋值
    return 0;
}
```

运行该程序将输出：

```
Resource acquired
Resource acquired
Resource destroyed
Resource acquired
Resource destroyed
Resource destroyed
```

（注：若编译器优化了返回值，可能仅显示4条输出）


程序执行流程分析：  
1. generateResource()中创建res，触发首次资源获取  
2. 返回res时触发拷贝构造，创建新资源  
3. res析构，释放原始资源  
4. 临时对象赋值给mainres时触发拷贝赋值，创建新资源  
5. 临时对象析构  
6. mainres析构  


这种实现虽安全但效率低下，共创建销毁3次资源。


移动构造函数与移动赋值  
----------------  

C++11通过移动语义解决此问题。移动构造函数（move constructor）和移动赋值运算符（move assignment operator）用于转移资源所有权而非复制。其参数为非常量右值引用（non-const rvalue reference），仅绑定右值。


改进后的Auto_ptr4类：

```cpp
template<typename T>
class Auto_ptr4
{
    T* m_ptr {};
public:
    // ... 构造函数与析构函数同前

    // 移动构造函数
    Auto_ptr4(Auto_ptr4&& a) noexcept
        : m_ptr{ a.m_ptr }
    {
        a.m_ptr = nullptr; // 转移后置空原指针
    }

    // 移动赋值
    Auto_ptr4& operator=(Auto_ptr4&& a) noexcept
    {
        if (&a == this) return *this;
        delete m_ptr;
        m_ptr = a.m_ptr;
        a.m_ptr = nullptr;
        return *this;
    }

    // ... 其他成员同前
};
```

运行改进后的程序，输出简化为：

```
Resource acquired
Resource destroyed
```

流程变化：  
1. generateResource()创建res  
2. 返回值时触发移动构造，转移资源到临时对象  
3. res析构（无资源可释放）  
4. 临时对象移动赋值给mainres  
5. 临时对象析构（无资源）  
6. mainres析构  


关键改进：资源仅被创建销毁一次。


相关说明  
----------------  

* **noexcept声明**：移动操作应标记为`noexcept`，表示不抛出异常。详见课程[27.9 — 异常规范与noexcept](Chapter-27/lesson27.9-exception-specifications-and-noexcept.md)  
* **隐式移动操作**：当满足以下条件时，编译器生成隐式移动函数：  
  - 无用户声明的拷贝操作  
  - 无用户声明的移动操作  
  - 无用户声明的析构函数  
  这些函数执行成员级移动（memberwise move），指针会被拷贝而非移动  
* **五法则（Rule of Five）**：若定义或删除拷贝构造函数、拷贝赋值、移动构造函数、移动赋值、析构函数中的任意一个，应显式处理所有五个函数  


禁用拷贝的示例  
----------------  

```cpp
template<typename T>
class Auto_ptr5
{
    // ... 基础成员同前

    // 禁用拷贝
    Auto_ptr5(const Auto_ptr5&) = delete;
    Auto_ptr5& operator=(const Auto_ptr5&) = delete;

    // 启用移动
    Auto_ptr5(Auto_ptr5&& a) noexcept : m_ptr{a.m_ptr} { a.m_ptr = nullptr; }
    Auto_ptr5& operator=(Auto_ptr5&& a) noexcept { /* 移动逻辑 */ }
};
```

此实现类似标准库的`std::unique_ptr`。


动态数组案例  
----------------  

深拷贝版本的动态数组类：

```cpp
template <typename T>
class DynamicArray
{
    T* m_array {};
    int m_length {};
    // ... 深拷贝构造与拷贝赋值
};

// 测试函数
DynamicArray<int> cloneArrayAndDouble(const DynamicArray<int>& arr)
{
    DynamicArray<int> dbl(arr.getLength());
    // ... 复制并加倍元素
}
```

替换为移动操作后，百万元素数组处理时间从0.00825秒降至0.0056秒，性能提升32.1%。


禁用移动操作  
----------------  

```cpp
class Name
{
    std::string m_name;
public:
    Name(Name&&) = delete;  // 禁用移动构造
    Name& operator=(Name&&) = delete; // 禁用移动赋值
};
```

若仅禁用移动操作但保留拷贝，可能导致返回值优化失败（因编译器仍尝试使用已删除的移动构造）。


swap问题与解决方案  
----------------  

错误实现会导致无限递归：

```cpp
// 错误示例
Name(Name&& name)
{
    std::swap(*this, name); // 调用std::swap会触发移动构造
}
```

正确方式应使用自定义swap函数：

```cpp
friend void swap(Name& a, Name& b) noexcept
{
    std::swap(a.m_name, b.m_name); // 直接交换成员
}

Name(Name&& name) noexcept
{
    swap(*this, name); // 调用自定义swap
}
```


[下一课 22.4 — std::move](Chapter-22/lesson22.4-stdmove.md)  
[返回主页](/)  
[上一课 22.2 — 右值引用](Chapter-22/lesson22.2-rvalue-references.md)