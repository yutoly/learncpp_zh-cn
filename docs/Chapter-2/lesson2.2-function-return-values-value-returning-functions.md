2.2 — 函数返回值（值返回函数）  
==========================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月5日（首次发布于2019年2月1日）  

考虑以下程序：  
```cpp
#include <iostream>

int main()
{
	// 从用户获取值
	std::cout << "输入整数：";
	int num{};
	std::cin >> num;

	// 输出双倍值
	std::cout << num << " 的双倍是：" << num * 2 << '\n';

	return 0;
}
```  
该程序包含两个概念部分：首先从用户获取值，然后告知用户该值的双倍结果。虽然这个简单程序无需拆分为多个函数，但若需要拆分该如何处理？从用户获取整数值是一个明确的任务，适合作为函数。  

尝试编写如下程序：  
```cpp
// 此程序无法工作
#include <iostream>

void getValueFromUser()
{
 	std::cout << "输入整数：";
	int input{};
	std::cin >> input;  
}

int main()
{
	getValueFromUser(); // 请求用户输入

	int num{}; // 如何获取getValueFromUser()的值来初始化此变量？

	std::cout << num << " 的双倍是：" << num * 2 << '\n';

	return 0;
}
```  
该程序存在缺陷：`getValueFromUser`函数终止后用户输入的值丢失，导致`num`始终初始化为0。需通过函数返回值机制将用户输入传回`main`。  

返回值机制  
----------------  
定义用户自定义函数时，需确定是否向调用者返回值。要实现返回值需满足两点：  

1. **返回类型（return type）**：函数名前指定的类型，决定返回值的类型（非具体值）。例如`void`表示不返回值，`int`表示返回整型值。  

2. **返回语句（return statement）**：由`return`关键字和表达式构成，以分号结尾。执行时：  
   - 计算表达式生成值  
   - 将该值拷贝回调用者（称为返回值）  
   - 函数退出，控制权交还调用者  

此过程称为**按值返回（return by value）**。  

值返回函数示例：  
```cpp
#include <iostream>

int returnFive()
{
    return 5; // 返回值5给调用者
}

int main()
{
    std::cout << returnFive() << '\n';    // 输出5
    std::cout << returnFive() + 2 << '\n';// 输出7
    returnFive(); // 返回值被忽略
    return 0;
}
```  
程序输出：  
```
5
7
```  
第三次调用`returnFive()`时返回值被忽略。  

修复示例程序  
----------------  
修正后的程序：  
```cpp
#include <iostream>

int getValueFromUser() // 返回整型值
{
 	std::cout << "输入整数：";
	int input{};
	std::cin >> input;  

	return input; // 返回用户输入值
}

int main()
{
	int num { getValueFromUser() }; // 用返回值初始化num
	std::cout << num << " 的双倍是：" << num * 2 << '\n';
	return 0;
}
```  
当初始化`num`时，`getValueFromUser()`被调用，用户输入值通过返回机制传递给`num`。  

关于main()函数  
----------------  
程序执行时操作系统调用`main()`函数。C++对`main()`的特殊要求：  
- 必须返回`int`类型  
- 禁止显式调用`main()`  

错误示例：  
```cpp
void foo()
{
    main(); // 编译错误：禁止显式调用main
}

void main() // 编译错误：返回类型非int
{
    foo();
}
```  

状态码  
----------------  
`main()`的返回值称为**状态码（status code）**：  
- `0`表示程序正常执行  
- 非零值通常表示失败（但可移植性受限）  

最佳实践：  
- `main()`应返回`0`表示正常执行  

预处理器宏`EXIT_SUCCESS`和`EXIT_FAILURE`（定义于`<cstdlib>`）提供更明确的返回方式。  

未定义行为警告  
----------------  
值返回函数必须通过`return`语句返回值，否则导致未定义行为。示例：  
```cpp
int getValueFromUserUB()
{
 	std::cout << "输入整数：";
	int input{};
	std::cin >> input;
	// 缺少return语句
}
```  
现代编译器会发出警告，运行此类程序将导致未定义行为。  

函数返回值特性  
----------------  
1. **单一返回值**：每次调用只能返回一个值（可通过后续课程方法解决此限制）  
2. **返回值语义**：由函数作者定义含义（计算结果、状态码等），建议通过注释说明  
3. **代码复用**：遵循DRY（Don't Repeat Yourself）原则，避免冗余代码  

示例复用函数：  
```cpp
#include <iostream>

int getValueFromUser()
{
 	std::cout << "输入整数：";
	int input{};
	std::cin >> input;  
	return input;
}

int main()
{
    int x{ getValueFromUser() }; // 第一次调用
    int y{ getValueFromUser() }; // 第二次调用
    std::cout << x << " + " << y << " = " << x + y << '\n';
    return 0;
}
```  
输出示例：  
```
输入整数：5
输入整数：7
5 + 7 = 12
```  

测验解析  
----------------  
**问题1**  
各程序分析：  
1a) 输出16  
1b) 编译错误（嵌套函数非法）  
1c) 无输出（返回值被忽略）  
1d) 输出5两次（第二个return不可达）  
1e) 编译错误（函数名含空格）  

**问题2**  
DRY（Don't Repeat Yourself）原则：通过减少代码冗余提高可维护性，降低错误率。  

[下一课 2.3 — void函数（非值返回函数）](Chapter-2/lesson2.3-void-functions-non-value-returning-functions.md)  
[返回主页](/)  
[上一课 2.1 — 函数简介](Chapter-2/lesson2.1-introduction-to-functions.md)