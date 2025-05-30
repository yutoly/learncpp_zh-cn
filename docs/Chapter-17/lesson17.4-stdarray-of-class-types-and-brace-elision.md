17.4 — 类类型的std::array与花括号省略
====================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日 PDT下午3:48（首次发布于2024年9月29日）

`std::array`不仅限于基础类型元素。实际上，`std::array`的元素可以是任何对象类型，包括复合类型。这意味着你可以创建指针的`std::array`，或结构体（或类）的`std::array`。

不过，初始化结构体或类的`std::array`容易让新程序员困惑，因此我们将用完整课程专门讲解这个主题。

> **作者提示**  
> 本课使用结构体进行演示，但内容同样适用于类。

定义并赋值结构体的std::array
----------------

从简单结构体开始：

```cpp
struct House
{
    int number{};
    int stories{};
    int roomsPerStory{};
};
```

定义`House`的`std::array`并进行元素赋值操作符合直觉：

```cpp
#include <array>
#include <iostream>

struct House
{
    // 同上
};

int main()
{
    std::array<House, 3> houses{};

    houses[0] = { 13, 1, 7 };
    houses[1] = { 14, 2, 5 };
    houses[2] = { 15, 2, 4 };

    for (const auto& house : houses)
    {
        std::cout << "House number " << house.number
                  << " has " << (house.stories * house.roomsPerStory)
                  << " rooms.\n";
    }
    return 0;
}
```

输出结果：

```
House number 13 has 7 rooms.
House number 14 has 10 rooms.
House number 15 has 8 rooms.
```

初始化结构体的std::array
----------------

只要显式指定元素类型，结构体数组的初始化也符合预期：

```cpp
constexpr std::array houses { // 使用CTAD推导模板参数<House, 3>
        House{ 13, 1, 7 },
        House{ 14, 2, 5 },
        House{ 15, 2, 4 }
    };
```

不显式指定元素类型的初始化
----------------

在赋值操作中编译器能自动推导类型：

```cpp
houses[0] = { 13, 1, 7 }; // 无需显式指定House
```

但以下初始化方式会失败：

```cpp
constexpr std::array<House, 3> houses { 
        { 13, 1, 7 }, // 错误
        { 14, 2, 5 },
        { 15, 2, 4 } 
    };
```

原因在于`std::array`内部实现结构：

```cpp
template<typename T, std::size_t N>
struct array
{
    T implementation_defined_name[N]; // 包含C风格数组
};
```

正确初始化方式需要额外花括号：

```cpp
constexpr std::array<House, 3> houses {{ // 外层花括号初始化内部C数组
        { 13, 4, 30 }, // 元素0
        { 14, 3, 10 }, // 元素1
        { 15, 3, 40 }, // 元素2
     }};
```

> **关键洞察**  
> 当元素类型需要值列表且未显式指定类型时，初始化`std::array`需要额外花括号。这是聚合初始化（aggregate initialization）的特性。

聚合类型的花括号省略
----------------

对于基础类型数组，支持花括号省略：

```cpp
constexpr std::array<int, 5> arr { 1, 2, 3, 4, 5 }; // 单层花括号
```

等效于：

```cpp
constexpr std::array<int, 5> arr {{ 1, 2, 3, 4, 5 }}; // 双层花括号
```

另一个示例
----------------

使用`Student`结构体初始化`std::array`：

```cpp
struct Student
{
    int id{};
    std::string_view name{};
};

constexpr std::array students{ 
    Student{0, "Alex"}, 
    Student{1, "Joe"}, 
    Student{2, "Bob"} 
};
```

测验时间
----------------

**问题1**  
定义包含`std::string_view name`和`int gold`成员的`Item`结构体，使用CTAD初始化4元素数组。

  
<details><summary>答案</summary>

```cpp
constexpr std::array store {
    Item{ "sword", 5 },
    Item{ "dagger", 3 },
    Item{ "club", 2 },
    Item{ "spear", 7 }
};
```
</details>

**问题2**  
更新问题1解决方案，不使用显式类型指定。

  
<details><summary>答案</summary>

```cpp
constexpr std::array<Item, 4> store {{ 
    { "sword", 5 },
    { "dagger", 3 },
    { "club", 2 },
    { "spear", 7 }
}};
```
</details>

[下一课 17.5 通过std::reference_wrapper实现引用数组](Chapter-17/lesson17.5-arrays-of-references-via-stdreference_wrapper.md)  
[返回主页](/)  
[上一课 17.3 std::array的传递与返回](Chapter-17/lesson17.3-passing-and-returning-stdarray.md)