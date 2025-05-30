6.1 — 运算符优先级与结合性
============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月13日下午3:55（太平洋夏令时）  
2025年2月19日

本章导读
----------------

本章基于课程[1.9 — 字面量与运算符简介](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)的概念构建，简要回顾如下：

**运算（operation）**是涉及零个或多个输入值（称为**操作数（operands）**）的数学过程，其产生新值（称为输出值）。待执行的具体运算由称为**运算符（operator）**的构造（通常为符号或符号对）表示。

例如，我们都知道`2 + 3`等于`5`。此例中，字面量`2`和`3`是操作数，符号`+`是指示对操作数应用数学加法以产生新值`5`的运算符。由于此处仅使用一个运算符，过程较为简单。

本章将讨论与运算符相关的主题，并探讨C++支持的多种常见运算符。

复合表达式求值
----------------

现在考虑复合表达式，如`4 + 2 * 3`。应将其分组为`(4 + 2) * 3`（结果为`18`）还是`4 + (2 * 3)`（结果为`10`）？根据标准数学优先级规则（规定乘法优先于加法），该表达式应分组为`4 + (2 * 3)`以得到值`10`。但编译器如何确定？

为求值表达式，编译器需执行两步操作：
* 在编译时解析表达式，确定操作数与运算符的分组方式（通过优先级和结合性规则实现，稍后讨论）。
* 在编译时或运行时对操作数求值并执行运算以生成结果。

运算符优先级
----------------

为辅助解析复合表达式，所有运算符被分配**优先级（precedence）**等级。优先级更高的运算符优先与操作数分组。

下表中可见，乘法和除法（优先级5）的优先级高于加法和减法（优先级6）。因此乘除将先于加减分组。换言之，`4 + 2 * 3`将被分组为`4 + (2 * 3)`。

运算符结合性
----------------

考虑复合表达式`7 - 4 - 1`。应分组为`(7 - 4) - 1`（结果为`2`）还是`7 - (4 - 1)`（结果为`4`）？由于两个减法运算符优先级相同，编译器无法仅凭优先级确定分组方式。

若同优先级运算符在表达式中相邻，运算符的**结合性（associativity）**指示编译器从左到右或从右到左求值运算符（而非操作数！）。减法优先级为6，该级运算符具有左到右结合性。因此表达式从左到右分组：`(7 - 4) - 1`。

运算符优先级与结合性表
----------------

下表主要作为参考图表，供后续解决优先级或结合性问题时查阅。

说明：
* 优先级1为最高级，17为最低级。高优先级运算符的操作数优先分组。
* L->R表示左到右结合性。
* R->L表示右到左结合性。

| 优先级/结合性 | 运算符                | 描述                                      | 模式                                      |
|---------------|-----------------------|------------------------------------------|------------------------------------------|
| 1 L->R        | `::` `::`            | 全局作用域（一元）<br>命名空间作用域（二元） | `::name`<br>`class_name::member_name`    |
| 2 L->R        | `()` `()` `type()` `type{}` `[]` `.` `->` `++` `--` `typeid` `const_cast` `dynamic_cast` `reinterpret_cast` `static_cast` `sizeof...` `noexcept` `alignof` | 圆括号<br>函数调用<br>函数式转型<br>列表初始化临时对象（C++11）<br>数组下标<br>对象成员访问<br>对象指针成员访问<br>后置递增<br>后置递减<br>运行时类型信息<br>移除const限定<br>运行时类型检查转型<br>类型间转型<br>编译时类型检查转型<br>获取参数包大小<br>编译时异常检查<br>获取类型对齐 | `(expression)`<br>`function_name(arguments)`<br>`type(expression)`<br>`type{expression}`<br>`pointer[expression]`<br>`object.member_name`<br>`object_pointer->member_name`<br>`lvalue++`<br>`lvalue--`<br>`typeid(type)`或`typeid(expression)`<br>`const_cast<type>(expression)`<br>`dynamic_cast<type>(expression)`<br>`reinterpret_cast<type>(expression)`<br>`static_cast<type>(expression)`<br>`sizeof...(expression)`<br>`noexcept(expression)`<br>`alignof(type)` |
| 3 R->L        | `+` `-` `++` `--` `!` `not` `~` `(type)` `sizeof` `co_await` `&` `*` `new` `new[]` `delete` `delete[]` | 一元正号<br>一元负号<br>前置递增<br>前置递减<br>逻辑非<br>逻辑非<br>按位取反<br>C风格转型<br>字节大小<br>等待异步调用<br>取地址<br>解引用<br>动态内存分配<br>动态数组分配<br>动态内存释放<br>动态数组释放 | `+expression`<br>`-expression`<br>`++lvalue`<br>`--lvalue`<br>`!expression`<br>`not expression`<br>`~expression`<br>`(new_type)expression`<br>`sizeof(type)`或`sizeof(expression)`<br>`co_await expression`（C++20）<br>`&lvalue`<br>`*expression`<br>`new type`<br>`new type[expression]`<br>`delete pointer`<br>`delete[] pointer` |
| 4 L->R        | `->*` `.*`           | 成员指针选择器<br>成员对象选择器          | `object_pointer->*pointer_to_member`<br>`object.*pointer_to_member` |
| 5 L->R        | `*` `/` `%`          | 乘法<br>除法<br>取余                      | `expression * expression`<br>`expression / expression`<br>`expression % expression` |
| 6 L->R        | `+` `-`              | 加法<br>减法                              | `expression + expression`<br>`expression - expression` |
| 7 L->R        | `<<` `>>`            | 左移/插入<br>右移/提取                    | `expression << expression`<br>`expression >> expression` |
| 8 L->R        | `<=>`                | 三路比较（C++20）                         | `expression <=> expression`              |
| 9 L->R        | `<` `<=` `>` `>=`    | 小于比较<br>小于等于比较<br>大于比较<br>大于等于比较 | `expression < expression`<br>`expression <= expression`<br>`expression > expression`<br>`expression >= expression` |
| 10 L->R       | `==` `!=`            | 相等<br>不等                              | `expression == expression`<br>`expression != expression` |
| 11 L->R       | `&`                  | 按位与                                    | `expression & expression`                |
| 12 L->R       | `^`                  | 按位异或                                  | `expression ^ expression`                |
| 13 L->R       | `|`                  | 按位或                                    | `expression | expression`                |
| 14 L->R       | `&&` `and`           | 逻辑与<br>逻辑与                          | `expression && expression`<br>`expression and expression` |
| 15 L->R       | `||` `or`            | 逻辑或<br>逻辑或                          | `expression || expression`<br>`expression or expression` |
| 16 R->L       | `throw` `co_yield` `?:` `=` `*=` `/=` `%=` `+=` `-=` `<<=` `>>=` `&=` `|=` `^=` | 抛出表达式<br>产出表达式（C++20）<br>条件运算符<br>赋值<br>乘后赋值<br>除后赋值<br>取余后赋值<br>加后赋值<br>减后赋值<br>左移后赋值<br>右移后赋值<br>按位与后赋值<br>按位或后赋值<br>按位异或后赋值 | `throw expression`<br>`co_yield expression`<br>`expression ? expression : expression`<br>`lvalue = expression`<br>`lvalue *= expression`<br>`lvalue /= expression`<br>`lvalue %= expression`<br>`lvalue += expression`<br>`lvalue -= expression`<br>`lvalue <<= expression`<br>`lvalue >>= expression`<br>`lvalue &= expression`<br>`lvalue |= expression`<br>`lvalue ^= expression` |
| 17 L->R       | `,`                  | 逗号运算符                                | `expression, expression`                 |

您应已识别部分运算符，如`+`、`-`、`*`、`/`、`()`和`sizeof`。但除非有其他编程语言经验，目前表中多数运算符可能难以理解。这很正常。本章将介绍其中许多运算符，其余将在需要时引入。

> **问：指数运算符在何处？**  
> C++未包含指数运算符（`operator^`在C++中有不同功能）。指数运算详见课程[6.3 — 取余与指数运算](Chapter-6/lesson6.3-remainder-and-exponentiation.md)。

注意：`operator<<`同时处理按位左移和插入，`operator>>`同时处理按位右移和提取。编译器可根据操作数类型确定执行的操作。

括号分组
----------------

根据优先级规则，`4 + 2 * 3`将被分组为`4 + (2 * 3)`。但若实际意图为`(4 + 2) * 3`？与标准数学相同，C++中可显式使用括号设定操作数分组。这之所以有效，是因为括号具有最高优先级之一，通常先于其内部内容求值。

使用括号提升复合表达式可读性
----------------

考虑表达式`x && y || z`。应求值为`(x && y) || z`还是`x && (y || z)`？查表可知`&&`优先级高于`||`。但运算符和优先级级别过多难以全记，且不应频繁查表理解复合表达式求值。

为减少错误并提升代码可读性（无需查表），建议对非平凡复合表达式添加括号以明确意图。

> **最佳实践**  
> 使用括号明确非平凡复合表达式的求值顺序（即使技术上非必需）。

经验法则：除加法、减法、乘法和除法外，所有表达式均应加括号。

上述最佳实践有一例外：仅含单个赋值运算符（无逗号运算符）的表达式，其赋值右操作数无需括号。

例如：
```cpp
x = (y + z + w);   // 避免此写法
x = y + z + w;     // 此写法可接受

x = ((y || z) && w); // 避免此写法
x = (y || z) && w;   // 此写法可接受

x = (y *= z); // 含多重赋值的表达式仍需括号
```

赋值运算符优先级仅高于逗号运算符（且后者极少使用）。因此只要仅含单一赋值（无逗号），即可确保右操作数在赋值前完全求值。

> **最佳实践**  
> 含单一赋值运算符的表达式，其赋值右操作数无需括号。

运算的值计算
----------------

C++标准使用术语**值计算（value computation）**指代表达式中运算符的执行以产生值。优先级和结合性规则决定值计算的顺序。

例如表达式`4 + 2 * 3`，根据优先级规则分组为`4 + (2 * 3)`。`(2 * 3)`的值计算必须先执行，才能完成`4 + 6`的值计算。

操作数的求值
----------------

C++标准（主要）使用术语**求值（evaluation）**指代操作数的求值（而非运算符或表达式的求值！）。例如表达式`a + b`，`a`将被求值产生某值，`b`被求值产生某值。这些值随后可用作`operator+`的操作数。

> **术语说明**  
> 非正式场合中，"evaluates"通常指整个表达式（值计算）的求值，而非仅表达式的操作数。

操作数求值顺序大多未指定
----------------

多数情况下，操作数（含函数参数）的求值顺序未指定，意味着可以任意顺序求值。

考虑以下表达式：
```cpp
a * b + c * d
```

根据前述优先级和结合性规则，该表达式将被分组为：
```cpp
(a * b) + (c * d)
```

若`a`为`1`，`b`为`2`，`c`为`3`，`d`为`4`，此表达式始终计算值`14`。

但优先级和结合性规则仅规定运算符与操作数的分组方式及值计算顺序，未指定操作数或子表达式的求值顺序。编译器可自由以任意顺序求值操作数`a`、`b`、`c`或`d`，也可自由先计算`a * b`或`c * d`。

对于多数表达式，此顺序无关紧要。上述示例中，无论变量`a`、`b`、`c`或`d`以何顺序求值，结果始终为`14`，不存在歧义。

但可能编写出求值顺序影响结果的表达式。考虑以下新手常见错误程序：
```cpp
#include <iostream>

int getValue()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;
    return x;
}

void printCalculation(int x, int y, int z)
{
    std::cout << x + (y * z);
}

int main()
{
    printCalculation(getValue(), getValue(), getValue()); // 此行存在歧义
    return 0;
}
```

若运行此程序并输入`1`、`2`、`3`，您可能认为将计算`1 + (2 * 3)`并输出`7`。但这假设`printCalculation()`的参数按左到右顺序求值（即形参`x`获值`1`，`y`获`2`，`z`获`3`）。若参数按右到左求值（即形参`z`获值`1`，`y`获`2`，`x`获`3`），程序将输出`5`。

> **提示**  
> Clang编译器按左到右顺序求值参数，GCC编译器按右到左顺序。

若需验证此行为，可在[Wandbox](https://wandbox.org/#)操作：粘贴上述程序，在*Stdin*标签页输入`1 2 3`，选择GCC或Clang后编译程序。输出将显示在页面底部（可能需要滚动）。您会注意到GCC与Clang的输出不同！

可通过将每个`getValue()`函数调用拆分为独立语句消除歧义：
```cpp
#include <iostream>

int getValue() { /* 同上 */ }

void printCalculation(int x, int y, int z) { /* 同上 */ }

int main()
{
    int a{ getValue() }; // 首先执行
    int b{ getValue() }; // 其次执行
    int c{ getValue() }; // 最后执行

    printCalculation(a, b, c); // 此行无歧义
    return 0;
}
```
此版本中，`a`始终为`1`，`b`为`2`，`c`为`3`。无论`printCalculation()`的参数求值顺序如何，形参`x`始终获值`1`，`y`获值`2`，`z`获值`3`。此版本将确定性地输出`7`。

> **关键洞察**  
> 操作数、函数参数和子表达式可以任意顺序求值。

常见误解是认为运算符优先级和结合性影响求值顺序。优先级和结合性仅用于确定操作数与运算符的分组方式以及值计算的顺序。

> **警告**  
> 确保编写的表达式（或函数调用）不依赖于操作数（或参数）的求值顺序。

> **相关内容**  
> 含副作用（side effects）的运算符也可能导致意外求值结果，详见课程[6.4 — 递增/递减运算符及副作用](Chapter-6/lesson6.4-increment-decrement-operators-and-side-effects.md)。

测验时间
----------------

**问题1**  
日常数学中，括号内表达式优先求值。例如`(2 + 3) * 4`中，`(2 + 3)`部分先求值。

本题提供一组无括号表达式。根据上表的运算符优先级和结合性规则，为每个表达式添加括号以明确编译器求值方式。

[显示提示](javascript:void(0))  
提示：使用上表"模式"列判断运算符为一元（单操作数）或二元（双操作数）。复习课程[1.9 — 字面量与运算符简介](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)可回顾一元/二元运算符概念。

| 示例问题：x = 2 + 3 % 4<br>二元运算符`%`优先级高于`+`或`=`，故先求值：x = 2 + (3 % 4)<br>二元运算符`+`优先级高于`=`，故随后求值：最终答案：x = (2 + (3 % 4))<br>现无需查表即可理解此表达式求值方式。 |
| --- |

a) x = 3 + 4 + 5;  
[显示答案](javascript:void(0))  
二元运算符`+`优先级高于`=`：  
x = (3 + 4 + 5)  
二元运算符`+`具左到右结合性：  
最终答案：x = ((3 + 4) + 5)

b) x = y = z;  
[显示答案](javascript:void(0))  
二元运算符`=`具右到左结合性：  
最终答案：x = (y = z)

c) z *= ++y + 5;  
[显示答案](javascript:void(0))  
一元运算符`++`优先级最高：  
z *= (++y) + 5  
二元运算符`+`优先级次之：  
最终答案：z *= ((++y) + 5)

d) a \|\| b && c \|\| d;  
[显示答案](javascript:void(0))  
二元运算符`&&`优先级高于`||`：  
a \|\| (b && c) \|\| d  
二元运算符`||`具左到右结合性：  
最终答案：(a \|\| (b && c)) \|\| d

[下一课 6.2 算术运算符](Chapter-6/lesson6.2-arithmetic-operators.md)  
[返回主页](/)  
[上一课 5.x 第5章总结与测验](Chapter-5/lesson5.x-chapter-5-summary-and-quiz.md)