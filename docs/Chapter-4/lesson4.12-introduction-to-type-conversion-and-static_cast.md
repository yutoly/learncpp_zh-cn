4.12 — 类型转换与static_cast简介  
========================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年3月3日（首次发布于2021年10月21日）  

隐式类型转换（implicit type conversion）  
----------------  

考虑以下程序：  
```
#include <iostream>

void print(double x) // print接收double类型参数
{
	std::cout << x << '\n';
}

int main()
{
	print(5); // 传入int值会发生什么？
	return 0;
}
```  
上例中，`print()`函数需要`double`类型参数，但调用者传入的是`int`类型的`5`。此时会发生什么？  

多数情况下，C\+\+允许我们在基础类型之间转换值。将数据从一种类型转换为另一种类型的过程称为**类型转换（type conversion）**。因此，int类型实参`5`会被转换为double值`5.0`后复制给形参`x`。`print()`函数将输出此值：  
```
5
```  
> **提示**  
> 默认情况下，小数部分为0的浮点值会省略小数点打印（例如`5.0`输出为`5`）。  

当编译器未经显式要求自动执行类型转换时，称为**隐式类型转换（implicit type conversion）**。上例中我们未显式要求将整数值`5`转为double值`5.0`，但函数需要double类型而传入int实参，编译器发现类型不匹配后执行了隐式转换。  

以下类似示例使用int变量替代字面值：  
```
#include <iostream>

void print(double x) // print接收double类型参数
{
	std::cout << x << '\n';
}

int main()
{
	int y { 5 };
	print(y); // y是int类型
	return 0;
}
```  
转换过程与上例相同：int变量`y`的值`5`被转换为double值`5.0`后复制给形参`x`。  

类型转换生成新值  
----------------  
类型转换过程不会修改原始数据值（或对象），而是以该数据为输入生成转换结果。  

> **关键洞察**  
> 值类型转换的行为类似于调用返回目标类型的函数：待转换数据作为参数传入，转换结果通过临时对象返回给调用者。  

上例中，转换既未将变量`y`从int改为double，也未将其值从`5`变为`5.0`。实际过程是以`y`的值`5`为输入，生成值为`5.0`的double类型临时对象，再传递给`print`函数。  

> **进阶阅读**  
> 部分高级类型转换（如`const_cast`或`reinterpret_cast`）不生成临时对象，而是重新解释现有值的类型。  

隐式类型转换警告  
----------------  
虽然隐式转换能满足多数需求，但某些情况下存在问题。参考以下程序：  
```
#include <iostream>

void print(int x) // print现在接收int参数
{
	std::cout << x << '\n';
}

int main()
{
	print(5.5); // 警告：传入double值
	return 0;
}
```  
本例中，`print()`改为接收`int`参数，但传入的是double值`5.5`。编译器将执行隐式类型转换，将double值`5.5`转为int类型以匹配函数参数。  

与初始示例不同，编译此程序时编译器会生成数据丢失警告。若开启"将警告视为错误"选项（建议开启），编译将中止。  

> **提示**  
> 编译此示例需临时禁用"将警告视为错误"设置。详见课程[0.11 — 编译器配置：警告与错误级别](Chapter-0/lesson0.11-configuring-your-compiler-warning-and-error-levels.md)。  

程序运行后输出：  
```
5
```  
注意：尽管传入`5.5`，程序却输出`5`。因为整型无法存储小数部分，double值`5.5`被隐式转换为`int`时小数部分被丢弃。  

由于浮点转整型会丢失小数部分，此类隐式转换将触发编译器警告。即使传入无小数部分的浮点值（如`5.0`），虽实际转换未丢失值，编译器仍可能警告转换不安全。  

> **关键洞察**  
> 部分类型转换（如`char`转`int`）始终保留原值，而另一些（如`double`转`int`）可能导致值改变。不安全的隐式转换通常产生编译器警告，或（在花括号初始化时）直接报错。  
>  
> 这是推荐花括号初始化的主因之一，它能阻止用会丢失值的初始化器初始化变量：  
> ```
> int main()
> {
>     double d { 5 }; // 正确：int转double安全
>     int x { 5.5 };  // 错误：double转int不安全
>     return 0;
> }
> ```  

> **相关内容**  
> 隐式类型转换是重要主题，将在课程[10.1 — 隐式类型转换](Chapter-10/lesson10.1-implicit-type-conversion.md)深入探讨。  

static_cast运算符显式类型转换简介  
----------------  
回到最近的`print()`示例：若我们*有意*传递double值给接收整型的函数（已知转换会丢弃小数部分），临时关闭警告选项是糟糕的做法——这会导致警告被忽略，可能掩盖更严重问题。  

C\+\+支持第二种类型转换方式：**显式类型转换（explicit type conversion）**。这种方式允许程序员显式指示编译器执行类型转换，并自行承担转换结果责任。若转换导致值丢失，编译器不会警告。  

多数显式转换使用`static_cast`运算符，其语法如下：  
```
static_cast<新类型>(表达式)
```  
static\_cast获取表达式的值，并将其转换为*新类型*（如int、bool、char、double）。  

> **关键洞察**  
> 当C\+\+语法（预处理除外）使用尖括号\<\>时，括号内通常是类型参数，这是C\+\+处理参数化类型的典型方式。  

用`static_cast`更新先前的程序：  
```
#include <iostream>

void print(int x)
{
	std::cout << x << '\n';
}

int main()
{
	print( static_cast<int>(5.5) ); // 显式将double值5.5转为int
	return 0;
}
```  
由于我们显式要求将double值`5.5`转为`int`，编译器不再生成数据丢失警告（可保持"将警告视为错误"开启）。  

> **相关内容**  
> C\+\+支持其他类型转换，将在课程[10.6 — 显式类型转换与static_cast](Chapter-10/lesson10.6-explicit-type-conversion-casting-and-static-cast.md)详述。  

用static\_cast将char转为int  
----------------  
在字符课程[4.11 — 字符](Chapter-4/lesson4.11-chars.md)中，使用`std::cout`打印char值会输出字符形式：  
```
#include <iostream>

int main()
{
    char ch{ 97 }; // 97是'a'的ASCII码
    std::cout << ch << '\n'; // 输出: a
    return 0;
}
```  
如需打印整数值而非字符，可通过`static_cast`将`char`显式转为`int`：  
```
#include <iostream>

int main()
{
    char ch{ 97 }; 
    // 将ch的值转为int打印
    std::cout << ch << " has value " << static_cast<int>(ch) << '\n';
    return 0;
}
```  
输出：  
```
a has value 97
```  
需注意：*static\_cast*的参数是表达式。传递变量时先求值再转换，变量本身不受影响。上例中`ch`仍是char类型且保留原值。  

用static\_cast进行有符号转换  
----------------  
有符号整型可通过static\_cast转为无符号整型，反之亦然。  

若转换值在目标类型范围内，值保持不变（仅类型改变）：  
```
#include <iostream>

int main()
{
    unsigned int u1 { 5 };
    // 将u1转为有符号int
    int s1 { static_cast<int>(u1) };
    std::cout << s1 << '\n'; // 输出5

    int s2 { 5 };
    // 将s2转为无符号int
    unsigned int u2 { static_cast<unsigned int>(s2) };
    std::cout << u2 << '\n'; // 输出5
    return 0;
}
```  
输出：  
```
5
5
```  
因`5`同时属于有符号int和无符号int范围，转换无问题。  

若转换值超出目标类型范围：  
* 目标类型为无符号时，值将取模包装（modulo wrapped），详见课程[4.5 — 无符号整数及其规避](Chapter-4/lesson4.5-unsigned-integers-and-why-to-avoid-them.md)。  
* 目标类型为有符号时，C\+\+20前为实现定义（implementation-defined），C\+\+20起采用取模包装。  

以下示例转换两个超出目标类型范围的值（假设32位整型）：  
```
#include <iostream>

int main()
{
    int s { -1 };
    std::cout << static_cast<unsigned int>(s) << '\n'; // 输出4294967295 

    unsigned int u { 4294967295 }; // 最大32位无符号整型
    std::cout << static_cast<int>(u) << '\n'; // C++20前为实现定义，C++20起输出-1
    return 0;
}
```  
C\+\+20输出：  
```
4294967295
-1
```  
有符号int值`-1`无法用无符号int表示，结果取模包装为`4294967295`。  
无符号int值`4294967295`无法用有符号int表示：C\+\+20前结果由实现定义（通常为`-1`），C\+\+20起取模包装为`-1`。  

> **警告**  
> C\+\+20前，将超出范围的无符号整型转为有符号整型会导致实现定义行为。  

std::int8\_t与std::uint8\_t可能表现类似字符  
----------------  
如课程[4.6 — 固定宽度整数与size_t](Chapter-4/lesson4.6-fixed-width-integers-and-size-t.md)所述，多数编译器将`std::int8_t`和`std::uint8_t`（及对应的fast/least类型）分别等同于`signed char`和`unsigned char`。通过字符知识可演示潜在问题：  
```
#include <cstdint>
#include <iostream>

int main()
{
    std::int8_t myInt{65};      // 用65初始化
    std::cout << myInt << '\n'; // 预期输出65，但通常输出'A'
    return 0;
}
```  
虽然`std::int8_t`自述为整型，但多数系统会将其视为`signed char`而输出`A`（某些系统可能输出`65`）。  

若需确保`std::int8_t`或`std::uint8_t`被作为整型处理，可用`static_cast`转换：  
```
#include <cstdint>
#include <iostream>

int main()
{
    std::int8_t myInt{65};
    std::cout << static_cast<int>(myInt) << '\n'; // 始终输出65
    return 0;
}
```  
当`std::int8_t`被视为字符时，控制台输入也会引发问题：  
```
#include <cstdint>
#include <iostream>

int main()
{
    std::cout << "Enter a number between 0 and 127: ";
    std::int8_t myInt{};
    std::cin >> myInt;

    std::cout << "You entered: " << static_cast<int>(myInt) << '\n';
    return 0;
}
```  
运行示例：  
```
Enter a number between 0 and 127: 35
You entered: 51
```  
原因：当`std::int8_t`被视为字符时，输入例程将输入解释为字符序列而非整数。输入`35`实际是字符`'3'`和`'5'`。因char对象仅能存储一个字符，故提取`'3'`（`'5'`留在输入流中）。字符`'3'`的ASCII码为51，故`myInt`存储值`51`。  

其他固定宽度类型始终作为整型输入/输出。  

测验时间  
----------------  
**问题1**  
编写程序要求用户输入单个字符，使用`static_cast`打印该字符及其ASCII码。输出应匹配：  
```
Enter a single character: a
You entered 'a', which has ASCII code 97.
```  
  
```
#include <iostream>

int main()
{
	std::cout << "Enter a single character: ";
	char c{};
	std::cin >> c;
	std::cout << "You entered '" << c << "', which has ASCII code " << static_cast<int>(c) << ".\n";
	return 0;
}
```  

**问题2**  
修改问题1的程序，改用隐式类型转换替代`static_cast`。能想到几种实现方式？  
> **注意**：实际开发中应优先使用显式转换，此处仅为测试隐式转换理解。  

  
**方案1**：用int变量初始化时隐式转换  
```
#include <iostream>

int main()
{
	std::cout << "Enter a single character: ";
	char c{};
	std::cin >> c;
	int ascii{ c }; // 初始化时隐式转换
	std::cout << "You entered '" << c << "', which has ASCII code " << ascii << ".\n";
	return 0;
}
```  
**方案2**：函数返回时隐式转换  
```
#include <iostream>

int charAsInt(char c) { return c; } // 返回时隐式转换

int main()
{
	std::cout << "Enter a single character: ";
	char c{};
	std::cin >> c;
	std::cout << "You entered '" << c << "', which has ASCII code " << charAsInt(c) << ".\n";
	return 0;
}
```  
**方案3**：函数参数传递时隐式转换  
```
#include <iostream>

int getInt(int c) { return c; } // 参数传递时隐式转换

int main()
{
	std::cout << "Enter a single character: ";
	char c{};
	std::cin >> c;
	std::cout << "You entered '" << c << "', which has ASCII code " << getInt(c) << ".\n";
	return 0;
}
```  

[下一课 4.x — 第4章总结与测验](Chapter-4/lesson4.x-chapter-4-summary-and-quiz.md)
[返回主页](/)  
[上一课 4.11 — 字符](Chapter-4/lesson4.11-chars.md)