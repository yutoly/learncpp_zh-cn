10.7 — 类型别名（typedefs）与类型别名  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月19日（首次发布）  
2024年2月11日（更新）  

类型别名（Type aliases）  
----------------  

在C++中，**using**关键字可为现有数据类型创建别名。创建类型别名的语法为：`using`关键字后接别名名称，再跟等号和原数据类型。例如：  
```cpp
using Distance = double; // 定义Distance作为double的别名
```  

定义后，类型别名可在任何需要类型的地方使用。例如：  
```cpp
Distance milesToDestination{ 3.4 }; // 定义double类型变量
```  

编译器遇到类型别名时，会替换为原始类型。示例程序：  
```cpp
#include <iostream>

int main()
{
    using Distance = double; // 定义Distance为double的别名

    Distance milesToDestination{ 3.4 }; // 定义double类型变量

    std::cout << milesToDestination << '\n'; // 输出double值

    return 0;
}
```  

输出：  
```
3.4
```  

程序中，`Distance`被定义为`double`的别名。变量`milesToDestination`实际编译为`double`类型。  

> **进阶阅读**  
> 类型别名可模板化，详见课程[13.14 — 类模板参数推导（CTAD）与推导指南](Chapter-13/lesson13.14-class-template-argument-deduction-ctad-and-deduction-guides.md)。  

类型别名的命名规范  
----------------  

历史上类型别名命名缺乏统一标准，常见三种形式：  
1. 以"_t"结尾（来自C语言标准库，如`size_t`）  
2. 以"_type"结尾（如`std::string::size_type`）  
3. 无后缀  

现代C++推荐使用首字母大写的无后缀命名，便于区分类型与变量/函数：  
```cpp
void printDistance(Distance distance); // Distance为类型，distance为参数
```  

> **最佳实践**  
> 类型别名使用首字母大写且不加后缀（除非有特殊需求）。  

类型别名非独立类型  
----------------  

类型别名不创建新类型，仅作为现有类型的同义词。以下示例虽语法正确但语义错误：  
```cpp
int main()
{
    using Miles = long;  // Miles是long的别名
    using Speed = long;  // Speed是long的别名

    Miles distance{ 5 }; // 实际类型为long
    Speed mhz{ 3200 };   // 实际类型为long

    distance = mhz;      // 语义错误但语法合法
    return 0;
}
```  

编译器将`Miles`和`Speed`均视为`long`，故不会报错。因此类型别名不具备**类型安全**性。  

> **扩展知识**  
> 某些语言支持**强类型别名**（strong typedef），C++20未直接支持，但第三方库可实现类似功能。枚举类（见[13.6 — 作用域枚举](Chapter-13/lesson13.6-scoped-enumerations-enum-classes.md)）有类似特性。  

类型别名的作用域  
----------------  

类型别名的作用域规则与变量相同：  
- 块内定义的别名具有块作用域  
- 全局命名空间定义的别名具有全局作用域  

跨文件使用时，可将别名定义在头文件中：  
mytypes.h:  
```cpp
#ifndef MYTYPES_H
#define MYTYPES_H

    using Miles = long;
    using Speed = long;

#endif
```  

Typedefs（类型定义别名）  
----------------  

**typedef**是创建类型别名的传统方式，现代C++推荐使用`using`：  
```cpp
typedef long Miles;      // 传统方式
using Miles = long;      // 现代方式
```  

typedef的缺点：  
1. 易混淆声明顺序  
2. 复杂类型声明可读性差  
3. 名称暗示定义新类型（实际仍是别名）  

> **最佳实践**  
> 优先使用类型别名而非typedef。  

何时使用类型别名  
----------------  

### 跨平台编码  
通过别名实现平台无关类型：  
```cpp
#ifdef INT_2_BYTES
using int8_t = char;
using int16_t = int;
#else
using int8_t = char;
using int16_t = short;
#endif
```  

标准库的`size_t`和固定宽度整数类型（如`std::int32_t`）均为类型别名。  

### 简化复杂类型  
减少冗长类型书写：  
```cpp
using VectPairSI = std::vector<std::pair<std::string, int>>;

bool hasDuplicates(VectPairSI pairlist) { /*...*/ } // 使用别名
```  

### 增强代码可读性  
明确返回值含义：  
```cpp
using TestScore = int;
TestScore gradeTest(); // 比int更清晰的返回类型
```  

### 便于维护  
批量修改类型：  
```cpp
using StudentId = short; // 修改为long时只需改此处
```  

注意事项与总结  
----------------  

类型别名可能引入理解成本，不当使用会降低代码清晰度。应权衡利弊，在提升可读性或维护性时使用。  

> **最佳实践**  
> 在显著提升代码可读性或维护性时审慎使用类型别名。  

测验答案  
----------------  

**问题1**  
将函数原型`int printData();`的返回类型改为别名`PrintError`：  
```cpp
using PrintError = int;
PrintError printData();
```  

[下一课 10.8 — auto关键字类型推导](Chapter-10/lesson10.8-type-deduction-for-objects-using-the-auto-keyword.md)  
[返回主页](/)  
[上一课 10.6 — 显式类型转换与static_cast](Chapter-10/lesson10.6-explicit-type-conversion-casting-and-static-cast.md)