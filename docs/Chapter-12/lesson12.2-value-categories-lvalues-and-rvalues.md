12.2 — 值类别（左值与右值）  
==============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月3日（首次发布于2022年1月18日）  

在讨论首个复合类型（左值引用）之前，我们需要先了解**左值（lvalue）**的概念。  

在课程[1.10 — 表达式简介](Chapter-1/lesson1.10-introduction-to-expressions.md)中，我们将表达式定义为"由字面量、变量、运算符和函数调用组成的可执行单元，能够生成单一值"。例如：  
```
#include <iostream>

int main()
{
    std::cout << 2 + 3 << '\n'; // 表达式2 + 3生成值5
    return 0;
}
```  
上述程序中，表达式`2 + 3`被求值为5并输出到控制台。  

在课程[6.4 — 自增/自减运算符与副作用](Chapter-6/lesson6.4-increment-decrement-operators-and-side-effects.md)中，我们还提到表达式可能产生持久化的副作用：  
```
#include <iostream>

int main()
{
    int x {5};
    ++x; // 此表达式语句具有递增x的副作用
    std::cout << x << '\n'; // 输出6
    return 0;
}
```  
上述程序中，表达式`++x`改变了x的值，即使表达式求值结束后该变化依然存在。  

除了生成值和副作用，表达式还能做第三件事：求值为对象或函数。我们将在后续内容中深入探讨这一点。  

表达式的属性  
----------------  

为了确定表达式的求值方式和使用场景，所有C++表达式都具有两个属性：类型（type）和值类别（value category）。  

### 表达式的类型  

表达式的类型等于其求值结果的类型（值、对象或函数的类型）。例如：  
```
int main()
{
    auto v1 {12 / 4}; // int / int => int
    auto v2 {12.0 / 4}; // double / int => double
    return 0;
}
```  
对于`v1`，编译器（在编译期）确定两个`int`操作数的除法将生成`int`结果，因此该表达式的类型为`int`。通过类型推断，`int`将作为`v1`的类型。  

对于`v2`，编译器确定`double`与`int`的除法将生成`double`结果。注意算术运算符要求操作数类型匹配，因此`int`操作数被转换为`double`后执行浮点除法。该表达式的类型为`double`。  

编译器可通过表达式类型判断其在给定上下文中是否有效。例如：  
```
#include <iostream>

void print(int x)
{
    std::cout << x << '\n';
}

int main()
{
    print("foo"); // 错误：print()期望int参数，但传入字符串字面量
    return 0;
}
```  
上述程序中，`print(int)`函数期望`int`参数，但传入的表达式（字符串字面量`"foo"`）类型不匹配且无可用转换，导致编译错误。  

注意表达式类型必须在编译期确定（否则类型检查和类型推导将失效）——但表达式的值可能在编译期（若为常量表达式）或运行期（非常量表达式）确定。  

### 表达式的值类别  

考虑以下程序：  
```
int main()
{
    int x{};

    x = 5; // 有效：可将5赋值给x
    5 = x; // 错误：不能将x的值赋给字面量5
    return 0;
}
```  
为何第一个赋值有效而第二个无效？答案在于表达式的第二个属性：**值类别（value category）**。值类别表明表达式求值结果是值、函数还是某种对象。  

C++11前只有两种值类别：**左值（lvalue）**和**右值（rvalue）**。C++11新增三个值类别（glvalue、prvalue和xvalue）以支持移动语义（move semantics）。  

> **作者提示**  
> 本节沿用C++11前的值类别划分以便入门，后续章节将介绍移动语义及相关值类别。  

左值与右值表达式  
----------------  

**左值（lvalue）**（全称"left value"或"locator value"）是求值为可识别对象或函数（或位域）的表达式。"可识别"指实体（如对象或函数）可通过地址与其他实体区分。具有标识的实体可通过标识符、引用或指针访问，通常生存期超过单个表达式。  
```
int main()
{
    int x{5};
    int y{x}; // x是左值表达式
    return 0;
}
```  
上述程序中，表达式`x`是左值表达式（求值为变量x）。  

自常量引入后，左值分为两个子类：  
* **可修改左值（modifiable lvalue）**：值可修改的左值  
* **不可修改左值（non-modifiable lvalue）**：值不可修改的左值（如const或constexpr）  
```
int main()
{
    int x{};
    const double d{};

    int y{x}; // x是可修改左值
    const double e{d}; // d是不可修改左值
    return 0;
}
```  

**右值（rvalue）**（全称"right value"）是除左值外的所有表达式。右值求值为值，常见形式包括字面量（C风格字符串字面量除外）和按值返回的函数/运算符返回值。右值不可识别，必须在当前表达式内立即使用。  
```
int return5() { return 5; }

int main()
{
    int x{5}; // 5是右值
    const double d{1.2}; // 1.2是右值

    int z{return5()}; // return5()是右值
    int w{x + 1}; // x+1是右值
    int q{static_cast<int>(d)}; // 转换结果是右值
    return 0;
}
```  
`return5()`、`x+1`和`static_cast<int>(d)`产生临时值，属于右值。  

> **关键洞察**  
> 左值表达式求值为可识别对象  
> 右值表达式求值为值  

值类别与运算符  
----------------  

运算符通常期望操作数为右值。例如二元`operator+`：  
```
#include <iostream>

int main()
{
    std::cout << 1 + 2; // 1和2是右值，operator+返回右值
    return 0;
}
```  
字面量`1`和`2`均为右值，`operator+`返回右值`3`。  

现在可以解答为何`x = 5`有效而`5 = x`无效：赋值运算符左操作数必须为可修改左值。后者失败因为`5`是右值。  
```
int main()
{
    int x{};

    x = 5; // 有效：x是可修改左值，5是右值
    5 = x; // 错误：5是右值
    return 0;
}
```  

### 左值到右值转换  

当需要右值但提供左值时，左值会隐式转换为右值：  
```
int main()
{
    int x{1};
    int y{2};

    x = y; // y是左值但合法（隐式转换）
    return 0;
}
```  
此处左值`y`转换为右值`2`后赋值给`x`。  

> **关键洞察**  
> 左值可隐式转换为右值，因此左值可用于需要右值的场景  
> 右值不可隐式转换为左值  

考虑以下示例：  
```
int main()
{
    int x{2};
    x = x + 1; // x在不同上下文分别作为左值和右值
    return 0;
}
```  
赋值左侧的`x`是左值（求值为变量x），右侧的`x`经过左值到右值转换后参与运算。`operator+`返回右值`3`作为赋值右操作数。  

如何区分左值与右值  
----------------  

判断表达式是左值还是右值的经验法则：  
* **左值**：求值为函数或可识别对象（包括变量），生存期超过当前表达式  
* **右值**：求值为值（包括字面量和临时对象），生存期不超过当前表达式  

完整列表可参考[技术文档](https://en.cppreference.com/w/cpp/language/value_category)。C++11中右值分为prvalue和xvalue两个子类。  

可通过编译器判断表达式类别：  
```
#include <iostream>
#include <string>

template <typename T>
constexpr bool is_lvalue(T&) { return true; }

template <typename T>
constexpr bool is_lvalue(T&&) { return false; }

#define PRINTVCAT(expr) std::cout << #expr << "是" << (is_lvalue(expr) ? "左值\n" : "右值\n")

int getint() { return 5; }

int main()
{
    PRINTVCAT(5);                // 右值
    PRINTVCAT(getint());         // 右值
    int x{5};
    PRINTVCAT(x);                // 左值
    PRINTVCAT(std::string{"Hello"}); // 右值
    PRINTVCAT("Hello");          // 左值（C风格字符串）
    PRINTVCAT(++x);              // 左值（前缀递增）
    PRINTVCAT(x++);              // 右值（后缀递增）
}
```  
输出：  
```
5是右值
getint()是右值
x是左值
std::string {"Hello"}是右值
"Hello"是左值
++x是左值
x++是右值
```  
该方法通过重载函数判断：左值引用版本处理左值，右值引用版本处理右值。  

> **进阶阅读**  
> C风格字符串字面量是左值（因数组退化为指针需地址）。详见课程[17.8 — C风格数组退化](Chapter-17/lesson17.8-c-style-array-decay.md)。  

现在我们可以进入首个复合类型：**左值引用（lvalue reference）**。  

[下一课 12.3 左值引用](Chapter-12/lesson12.3-lvalue-references.md)  
[返回主页](/)  
[上一课 12.1 复合数据类型简介](Chapter-12/lesson12.1-introduction-to-compound-data-types.md)