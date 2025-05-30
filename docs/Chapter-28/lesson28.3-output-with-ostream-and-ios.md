28.3 — 使用ostream与ios进行输出  
===================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年3月12日，太平洋夏令时下午3:10  
2024年3月16日  

本章将探讨iostream输出类（ostream）的各个方面。  

**插入运算符**  

插入运算符（<<）用于将信息放入输出流。C++为所有内置数据类型预定义了插入操作，您还可以通过[重载插入运算符](93-overloading-the-io-operators/)为自定义类实现该功能。  

**格式化**  

修改格式选项有两种方式：标志（flags）和操纵器（manipulators）。**标志**可视为可开关的布尔变量，**操纵器**则是置于流中影响输入输出方式的对象。  

使用**setf()**函数并传入相应标志来开启选项。例如默认情况下C++不会在正数前显示+号，但通过std::ios::showpos标志可改变此行为：  

```cpp
std::cout.setf(std::ios::showpos); // 启用std::ios::showpos标志
std::cout << 27 << '\n';
```  

输出结果：  

```
+27
```  

使用按位或（|）运算符可同时启用多个标志：  

```cpp
std::cout.setf(std::ios::showpos | std::ios::uppercase); // 同时启用showpos和uppercase
std::cout << 1234567.89f << '\n';
```  

输出结果：  

```
+1.23457E+06
```  

使用**unsetf()**函数关闭标志：  

```cpp
std::cout.setf(std::ios::showpos);
std::cout << 27 << '\n';
std::cout.unsetf(std::ios::showpos);
std::cout << 28 << '\n';
```  

输出结果：  

```
+27
28
```  

使用setf()时需注意格式组（format group）问题。格式组是执行相似（有时互斥）格式化选项的标志集合。例如"basefield"组包含控制整数基数的"oct"、"dec"、"hex"标志。默认启用"dec"，因此直接设置hex会失效：  

```cpp
std::cout.setf(std::ios::hex);
std::cout << 27 << '\n'; // 输出仍为27
```  

解决方案一：手动关闭dec标志  

```cpp
std::cout.unsetf(std::ios::dec);
std::cout.setf(std::ios::hex);
std::cout << 27 << '\n'; // 输出1b
```  

解决方案二：使用双参数setf()  

```cpp
std::cout.setf(std::ios::hex, std::ios::basefield);
std::cout << 27 << '\n'; // 输出1b
```  

操纵器更为便捷，能自动处理标志状态：  

```cpp
std::cout << std::hex << 27 << '\n'; // 十六进制
std::cout << 28 << '\n'; // 保持十六进制
std::cout << std::dec << 29 << '\n'; // 恢复十进制
```  

输出结果：  

```
1b
1c
29
```  

**常用格式化工具**  

以下列出常用标志、操纵器和成员函数（标志位于std::ios，操纵器位于std命名空间，成员函数属于std::ostream）：  

| 分组       | 标志                   | 说明                     |
|------------|------------------------|--------------------------|
|            | std::ios::boolalpha    | 布尔值显示true/false     |

| 操纵器          | 说明                     |
|-----------------|--------------------------|
| std::boolalpha  | 布尔显示true/false       |
| std::noboolalpha| 布尔显示0/1（默认）      |

示例：  

```cpp
std::cout << true << ' ' << false << '\n';
std::cout << std::boolalpha << true << ' ' << false << '\n';
```  

输出：  

```
1 0
true false
```  

| 分组       | 标志                   | 说明                     |
|------------|------------------------|--------------------------|
|            | std::ios::showpos      | 正数前显示+号            |

| 操纵器          | 说明                     |
|-----------------|--------------------------|
| std::showpos    | 正数前显示+号            |
| std::noshowpos  | 取消显示+号（默认）      |

示例：  

```cpp
std::cout << std::showpos << 5 << '\n'; // +5
```  

| 分组       | 标志                   | 说明                     |
|------------|------------------------|--------------------------|
|            | std::ios::uppercase    | 使用大写字母             |

| 操纵器          | 说明                     |
|-----------------|--------------------------|
| std::uppercase  | 科学计数法用大写E        |
| std::nouppercase| 小写e（默认）            |

示例：  

```cpp
std::cout << 12345678.9 << '\n'; // 1.23457e+007
std::cout << std::uppercase << 12345678.9 << '\n'; // 1.23457E+007
```  

**精度、表示法与小数点**  

通过操纵器可控制浮点数的显示精度和格式：  

| 分组             | 标志                   | 说明                     |
|------------------|------------------------|--------------------------|
| std::ios::floatfield | std::ios::fixed      | 十进制表示法             |
| std::ios::floatfield | std::ios::scientific | 科学计数法               |
| std::ios::floatfield | （无）               | 自动选择表示法           |
| std::ios::floatfield | std::ios::showpoint  | 始终显示小数点及末尾零   |

| 操纵器          | 说明                     |
|-----------------|--------------------------|
| std::fixed      | 十进制表示               |
| std::scientific | 科学计数法               |
| std::setprecision(n) | 设置精度（需包含iomanip头文件） |

示例：  

```cpp
std::cout << std::fixed << std::setprecision(3) << 123.456 << '\n'; // 123.456
std::cout << std::scientific << std::setprecision(3) << 123.456 << '\n'; // 1.235e+02
```  

**宽度、填充字符与对齐**  

通过设置字段宽度控制输出对齐：  

| 分组             | 标志                   | 说明                     |
|------------------|------------------------|--------------------------|
| std::ios::adjustfield | std::ios::left      | 左对齐                   |
| std::ios::adjustfield | std::ios::right     | 右对齐（默认）           |
| std::ios::adjustfield | std::ios::internal  | 符号左对齐，数值右对齐   |

| 操纵器          | 说明                     |
|-----------------|--------------------------|
| std::setw(n)    | 设置字段宽度             |
| std::setfill(c) | 设置填充字符             |

示例：  

```cpp
std::cout << std::setw(10) << std::left << -12345 << '\n'; // -12345****
std::cout << std::setw(10) << std::internal << -12345 << '\n'; // -****12345
```  

注意：setw()仅影响下一次输出操作。  

ostream类和iostream库还包含其他输出功能，具体可参考标准库相关文档。  

[下一课 28.4 字符串流类](Chapter-28/lesson28.4-stream-classes-for-strings.md)  
[返回主页](/)  
[上一课 28.2 使用istream输入](Chapter-28/lesson28.2-input-with-istream.md)