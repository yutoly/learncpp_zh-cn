7.7 — 外部链接与变量前向声明  
=========================================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月11日（首次发布于2020年1月3日）  

在上一课（[7.6 — 内部链接](Chapter-7/lesson7.6-internal-linkage.md)）中，我们讨论了`内部链接（internal linkage）`如何将标识符的使用限制在单个文件内。本课将探讨`外部链接（external linkage）`的概念。  

具有**外部链接（external linkage）**的标识符可以从其定义所在文件和其他代码文件（通过前向声明）中访问和使用。从这个意义上说，具有外部链接的标识符是真正"全局"的，因为它们可以在程序任何地方使用！  

> **关键洞察**  
> 具有外部链接的标识符对链接器可见。这使得链接器能够：  
> * 将翻译单元（translation unit）中使用的标识符与其他翻译单元中的定义相连接  
> * 对inline标识符进行去重处理，保留一个规范定义（详见[7.9 — inline函数与变量](Chapter-7/lesson7.9-inline-functions-and-variables.md)）  

函数的默认外部链接  
----------------  

在课程[2.8 — 多文件程序](Chapter-2/lesson2.8-programs-with-multiple-code-files.md)中，您已了解如何从其他文件调用函数。这是因为函数默认具有外部链接。  

要调用其他文件中定义的函数，必须在调用文件中放置该函数的`前向声明（forward declaration）`。前向声明告知编译器函数的存在，链接器则将函数调用与具体定义相连接。  

示例：  
a.cpp：  
```cpp
#include <iostream>

void sayHi() // 该函数具有外部链接，其他文件可见
{
    std::cout << "Hi!\n";
}
```

main.cpp：  
```cpp
void sayHi(); // 函数前向声明，使本文件可访问sayHi

int main()
{
    sayHi(); // 调用其他文件定义的函数，链接器将连接至定义
    return 0;
}
```  

程序输出：  
```
Hi!
```  

此例中，`main.cpp`中的`sayHi()`前向声明允许访问`a.cpp`中的定义。前向声明满足编译器要求，链接器完成函数调用与定义的连接。若`sayHi()`具有内部链接，链接器将无法连接并产生错误。  

具有外部链接的全局变量  
----------------  

具有外部链接的全局变量有时被称为**外部变量（external variables）**。要使全局变量具有外部链接（从而可被其他文件访问），可使用`extern`关键字：  
```cpp
int g_x { 2 };          // 非常量全局变量默认外部链接（无需extern）

extern const int g_y { 3 };    // const全局变量可用extern定义外部链接
extern constexpr int g_z { 3 }; // constexpr全局变量可用extern定义外部链接（但用处有限，见下节警告）
```  

非常量全局变量默认具有外部链接，因此无需额外标记`extern`。  

通过extern进行变量前向声明  
----------------  

要使用其他文件定义的外部全局变量，必须在调用文件中使用`extern`关键字进行变量前向声明（不带初始值）。  

示例：  
main.cpp：  
```cpp
#include <iostream>

extern int g_x;       // extern声明在其他位置定义的g_x
extern const int g_y; // extern声明在其他位置定义的const g_y

int main()
{
    std::cout << g_x << ' ' << g_y << '\n'; // 输出2 3
    return 0;
}
```  

变量定义（a.cpp）：  
```cpp
// 全局变量定义
int g_x { 2 };              // 非常量全局变量默认外部链接
extern const int g_y { 3 }; // extern赋予g_y外部链接
```  

此例中，`a.cpp`和`main.cpp`引用同一全局变量`g_x`。尽管`g_x`在`a.cpp`中定义，但通过前向声明可在`main.cpp`中使用其值。  

> **注意**  
> `extern`关键字在不同上下文中有不同含义：  
> * 赋予变量外部链接  
> * 进行外部变量前向声明  
> 完整总结见课程[7.12 — 作用域、持续期与链接总结](Chapter-7/lesson7.12-scope-duration-and-linkage-summary.md)。  

> **警告**  
> 若定义未初始化的非常量全局变量，不要使用`extern`，否则C++会认为这是变量前向声明。  

> **关于constexpr的警告**  
> 虽然constexpr变量可通过`extern`获得外部链接，但不能前向声明为constexpr。因为编译器需在编译时知道其值。若该值在其他文件定义，编译器将无法获取。但可将constexpr变量前向声明为const（视为运行时const），不过实用性有限。  

> **注意**  
> 函数前向声明无需`extern`——编译器通过是否提供函数体区分定义与声明。变量前向声明必须使用`extern`以区分未初始化定义与前向声明：  
> ```cpp
> // 非常量
> int g_x;        // 变量定义（无初始值）
> int g_x { 1 };  // 变量定义（带初始值）
> extern int g_x; // 前向声明（无初始值）
> 
> // 常量
> extern const int g_y { 1 }; // 变量定义（const必须初始化）
> extern const int g_y;       // 前向声明（无初始值）
> ```  

避免对带初始化的非常量全局变量使用extern  
----------------  

以下两行语义等价：  
```cpp
int g_x { 1 };        // 默认extern
extern int g_x { 1 }; // 显式extern（可能引发编译器警告）
```  

编译器可能对后者发出警告（尽管语法有效）。按惯例，`extern`用于非常量变量前向声明。添加初始值会使其成为定义，导致编译器警告。  

> **最佳实践**  
> * 仅将`extern`用于全局变量前向声明或const全局变量定义  
> * 不要对非常量全局变量定义使用`extern`（它们隐式具有外部链接）  

快速总结  
----------------  
```cpp
// 全局变量前向声明（extern不带初始值）：
extern int g_y;                 // 非常量全局变量前向声明
extern const int g_y;           // const全局变量前向声明
extern constexpr int g_y;       // 非法：constexpr变量不可前向声明

// 外部全局变量定义（无extern）：
int g_x;                        // 定义未初始化外部全局变量（默认零初始化）
int g_x { 1 };                  // 定义带初始值外部全局变量

// 外部const全局变量定义（extern带初始值）：
extern const int g_x { 2 };     // 定义带初始值const外部全局变量
extern constexpr int g_x { 3 }; // 定义带初始值constexpr外部全局变量
```  

完整总结见课程[7.12 — 作用域、持续期与链接总结](Chapter-7/lesson7.12-scope-duration-and-linkage-summary.md)。  

测验时间  
----------------  

**问题1**  
变量的作用域、持续期和链接有何区别？全局变量具有何种作用域、持续期和链接？  
  
<details><summary>答案</summary>作用域决定变量可访问范围，持续期决定变量创建与销毁时机，链接决定变量能否导出到其他文件。<br>全局变量具有文件作用域（从声明处到文件末尾可访问）、静态持续期（程序启动时创建，结束时销毁），可通过static/internal或extern/external指定链接类型。</details>  

[下一课 7.8 为什么（非常量）全局变量有害](Chapter-7/lesson7.8-why-non-const-global-variables-are-evil.md)  
[返回主页](/)  
[上一课 7.6 内部链接](Chapter-7/lesson7.6-internal-linkage.md)