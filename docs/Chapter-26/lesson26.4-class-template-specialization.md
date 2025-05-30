26.4 — 类模板特化（class template specialization）  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年7月5日（首次发布于2008年8月16日）  

 

在上一课[26.3 — 函数模板特化（function template specialization）](Chapter-26/lesson26.3-function-template-specialization.md)中，我们学习了如何通过特化函数为特定数据类型提供不同功能。事实上，不仅函数可以特化，类模板也可以进行特化！


考虑需要存储8个对象的场景。以下是一个简化的类模板实现：



```cpp
#include <iostream>

template <typename T>
class Storage8
{
private:
    T m_array[8];

public:
    void set(int index, const T& value)
    {
        m_array[index] = value;
    }

    const T& get(int index) const
    {
        return m_array[index];
    }
};

int main()
{
    // 定义整数类型的Storage8
    Storage8<int> intStorage;

    for (int count{ 0 }; count < 8; ++count)
        intStorage.set(count, count);

    for (int count{ 0 }; count < 8; ++count)
        std::cout << intStorage.get(count) << '\n';

    // 定义布尔类型的Storage8
    Storage8<bool> boolStorage;
    for (int count{ 0 }; count < 8; ++count)
        boolStorage.set(count, count & 3);

	std::cout << std::boolalpha;

    for (int count{ 0 }; count < 8; ++count)
    {
        std::cout << boolStorage.get(count) << '\n';
    }

    return 0;
}
```

该程序输出：



```
0
1
2
3
4
5
6
7
false
true
true
true
false
true
true
true

```

虽然这个类完全可用，但`Storage8<bool>`的实现效率低下。由于变量必须具有地址且CPU无法寻址小于字节的单位，所有变量至少占用1字节。因此，`bool`类型实际仅需1位存储，却占用了整个字节！`Storage8<bool>`存储8个`bool`时，有效信息仅1字节，浪费了7字节空间。


通过位运算，我们可以将8个布尔值压缩到1字节中。为此需要为`bool`类型重新设计类，但若采用新类名会增加复杂度。C++提供了更好的解决方案：类模板特化（class template specialization）。


类模板特化


类模板特化允许为特定数据类型定制模板类。这里我们将为`Storage8<bool>`创建特化版本，覆盖通用模板。


特化类被视为完全独立的类，即使其实例化方式与模板类相同。这意味着我们可以自由修改特化类的实现细节和公开接口。


所有模板特化必须能看到完整定义，且特化前需先定义通用模板。


`Storage8<bool>`特化示例如下：



```cpp
#include <cstdint>

// 先定义通用模板类
template <typename T>
class Storage8
{
private:
    T m_array[8];

public:
    void set(int index, const T& value)
    {
        m_array[index] = value;
    }

    const T& get(int index) const
    {
        return m_array[index];
    }
};

// 定义bool类型的特化版本
template <> // 无模板参数的模板类
class Storage8<bool> // 为bool特化的Storage8
{
private:
    std::uint8_t m_data{}; // 使用8位无符号整型

public:
    // 无需理解以下位运算细节
    void set(int index, bool value)
    {
        auto mask{ 1 << index }; // 生成位掩码

        if (value)  // 置位
            m_data |= mask;   // 位或操作置1
        else  // 复位
            m_data &= ~mask;  // 位与操作置0
	}
	
    bool get(int index)
    {
        auto mask{ 1 << index };
        return (m_data & mask); // 隐式转换为bool
    }
};

// 主函数与之前相同
int main()
{
    // 实例化int版本（使用通用模板）
    Storage8<int> intStorage;

    for (int count{ 0 }; count < 8; ++count)
    {
        intStorage.set(count, count);
	}

    for (int count{ 0 }; count < 8; ++count)
    {
        std::cout << intStorage.get(count) << '\n';
    }

    // 实例化bool版本（使用特化类）
    Storage8<bool> boolStorage;
    
    for (int count{ 0 }; count < 8; ++count)
    {
        boolStorage.set(count, count & 3);
    }

	std::cout << std::boolalpha;

    for (int count{ 0 }; count < 8; ++count)
    {
        std::cout << boolStorage.get(count) << '\n';
    }

    return 0;
}
```

特化类以`template<>`开头表示无模板参数。`<bool>`表明这是`Storage8`的bool特化版本。特化类使用`std::uint8_t`（1字节）替代8元素数组。


当实例化`Storage<T>`（T非bool）时使用通用模板，实例化`Storage8<bool>`时使用特化版本。两者保持相同公开接口，便于统一使用。


程序输出与之前相同：



```
0
1
2
3
4
5
6
7
false
true
true
true
false
true
true
true

```

特化成员函数


在之前课程中我们见过以下示例：


```cpp
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

int main()
{
    // 定义存储单元
    Storage i { 5 };
    Storage d { 6.7 };

    // 输出值
    i.print();
    d.print();
}
```

我们想特化`print()`函数，使双精度数以科学计数法输出。通过类模板特化可以定义`Storage<double>`特化类：



```cpp
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

// 显式的double特化类模板
template <>
class Storage<double>
{
private:
    double m_value {};
public:
    Storage(double value)
      : m_value { value }
    {
    }

    void print();
};

// 在类外定义print（后续解释原因）
void Storage<double>::print()
{
    std::cout << std::scientific << m_value << '\n';
}

int main()
{
    Storage i { 5 };
    Storage d { 6.7 }; // 使用显式特化的Storage<double>

    i.print(); // 调用Storage<int>::print
    d.print(); // 调用Storage<double>::print
}
```

这种方式存在大量冗余代码。更好的方法是让编译器隐式生成`Storage<double>`，仅显式特化`print()`成员函数：



```cpp
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

// 特化Storage<double>::print成员函数
template<>
void Storage<double>::print()
{
    std::cout << std::scientific << m_value << '\n';
}

int main()
{
    Storage i { 5 };
    Storage d { 6.7 }; // 隐式实例化Storage<double>

    i.print(); // 调用通用模板的print
    d.print(); // 调用特化的print
}
```

如前一课所述，显式函数特化不会隐式内联，若在头文件中定义需添加`inline`关键字。


特化类的定义位置


编译器必须同时看到通用模板和特化类的完整定义。通常将特化类定义放在通用模板下方，确保包含头文件时两者都可见。


若特化仅在单个翻译单元使用，可定义在对应的源文件中。其他翻译单元将继续使用通用版本。


避免将特化放在独立头文件中，以防因包含遗漏导致意外使用通用版本。


[下一课 26.5 部分模板特化](Chapter-26/lesson26.5-partial-template-specialization.md)  
[返回主页](/)  
[上一课 26.3 函数模板特化](Chapter-26/lesson26.3-function-template-specialization.md)