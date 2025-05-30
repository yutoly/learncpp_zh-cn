26.1 — 模板类（Template classes）  
========================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年7月23日（首次发布于2008年6月16日）  

在[11.6 — 函数模板](Chapter-11/lesson11.6-function-templates.md)章节中，我们学习了如何通过函数模板（function templates）实现函数的通用化。虽然这是迈向泛型编程的重要一步，但仍有未解决的挑战。让我们通过具体案例来探索模板的更多应用。  

模板与容器类（Templates and container classes）  
----------------  

在[23.6 — 容器类](Chapter-23/lesson23.6-container-classes.md)课程中，我们通过组合（composition）实现了包含多个类实例的容器类。以IntArray类为例，以下是一个简化版本：  
```
#ifndef INTARRAY_H
#define INTARRAY_H

#include <cassert>

class IntArray
{
private:
    int m_length{};
    int* m_data{};

public:
    IntArray(int length)
    {
        assert(length > 0);
        m_data = new int[length]{};
        m_length = length;
    }

    IntArray(const IntArray&) = delete;
    IntArray& operator=(const IntArray&) = delete;

    ~IntArray()
    {
        delete[] m_data;
    }

    void erase()
    {
        delete[] m_data;
        m_data = nullptr;
        m_length = 0;
    }

    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }

    int getLength() const { return m_length; }
};

#endif
```  
若需创建双精度数组类DoubleArray，传统方法需要完整复制并修改数据类型：  
```
#ifndef DOUBLEARRAY_H
#define DOUBLEARRAY_H

#include <cassert>

class DoubleArray
{
private:
    int m_length{};
    double* m_data{};

public:
    DoubleArray(int length)
    {
        assert(length > 0);
        m_data = new double[length]{};
        m_length = length;
    }

    // 其他成员与IntArray相同...
};
#endif
```  
两类的唯一实质差异是数据类型（int vs double）。这正是模板（templates）大显身手的场景。  

创建模板类  
----------------  
模板类的创建方式与模板函数相似。以下是模板化的数组类：  
Array.h:  
```
#ifndef ARRAY_H
#define ARRAY_H

#include <cassert>

template <typename T> // 新增模板声明
class Array
{
private:
    int m_length{};
    T* m_data{}; // 类型改为T

public:
    Array(int length)
    {
        assert(length > 0);
        m_data = new T[length]{}; // 分配T类型数组
        m_length = length;
    }

    // 禁止拷贝
    Array(const Array&) = delete;
    Array& operator=(const Array&) = delete;

    ~Array()
    {
        delete[] m_data;
    }

    void erase()
    {
        delete[] m_data;
        m_data = nullptr;
        m_length = 0;
    }

    T& operator[](int index); // 返回T&
    int getLength() const { return m_length; }
};

template <typename T>
T& Array<T>::operator[](int index)
{
    assert(index >= 0 && index < m_length);
    return m_data[index];
}

#endif
```  
该版本与IntArray的主要区别是添加了模板声明，并将数据类型替换为T。注意在类外定义`operator[]`时需要独立的模板声明，类名应使用Array<T>（除非在类内部使用）。  

使用示例：  
```
#include <iostream>
#include "Array.h"

int main()
{
	const int length{12};
	Array<int> intArray{length};
	Array<double> doubleArray{length};

	for (int count{0}; count < length; ++count)
	{
		intArray[count] = count;
		doubleArray[count] = count + 0.5;
	}

	for (int count{length-1}; count >= 0; --count)
		std::cout << intArray[count] << '\t' << doubleArray[count] << '\n';

	return 0;
}
```  
输出：  
```
11      11.5
10      10.5
9       9.5
...
0       0.5
```  
模板类的实例化方式与模板函数相同——编译器按需生成特定类型的副本。模板类非常适合容器类（container classes）的实现，能有效避免代码重复。  

模板类的分割问题  
----------------  
模板不是具体的类或函数，而是生成它们的模具。这导致传统头文件/源文件分离方法失效。考虑以下错误示例：  
Array.h声明模板类，Array.cpp定义`operator[]`，main.cpp使用模板。编译时将产生链接错误：  
```
未定义引用 `Array<int>::operator[](int)'
```  
问题根源在于编译器需要在翻译单元（translation unit）中同时看到完整模板定义和具体类型才能实例化。解决方案：  

1. **单文件方案**：将所有模板代码放入头文件。优点简单，缺点可能增加编译时间。  
2. **.inl文件方案**：将成员函数定义移至Array.inl，并在Array.h底部包含该文件。需确保.inl文件不被单独编译。  
3. **显式实例化方案**：创建templates.cpp文件显式实例化所需类型：  
```
#include "Array.h"
#include "Array.cpp" // 违反常规但特殊处理

template class Array<int>;  // 显式实例化
template class Array<double>;
```  
其他文件包含Array.h后，链接器会使用这些显式实例化定义。此方法效率较高但需维护实例化列表。  

下一课：[26.2 — 模板非类型参数](Chapter-26/lesson26.2-template-non-type-parameters.md)  
[返回主页](/)  
[上一课：25.x — 第25章总结与测验](Chapter-25/lesson25.x-chapter-25-summary-and-quiz.md)