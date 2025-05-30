17.5 — 通过std::reference_wrapper实现引用数组
========================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看Alex的所有文章")
2023年9月11日，下午3:50（太平洋夏令时）
2023年10月14日

在上一课中，我们提到数组可以包含任何对象类型的元素。这包括基础类型的对象（如int）和复合类型的对象（如指向int的指针）。
```
#include <array>
#include <iostream>
#include <vector>

int main()
{
    int x { 1 };
    int y { 2 };

    [[maybe_unused]] std::array valarr { x, y };   // int值数组
    [[maybe_unused]] std::vector ptrarr { &x, &y }; // int指针向量
    
    return 0;
}
```
然而，由于引用（reference）不是对象，无法创建引用数组。数组元素必须可赋值，而引用不能重新关联（reseated）。
```
#include <array>
#include <iostream>

int main()
{
    int x { 1 };
    int y { 2 };

    [[maybe_unused]] std::array<int&, 2> refarr { x, y }; // 编译错误：无法定义引用数组

    int& ref1 { x };
    int& ref2 { y };
    [[maybe_unused]] std::array valarr { ref1, ref2 }; // 正确：实际为std::array<int, 2>，而非引用数组

    return 0;
}
```
本课示例将使用`std::array`，但此方法适用于所有数组类型。若需引用数组，可通过替代方案实现。

std::reference_wrapper
----------------
`std::reference_wrapper`是定义在\<functional\>头文件中的标准库类模板。它接受类型模板参数T，行为类似于可修改的T类型左值引用（lvalue reference）。

关于`std::reference_wrapper`需注意：
* `operator=`会重新关联`std::reference_wrapper`（改变引用的对象）。
* `std::reference_wrapper<T>`可隐式转换为`T&`。
* `get()`成员函数用于获取`T&`引用，适用于更新被引用对象的值。

简单示例如下：
```
#include <array>
#include <functional> // 引入std::reference_wrapper
#include <iostream>

int main()
{
    int x { 1 };
    int y { 2 };
    int z { 3 };

    std::array<std::reference_wrapper<int>, 3> arr { x, y, z };
    
    arr[1].get() = 5; // 修改数组元素1引用的对象

    std::cout << arr[1] << y << '\n'; // 显示arr[1]和y已被修改，输出55
    
    return 0;
}
```
输出结果：
```
55
```
注意必须使用`arr[1].get() = 5`而非`arr[1] = 5`。后者存在歧义：编译器无法区分意图是重新关联`std::reference_wrapper<int>`到值5（此操作本非法）还是修改引用值。使用`get()`可消除歧义。

打印`arr[1]`时，编译器会将其隐式转换为可打印的`int&`，因此此处无需`get()`。

std::ref与std::cref
----------------
在C++17之前，CTAD（类模板实参推导（class template argument deduction））尚未出现，必须显式指定类类型的所有模板参数。创建`std::reference_wrapper<int>`需如下操作：
```
    int x { 5 };

    std::reference_wrapper<int> ref1 { x };        // C++11
    auto ref2 { std::reference_wrapper<int>{ x }}; // C++11
```
冗长的名称和显式模板参数使得批量创建引用包装器（reference wrapper）十分繁琐。

为简化操作，标准库提供`std::ref()`和`std::cref()`函数作为快捷方式，分别创建`std::reference_wrapper`和`const std::reference_wrapper`包装对象。这些函数可与`auto`联用避免显式指定模板参数：
```
    int x { 5 };
    auto ref { std::ref(x) };   // C++11，推导为std::reference_wrapper<int>
    auto cref { std::cref(x) }; // C++11，推导为std::reference_wrapper<const int>
```
当然，C++17引入CTAD后也可直接使用：
```
    std::reference_wrapper ref1 { x };        // C++17
    auto ref2 { std::reference_wrapper{ x }}; // C++17
```
但`std::ref()`和`std::cref()`书写更简短，至今仍广泛用于创建`std::reference_wrapper`对象。

[下一课 17.6 — std::array与枚举类型](Chapter-17/lesson17.6-stdarray-and-enumerations.md)
[返回主页](/)  
[上一课 17.4 — 类类型的std::array与大括号省略](Chapter-17/lesson17.4-stdarray-of-class-types-and-brace-elision.md)