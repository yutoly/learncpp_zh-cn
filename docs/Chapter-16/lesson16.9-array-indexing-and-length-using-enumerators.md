16.9 — 使用枚举项进行数组索引与长度管理  
===================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年5月8日（首次发布于2023年9月11日）  

数组文档化面临的主要问题在于：整型索引无法向开发者传达索引的语义信息。  

考虑存储5个考试分数的数组：  

```cpp
#include <vector>

int main()
{
    std::vector testScores { 78, 94, 66, 77, 14 };

    testScores[2] = 76; // 这个索引代表哪位学生？
}
```  

`testScores[2]`对应的学生身份并不明确。  

**使用非限定作用域枚举（unscoped enumeration）进行索引**  
在课程[16.3 — std::vector的无符号长度与下标问题](Chapter-16/lesson16.3-stdvector-and-the-unsigned-length-and-subscript-problem.md)中，我们详细讨论了`std::vector<T>::operator[]`的索引类型`size_type`（通常为`std::size_t`的别名）。因此，索引需为`std::size_t`类型或其可转换类型。  

由于非限定作用域枚举可隐式转换为`std::size_t`，我们可以使用它们作为数组索引来增强代码可读性：  

```cpp
#include <vector>

namespace Students
{
    enum Names
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        max_students // 5
    };
}

int main()
{
    std::vector testScores { 78, 94, 66, 77, 14 };
    testScores[Students::stan] = 76; // 明确更新stan的成绩
    return 0;
}
```  

这种方式显著提升了数组元素的语义清晰度。  

由于枚举项（enumerator）隐含`constexpr`属性，其转换为无符号整型不会引发窄化转换，从而避免了有符号/无符号索引问题。  

**使用非constexpr的非限定作用域枚举进行索引**  
非限定作用域枚举的底层类型由实现定义（可能为有符号或无符号整型）。若使用枚举类型的非`constexpr`变量进行索引，在底层类型为有符号的平台可能触发符号转换警告：  

```cpp
#include <vector>

namespace Students
{
    enum Names
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        max_students // 5
    };
}

int main()
{
    std::vector testScores { 78, 94, 66, 77, 14 };
    Students::Names name { Students::stan }; // 非constexpr
    testScores[name] = 76; // 若底层类型为有符号可能触发警告
    return 0;
}
```  

解决方案之一是显式指定枚举的底层类型为无符号整型：  

```cpp
namespace Students
{
    enum Names : unsigned int // 显式指定底层类型
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        max_students // 5
    };
}
```  

**使用计数枚举项（count enumerator）**  
在枚举列表末尾添加名为`max_students`的额外枚举项。若之前所有枚举项使用默认值（推荐做法），该枚举项的值将等于之前枚举项的数量。我们称其为**计数枚举项**，其值代表之前定义的枚举项总数。  

此计数枚举项可用于需要统计数量的场景：  

```cpp
std::vector<int> testScores(Students::max_students); // 创建5元素的vector
std::cout << "班级人数：" << Students::max_students; // 输出学生总数
```  

当新增枚举项时，`max_students`会自动更新：  

```cpp
enum Names
{
    kenny, kyle, stan, butters, cartman,
    wendy, // 新增枚举项（值5）
    max_students // 值自动变为6
};
```  

**使用计数枚举项断言数组长度**  
当使用初始化列表创建数组时，建议断言数组长度是否匹配计数枚举项。这有助于发现枚举项增减与初始化值数量不匹配的问题：  

```cpp
#include <cassert>

std::vector testScores { 78, 94, 66, 77, 14 };
assert(std::size(testScores) == max_students); // 验证数组长度
```  

> **最佳实践**  
> * 对constexpr数组使用`static_assert`验证长度  
> * 对非constexpr数组使用`assert`验证长度  

**数组与枚举类（enum class）**  
枚举类（enum class）不会污染命名空间，但缺乏到整型的隐式转换。解决方案包括显式转换或重载一元`operator+`：  

```cpp
// 方法1：显式转换
testScores[static_cast<int>(StudentNames::stan)] = 76;

// 方法2：重载运算符+
constexpr auto operator+(StudentNames a) noexcept {
    return static_cast<std::underlying_type_t<StudentNames>>(a);
}
testScores[+StudentNames::stan] = 76; // 使用一元+运算符
```  

**测验**  
创建包含动物名称的枚举，使用数组存储各动物腿数，并验证初始化器数量：  

```cpp
#include <cassert>
#include <iostream>
#include <vector>

namespace Animals
{
    enum Animals { chicken, dog, cat, elephant, duck, snake, max_animals };
    const std::vector legs{ 2, 4, 4, 4, 2, 0 }; // 各动物腿数
}

int main()
{
    assert(std::size(Animals::legs) == Animals::max_animals);
    std::cout << "大象有" << Animals::legs[Animals::elephant] << "条腿\n";
    return 0;
}
```  

[下一课 16.10 — std::vector的调整大小与容量](Chapter-16/lesson16.10-stdvector-resizing-and-capacity.md)  
[返回主页](/)  
[上一课 16.8 — 基于范围的for循环（for-each）](Chapter-16/lesson16.8-range-based-for-loops-for-each.md)