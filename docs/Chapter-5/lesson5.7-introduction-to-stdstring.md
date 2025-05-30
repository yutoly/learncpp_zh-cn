5.7 — std::string简介  
==================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2015年5月8日，上午7:59（太平洋夏令时）  
2025年1月3日更新  

在课程[5.2 — 字面量](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)中，我们介绍了C风格字符串字面量：
```cpp
#include <iostream>
 
int main()
{
    std::cout << "Hello, world!"; // "Hello world!"是C风格字符串字面量
    return 0;
}
```
虽然C风格字符串字面量可以使用，但C风格字符串变量行为异常、难以操作（例如无法通过赋值更新其值）且存在安全隐患（例如：将较长字符串复制到较短字符串分配的空间会导致未定义行为）。在现代C++中，应尽量避免使用C风格字符串变量。  

幸运的是，C++引入了两种更易用且更安全的字符串类型：`std::string` 和 `std::string_view`（C++17）。与之前介绍的类型不同，`std::string` 和 `std::string_view` 非基本类型（它们是类类型，将在后续课程讨论）。但两者的基础用法足够直观实用，我们在此先行介绍。  

## std::string 简介  
在C++中操作字符串最便捷的方式是通过定义在<string>头文件中的 `std::string` 类型。  

创建 `std::string` 对象的方式与其他对象相同：
```cpp
#include <string> // 允许使用std::string

int main()
{
    std::string name {}; // 空字符串
    return 0;
}
```
与普通变量类似，可按预期对std::string对象初始化或赋值：
```cpp
#include <string>

int main()
{
    std::string name { "Alex" }; // 用字面量"Alex"初始化name
    name = "John";               // 将name改为"John"
    return 0;
}
```
注意：字符串可由数字字符组成：
```cpp
std::string myID{ "45" }; // "45"与整数45不同！
```
字符串形式的数字被视为文本而非数值，因此无法进行数学运算（例如乘法）。C++不会自动在字符串与整型/浮点型数值间转换（相关方法将在后续课程介绍）。  

## 使用 std::cout 输出字符串  
`std::string` 对象可通过 `std::cout` 正常输出：
```cpp
#include <iostream>
#include <string>

int main()
{
    std::string name { "Alex" };
    std::cout << "我的名字是：" << name << '\n';
    return 0;
}
```
输出结果：
```
我的名字是：Alex
```
空字符串将无输出：
```cpp
#include <iostream>
#include <string>

int main()
{
    std::string empty{ };
    std::cout << '[' << empty << ']';
    return 0;
}
```
输出结果：
```
[]
```

## std::string 可处理不同长度的字符串  
`std::string` 最便捷的特性之一是能存储不同长度的字符串：
```cpp
#include <iostream>
#include <string>

int main()
{
    std::string name { "Alex" }; // 用字面量"Alex"初始化
    std::cout << name << '\n';

    name = "Jason";              // 改为更长字符串
    std::cout << name << '\n';

    name = "Jay";                // 改为更短字符串
    std::cout << name << '\n';
    return 0;
}
```
输出结果：
```
Alex
Jason
Jay
```
上例中，`name` 用含5字符（4个显式字符+空终止符）的 `"Alex"` 初始化，后改为更长和更短字符串。`std::string` 能完美处理！甚至可在 `std::string` 中存储超长字符串，这是其强大特性的体现。  

> **关键洞察**  
> 若 `std::string` 内存不足，会通过动态内存分配（dynamic memory allocation）在运行时申请额外内存。这种内存获取能力使其高度灵活，但也导致速度相对较慢（我们将在后续章节讨论动态内存分配）。  

## 使用 std::cin 输入字符串  
通过 `std::cin` 输入 `std::string` 可能出现意外：
```cpp
#include <iostream>
#include <string>

int main()
{
    std::cout << "请输入全名：";
    std::string name{};
    std::cin >> name; // 因std::cin遇空白符截断，结果不符合预期

    std::cout << "请输入最喜欢的颜色：";
    std::string color{};
    std::cin >> color;

    std::cout << "您的名字是" << name 
              << "，最喜欢的颜色是" << color << '\n';
    return 0;
}
```
程序运行示例：
```
请输入全名：John Doe
请输入最喜欢的颜色：您的名字是John，最喜欢的颜色是Doe
```
结果异常！原因在于：使用 `operator>>` 从 `std::cin` 提取字符串时，该运算符仅返回首个空白符前的字符，其余字符留在 `std::cin` 中等待下次提取。  

因此提取到 `name` 时仅获得 `"John"`，`" Doe"` 留在 `std::cin` 内。当再次提取到 `color` 时，直接获取了 `"Doe"` 而非等待新输入。  

## 使用 std::getline() 输入文本  
要读取整行文本，应改用 `std::getline()` 函数。该函数需两个参数：`std::cin` 和字符串变量。  

改进后的程序：
```cpp
#include <iostream>
#include <string> // 需包含此头文件以使用std::string和std::getline

int main()
{
    std::cout << "请输入全名：";
    std::string name{};
    std::getline(std::cin >> std::ws, name); // 读取整行文本到name

    std::cout << "请输入最喜欢的颜色：";
    std::string color{};
    std::getline(std::cin >> std::ws, color); // 读取整行文本到color

    std::cout << "您的名字是" << name 
              << "，最喜欢的颜色是" << color << '\n';
    return 0;
}
```
现在程序运行符合预期：
```
请输入全名：John Doe
请输入最喜欢的颜色：蓝色
您的名字是John Doe，最喜欢的颜色是蓝色
```

## std::ws 的作用  
在课程[4.8 — 浮点数](Chapter-4/lesson4.8-floating-point-numbers.md)中，我们讨论了可改变输出显示方式的输出操纵器（output manipulator），例如用 `std::setprecision()` 设置输出精度。  

C++也支持改变输入接收方式的输入操纵器（input manipulator）。`std::ws` 输入操纵器指示 `std::cin` 在提取前忽略所有前导空白符（leading whitespace）。前导空白符指字符串开头出现的空白字符（空格、制表符、换行符）。  

通过以下程序探究其必要性：
```cpp
#include <iostream>
#include <string>

int main()
{
    std::cout << "选择1或2：";
    int choice{};
    std::cin >> choice;

    std::cout << "请输入姓名：";
    std::string name{};
    std::getline(std::cin, name); // 注意：未使用std::ws

    std::cout << "您好，" << name 
              << "，您选择了" << choice << '\n';
    return 0;
}
```
运行输出：
```
选择1或2：2
请输入姓名：您好，，您选择了2
```
程序首先要求输入1或2，此时运行正常。但当要求输入姓名时，并未等待输入就直接输出了结果。  

原因在于：使用 `operator>>` 输入时，`std::cin` 不仅捕获输入值，还会捕获按下回车键时产生的换行符（`'\n'`）。输入 `2` 后按回车，`std::cin` 捕获 `"2\n"`，提取 `2` 到 `choice` 后留下换行符。当 `std::getline()` 尝试提取文本到 `name` 时，发现 `std::cin` 中已有 `"\n"`，将其视为空字符串输入。  

使用 `std::ws` 可修正此问题：
```cpp
#include <iostream>
#include <string>

int main()
{
    std::cout << "选择1或2：";
    int choice{};
    std::cin >> choice;

    std::cout << "请输入姓名：";
    std::string name{};
    std::getline(std::cin >> std::ws, name); // 注意：添加了std::ws

    std::cout << "您好，" << name 
              << "，您选择了" << choice << '\n';
    return 0;
}
```
现在程序运行符合预期：
```
选择1或2：2
请输入姓名：Alex
您好，Alex，您选择了2
```

> **最佳实践**  
> 使用 `std::getline()` 读取字符串时，应通过 `std::cin >> std::ws` 忽略前导空白符。需对每次 `std::getline()` 调用执行此操作，因 `std::ws` 的效果不跨调用保留。  

> **关键洞察**  
> 提取到变量时，提取运算符（`>>`）会忽略前导空白符，并在遇到非前导空白符时停止提取。  
> `std::getline()` 不忽略前导空白符。如需忽略，应将 `std::cin >> std::ws` 作为首个参数。它在遇到换行符时停止提取。  

## std::string 的长度  
要获取 `std::string` 的字符数，可调用其长度获取方法。语法形式如下：
```cpp
#include <iostream>
#include <string>

int main()
{
    std::string name{ "Alex" };
    std::cout << name << "有" 
              << name.length() << "个字符\n";
    return 0;
}
```
输出结果：
```
Alex有4个字符
```
虽然 `std::string` 必须空终止（null-terminated）（C++11起），但其返回长度不包含隐式空终止符。  

注意：获取长度的 `length()` 不是独立函数，而是嵌套在 `std::string` 内的特殊函数——成员函数（member function）。因其声明在 `std::string` 内部，文档中常写作 `std::string::length()`。  

> **关键洞察**  
> 普通函数调用形式为 `函数(对象)`，成员函数调用形式为 `对象.函数()`。  

> **注意**  
> `std::string::length()` 返回无符号整型值（通常为 `size_t`）。若需赋给 `int` 变量，应使用 `static_cast` 避免有符号/无符号转换警告：
> ```cpp
> int length { static_cast<int>(name.length()) };
> ```

> **进阶阅读**  
> C++20中可用 `std::ssize()` 获取带符号的大整型长度（通常为 `std::ptrdiff_t`）：
> ```cpp
> #include <iostream>
> #include <string>
> 
> int main()
> {
>     std::string name{ "Alex" };
>     std::cout << name << "有" 
>               << std::ssize(name) << "个字符\n";
>     return 0;
> }
> ```
> 因 `ptrdiff_t` 可能大于 `int`，若需将结果存入 `int` 变量，应进行 `static_cast` 转换：
> ```cpp
> int len { static_cast<int>(std::ssize(name)) };
> ```

## 初始化 std::string 的开销  
每当初始化 std::string 时，都会复制初始字符串。字符串复制开销较大，应尽量减少复制次数。  

## 不要按值传递 std::string  
当 `std::string` 按值传递给函数时，函数参数需实例化并初始化，导致高开销复制。替代方案（使用 `std::string_view`）将在课程[5.8 — std::string_view 简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)讨论。  

> **最佳实践**  
> 避免按值传递 `std::string`，因其会产生高开销复制。  

> **提示**  
> 多数情况下，应改用 `std::string_view` 参数（见课程[5.8 — std::string_view 简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)）。  

## 返回 std::string  
函数通过值返回时，返回值通常从函数复制回调用方。因此可能认为按值返回 `std::string` 会产生高开销复制。  

但经验法则：当返回语句表达式属于以下情况时，可安全按值返回 `std::string`：  
* `std::string` 类型的局部变量  
* 通过值返回的函数调用或运算符产生的 `std::string`  
* 在返回语句中创建的 `std::string` 临时对象  

> **进阶阅读**  
> `std::string` 支持移动语义（move semantics），允许在函数结束时将被销毁的对象按值返回而无需复制。移动语义原理超出本文范围，将在课程[16.5 — 返回 std::vector 及移动语义简介](Chapter-16/lesson16.5-returning-stdvector-and-an-introduction-to-move-semantics.md)介绍。  

多数其他情况下，应避免按值返回 `std::string` 以减少高开销复制。  

> **提示**  
> 若返回C风格字符串字面量，应改用 `std::string_view` 返回类型（见课程[5.9 — std::string_view（下）](Chapter-5/lesson5.9-stdstring_view-part-2.md)）。  

> **进阶阅读**  
> 某些情况下，`std::string` 也可通过（const）引用返回以避免复制，详见课程[12.12 — 按引用返回与按地址返回](Chapter-12/lesson12.12-return-by-reference-and-return-by-address.md)和[14.6 — 访问函数](Chapter-14/lesson14.6-access-functions.md)。  

## std::string 的字面量  
双引号字符串字面量（如"Hello, world!"）默认是C风格字符串（故类型特殊）。  

可通过在双引号字面量后添加小写 `s` 后缀创建 `std::string` 类型的字符串字面量：
```cpp
#include <iostream>
#include <string> // 需包含此头文件以使用std::string

int main()
{
    using namespace std::string_literals; // 便于访问s后缀

    std::cout << "foo\n";   // 无后缀是C风格字符串字面量
    std::cout << "goo\n"s;  // s后缀是std::string字面量
    return 0;
}
```

> **提示**  
> "s"后缀位于命名空间 `std::literals::string_literals`。  
> 最简访问方式是使用 using 指令 `using namespace std::literals`，但此操作会导入标准库所有字面量。  
> 建议使用 `using namespace std::string_literals` 仅导入 `std::string` 字面量（using 指令用法详见课程[7.13 — using声明与using指令](Chapter-7/lesson7.13-using-declarations-and-using-directives.md)）。因后缀定义与代码冲突概率低，此类 using 指令通常可接受，但避免在头文件的函数外部使用。  

通常无需频繁使用 `std::string` 字面量（因可用C风格字符串字面量初始化 `std::string` 对象），但在涉及类型推导的某些场景（见课程[10.8 — 使用auto关键字进行对象类型推导](Chapter-10/lesson10.8-type-deduction-for-objects-using-the-auto-keyword.md)示例）中会更便捷。  

> **进阶阅读**  
> `"Hello"s` 解析为 `std::string { "Hello", 5 }`，这会创建用C风格字符串字面量"Hello"（长度5，不含隐式空终止符）初始化的临时 `std::string`。  

## 常量表达式字符串  
若尝试定义 `constexpr std::string`，编译器可能报错：
```cpp
#include <iostream>
#include <string>

int main()
{
    using namespace std::string_literals;

    constexpr std::string name{ "Alex"s }; // 编译错误

    std::cout << "我的名字是：" << name;
    return 0;
}
```
因为 `constexpr std::string` 在C++17及更早版本完全不支持，在C++20/23中仅有限支持。如需常量表达式字符串，请改用 `std::string_view`（见课程[5.8 — std::string_view 简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)）。  

## 结论  
`std::string` 的实现涉及许多未涵盖的语言特性，较为复杂。但幸运的是，进行基础字符串输入输出等简单任务时无需理解这些复杂性。鼓励您现在开始实践字符串操作，后续课程将深入探讨更多字符串功能。  

## 测验  
**问题1**  
编写程序要求用户输入全名和年龄，输出年龄与名字字符数之和（使用 `std::string::length()` 成员函数获取字符串长度）。为简化处理，将名字中的空格计为字符。  

样例输出：
```
请输入全名：John Doe
请输入年龄：32
您的年龄+名字长度=40
```
提示：注意避免混合有符号和无符号值。`std::string::length()` 返回无符号值。若支持C++20，使用 `std::ssize()` 获取带符号长度；否则将 `std::string::length()` 返回值 static_cast 为 int。  

<details><summary>查看答案</summary>

```cpp
#include <iostream>
#include <string>

int main()
{
    std::cout << "请输入全名：";
    std::string name{};
    std::getline(std::cin >> std::ws, name); // 读取整行文本到name

    std::cout << "请输入年龄：";
    int age{}; // age需为整型以进行数学运算
    std::cin >> age;

    // age为有符号，name.length()为无符号——不应混合使用
    // 将name.length()转为有符号值
    int nameLen { static_cast<int>(name.length()) }; // 获取名字字符数（含空格）
    std::cout << "您的年龄+名字长度=" << age + nameLen << '\n';
    return 0;
}
```
</details>

[下一课 5.8 std::string_view 简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)  
[返回目录](/)  
[上一课 5.6 常量表达式变量](Chapter-5/lesson5.6-constexpr-variables.md)