5.2 — 字面量（Literals）
===============

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")
2007年6月9日 下午10:43（太平洋夏令时）
2025年3月17日

**字面量（literal）**是直接插入代码中的值。例如：
```
return 5;                     // 5 是整数字面量（integer literal）
bool myNameIsAlex { true };   // true 是布尔字面量（boolean literal）
double d { 3.4 };             // 3.4 是双精度字面量（double literal）
std::cout << "Hello, world!"; // "Hello, world!" 是C风格字符串字面量（C-style string literal）
```
字面量有时称为**字面常量（literal constant）**，因为其含义不可重定义（`5`始终表示整数值5）。

### 字面量的类型
与对象拥有类型类似，所有字面量均有类型。字面量的类型由其值推导得出。例如：整数字面量（如`5`）默认推导为`int`类型。

| 字面量值示例      | 默认字面量类型       | 说明                     |
|-------------------|----------------------|--------------------------|
| 整数值：5, 0, -3  | int                  |                          |
| 布尔值：true, false | bool                 |                          |
| 浮点值：1.2, 0.0, 3.4 | double（非float！） |                          |
| 字符：'a', '\\n'  | char                 |                          |
| C风格字符串："Hello, world!" | const char[14]      | 详见下方C风格字符串字面量章节 |

### 字面量后缀（suffix）
若字面量默认类型不符合需求，可通过添加后缀改变类型。常见后缀如下：

| 数据类型          | 后缀         | 含义                          |
|-------------------|--------------|-------------------------------|
| 整数类型（integral） | u 或 U      | unsigned int                 |
| 整数类型          | l 或 L      | long                         |
| 整数类型          | ul, uL 等组合 | unsigned long                |
| 整数类型          | ll 或 LL    | long long                    |
| 整数类型          | ull, uLL 等组合 | unsigned long long           |
| 整数类型          | z 或 Z      | std::size_t的有符号版本（C++23） |
| 整数类型          | uz, uZ 等组合 | std::size_t（C++23）         |
| 浮点类型（floating point） | f 或 F      | float                        |
| 浮点类型          | l 或 L      | long double                  |
| 字符串            | s           | std::string                  |
| 字符串            | sv          | std::string_view             |

我们将在后文详细讨论整数和浮点字面量及其后缀。多数情况下无需后缀（除`f`外）。

> **相关内容**  
> `s`和`sv`后缀需额外代码支持，详见课程：
> * [5.7 — std::string简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)
> * [5.8 — std::string_view简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)  
>  
> 复数和时间字面量存在额外（罕见）后缀，文档参见[此处](https://en.cppreference.com/w/cpp/symbol_index/literals)。

> **进阶阅读**  
> 除`f`后缀外，后缀多用于涉及类型推导的场景。参见：
> * [10.8 — 使用auto关键字的对象类型推导](Chapter-10/lesson10.8-type-deduction-for-objects-using-the-auto-keyword.md)
> * [13.14 — 类模板参数推导（CTAD）与推导指引](Chapter-13/lesson13.14-class-template-argument-deduction-ctad-and-deduction-guides.md)

### 后缀大小写规范
多数后缀不区分大小写，例外情况：
* `s`和`sv`必须小写
* 连续两个`l`或`L`字符需大小写一致（不接受`lL`或`Ll`）

因小写`l`在某些字体中易与数字`1`混淆，部分开发者倾向使用大写后缀，也有开发者除`L`外均用小写。

> **最佳实践**  
> 优先使用大写L后缀而非小写l。

### 整数字面量（Integral literals）
通常无需为整数字面量添加后缀，示例如下：
```
#include <iostream>

int main()
{
    std::cout << 5 << '\n';  // 5（无后缀）默认类型为int
    std::cout << 5L << '\n'; // 5L 类型为long
    std::cout << 5u << '\n'; // 5u 类型为unsigned int
    return 0;
}
```
多数情况下，即使初始化非`int`类型，使用无后缀`int`字面量亦可：
```
int main()
{
    int a { 5 };          // 正确：类型匹配
    unsigned int b { 6 }; // 正确：编译器将int值6转换为unsigned int值6
    long c { 7 };         // 正确：编译器将int值7转换为long值7
    return 0;
}
```
此类场景中，编译器会将int字面量转换为目标类型：
* 第一种情况：`5`已是默认`int`类型，编译器直接用于初始化`int`变量`a`
* 第二种情况：`int`值`6`与`unsigned int b`类型不匹配，编译器将其转换为`unsigned int`值6后初始化`b`
* 第三种情况：`int`值`7`与`long c`类型不匹配，编译器将其转换为`long`值7后初始化`c`

### 浮点字面量（Floating point literals）
浮点字面量默认类型为`double`。若需`float`类型，应使用`f`（或`F`）后缀：
```
#include <iostream>

int main()
{
    std::cout << 5.0 << '\n';  // 5.0（无后缀）默认类型为double
    std::cout << 5.0f << '\n'; // 5.0f 类型为float
    return 0;
}
```
初学者常困惑为何以下代码触发编译器警告：
```
float f { 4.1 }; // 警告：4.1是double字面量，非float字面量
```
因`4.1`无后缀，字面量类型为`double`而非`float`。编译器推导字面量类型时不考虑其用途（本例中用于初始化`float`变量）。因字面量类型（`double`）与变量类型（`float`）不匹配，需将字面量值转换为`float`才能初始化变量`f`。`double`转`float`可能导致精度损失，故编译器发出警告。

解决方案：
```
float f { 4.1f }; // 使用'f'后缀使字面量成为float类型
double d { 4.1 }; // 将变量改为double类型以匹配字面量类型
```

### 浮点字面量的科学计数法
浮点字面量有两种书写方式：
1. **标准表示法**：含小数点的数字
```
double pi { 3.14159 }; // 3.14159是标准表示法的double字面量
double d { -1.23 };    // 字面量可为负数
double why { 0. };     // 语法有效，但建议写为0.0（避免小数点不易辨识）
```
2. **科学计数法**：用`e`表示指数
```
double avogadro { 6.02e23 };    // 6.02 x 10^23（科学计数法double字面量）
double protonCharge { 1.6e-19 }; // 质子电荷量1.6 x 10^-19
```

### 字符串字面量（String literals）
编程中，**字符串（string）**是表示文本（如名称、单词、句子）的字符序列。首个C++程序通常如下：
```
#include <iostream>
 
int main()
{
    std::cout << "Hello, world!";
    return 0;
}
```
`"Hello, world!"`即字符串字面量。字符串字面量由双引号标识（区别于单引号的字符字面量）。

因字符串广泛使用，多数现代编程语言将其作为基础类型。由于历史原因，C++中字符串非基础类型，而是复杂难用的特殊类型（后续课程将解释其机制）。此类字符串常称**C字符串（C strings）**或**C风格字符串（C-style strings）**，继承自C语言。

关于C风格字符串字面量需注意两点：
1. **隐式空终止符（null terminator）**：如`"hello"`看似5字符，实际含6字符：`'h'`,`'e'`,`'l'`,`'l'`,`'o'`及`'\0'`（ASCII码0）。结尾的`'\0'`称为**空终止符**，标识字符串结束。含空终止符的字符串称**空终止字符串（null-terminated string）**。

> **进阶阅读**  
> 此即`"Hello, world!"`类型为`const char[14]`而非`const char[13]`的原因——隐式空终止符计入字符数。  
> 空终止符设计亦源于历史需求：用于确定字符串结尾。

2. **生存期特性**：与多数字面量（非对象的值）不同，C风格字符串字面量是const对象，程序启动时创建并保证在整个程序周期存在。此特性在讨论`std::string_view`时尤为重要。

> **关键洞察**  
> C风格字符串字面量是程序启动时创建的const对象，保证在整个程序周期存在。  
> 不同于C风格字符串，`std::string`和`std::string_view`字面量生成临时对象。这些临时对象必须立即使用，因其在所属完整表达式结束时销毁。

> **相关内容**  
> `std::string`和`std::string_view`字面量分别详见：  
> * [5.7 — std::string简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)  
> * [5.8 — std::string_view简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)

### 魔法数字（Magic numbers）
**魔法数字（magic number）**指含义不明确或后续可能需要修改的字面量（通常为数字）。以下两条语句展示魔法数字示例：
```
const int maxStudentsPerSchool{ numClassrooms * 30 };
setMax(30);
```
此处的`30`含义为何？前者可能表示每班学生数，但不够明确；后者含义未知，需查看函数实现才能理解。

复杂程序中，若无注释说明，推断字面量含义极为困难。使用魔法数字通常被视为不良实践：除缺乏上下文外，若需修改数值也会引发问题。假设学校购置新课桌使班级容量从30增至35，程序需同步更新。

为此需将`30`改为`35`，但应修改哪些？`maxStudentsPerSchool`的`30`较明显，但`setMax()`的参数`30`呢？若含义相同则需修改，否则应保留（避免破坏程序）。全局搜索替换可能误改不应变更的`setMax()`参数。因此需检查代码中所有`30`字面量（可能数百处），逐一判断是否修改，耗时且易错。

通过符号常量可轻松解决上下文缺失和修改问题：
```
const int maxStudentsPerClass { 30 };
const int totalStudents{ numClassrooms * maxStudentsPerClass }; // 明确30含义

const int maxNameLength{ 30 };
setMax(maxNameLength); // 明确此30用于不同上下文
```
常量名提供上下文，且仅需修改一处即可全局生效。

> **注意**  
> 魔法数字不限于数字，也可是文本（如名称）或其他类型：
> ```
> int main()
> {
>     printAppWelcome("MyCalculator"); // 错误：应用名称可能多处使用或变更
> }
> ```

明显上下文使用且不易变更的字面量通常不被视为魔法数字。`-1`、`0`、`0.0`和`1`常用于此类场景：
```
int idGenerator { 0 };         // 合理：ID生成器从0开始
idGenerator = idGenerator + 1; // 合理：仅递增生成器
```
某些数字在上下文中含义明确（故不被视为魔法数字）：
```
int kmtoM(int km)
{
    return km * 1000; // 合理：1000显然是换算系数
}
```
连续整数ID通常也不视为魔法数字：
```
int main()
{
    // 合理：仅为连续ID/计数
    printPlayerInfo(1); // 此处`1`改为`player1`无实质改善
    printPlayerInfo(2);
}
```

> **最佳实践**  
> 避免代码中的魔法数字（使用constexpr变量替代，见课程[5.6 — Constexpr变量](Chapter-5/lesson5.6-constexpr-variables.md)）。

[下一课 5.3 数字系统（十进制、二进制、十六进制与八进制）](Chapter-5/lesson5.3-numeral-systems-decimal-binary-hexadecimal-and-octal.md)  
[返回目录](/)
[上一课 5.1 常量变量（具名常量）](Chapter-5/lesson5.1-constant-variables-named-constants.md)