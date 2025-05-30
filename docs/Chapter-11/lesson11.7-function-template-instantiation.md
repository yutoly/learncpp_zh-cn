11.7 — 函数模板实例化  
=======================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2021年6月17日下午5:50 PDT  
2024年8月21日更新  

前文提要  
----------------  

在课程[11.6 — 函数模板](Chapter-11/lesson11.6-function-templates.md)中，我们将普通`max()`函数转换为`max<T>`函数模板：  
```cpp
template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}
```  

本节重点讲解函数模板的使用方法。  

使用函数模板  
----------------  

函数模板并非实际函数——其代码不会直接编译或执行。函数模板的核心作用是：生成可编译执行的函数。  

调用`max<T>`函数模板的语法如下：  
```cpp
max<实际类型>(参数1, 参数2); // 实际类型如int或double
```  

该语法与普通函数调用的主要区别在于尖括号内的类型指定（称为**模板实参**），用于替换模板类型`T`。  

示例解析：  
```cpp
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n'; // 实例化并调用max<int>(int, int)
    return 0;
}
```  

当编译器遇到`max<int>(1, 2)`调用时，发现`max<int>(int, int)`函数不存在，于是隐式使用`max<T>`模板生成该函数。  

**函数模板实例化**（简称实例化）指从函数模板生成具体类型函数的过程。通过函数调用触发的实例化称为**隐式实例化**。从模板生成的函数称为**特化**（specialization），通常称为**函数实例**（function instance），对应的模板称为**主模板**（primary template）。函数实例与普通函数无异。  

术语说明  
----------------  

"特化"更多指**显式特化**（通过[26.3 — 函数模板特化](Chapter-26/lesson26.3-function-template-specialization.md)课程学习）。  

实例化过程本质是编译器克隆主模板并用指定类型（如`int`）替换模板类型`T`。因此`max<int>(1, 2)`生成的函数实例类似于：  
```cpp
template<> // 暂时忽略此行
int max<int>(int x, int y) // 生成的max<int>(int, int)
{
    return (x < y) ? y : x;
}
```  

完整编译后代码示例：  
```cpp
#include <iostream>

template <typename T> 
T max(T x, T y); // 函数模板声明

template<> // int特化版本
int max<int>(int x, int y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n';
    return 0;
}
```  

注意：  
- 每个翻译单元中，函数模板仅在首次调用时实例化  
- 未调用的函数模板不会实例化  

多类型实例化示例：  
```cpp
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n';    // 实例化int版本
    std::cout << max<int>(4, 3) << '\n';    // 调用已实例化的int版本
    std::cout << max<double>(1, 2) << '\n'; // 实例化double版本
    return 0;
}
```  

编译后生成两个特化版本：  
```cpp
template<> int max<int>(int x, int y) { /*...*/ }
template<> double max<double>(double x, double y) { /*...*/ }
```  

注意`max<double>`调用时int参数隐式转换为double。  

模板实参推导  
----------------  

当模板实参与函数参数类型匹配时，可使用**模板实参推导**，编译器根据实参类型自动推导模板类型。例如：  
```cpp
std::cout << max<>(1, 2) << '\n'; // 推导为max<int>
std::cout << max(1, 2) << '\n';   // 普通函数调用语法
```  

语法差异：  
- `max<>`仅考虑模板函数  
- `max()`优先考虑非模板函数  

示例说明：  
```cpp
#include <iostream>

template <typename T>
T max(T x, T y) { /*...*/ }

int max(int x, int y) { /*...*/ }

int main()
{
    max<int>(1, 2);  // 调用模板版本
    max<>(1, 2);     // 推导调用模板版本
    max(1, 2);       // 调用非模板版本
    return 0;
}
```  

最佳实践  
----------------  

优先使用普通函数调用语法（除非需要强制使用模板版本）。原因：  
1. 语法简洁  
2. 较少出现模板与非模板版本冲突  
3. 非模板版本通常更优化  

示例：  
```cpp
#include <iostream>

template <typename T>
void print(T x) { /* 通用实现 */ }

void print(bool x) { /* 布尔特化实现 */ }

int main()
{
    print(true); // 调用非模板版本
    return 0;
}
```  

含非模板参数的函数模板  
----------------  

函数模板可同时包含模板参数和非模板参数：  
```cpp
template <typename T>
int someFcn(T, double) { return 5; }

int main()
{
    someFcn(1, 3.4);    // T=int
    someFcn(1.2, 3.4);  // T=double
    return 0;
}
```  

实例化可能失败的情况  
----------------  

语法正确但语义错误的实例化会导致编译错误：  
```cpp
template <typename T>
T addOne(T x) { return x + 1; }

int main()
{
    addOne(std::string("Hello")); // 错误：字符串+1无效
    return 0;
}
```  

警告  
----------------  

编译器仅检查语法有效性，需开发者自行确保语义正确。  

高级技巧  
----------------  

通过显式特化和`= delete`禁用特定类型的实例化：  
```cpp
template <>
const char* addOne(const char*) = delete; // 禁用C风格字符串版本

int main()
{
    addOne("Hello"); // 编译错误
    return 0;
}
```  

非模板参数的默认实参  
----------------  

函数模板的非模板参数可设默认值：  
```cpp
template <typename T>
void print(T val, int times=1) { /*...*/ }

int main()
{
    print(5);    // 打印1次
    print('a',3);// 打印3次
    return 0;
}
```  

含可变静态局部变量的注意事项  
----------------  

不同实例化的模板函数拥有独立的静态局部变量：  
```cpp
template <typename T>
void printID(T val) {
    static int id = 0;
    std::cout << ++id << val;
}

int main()
{
    printID(1);    // 输出1
    printID(2);    // 输出2
    printID(1.1);  // 输出1（不同实例）
    return 0;
}
```  

泛型编程  
----------------  

模板类型又称**泛型类型**，模板编程称为**泛型编程**，其优势在于：  
- 聚焦算法逻辑而非具体类型  
- 减少代码维护成本  

优缺点分析  
----------------  

优点：  
- 减少重复代码  
- 提升类型安全性  

缺点：  
- 代码膨胀（每个类型生成独立实例）  
- 编译时间增加  
- 错误信息复杂  

最佳实践建议  
----------------  

优先编写普通函数，需要类型灵活性时转换为模板。  

[下一课：11.8 — 含多模板类型的函数模板](Chapter-11/lesson11.8-function-templates-with-multiple-template-types.md)  
[返回主页](/)  
[上一课：11.6 — 函数模板](Chapter-11/lesson11.6-function-templates.md)