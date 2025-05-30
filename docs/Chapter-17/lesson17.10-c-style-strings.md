17.10 — C风格字符串（C-style strings）  
=========================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年5月25日（首次发布于2007年7月9日）  

在课程[17.7 — C风格数组简介](Chapter-17/lesson17.7-introduction-to-c-style-arrays.md)中，我们介绍了C风格数组，它允许定义元素的顺序集合：  
```cpp
int testScore[30] {}; // 包含30个int的数组，索引0到29
```  

在课程[5.2 — 字面量](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)中，我们将字符串（string）定义为顺序字符的集合（如"Hello, world!"），并引入了C风格字符串字面量。我们还指出C风格字符串字面量"Hello, world!"的类型是`const char[14]`（13个显式字符加1个隐藏的空终止符）。  

现在应该显而易见的是，C风格字符串（C-style strings）其实就是元素类型为`char`或`const char`的C风格数组！  

尽管C风格字符串字面量在代码中可以使用，但C风格字符串对象在现代C++中已不再受青睐，因为它们难以使用且存在安全隐患（现代替代方案是`std::string`和`std::string_view`）。不过您仍可能在旧代码中遇到C风格字符串对象的使用，因此我们有必要对其进行介绍。  

本文将重点讨论现代C++中关于C风格字符串对象的核心要点。  

定义C风格字符串  
----------------  

要定义C风格字符串变量，只需声明`char`（或`const char`/`constexpr char`）类型的C风格数组变量：  
```cpp
char str1[8]{};                    // 包含8个char的数组，索引0到7

const char str2[]{ "string" };     // 包含7个char的数组，索引0到6
constexpr char str3[] { "hello" }; // 包含6个const char的数组，索引0到5
```  
请记住需要为隐式的空终止符（null terminator）预留额外字符。  

定义带初始化器的C风格字符串时，强烈建议省略数组长度，让编译器自动计算。这样未来修改初始化器时，无需手动更新长度，也不会忘记为终止符预留空间。  

C风格字符串的退化  
----------------  

在课程[17.8 — C风格数组退化](Chapter-17/lesson17.8-c-style-array-decay.md)中，我们讨论了C风格数组在多数情况下会退化为指针。由于C风格字符串属于C风格数组，它们也会退化：  

- C风格字符串字面量退化为`const char*`  
- C风格字符串数组根据是否const退化为`const char*`或`char*`  

当C风格字符串退化为指针时，字符串长度（编码在类型信息中）会丢失。这种长度信息丢失正是C风格字符串需要空终止符的原因。字符串长度可通过从头开始计数直到遇到终止符来（低效地）重新获取。  

输出C风格字符串  
----------------  

输出C风格字符串时，`std::cout`会持续输出字符直到遇到空终止符。这个终止符标记字符串结束，使得已退化的字符串（丢失长度信息）仍可被打印。  
```cpp
#include <iostream>

void print(char ptr[])
{
    std::cout << ptr << '\n'; // 输出字符串
}

int main()
{
    char str[]{ "string" };
    std::cout << str << '\n'; // 输出string

    print(str);

    return 0;
}
```  
如果尝试打印没有终止符的字符串（如终止符被意外覆盖），将导致未定义行为。最常见的情况是打印完字符串所有字符后，继续输出相邻内存内容（解释为字符），直到遇到值为0的字节（视为终止符）。  

输入C风格字符串  
----------------  

考虑用户需要输入任意次数的骰子结果（如`524412616`），我们无法预知用户会输入多少字符。由于C风格字符串是固定大小的数组，解决方案是声明足够大的数组：  
```cpp
#include <iostream>

int main()
{
    char rolls[255] {}; // 声明足够存储254字符+终止符的数组
    std::cout << "输入骰子结果：";
    std::cin >> rolls;
    std::cout << "您输入的是：" << rolls << '\n';

    return 0;
}
```  

在C++20之前，`std::cin >> rolls`会尽可能多提取字符到`rolls`（遇到首个非前导空白符停止）。无法阻止用户输入超过254字符（无意或恶意），此时输入将溢出数组导致未定义行为。  

> **关键洞察**  
> **数组溢出（array overflow）**或**缓冲区溢出（buffer overflow）**是当数据量超过存储容量时的安全问题。此时溢出内存将被覆盖，导致未定义行为。攻击者可利用此漏洞改变程序行为。  

C++20修改了`operator>>`，使其仅适用于非退化的C风格字符串。这限制了`operator>>`最多提取数组长度允许的字符数，防止溢出。但这也意味着不能对退化的字符串使用`operator>>`。  

推荐使用以下方式读取C风格字符串：  
```cpp
#include <iostream>
#include <iterator> // 提供std::size

int main()
{
    char rolls[255] {}; 
    std::cout << "输入骰子结果：";
    std::cin.getline(rolls, std::size(rolls));
    std::cout << "您输入的是：" << rolls << '\n';

    return 0;
}
```  
`cin.getline()`会读取最多254字符（含空白符）到`rolls`，超限字符被丢弃。对于非退化数组，使用`std::size()`获取长度很方便。退化数组需其他方式确定长度，错误长度可能导致程序故障或安全问题。  

现代C++中，存储用户输入文本更安全的做法是使用`std::string`，它会自动调整大小以适应内容。  

修改C风格字符串  
----------------  

需注意C风格字符串遵循与C风格数组相同的规则：初始化时可赋值，后续不能使用赋值运算符：  
```cpp
char str[]{ "string" }; // 正确
str = "rope";           // 错误！
```  
这使得C风格字符串的使用略显笨拙。  

由于是数组，可使用[]运算符修改单个字符：  
```cpp
#include <iostream>

int main()
{
    char str[]{ "string" };
    std::cout << str << '\n';
    str[1] = 'p';
    std::cout << str << '\n';

    return 0;
}
```  
输出：  
```
string
spring
```  

获取C风格字符串长度  
----------------  

作为C风格数组，可用`std::size()`（C++20中`std::ssize()`）获取数组长度，但有两个注意事项：  
1. 不适用于退化的字符串  
2. 返回数组实际长度而非字符串长度  

```cpp
#include <iostream>

int main()
{
    char str[255]{ "string" }; // 6字符+终止符
    std::cout << "长度 = " << std::size(str) << '\n'; // 输出255

    char *ptr { str };
    std::cout << "长度 = " << std::size(ptr) << '\n'; // 编译错误

    return 0;
}
```  

替代方案是使用`<cstring>`头文件中的`strlen()`函数。`strlen()`适用于退化数组，返回字符串实际长度（不含终止符）：  
```cpp
#include <cstring> 
#include <iostream>

int main()
{
    char str[255]{ "string" }; 
    std::cout << "长度 = " << std::strlen(str) << '\n'; // 输出6

    char *ptr { str };
    std::cout << "长度 = " << std::strlen(ptr) << '\n'; // 输出6

    return 0;
}
```  
但`std::strlen()`效率较低，需遍历整个数组直到遇到终止符。  

其他C风格字符串操作函数  
----------------  

作为C语言主要字符串类型，C标准库提供了许多操作函数，这些函数通过`<cstring>`头文件继承到C++中。常见函数包括：  
* `strlen()` — 返回字符串长度  
* `strcpy()`, `strncpy()`, `strcpy_s()` — 覆盖字符串  
* `strcat()`, `strncat()` — 追加字符串  
* `strcmp()`, `strncmp()` — 比较字符串（相等返回`0`）  

除`strlen()`外，建议避免使用这些函数。  

避免使用非const C风格字符串  
----------------  

除非有特殊需求，否则应避免使用非const C风格字符串，因其易用性差且易溢出导致未定义行为（潜在安全问题）。  

在需要处理C风格字符串或固定缓冲区的罕见情况下（如内存受限设备），建议使用经过充分测试的第三方固定长度字符串库。  

> **最佳实践**  
> 优先使用`std::string`，避免非const C风格字符串。  

测验  
----------------  

**问题1**  
编写函数逐字符打印C风格字符串。使用指针和指针算术遍历每个字符。在`main`函数中用"Hello, world!"测试。  
  
<details><summary>答案</summary>  
```cpp
#include <iostream>

void printCString(const char str[])
{
    while (*str != '\0')
    {
        std::cout << *str;
        ++str;
    }
}

int main()
{
    printCString("Hello world!");
    std::cout << '\n';
    return 0;
}
```  
</details>  

**问题2**  
修改问题1的函数，倒序打印字符串。  
  
<details><summary>答案</summary>  
```cpp
#include <iostream>

void printCStringBackwards(const char str[])
{
    const char *ptr{ str };
    while (*ptr != '\0') ++ptr;
    while (ptr-- != str) std::cout << *ptr;
}

int main()
{
    printCStringBackwards("Hello world!");
    std::cout << '\n';
    return 0;
}
```  
</details>  

[下一课17.11 C风格字符串符号常量](Chapter-17/lesson17.11-c-style-string-symbolic-constants.md)  
[返回主页](/)  
[上一课17.9 指针算术与下标运算](Chapter-17/lesson17.9-pointer-arithmetic-and-subscripting.md)