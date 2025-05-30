17.7 — C风格数组简介  
=======================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月27日（首次发布）  
2024年10月13日（最后更新）  

 


 

在学习了`std::vector`和`std::array`后，我们将通过介绍最后一种数组类型——C风格数组（C-style arrays）来完成数组知识体系的构建。


如课程[16.1 — 容器与数组简介](Chapter-16/lesson16.1-introduction-to-containers-and-arrays.md)所述，C风格数组继承自C语言，是C++核心语言的内建特性（与其他标准库容器类数组不同）。这意味着使用它们时无需包含头文件。


> **旁注**  
> 由于它们是语言原生支持的唯一数组类型，标准库的数组容器类型（如`std::array`和`std::vector`）通常基于C风格数组实现。


声明C风格数组  
----------------  

作为核心语言的一部分，C风格数组拥有特殊的声明语法。在C风格数组声明中，使用方括号（`[]`）告知编译器被声明对象是C风格数组。方括号内可选的数组长度（array length）是`std::size_t`类型的整数值，用于指定数组元素数量。


以下定义创建了包含30个`int`元素的C风格数组变量`testScore`：


```cpp
int main()
{
    int testScore[30] {};      // 定义包含30个值初始化int元素的C风格数组（无需包含头文件）

//  std::array<int, 30> arr{}; // 对比：包含30个值初始化int元素的std::array（需包含<array>）

    return 0;
}
```

数组长度必须至少为1。若长度为0、负数或非整数值，编译器将报错。


> **进阶阅读**  
> 堆上动态分配的C风格数组允许长度为0。


数组长度必须为常量表达式  
----------------  

与`std::array`类似，声明C风格数组时，其长度必须是常量表达式（类型为`std::size_t`，通常不影响使用）。


> **提示**  
> 某些编译器可能允许使用非常量表达式长度，以兼容C99的变长数组（VLA）特性。  
> 变长数组不符合C++标准，不应在C++程序中使用。若编译器允许此类数组，可能未禁用编译器扩展（见[0.10 — 配置编译器：编译器扩展](Chapter-0/lesson0.10-configuring-your-compiler-compiler-extensions.md)）。


数组下标访问  
----------------  

与`std::array`类似，C风格数组可使用下标运算符（`operator[]`）访问元素：

```cpp
#include <iostream>

int main()
{
    int arr[5]; // 定义含5个int元素的数组

    arr[1] = 7; // 使用下标运算符访问数组元素1
    std::cout << arr[1]; // 输出7

    return 0;
}
```

不同于标准库容器类（仅接受`std::size_t`类型的无符号索引），C风格数组的下标可以是任何整数类型（有符号或无符号）或非限定枚举值。这意味着C风格数组不受标准库容器的符号转换问题影响！

```cpp
#include <iostream>

int main()
{
    const int arr[] { 9, 8, 7, 6, 5 };

    int s { 2 };
    std::cout << arr[s] << '\n'; // 正确：使用有符号索引

    unsigned int u { 2 };
    std::cout << arr[u] << '\n'; // 正确：使用无符号索引

    return 0;
}   
```

> **提示**  
> C风格数组接受有符号或无符号索引（及非限定枚举）。


`operator[]`不进行边界检查，越界索引将导致未定义行为。


> **旁注**  
> 声明数组（如`int arr[5]`）时，`[]`是声明语法的一部分，而非调用下标运算符。


聚合初始化  
----------------  

与`std::array`类似，C风格数组属于聚合类型（aggregates），可使用聚合初始化（aggregate initialization）进行初始化。


简而言之，聚合初始化允许直接初始化聚合体的成员。为此，我们提供初始化列表（initializer list）——用大括号包裹的逗号分隔值列表。

```cpp
int main()
{
    int fibonnaci[6] = { 0, 1, 1, 2, 3, 5 }; // 使用大括号列表进行拷贝列表初始化
    int prime[5] { 2, 3, 5, 7, 11 };         // 使用大括号列表进行列表初始化（推荐）

    return 0;
}
```

这些初始化形式均从元素0开始按顺序初始化数组成员。


若未提供初始化器，数组元素将被默认初始化（default initialized）。通常这会导致元素未初始化。因此，在定义无初始化器的数组时，应进行值初始化（value initialization）（使用空大括号）。

```cpp
int main()
{
    int arr1[5];    // 成员默认初始化（int元素未初始化）
    int arr2[5] {}; // 成员值初始化（int元素零初始化）（推荐）

    return 0;
}
```

若初始化器数量超过数组长度，编译器报错。若少于数组长度，未提供初始化器的元素将进行值初始化：

```cpp
int main()
{
    int a[4] { 1, 2, 3, 4, 5 }; // 编译错误：初始化器过多
    int b[4] { 1, 2 };          // arr[2]和arr[3]值初始化

    return 0;
}
```

C风格数组的一个缺点是必须显式指定元素类型。由于它们不是类模板，无法使用CTAD（类模板参数推导）。使用`auto`也无法通过初始化列表推导元素类型：

```cpp
int main()
{
    auto squares[5] { 1, 4, 9, 16, 25 }; // 编译错误：C风格数组无法使用类型推导

    return 0;
}
```

省略长度  
----------------  

以下数组定义存在冗余：

```cpp
int main()
{
    const int prime[5] { 2, 3, 5, 7, 11 }; // 显式指定长度为5

    return 0;
}
```

我们显式声明数组长度为5，同时提供了5个初始化器。当使用初始化列表时，可省略长度声明，让编译器根据初始化器数量推导数组长度。

以下定义等价：

```cpp
int main()
{
    const int prime1[5] { 2, 3, 5, 7, 11 }; // 显式指定长度5
    const int prime2[] { 2, 3, 5, 7, 11 };  // 编译器推导长度5

    return 0;
}
```

仅当为所有元素提供显式初始化器时有效：

```cpp
int main()
{
    int bad[] {}; // 错误：编译器推导为零长度数组（非法）！

    return 0;
}
```

当使用初始化列表初始化所有元素时，推荐省略数组长度。这样增删初始化器时，数组长度自动调整，避免长度与初始化器数量不匹配。


> **最佳实践**  
> 显式初始化所有数组元素时，推荐省略C风格数组长度。


const与constexpr数组  
----------------  

与`std::array`类似，C风格数组可为`const`或`constexpr`。const数组必须初始化，且后续不能修改元素值。

```cpp
#include <iostream>

namespace ProgramData
{
    constexpr int squares[5] { 1, 4, 9, 16, 25 }; // constexpr int数组
}

int main()
{
    const int prime[5] { 2, 3, 5, 7, 11 }; // const int数组
    prime[0] = 17; // 编译错误：不能修改const int

    return 0;
}
```

sizeof运算符  
----------------  

在之前的课程中，我们使用`sizeof()`运算符获取对象或类型的字节大小。应用于C风格数组时，`sizeof()`返回整个数组占用的字节数：

```cpp
#include <iostream>

int main()
{
    const int prime[] { 2, 3, 5, 7, 11 }; // 编译器推导长度5
    
    std::cout << sizeof(prime); // 输出20（假设int占4字节）

    return 0;
}
```

假设int占4字节，上述程序输出`20`。数组包含5个int元素，总大小5*4=20字节。


注意此处无额外开销。C风格数组对象仅包含其元素。


获取数组长度  
----------------  

在C++17中，可使用`std::size()`（定义于\<iterator\>头文件），返回无符号整型（`std::size_t`）的数组长度。C++20引入`std::ssize()`，返回有符号整型（可能为`std::ptrdiff_t`）。

```cpp
#include <iostream>
#include <iterator> // 包含std::size和std::ssize

int main()
{
    const int prime[] { 2, 3, 5, 7, 11 };   // 编译器推导长度5

    std::cout << std::size(prime) << '\n';  // C++17，返回无符号整型5
    std::cout << std::ssize(prime) << '\n'; // C++20，返回有符号整型5

    return 0;
}
```

> **提示**  
> `std::size()`和`std::ssize()`的标准头文件是\<iterator\>。但由于其广泛使用，其他头文件（如\<array\>和\<vector\>）也可能包含它们。使用C风格数组时若未包含这些头文件，应包含\<iterator\>。完整列表参见[cppreference文档](https://en.cppreference.com/w/cpp/iterator/size)。


获取数组长度（C++14及更早）  
----------------  

在C++17之前，无标准库函数获取C风格数组长度。若使用C++11或14，可使用以下函数模板：

```cpp
#include <cstddef> // 包含std::size_t
#include <iostream>

template <typename T, std::size_t N>
constexpr std::size_t length(const T(&)[N]) noexcept
{
	return N;
}

int main() {

	int array[]{ 1, 1, 2, 3, 5, 8, 13, 21 };
	std::cout << "数组包含：" << length(array) << "个元素\n";

	return 0;
}
```

该模板通过引用接收C风格数组，返回表示数组长度的非类型模板参数。


旧代码中可能通过总大小除以元素大小计算长度：

```cpp
#include <iostream>

int main()
{
    int array[8] {};
    std::cout << "数组包含：" << sizeof(array) / sizeof(array[0]) << "个元素\n";

    return 0;
}
```

输出：

```
数组包含：8个元素
```

原理：数组总大小等于长度乘以元素大小（`数组大小 = 长度 * 元素大小`），通过代数变换得`长度 = 数组大小 / 元素大小`。通常使用`sizeof(array[0])`或`sizeof(*array)`获取元素大小。


然而，如后续课程所示，此方法在数组退化（array decay）时会失效。C++17的`std::size()`和上述模板函数在这种情况下会引发编译错误，更为安全。


> **相关内容**  
> 数组退化将在下一课[17.8 — C风格数组退化](Chapter-17/lesson17.8-c-style-array-decay.md)中讨论。


不支持赋值  
----------------  

C++数组不支持赋值操作：

```cpp
int main()
{
    int arr[] { 1, 2, 3 }; // 正确：初始化有效
    arr[0] = 4;            // 正确：可修改单个元素
    arr = { 5, 6, 7 };     // 编译错误：数组赋值无效

    return 0;
}
```

技术原因是赋值要求左操作数为可修改左值，而C风格数组不被视为可修改左值。


若需为数组赋予新值列表，最好改用`std::vector`。或逐个元素赋值，或使用`std::copy`复制现有数组：

```cpp
#include <algorithm> // 包含std::copy

int main()
{
    int arr[] { 1, 2, 3 };
    int src[] { 5, 6, 7 };

    // 将src复制到arr
    std::copy(std::begin(src), std::end(src), std::begin(arr));

    return 0;
}
```

测验时间  
----------------  

**问题1**  
将以下`std::array`定义转换为等效的constexpr C风格数组定义：

```cpp
constexpr std::array<int, 3> a{}; // 分配3个int
```

  
<details><summary>答案</summary>constexpr int a[3] {}; // 分配3个int</details>  

**问题2**  
以下程序存在哪三个错误？

```cpp
#include <iostream>

int main()
{
    int length{ 5 };
    const int arr[length] { 9, 7, 5, 3, 1 };
    
    std::cout << arr[length];
    arr[0] = 4;
    
    return 0;
}
```

  
<details><summary>答案</summary>  
1. 数组长度必须为编译时常量，此处`length`非常量  
2. `arr[length]`越界访问导致未定义行为  
3. `const int`数组元素不可修改  
</details>  

**问题3**  
"完美平方"指平方根为整数的自然数。使用全局constexpr C风格数组存储0-9（含）的完美平方。循环要求用户输入单数字整数或-1退出，判断输入是否为完美平方。


  
<details><summary>答案</summary>  
```cpp
#include <iostream>

namespace ProgramData
{
    constexpr int squares[] { 0, 1, 4, 9 };
}

bool matchSquare(int input)
{
    for (const auto& e : ProgramData::squares)
    {
        if (input == e)
            return true;
    }

    return false;
}

int main()
{
    while (true)
    {
        std::cout << "输入单数字整数或-1退出: ";
        int input{};
        std::cin >> input;

        if (input == -1)
            break;

        if (matchSquare(input))
            std::cout << input << "是完美平方\n";
        else
            std::cout << input << "不是完美平方\n";
    }

    std::cout << "再见\n";
    return 0;
}
```
</details>  


[下一课 17.8 C风格数组退化](Chapter-17/lesson17.8-c-style-array-decay.md)  
[返回主页](/)  
[上一课 17.6 std::array与枚举](Chapter-17/lesson17.6-stdarray-and-enumerations.md)