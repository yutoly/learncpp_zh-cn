12.15 — std::optional  
======================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月8日（首次发布于2024年3月19日）  

在课程[9.4 — 错误检测与处理](Chapter-9/lesson9.4-detecting-and-handling-errors.md)中，我们讨论了函数遇到无法自行处理的错误时的情形。例如考虑以下计算并返回值的函数：  

```cpp
int doIntDivision(int x, int y)
{
    return x / y;
}
```  

当调用者传入语义无效的值（如`y`=0）时，该函数无法计算返回值（因为除以0在数学上未定义）。此时该如何处理？由于计算结果函数不应有副作用，它无法自行合理解决该错误。此类情况下，通常做法是让函数检测错误，然后将错误传回调用者处理。  

之前课程介绍了两种向调用者返回错误的方式：  
* 将void返回类型改为bool（表示成功或失败）  
* 让值返回函数返回哨兵值（sentinel value，即函数正常返回值范围外的特殊值）  

后者的示例如下，`reciprocal()`函数在用户传入无效参数时返回0.0（该值不会自然产生）：  

```cpp
#include <iostream>

// 倒数函数，x=0时返回0.0作为错误标志
double reciprocal(double x)
{
    if (x == 0.0)
       return 0.0;

    return 1.0 / x;
}

void testReciprocal(double d)
{
     double result { reciprocal(d) };
     std::cout << "The reciprocal of " << d << " is ";
     if (result != 0.0)
         std::cout << result << '\n';
     else
         std::cout << "undefined\n";
}

int main()
{
    testReciprocal(5.0);
    testReciprocal(-4.0);
    testReciprocal(0.0);
    return 0;
}
```  

此方案虽可行，但存在潜在缺陷：  
* 程序员需了解各函数使用的哨兵值（不同函数可能不同）  
* 相同函数的不同版本可能使用不同哨兵值  
* 不适用于所有哨兵值均为有效返回值的情况  

以`doIntDivision()`为例，当`y`=0时无法返回有效值。我们可尝试使用极端值作为哨兵：  

```cpp
#include <limits>

// 失败时返回std::numeric_limits<int>::lowest()
int doIntDivision(int x, int y)
{
    if (y == 0)
        return std::numeric_limits<int>::lowest();
    return x / y;
}
```  

`std::numeric_limits<T>::lowest()`返回类型`T`的最小负值。但此方法存在两个缺点：  
1. 每次调用都需检查返回值是否为该极端值  
2. 存在半谓词问题（semipredicate problem）：当用户传入`std::numeric_limits<int>::lowest()`作为`x`时，返回值将无法区分成功与失败  

第三种方案是返回两个值：bool表示是否成功，实际返回值或无效值。C++17之前的版本需自行实现此逻辑，但各方案易导致不一致性错误。  

返回std::optional  
----------------  

C++17引入`std::optional`类模板，用于实现可选值。`std::optional<T>`可持有`T`类型值或无值：  

```cpp
#include <iostream>
#include <optional>

std::optional<int> doIntDivision(int x, int y)
{
    if (y == 0)
        return {}; // 或 return std::nullopt
    return x / y;
}

int main()
{
    std::optional<int> result1 { doIntDivision(20, 5) };
    if (result1)
        std::cout << "Result 1: " << *result1 << '\n';

    std::optional<int> result2 { doIntDivision(5, 0) };
    if (result2)
        std::cout << "Result 2: " << *result2 << '\n';
    else
        std::cout << "Result 2: failed\n";
    return 0;
}
```  

输出：  
```
Result 1: 4
Result 2: failed
```  

使用`std::optional`时：  
* 构造含值：`std::optional<int> o1{5};`  
* 构造无值：`std::optional<int> o2{};`或`std::optional<int> o3{std::nullopt};`  
* 检查有值：`o1.has_value()`或隐式转换为bool`if(o2)`  
* 获取值：  
  - 解引用`*o1`（无值时未定义行为）  
  - `o2.value()`（无值时抛出异常）  
  - `o3.value_or(42)`（无值时返回默认值）  

与指针的对比：  

| 行为             | 指针              | std::optional       |
|------------------|-------------------|---------------------|
| 无值初始化       | {}或nullptr       | {}或std::nullopt    |
| 有值初始化       | 地址              | 值                  |
| 检查有值         | 隐式转bool        | 隐式转bool/has_value() |
| 取值             | 解引用            | 解引用/value()      |

`std::optional`具有值语义（value semantics），赋值时复制整个对象。这使得可以安全返回局部对象的值。  

优缺点  
----------------  
优点：  
- 明确文档化函数可能返回无值  
- 无需记忆哨兵值  
- 语法直观  

缺点：  
- 必须在使用前检查是否有值  
- 无法提供失败原因信息  

最佳实践  
----------------  
优先使用`std::optional`代替哨兵值，除非需要返回额外错误信息。C++23引入的`std::expected`可处理带错误码的情况。  

作为可选函数参数  
----------------  
传统使用指针实现可选参数：  

```cpp
void printIDNumber(const int *id=nullptr)
{
    if (id)
        std::cout << "ID: " << *id << '\n';
    else
        std::cout << "ID unknown\n";
}
```  

使用`std::optional`的版本：  

```cpp
#include <optional>

void printIDNumber(std::optional<const int> id = std::nullopt)
{
    if (id)
        std::cout << "ID: " << *id << '\n';
    else
        std::cout << "ID unknown\n";
}
```  

优点：  
1. 明确参数可选性  
2. 可接受右值参数  

但`std::optional`会复制参数，对于昂贵复制类型（如`std::string`）不适用。此时建议：  
- 若`T`通常传值，使用`std::optional<T>`  
- 否则使用`const T*`  

高级技巧：使用`std::reference_wrapper`模拟引用参数，但可能增加复杂性。多数情况下，函数重载更优：  

```cpp
void printEmployeeID(); // 无参版本
void printEmployeeID(const Employee& e); // 有参版本
```  

最佳实践  
----------------  
优先将`std::optional`用于可选返回类型。  
优先使用函数重载实现可选参数。若不可行，当`T`通常传值时使用`std::optional<T>`，昂贵复制类型使用`const T*`。  

[下一课 12.x — 第12章总结与测验](Chapter-12/lesson12.x-chapter-12-summary-and-quiz.md)  
[返回主页](/)  
[上一课 12.14 — 指针、引用与const的类型推导](Chapter-12/lesson12.14-type-deduction-with-pointers-references-and-const.md)