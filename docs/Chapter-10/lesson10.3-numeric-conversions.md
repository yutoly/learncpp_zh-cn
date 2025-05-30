10.3 — 数值转换（Numeric conversions）
===========================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年8月20日（首次发布于2021年6月17日）  

在上一课[10.2 — 浮点数与整型的提升（Floating-point and integral promotion）](Chapter-10/lesson10.2-floating-point-and-integral-promotion.md)中，我们讨论了数值提升（numeric promotion）——将特定较窄的数值类型转换为更宽的数值类型（通常是`int`或`double`）以实现高效处理。C++还支持另一类数值类型转换，称为**数值转换（numeric conversions）**，涵盖基本类型间的其他转换。  

> **关键洞察**  
> 所有被数值提升规则（[10.2 — 浮点数与整型的提升](Chapter-10/lesson10.2-floating-point-and-integral-promotion.md)）涵盖的类型转换都称为数值提升，而非数值转换。  

数值转换有五种基本类型：  
1. **整型间的转换**（排除整型提升）：  
```cpp
short s = 3;     // 将int转换为short
long l = 3;      // 将int转换为long
char ch = s;     // 将short转换为char
unsigned int u = 3; // 将int转换为unsigned int
```

2. **浮点类型间的转换**（排除浮点提升）：  
```cpp
float f = 3.0;    // 将double转换为float
long double ld = 3.0; // 将double转换为long double
```

3. **浮点类型到整型的转换**：  
```cpp
int i = 3.5; // 将double转换为int
```

4. **整型到浮点类型的转换**：  
```cpp
double d = 3; // 将int转换为double
```

5. **整型或浮点类型到bool的转换**：  
```cpp
bool b1 = 3;   // 将int转换为bool
bool b2 = 3.0; // 将double转换为bool
```

> **补充说明**  
> 由于大括号初始化（brace initialization）严格禁止某些数值转换（下节课详述），本课使用拷贝初始化（copy initialization）以保持示例简洁。  

安全与不安全转换  
----------------  
不同于数值提升（总是保留值且"安全"），多数数值转换是不安全的。**不安全转换（unsafe conversion）**指源类型的某些值无法被目标类型等值表示的情况。  

数值转换可分为三类安全级别：  
1. **值保留转换（value-preserving conversions）**：目标类型能精确表示源类型所有可能值的安全转换。  
例如`int`转`long`和`short`转`double`是安全转换：  
```cpp
int main()
{
    int n { 5 };
    long l = n; // 正确：生成long值5

    short s { 5 };
    double d = s; // 正确：生成double值5.0
    return 0;
}
```
编译器通常不会对隐式值保留转换发出警告。此类转换后的值可无损转回源类型：  
```cpp
int n = static_cast<int>(static_cast<long>(3)); // int 3转long再转回
char c = static_cast<char>(static_cast<double>('c')); // 'c'转double再转回
```

2. **重新解释型转换（reinterpretive conversions）**：转换后值可能改变但未丢失数据的不安全转换。有符号/无符号转换属于此类：  
```cpp
int n1 { 5 };
unsigned int u1 { n1 }; // 正确：转为无符号5（值保留）

int n2 { -5 };
unsigned int u2 { n2 }; // 错误：生成超出有符号int范围的大整数值
```
有符号负数转无符号将产生模数回绕（modulo wrap）。此类转换通常导致意外行为。  

> **相关课程**  
> 有符号/无符号转换规则详见[4.12 — 类型转换与static_cast简介](Chapter-4/lesson4.12-introduction-to-type-conversion-and-static_cast.md)。  

> **警告**  
> 尽管不安全，多数编译器默认禁用隐式有符号/无符号转换警告。建议特别注意此类转换。  

重新解释型转换可无损转回源类型：  
```cpp
int u = static_cast<int>(static_cast<unsigned int>(-5)); // -5转无符号再转回
```

> **进阶阅读**  
> C++20前无符号值超出有符号范围时为实现定义行为，C++20要求使用补码后该行为明确为重新解释型转换。  

3. **有损转换（lossy conversions）**：转换过程可能丢失数据的不安全转换：  
```cpp
int i = 3.5;   // 正确：转为int 3（值保留）
int j = 3.5;   // 数据丢失：转为int 3（丢失0.5）

float f = 1.2;        // 正确：转为float 1.2（值保留）
float g = 1.23456789; // 数据丢失：转为float 1.23457（精度丢失）
```
转换回源类型将产生不同值：  
```cpp
double d = static_cast<double>(static_cast<int>(3.5)); // 3.5转int再转回得3.0
double d2 = static_cast<double>(static_cast<float>(1.23456789)); // 转回得1.23457
```
编译器通常对隐式有损转换发出警告。  

> **注意**  
> 部分转换的安全性取决于平台。例如`int`转`double`在4字节int和8字节double系统中是安全的，但在8字节int系统中可能丢失数据。  

数值转换注意事项  
----------------  
* **溢出处理**：无符号值溢出明确定义，有符号值溢出是未定义行为  
* **整型转浮点**：值在目标范围内时有效，但可能丢失精度  
* **浮点转整型**：截断小数部分  
* **类型范围不匹配**：导致意外结果（如`int 30000`转`char`产生48）  

编译器通常会对危险转换发出警告（部分有符号/无符号转换除外）。  

[下一课 10.4 窄化转换、列表初始化与constexpr初始化器](Chapter-10/lesson10.4-narrowing-conversions-list-initialization-and-constexpr-initializers.md)  
[返回主页](/)  
[上一课 10.2 浮点数与整型的提升](Chapter-10/lesson10.2-floating-point-and-integral-promotion.md)