11.5 — 默认参数  
=========================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年8月6日，下午4:38（太平洋夏令时）  
2024年11月10日  

**默认参数（default argument）** 是为函数形参提供的默认值。例如：  
```
void print(int x, int y=10) // 10 是默认参数
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}
```  
函数调用时，调用方可为含默认参数的形参选择性提供实参。若提供实参，则使用调用时的实参值；若未提供，则使用默认参数值。  

考虑以下程序：  
```
#include <iostream>

void print(int x, int y=4) // 4 是默认参数
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}

int main()
{
    print(1, 2); // y 使用用户提供的实参 2
    print(3);    // y 使用默认参数 4，等效于 print(3, 4)

    return 0;
}
```  
程序输出：  
```
x: 1
y: 2
x: 3
y: 4
```  
首次调用为两个形参都提供了显式实参，故使用实参值。第二次调用省略了第二个实参，因此使用默认值 `4`。  

注意：必须使用等号指定默认参数。圆括号或花括号初始化无效：  
```
void foo(int x = 5);   // 正确
void goo(int x ( 5 )); // 编译错误
void boo(int x { 5 }); // 编译错误
```  
值得注意的是，编译器在调用处处理默认参数。上例中，当编译器解析 `print(3)` 时，会将其重写为 `print(3, 4)` 以保证实参与形参数量匹配。重写后的函数调用按常规流程执行。  

> **关键洞察**  
> 默认参数由编译器在函数调用处插入。  

默认参数在 C++ 中广泛使用，您将在后续课程及代码中频繁接触。  

### 何时使用默认参数  
当函数需要具有合理默认值、但允许调用方按需覆盖时，默认参数是理想选择。例如：  
```
int rollDie(int sides=6);                 // 掷骰子
void openLogFile(std::string filename="default.log"); // 打开日志
```  

> **作者注**  
> 由于用户可选择提供实参或使用默认值，含默认值的形参有时称为**可选参数（optional parameter）**。但该术语也用于指代其他类型参数（如地址传递参数或使用 `std::optional` 的参数），故建议避免此称呼。  

默认参数在向现有函数添加新形参时尤为实用。若添加无默认参数的新形参，将破坏所有现有函数调用（因未提供该形参实参），导致大量调用代码需更新（若无法控制调用代码则不可行）。而添加含默认参数的新形参时，现有调用仍有效（使用默认值），同时允许新调用按需指定显式实参。  

### 多重默认参数  
函数可含多个带默认参数的形参：  
```
#include <iostream>

void print(int x=10, int y=20, int z=30)
{
    std::cout << "值: " << x << " " << y << " " << z << '\n';
}

int main()
{
    print(1, 2, 3); // 全显式实参
    print(1, 2);    // 最右侧形参使用默认值
    print(1);       // 右侧两个形参使用默认值
    print();        // 全使用默认值

    return 0;
}
```  
输出：  
```
值: 1 2 3
值: 1 2 30
值: 1 20 30
值: 10 20 30
```  
截至 C++23，C++ 不支持 `print(,,3)` 这类语法（即对 `x` 和 `y` 使用默认参数，仅显式指定 `z`）。这导致三大限制：  

1. 函数调用中，显式实参必须位于最左侧（含默认参数的形参不可跳过）。  
   例如：  
```
void print(std::string_view sv="Hello", double d=10.0);

int main()
{
    print();           // 正确：两个参数均使用默认值
    print("Macaroni"); // 正确：d 默认为 10.0
    print(20.0);       // 错误：与函数不匹配（无法跳过 sv 的实参）
    return 0;
}
```  

2. 若某形参有默认参数，其右侧所有后续形参也必须有默认参数。  
   以下代码非法：  
```
void print(int x=10, int y); // 非法
```  
> **规则**  
> 若形参有默认参数，其右侧所有后续形参也必须有默认参数。  

3. 若多个形参含默认参数，最左侧形参应最可能被用户显式设置。  

### 默认参数不可重复声明且需先声明后使用  
默认参数在翻译单元内声明后不可重复声明。对于含前向声明和定义的函数，默认参数仅可声明于前向声明**或**定义中，不可两者同时声明。  
```
#include <iostream>

void print(int x, int y=4); // 前向声明

void print(int x, int y=4)  // 编译错误：默认参数重定义
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}
```  
默认参数必须在翻译单元中先声明后使用：  
```
#include <iostream>

void print(int x, int y); // 前向声明，无默认参数

int main()
{
    print(3); // 编译错误：y 的默认参数尚未定义
    return 0;    
}

void print(int x, int y=4) // 定义处声明默认参数
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}
```  
最佳实践是将默认参数置于前向声明而非函数定义中，因前向声明更可能被其他文件包含（尤其在头文件中）：  
*foo.h*：  
```
#ifndef FOO_H
#define FOO_H
void print(int x, int y=4); // 前向声明含默认参数
#endif
```  
*main.cpp*：  
```
#include "foo.h"
#include <iostream>

void print(int x, int y) // 定义不含默认参数
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}

int main()
{
    print(5); // 正确：使用默认参数
    return 0;
}
```  
上例中，因 *main.cpp* 包含含默认参数前向声明的 *foo.h*，故可正常使用默认参数。  

> **最佳实践**  
> 若函数有前向声明（尤其在头文件中），将默认参数置于此处；否则置于函数定义中。  

### 默认参数与函数重载  
含默认参数的函数可被重载。例如：  
```
#include <iostream>
#include <string_view>

void print(std::string_view s) // 重载版本1
{
    std::cout << s << '\n';
}

void print(char c = ' ') // 重载版本2
{
    std::cout << c << '\n';
}

int main()
{
    print("Hello, world"); // 解析为 print(std::string_view)
    print('a');            // 解析为 print(char)
    print();               // 解析为 print(char)（等效 print(' ')）
    return 0;
}
```  
`print()` 实际调用 `print(char)`，效果等同于显式调用 `print(' ')`。  

考虑以下情况：  
```
void print(int x);                  // 签名 print(int)
void print(int x, int y = 10);      // 签名 print(int, int)
void print(int x, double y = 20.5); // 签名 print(int, double) 
```  
默认值非函数签名组成部分，故这些声明属于合法重载。  

> **相关内容**  
> 函数重载解析详见课程 [11.2 — 函数重载解析](Chapter-11/lesson11.2-function-overload-differentiation.md)。  

### 默认参数可能导致歧义匹配  
默认参数易引发歧义函数调用：  
```
void foo(int x = 0)    {}
void foo(double d = 0.0) {}

int main()
{
    foo(); // 歧义函数调用
    return 0;
}
```  
此例中，编译器无法判断 `foo()` 应解析为 `foo(0)` 还是 `foo(0.0)`。  

稍复杂的例子：  
```
void print(int x);                  // 签名 print(int)
void print(int x, int y = 10);      // 签名 print(int, int)
void print(int x, double y = 20.5); // 签名 print(int, double) 

int main()
{
    print(1, 2);   // 解析为 print(int, int)
    print(1, 2.5); // 解析为 print(int, double) 
    print(1);      // 歧义函数调用
    return 0;
}
```  
对于 `print(1)`，编译器无法确定应解析为 `print(int)`、`print(int, int)` 或 `print(int, double)`。  

若需调用 `print(int, int)` 或 `print(int, double)`，可显式指定第二参数。但若需调用 `print(int)`，则无直接实现方式。  

### 默认参数不适用于通过函数指针调用的函数（高级主题）  
此机制详见课程 [20.1 — 函数指针](Chapter-20/lesson20.1-function-pointers.md)。因默认参数在此调用方式中不被考虑，故可作为规避默认参数所致歧义的解决方案。  

[下一课 11.6 函数模板](Chapter-11/lesson11.6-function-templates.md)  
[返回主页](/)  
[上一课 11.4 删除函数](Chapter-11/lesson11.4-deleting-functions.md)