26.2 — 模板非类型参数
=====================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日（首次发布于2008年6月19日）

在前几课中，我们学习了如何使用模板类型参数（template type parameters）创建与类型无关的函数和类。模板类型参数是作为实参传入类型的占位符。

但模板类型参数并非唯一可用的模板参数类型。模板类和函数还可使用另一种称为非类型参数（non-type parameters）的模板参数。

**非类型参数**

模板非类型参数指参数类型已预定义，并由作为实参传入的 constexpr（常量表达式）值替代的模板参数。

非类型参数可以是以下任意类型：
* 整型（integral type）
* 枚举类型（enumeration type）
* 类对象的指针或引用
* 函数的指针或引用
* 类成员函数的指针或引用
* std::nullptr_t
* 浮点类型（floating point type）（自 C++20 起）

以下示例创建了同时使用类型参数和非类型参数的非动态（静态）数组类。类型参数控制静态数组的数据类型，整型非类型参数控制静态数组大小：

```cpp
#include <iostream>

template <typename T, int size> // size 是整型非类型参数
class StaticArray
{
private:
    // 非类型参数控制数组大小
    T m_array[size] {};

public:
    T* getArray();
    
    T& operator[](int index)
    {
        return m_array[index];
    }
};

// 演示含非类型参数的类外函数定义
template <typename T, int size>
T* StaticArray<T, size>::getArray()
{
    return m_array;
}

int main()
{
    // 声明含 12 个整数的数组
    StaticArray<int, 12> intArray;

    // 按顺序填充并逆序打印
    for (int count { 0 }; count < 12; ++count)
        intArray[count] = count;

    for (int count { 11 }; count >= 0; --count)
        std::cout << intArray[count] << ' ';
    std::cout << '\n';

    // 声明含 4 个双精度浮点数的缓冲区
    StaticArray<double, 4> doubleArray;

    for (int count { 0 }; count < 4; ++count)
        doubleArray[count] = 4.4 + 0.1 * count;

    for (int count { 0 }; count < 4; ++count)
        std::cout << doubleArray[count] << ' ';

    return 0;
}
```

该代码输出如下：
```
11 10 9 8 7 6 5 4 3 2 1 0
4.4 4.5 4.6 4.7
```

此例值得注意之处在于：我们无需动态分配 m_array 成员变量！因为对于 StaticArray 类的任何实例，size 必须是 constexpr（编译期常量）。例如实例化 StaticArray<int, 12> 时，编译器会将 size 替换为 12，因此 m_array 类型为 int[12]，可静态分配。

标准库类 std::array 即利用此特性。当声明 std::array<int, 5> 时，int 是类型参数，5 是非类型参数！

注意：若尝试用非 constexpr 值实例化模板非类型参数将失败：
```cpp
template <int size>
class Foo
{
};

int main()
{
    int x{ 4 }; // x 非 constexpr
    Foo<x> f;   // 错误：模板非类型实参必须是 constexpr
    return 0;
}
```
此时编译器将报错。

[下一课 26.3 函数模板特化](Chapter-26/lesson26.3-function-template-specialization.md)  
[返回主页](/)  
[上一课 26.1 模板类](Chapter-26/lesson26.1-template-classes.md)