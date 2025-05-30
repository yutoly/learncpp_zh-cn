11.x — 第11章总结与测验  
===================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年9月28日（2023年12月28日首次发布）  

本章回顾  
----------------  

**函数重载（function overloading）**允许我们创建多个同名函数，只要每个同名函数的参数类型集合不同（或可通过其他方式区分）。这样的函数称为**重载函数（overloaded function）**或简称**重载（overload）**。返回类型不参与函数区分。  

解析重载函数时，若找不到精确匹配，编译器会优先选择通过数值提升（numeric promotion）匹配的重载函数而非需要数值转换（numeric conversion）的版本。当调用重载函数时，编译器会根据函数调用使用的参数匹配最合适的重载版本，这个过程称为**重载解析（overload resolution）**。  

当编译器发现两个或多个重载函数都能匹配函数调用且无法确定最优选择时，会产生**歧义匹配（ambiguous match）**。  

**默认参数（default argument）**是为函数参数提供的默认值。带默认参数的参数必须始终位于参数列表最右端，且在解析重载函数时不参与区分。  

**函数模板（function template）**允许我们创建类似函数的定义，作为生成相关函数的模板。在函数模板中，我们使用**类型模板参数（type template parameter）**作为后续指定类型的占位符。告知编译器正在定义模板并声明模板类型的语法称为**模板参数声明（template parameter declaration）**。  

从函数模板（带模板类型）创建具体类型函数的过程称为**函数模板实例化（function template instantiation）**，简称**实例化（instantiation）**。当因函数调用触发此过程时，称为**隐式实例化（implicit instantiation）**。实例化后的函数称为**函数实例（function instance）**或简称**实例（instance）**，有时也称**模板函数（template function）**。  

**模板参数推导（template argument deduction）**允许编译器从函数调用参数推导出用于实例化函数的具体类型。模板参数推导不执行类型转换。  

模板类型有时称为**泛型类型（generic type）**，使用模板的编程方式称为**泛型编程（generic programming）**。  

在C++20中，当普通函数的参数类型使用`auto`关键字时，编译器会自动将函数转换为函数模板，每个`auto`参数成为独立的模板类型参数。这种创建函数模板的方法称为**缩写函数模板（abbreviated function template）**。  

**非类型模板参数（non-type template parameter）**是具有固定类型的模板参数，作为传入的`constexpr`值的占位符。  

测验时间  
----------------  

**问题1**  
1a) 以下程序输出结果是什么？为什么？  

```cpp
#include <iostream>

void print(int x)
{
    std::cout << "int " << x << '\n';
}

void print(double x)
{
    std::cout << "double " << x << '\n';
}

int main()
{
    short s { 5 };
    print(s);

    return 0;
}
```  

  
<details><summary>答案</summary>输出为`int 5`。将`short`转为`int`是数值提升，而转为`double`是数值转换。编译器优先选择数值提升的版本。</details>  

1b) 以下代码为何无法编译？  

```cpp
#include <iostream>

void print()
{
    std::cout << "void\n";
}

void print(int x=0)
{
    std::cout << "int " << x << '\n';
}

void print(double x)
{
    std::cout << "double " << x << '\n';
}

int main()
{
    print(5.0f);
    print();

    return 0;
}
```  

  
<details><summary>答案</summary>带默认参数的函数在重载解析时不参与参数计数，编译器无法确定`print()`应调用无参版本还是带默认参数的版本。</details>  

1c) 以下代码为何无法编译？  

```cpp
#include <iostream>

void print(long x)
{
    std::cout << "long " << x << '\n';
}

void print(double x)
{
    std::cout << "double " << x << '\n';
}

int main()
{
    print(5);

    return 0;
}
```  

  
<details><summary>答案</summary>字面量5是`int`类型。将`int`转为`long`或`double`均需数值转换，编译器无法判断哪个版本更优。</details>  

**问题2**  
\> 步骤1  
编写名为`add()`的函数模板，使两个相同类型的值相加。以下程序应运行：  

```cpp
#include <iostream>

// 在此编写add函数模板

int main()
{
	std::cout << add(2, 3) << '\n';
	std::cout << add(1.2, 3.4) << '\n';

	return 0;
}
```  

并产生输出：  

```
5
4.6
```  

  
<details><summary>答案</summary>  
```cpp
template <typename T>
T add(T x, T y)
{
	return x + y;
}
```</details>  

\> 步骤2  
编写名为`mult()`的函数模板，使任意类型值（第一参数）与整数（第二参数）相乘。第二参数不应是模板类型，返回值类型与第一参数相同。以下程序应运行：  

```cpp
#include <iostream>

// 在此编写mult函数模板

int main()
{
	std::cout << mult(2, 3) << '\n';
	std::cout << mult(1.2, 3) << '\n';

	return 0;
}
```  

并产生输出：  

```
6
3.6
```  

  
<details><summary>答案</summary>  
```cpp
template <typename T>
T mult(T x, int y)
{
	return x * y;
}
```</details>  

\> 步骤3  
编写名为`sub()`的函数模板，使两个不同类型的值相减。以下程序应运行：  

```cpp
#include <iostream>

// 在此编写sub函数模板

int main()
{
	std::cout << sub(3, 2) << '\n';
	std::cout << sub(3.5, 2) << '\n';
	std::cout << sub(4, 1.5) << '\n';

	return 0;
}
```  

并产生输出：  

```
1
1.5
2.5
```  

  
<details><summary>答案</summary>  
```cpp
template <typename T, typename U>
auto sub(T x, U y)
{
	return x - y;
}

/* C++20可用缩写函数模板：
auto sub(auto x, auto y)
{
	return x - y;
}
*/
```</details>  

**问题3**  
以下程序输出结果是什么？为什么？  

```cpp
#include <iostream>

template <typename T>
int count(T) // 等同于int count(T x)，省略参数名因未使用
{
    static int c { 0 };
    return ++c;
}

int main()
{
    std::cout << count(1) << '\n';
    std::cout << count(1) << '\n';
    std::cout << count(2.3) << '\n';
    std::cout << count<double>(1) << '\n';
    
    return 0;
}
```  

  
<details><summary>答案</summary>  
输出：  
```
1
2
1
2
```  
解释：  
1. `count(1)`实例化`count<int>`，返回1  
2. 再次调用已存在的`count<int>`，返回2  
3. `count(2.3)`实例化`count<double>`，新静态变量返回1  
4. 显式调用`count<double>`，`int`转`double`，返回2  
</details>  

**问题4**  
以下程序输出结果是什么？  

```cpp
#include <iostream>

int foo(int n)
{
    return n + 10;
}

template <typename T>
int foo(T n)
{
    return n;
}

int main()
{
    std::cout << foo(1) << '\n';      // #1
    short s { 2 };
    std::cout << foo(s) << '\n';      // #2
    std::cout << foo<int>(4) << '\n'; // #3
    std::cout << foo<int>(s) << '\n'; // #4
    std::cout << foo<>(6) << '\n';    // #5
    
    return 0;
}
```  

  
<details><summary>答案</summary>  
输出：  
```
11
2
4
2
6
```  
解析：  
1. 精确匹配非模板函数`foo(int)`  
2. 优先实例化`foo<short>`而非转换  
3. 显式调用模板实例`foo<int>`  
4. `short`提升为`int`匹配模板实例  
5. 仅匹配模板，调用`foo<int>`  
</details>  

[下一课 F.1 — constexpr函数](Chapter-F/lessonF.1-constexpr-functions.md)  
[返回主页](/)  
[上一课 11.10 — 在多文件中使用函数模板](Chapter-11/lesson11.10-using-function-templates-in-multiple-files.md)