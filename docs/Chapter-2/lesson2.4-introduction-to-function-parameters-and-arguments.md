2.4 — 函数形参与实参入门  
========================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月18日（首次发布于2015年1月25日）  

前课回顾  
----------------  
在上一课中，我们学习了如何让函数向调用者返回值。通过该技术创建了模块化的*getValueFromUser*函数，应用示例如下：  

```cpp
#include <iostream>

int getValueFromUser()
{
    std::cout << "Enter an integer: ";
    int input{};
    std::cin >> input;  

    return input;
}

int main()
{
    int num { getValueFromUser() };
    std::cout << num << " doubled is: " << num * 2 << '\n';
    return 0;
}
```  

问题引入  
----------------  
若想将输出语句也封装为独立函数，可能尝试如下写法：  

```cpp
void printDouble()
{
    std::cout << num << " doubled is: " << num * 2 << '\n';
}
```  

此代码无法编译，因为`printDouble`函数无法识别`num`标识符。若在函数内定义`num`变量：  

```cpp
void printDouble()
{
    int num{}; // 添加局部变量
    std::cout << num << " doubled is: " << num * 2 << '\n';
}
```  

虽能通过编译，但程序逻辑错误（始终输出"0 doubled is: 0"）。核心问题在于`printDouble`无法获取用户输入值。  

函数形参与实参  
----------------  
**函数形参（function parameter）**是函数头中声明的变量，其行为类似于函数内部变量，但通过调用者提供的值进行初始化。形参在函数名后的括号内声明，多个参数以逗号分隔：  

```cpp
void printValue(int x) // int x 为形参
{
    std::cout << x << '\n';
}

int add(int x, int y) // 两个形参
{
    return x + y;
}
```  

**实参（argument）**是函数调用时传递给形参的值：  

```cpp
printValue(6); // 6 是实参
add(2, 3);     // 2 和 3 是实参
```  

形参与实参的协作机制  
----------------  
函数调用时，所有形参被创建为变量，实参值通过**值传递（pass by value）**方式拷贝至对应形参（使用拷贝初始化）。例如：  

```cpp
void printValues(int x, int y)
{
    std::cout << x << '\n' << y << '\n';
}

int main()
{
    printValues(6, 7); // x=6, y=7
    return 0;
}
```  

输出：  
```
6
7
```  

实参数量必须与形参数量严格匹配，否则引发编译错误。实参可以是任意合法表达式。  

修正示例程序  
----------------  
通过形参机制修正初始程序：  

```cpp
void printDouble(int value) // 添加int型形参
{
    std::cout << value << " doubled is: " << value * 2 << '\n';
}

int main()
{
    int num { getValueFromUser() };
    printDouble(num); // 传递num作为实参
    return 0;
}
```  

此时`num`的值被拷贝至`value`形参，函数正确使用该值。  

返回值作为实参  
----------------  
可简化代码，直接使用函数返回值作为实参：  

```cpp
printDouble(getValueFromUser()); // 直接传递返回值
```  

形参与返回值的协同工作  
----------------  
结合形参与返回值，可创建数据处理函数：  

```cpp
int add(int x, int y)
{
    return x + y;
}

int main()
{
    std::cout << add(4, 5); // 输出9
    return 0;
}
```  

执行流程：  
1. `add(4,5)`调用初始化`x=4`, `y=5`  
2. 返回`x+y=9`至调用处  
3. 输出结果  

进阶示例  
----------------  
```cpp
std::cout << add(1, multiply(2, 3)); // 1+(2*3)=7
std::cout << add(1, add(2, 3));      // 1+(2+3)=6
```  

未引用形参与无名形参  
----------------  
**未引用形参（unreferenced parameters）**指函数中未使用的参数。为避免编译器警告，可省略参数名：  

```cpp
void doSomething(int /*count*/) // 无名形参
{
    // 使用注释说明参数用途
}
```  

最佳实践  
----------------  
* 当函数参数存在但未被使用时，省略参数名  
* 可使用注释说明无名形参的原始用途  

总结  
----------------  
函数形参与返回值是实现代码复用的关键机制，使函数能够处理输入数据并返回计算结果，而无需预先知道具体数值。  

测验  
----------------  
**问题1**  
错误原因：`multiply`函数声明为`void`却尝试返回`int`值。  

**问题2**  
错误1：调用`multiply`时实参数量不足  
错误2：`multiply`函数缺少`return`语句  

**问题3**  
`multiply(add(1,2,3),4)` => `multiply(6,4)` => 输出24  

**问题4**  
```cpp
int doubleNumber(int x)
{
    return 2 * x;
}
```  

**问题5**  
```cpp
#include <iostream>

int doubleNumber(int x) { return 2*x; }

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;
    std::cout << doubleNumber(x);
    return 0;
}
```  

[下一课 2.5 — 局部作用域入门](Chapter-2/lesson2.5-introduction-to-local-scope.md)  
[返回主页](/)  
[上一课 2.3 — void函数（无返回值函数）](Chapter-2/lesson2.3-void-functions-non-value-returning-functions.md)