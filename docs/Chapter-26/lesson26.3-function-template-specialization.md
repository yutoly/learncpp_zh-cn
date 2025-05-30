26.3 — 函数模板特化
========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2016年12月3日，下午5:10（太平洋标准时间）  
2024年7月30日更新  

当为给定类型实例化函数模板时，编译器会复制模板函数并用变量声明中使用的实际类型替换模板类型参数。这意味着特定函数对于每个实例化类型都具有相同的实现细节（仅使用不同类型）。虽然大多数情况下这正是所需行为，但偶尔需要为特定数据类型实现略有不同的模板函数。  

使用非模板函数  
----------------  

考虑以下示例：  

```cpp
#include <iostream>

template <typename T>
void print(const T& t)
{
    std::cout << t << '\n';
}

int main()
{
    print(5);
    print(6.7);
    
    return 0;
}
```  

输出结果：  
```
5
6.7
```  

假设我们希望双精度浮点数（且仅双精度浮点数）以科学计数法输出。实现特定类型不同行为的一种方法是定义非模板函数：  

```cpp
#include <iostream>

template <typename T>
void print(const T& t)
{
    std::cout << t << '\n';
}

void print(double d)
{
    std::cout << std::scientific << d << '\n';
}

int main()
{
    print(5);
    print(6.7);
    
    return 0;
}
```  

当编译器解析`print(6.7)`时，会发现我们已定义`print(double)`，因此使用该函数而非从`print(const T&)`实例化版本。输出结果变为：  
```
5
6.700000e+000
```  

这种定义方式的优点是：非模板函数不需要与模板函数具有相同的签名。注意`print(const T&)`使用常量引用传递，而`print(double)`使用值传递。通常建议优先使用非模板函数。  

函数模板特化  
----------------  

另一种实现类似效果的方法是使用显式模板特化（explicit template specialization）。**显式模板特化**（常简称为**模板特化**）允许我们为特定类型或值显式定义模板的不同实现。当所有模板参数都被特化时，称为**全特化（full specialization）**；仅部分模板参数被特化时，称为**部分特化（partial specialization）**。  

为`T`为`double`类型创建`print<T>`的特化版本：  

```cpp
#include <iostream>

// 主模板必须首先声明
template <typename T>
void print(const T& t)
{
    std::cout << t << '\n';
}

// 主模板print<T>针对double类型的全特化
// 全特化不会隐式内联，若置于头文件需显式标记inline
template<>                          // 空模板参数声明
void print<double>(const double& d) // 特化为double类型
{
    std::cout << std::scientific << d << '\n'; 
}

int main()
{
    print(5);
    print(6.7);
    
    return 0;
}
```  

要特化模板，编译器必须首先看到主模板的声明。上例中的主模板是`print<T>(const T&)`。  

观察函数模板特化的结构：  
```cpp
template<>                          
void print<double>(const double& d)
```  

首先需要模板参数声明告知编译器正在处理模板相关操作。此处无需实际模板参数，故使用空尖括号。由于特化中没有模板参数，这属于全特化。  

`print<double>`表明正在为`double`类型特化主模板函数。特化的函数签名必须与主模板一致（仅将主模板中的`T`替换为`double`）。主模板使用常量引用传递，特化版本也必须使用`const double&`参数类型，不能改用值传递。此示例输出结果与前例相同。  

注意：若存在匹配的非模板函数和模板函数特化，非模板函数将优先调用。此外，全特化不会隐式内联，若置于头文件中需显式标记`inline`以避免ODR（单一定义规则）违规。  

> **警告**  
> 全特化不会隐式内联（部分特化会隐式内联）。若将全特化置于头文件，应标记为`inline`以防止多翻译单元包含时违反ODR。  

与普通函数类似，若希望特定函数调用引发编译错误，可以删除函数模板特化（使用`= delete`）。通常建议优先使用非模板函数而非函数模板特化。  

成员函数的模板特化？  
----------------  

考虑以下类模板：  

```cpp
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

int main()
{
    // 定义存储单元
    Storage i { 5 };
    Storage d { 6.7 };

    // 输出值
    i.print();
    d.print();
}
```  

输出结果：  
```
5
6.7
```  

若需要为`print()`函数创建针对双精度数的科学计数法版本，由于`print()`是成员函数，无法定义非成员函数。此时需要特化`Storage<double>::print()`，这属于类模板特化而非函数模板特化。具体实现将在下节课讲解。  

[下一课 26.4 类模板特化](Chapter-26/lesson26.4-class-template-specialization.md)  
[返回主页](/)  
[上一课 26.2 模板非类型参数](Chapter-26/lesson26.2-template-non-type-parameters.md)