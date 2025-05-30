2.3 — void函数（非值返回函数）
======================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2022年4月15日 PDT下午5:19（首次发布于2023年10月23日）

在前序课程（[2.1 — 函数简介](Chapter-2/lesson2.1-introduction-to-functions.md)）中，我们展示了函数定义的基本语法：

```cpp
returnType identifier() // identifier替换为函数名
{
// 代码内容
}
```

虽然我们演示过返回类型为`void`的函数示例，但未深入讨论其含义。本节将详细探讨返回类型为`void`的函数。

void返回值
----------------

函数并非必须向调用者返回值。使用**void**返回类型即表示函数不返回任何值。例如：

```cpp
#include <iostream>

// void表示该函数不向调用者返回值
void printHi()
{
    std::cout << "Hi" << '\n';
    // 此函数无需返回值，故不需要return语句
}

int main()
{
    printHi(); // 正确：调用printHi()函数，不接收返回值
    return 0;
}
```

上述示例中，`printHi`函数具有实际功能（输出"Hi"），但无需向调用者返回数据，因此声明为`void`返回类型。

当`main`调用`printHi`时，执行函数体内的代码并打印"Hi"。`printHi`执行完毕后，控制权返回`main`继续执行。

不返回值的函数称为**非值返回函数（non-value returning function）**（亦称**void函数**）。

void函数无需return语句
----------------

void函数会在执行完毕后自动返回调用者，无需显式return语句。

虽然可以在void函数中使用空return语句（不带返回值），但这与函数自然结束的效果相同。因此在void函数末尾添加空return语句是冗余的：

```cpp
#include <iostream>

void printHi()
{
    std::cout << "Hi" << '\n';
    return; // 冗余：函数本将在此处自动返回
}

int main()
{
    printHi();
    return 0;
}
```

最佳实践
----------------

不要在非值返回函数末尾添加return语句。

void函数不能用于需要值的表达式
----------------

某些表达式需要提供具体值。例如：

```cpp
#include <iostream>

int main()
{
    std::cout << 5; // 正确：5是待打印的字面值
    std::cout << ;  // 编译错误：未提供值
    return 0;
}
```

上述程序中，`std::cout <<`运算符右侧必须提供有效值。考虑以下示例：

```cpp
#include <iostream>

void printHi()
{
    std::cout << "Hi" << '\n';
}

int main()
{
    printHi();         // 正确：无需返回值
    std::cout << printHi(); // 编译错误
    return 0;
}
```

第一次调用`printHi()`不涉及返回值处理，故合法。第二次尝试将`printHi`的返回值传给`std::cout`时，由于`printHi`返回void，编译器将报错。

关键提示
----------------

* 独立函数调用语句：只需函数行为，不关心返回值。可调用void函数或忽略值返回函数的返回值
* 需要值的上下文（如`std::cout`）：必须调用值返回函数

```cpp
#include <iostream>

void returnNothing() {}
int returnFive() { return 5; }

int main()
{
    returnNothing();          // 合法
    returnFive();             // 合法（忽略返回值）
    std::cout << returnFive();    // 合法
    std::cout << returnNothing(); // 编译错误
    return 0;
}
```

void函数返回值将导致编译错误
----------------

尝试从void函数返回值将引发错误：

```cpp
void printHi()
{
    std::cout << "In printHi()" << '\n';
    return 5; // 编译错误：试图返回值
}
```

测验时间
----------------

问题1  
分析下列程序，指出其输出或是否编译失败。

1a)

```cpp
#include <iostream>

void printA() { std::cout << "A\n"; }
void printB() { std::cout << "B\n"; }

int main()
{
    printA();
    printB();
    return 0;
}
```

  
<details><summary>答案</summary>程序分两行输出A和B。</details>

1b)

```cpp
#include <iostream>

void printA() { std::cout << "A\n"; }

int main()
{
    std::cout << printA() << '\n';
    return 0;
}
```

  
<details><summary>答案</summary>编译失败。printA()返回void，无法用于std::cout输出。</details>

[下一课 2.4 — 函数形参与实参简介](Chapter-2/lesson2.4-introduction-to-function-parameters-and-arguments.md)  
[返回主页](/)  
[上一课 2.2 — 函数返回值（值返回函数）](Chapter-2/lesson2.2-function-return-values-value-returning-functions.md)