12.x — 第12章 小结与测验  
===============================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月4日（首次发布于2022年4月8日）  

快速回顾  
----------------  

**复合数据类型（compound data type）**（也称**组合数据类型**）是由基础数据类型（或其他复合数据类型）构建而成的数据类型。  

表达式的**值类别（value category）**决定了表达式解析结果是值、函数还是某种对象。  

**左值（lvalue）**是解析为具有身份标识的函数或对象的表达式。具有**身份标识（identity）**的对象或函数拥有标识符或可识别的内存地址。左值分为两种子类型：**可修改左值（modifiable lvalue）**是可以被修改的左值；**不可修改左值（non-modifiable lvalue）**是其值不可被修改的左值（通常因为它们被声明为const或constexpr）。  

**右值（rvalue）**是不属于左值的表达式。包括字面量（字符串字面量除外）和函数或运算符的返回值（按值返回时）。  

**引用（reference）**是现有对象的别名。引用定义后，对其进行的任何操作都会作用于被引用对象。C++包含两种引用类型：左值引用和右值引用。**左值引用（lvalue reference）**（通常简称**引用**）作为现有左值（如变量）的别名。**左值引用变量（lvalue reference variable）**是指向左值（通常是其他变量）的引用变量。  

当引用被初始化为某个对象（或函数）时，我们称其**绑定（bound）**到该对象（或函数）。被引用的对象（或函数）有时称为**引用对象（referent）**。  

左值引用不能绑定到不可修改左值或右值（否则可能通过引用修改这些值，违反其const属性）。因此左值引用有时被称为**非const左值引用（lvalue references to non-const）**（简称为**非const引用**）。  

在C++中，引用初始化后不能**重新绑定（reseated）**，即不能更改为引用其他对象。  

当被引用对象在引用之前被销毁时，引用将指向已不存在的对象，称为**悬垂引用（dangling reference）**。访问悬垂引用会导致未定义行为。  

通过在声明左值引用时使用`const`关键字，可以令左值引用将引用对象视为常量。这种引用称为**const值左值引用（lvalue reference to a const value）**（也称**const引用**）。const引用可以绑定到可修改左值、不可修改左值和右值。  

**临时对象（temporary object）**（有时称**无名对象**或**匿名对象**）是在单个表达式中为临时使用创建（随后销毁）的对象。  

使用**引用传递（pass by reference）**时，我们将函数参数声明为引用（或const引用）而非普通变量。调用函数时，每个引用参数绑定到对应实参。由于引用作为实参的别名，不会创建实参的副本。  

**取址运算符（address-of operator）**（&）返回其操作数的内存地址。**解引用运算符（dereference operator）**（*）将给定内存地址的值作为左值返回。  

**指针（pointer）**是持有内存地址（通常是其他变量的地址）的对象。指针允许我们存储其他对象的地址以供后续使用。与普通变量类似，指针默认不初始化。未初始化的指针称为**野指针（wild pointer）**。**悬垂指针（dangling pointer）**指向已失效对象（例如被销毁的对象）。  

除内存地址外，指针还可以持有另一个特殊值：空值。**空值（null value）**（简称**null**）表示无值的特殊值。持有空值的指针称为**空指针（null pointer）**。关键字**nullptr**表示空指针字面量，可用于显式初始化指针为空值。  

指针应持有有效对象的地址或设为`nullptr`。这样我们只需检测指针是否为空，即可假定所有非空指针都是有效的。  

**指向const值的指针（pointer to a const value）**（简称**const值指针**）是（非const）指针，指向常量值。  

**const指针（const pointer）**是其地址在初始化后不可更改的指针。  

**指向const值的const指针（const pointer to a const value）**既不可更改地址，也不可通过指针修改所指向的值。  

使用**地址传递（pass by address）**时，调用者提供对象的地址（通过指针）而非对象本身。该指针（持有对象地址）被复制到被调用函数的指针参数中（现在也持有该对象地址）。函数可解引用指针来访问传入地址的对象。  

**引用返回（return by reference）**返回绑定到被返回对象的引用，避免复制返回值。使用引用返回时需注意：程序员必须确保返回的引用对象在函数返回后仍然存在。否则引用将悬垂（指向已销毁对象），使用该引用会导致未定义行为。如果参数通过引用传入函数，则可以安全地通过引用返回该参数。  

若函数返回引用，且该引用用于初始化或赋值给非引用变量，返回值将被复制（如同按值返回）。  

使用`auto`关键字进行变量类型推导时，会去除推导类型中的引用和顶层const限定符。如有需要，可在变量声明中重新应用这些限定符。  

**地址返回（return by address）**的工作原理与引用返回几乎相同，区别在于返回的是对象的指针而非引用。  

测验时间  
----------------  

**问题1**  
对以下运算符<<右侧的表达式，判断其是左值还是右值：  

a)  
```cpp
std::cout << 5;
```  
  
<details><summary>答案</summary>字面量是右值，因此`5`是右值</details>  

b)  
```cpp
int x{5}; 
std::cout << x;
```  
  
<details><summary>答案</summary>表达式`x`标识变量`x`，因此是左值</details>  

c)  
```cpp
int x{5}; 
std::cout << x + 1;
```  
  
<details><summary>答案</summary>表达式`x + 1`计算临时值，因此是右值</details>  

d)  
```cpp
int foo() { return 5; } 
std::cout << foo();
```  
  
<details><summary>答案</summary>函数返回值（按值返回时）是右值</details>  

e)  
```cpp
int& max(int &x, int &y) { return x > y ? x : y; } 
int x{5}; 
int y{6}; 
std::cout << max(x, y);
```  
  
<details><summary>答案</summary>max()返回左值引用，属于左值</details>  

**问题2**  
以下程序输出结果是什么？  
```cpp
#include <iostream>

int main()
{
    int x{4};
    int y{6};

    int& ref{x};
    ++ref;
    ref = y;
    ++ref;

    std::cout << x << ' ' << y;

    return 0;
}
```  
  
<details><summary>答案</summary>输出`7 6`。注释说明：引用不能重新绑定，`ref = y`等价于`x = y`</details>  

**问题3**  
列举两个优先使用const引用传递参数而非非const引用的原因。  
  
<details><summary>答案</summary>1.避免意外修改实参；2.const引用可接受可修改左值、不可修改左值和右值</details>  

**问题4**  
const指针与指向const的指针有何区别？  
  
<details><summary>答案</summary>const指针地址不可变，指向const的指针不可通过指针修改值但可重定向</details>  

**问题5**  
编写名为`sort2`的函数，对两个int变量进行排序。提示：使用`std::swap()`。  
  
<details><summary>答案</summary>  
```cpp
#include <algorithm>
void sort2(int& lesser, int& greater)
{
    if (lesser > greater)
        std::swap(lesser, greater);
}
```  
</details>  

[下一课 13.1 程序定义类型简介](Chapter-13/lesson13.1-introduction-to-program-defined-user-defined-types.md)  
[返回主页](/)  
[上一课 12.15 std::optional](Chapter-12/lesson12.15-stdoptional.md)