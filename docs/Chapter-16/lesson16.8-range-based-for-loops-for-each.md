16.8 — 范围for循环（for-each）
==========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月28日（首次发布于2015年7月31日）

在课程[16.6 — 数组与循环](Chapter-16/lesson16.6-arrays-and-loops.md)中，我们展示了使用普通for循环通过索引变量遍历数组元素的示例。以下是另一个类似案例：

```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector fibonacci { 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };

    std::size_t length { fibonacci.size() };
    for (std::size_t index { 0 }; index < length; ++index)
       std::cout << fibonacci[index] << ' ';

    std::cout << '\n';

    return 0;
}
```

虽然普通for循环提供了遍历数组的便捷方式，但容易引发越界错误和符号问题（详见课程[16.7 — 数组、循环与符号挑战解决方案](Chapter-16/lesson16.7-arrays-loops-and-sign-challenge-solutions.md)）。

由于正向遍历数组是常见操作，C++支持另一种称为**范围for循环（range-based for loop）**（亦称**for-each循环**）的遍历方式，无需显式索引即可遍历容器。范围for循环更简洁、安全，且兼容所有C++标准数组类型（包括`std::vector`、`std::array`和C风格数组）。

范围for循环
----------------

范围for语句的语法结构如下：

```cpp
for (元素声明 : 数组对象)
   语句;
```

当遇到范围for循环时，循环将遍历`数组对象`中的每个元素。每次迭代时，当前数组元素的值将被赋给`元素声明`中声明的变量，然后执行`语句`。

> **最佳实践**  
> `元素声明`应与数组元素类型一致，否则会发生类型转换。

以下示例使用范围for循环打印`fibonacci`数组的所有元素：

```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector fibonacci { 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };

    for (int num : fibonacci) // 遍历fibonacci数组并将每个值复制到`num`
       std::cout << num << ' '; // 打印当前num的值

    std::cout << '\n';

    return 0;
}
```

输出结果：

```
0 1 1 2 3 5 8 13 21 34 55 89
```

注意此示例无需使用数组长度或索引！

关键洞察
----------------
声明元素（上例中的`num`）并非数组索引，而是被赋值为当前迭代的数组元素值。由于`num`接收的是数组元素的副本，当元素类型较大时可能产生复制开销。

最佳实践
----------------
遍历容器时优先选择范围for循环而非普通for循环。

范围for循环与空容器
----------------
当遍历空容器时，范围for循环体不会执行：

```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector empty { };

    for (int num : empty)
       std::cout << "Hi mom!\n";

    return 0;
}
```

上述示例无输出。

范围for循环与auto类型推导
----------------
使用`auto`关键字让编译器推导元素类型可避免冗余类型指定和拼写错误：

```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector fibonacci { 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };

    for (auto num : fibonacci) // num被推导为int类型
       std::cout << num << ' ';

    std::cout << '\n';

    return 0;
}
```

若数组元素类型更新（如从`int`改为`long`），`auto`会自动推导新类型，保持同步。

使用引用避免元素复制
----------------
遍历`std::string`数组时，通过const引用可避免昂贵的复制操作：

```cpp
#include <iostream>
#include <string>
#include <vector>

int main()
{
    std::vector<std::string> words{ "peter", "likes", "frozen", "yogurt" };

    for (const auto& word : words) // word现在是const引用
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
```

非const引用还可用于修改数组元素。

auto、auto&与const auto&的选择
----------------
通常：
- `auto`：用于易复制类型
- `auto&`：需修改元素时
- `const auto&`：高开销复制类型

但为保持未来兼容性，建议优先使用`const auto&`。

最佳实践
----------------
范围for循环中元素类型应声明为：
- `auto`：需要修改副本时
- `auto&`：需要修改原元素时
- `const auto&`：仅需读取原元素时

范围for循环与其他标准容器
----------------
范围for循环兼容多种数组类型，包括（非衰减）C风格数组、`std::array`、链表、树和映射：

```cpp
#include <array>
#include <iostream>

int main()
{
    std::array fibonacci{ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };

    for (auto number : fibonacci)
    {
        std::cout << number << ' ';
    }

    std::cout << '\n';

    return 0;
}
```

高级说明
----------------
- 范围for循环不兼容衰减的C风格数组（需要数组长度信息）
- 不兼容枚举类型（解决方法见课程[17.6 — std::array与枚举](Chapter-17/lesson17.6-stdarray-and-enumerations.md)）

获取当前元素索引
----------------
范围for循环不直接提供元素索引。若需要索引，可声明计数器变量，但此时建议改用普通for循环。

C++20反向范围for循环
----------------
使用`std::views::reverse`可创建反向视图：

```cpp
#include <iostream>
#include <ranges>
#include <string_view>
#include <vector>

int main()
{
    std::vector<std::string_view> words{ "Alex", "Bobby", "Chad", "Dave" };

    for (const auto& word : std::views::reverse(words)) // 创建反向视图
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
```

输出：

```
Dave Chad Bobby Alex
```

测验
----------------

**问题1**  
定义包含"Alex", "Betty", "Caroline", "Dave", "Emily", "Fred", "Greg", "Holly"的`std::vector`，要求用户输入姓名并使用范围for循环检查是否存在。

示例代码：

```cpp
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

int main()
{
    std::vector<std::string_view> names{ "Alex", "Betty", "Caroline", "Dave",
        "Emily", "Fred", "Greg", "Holly" };
    
    std::cout << "Enter a name: ";
    std::string username{};
    std::cin >> username;

    bool found{ false };

    for (std::string_view name : names)
    {
        if (name == username)
        {
            found = true;
            break;
        }
    }

    if (found)
        std::cout << username << " was found.\n";
    else
        std::cout << username << " was not found.\n";

    return 0;
}
```

**问题2**  
创建模板函数`isValueInArray()`，接受`std::vector`和值作为参数，返回布尔值表示是否存在。

示例代码：

```cpp
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

template <typename T>
bool isValueInArray(const std::vector<T>& arr, const T& value )
{
    for (const auto& a : arr)
    {
        if (a == value)
            return true;
    }
    return false;
}

int main()
{
    std::vector<std::string_view> names{ "Alex", "Betty", "Caroline", "Dave",
        "Emily", "Fred", "Greg", "Holly" };
    
    std::cout << "Enter a name: ";
    std::string username{};
    std::cin >> username;

    bool found{ isValueInArray<std::string_view>(names, username) };

    if (found)
        std::cout << username << " was found.\n";
    else
        std::cout << username << " was not found.\n";

    return 0;
}
```

[下一课 16.9 — 使用枚举实现数组索引与长度](Chapter-16/lesson16.9-array-indexing-and-length-using-enumerators.md)
[返回主页](/)  
[上一课 16.7 — 数组、循环与符号挑战解决方案](Chapter-16/lesson16.7-arrays-loops-and-sign-challenge-solutions.md)