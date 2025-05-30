8.8 — 循环与while语句入门  
=================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月5日（首次发布于2007年6月22日）  

循环简介  
----------------  

真正的乐趣现在开始——接下来的课程我们将学习循环（loops）。循环是允许代码重复执行直到满足特定条件的控制流结构。循环为编程工具包增加了极大的灵活性，让许多原本困难的任务成为可能。  

例如要打印1到10之间的所有数字，没有循环时可能需要这样写：  

```cpp
#include <iostream>

int main()
{
    std::cout << "1 2 3 4 5 6 7 8 9 10";
    std::cout << " done!\n";
    return 0;
}
```  

虽然可行，但当需要打印更多数字时（比如1到1000），这种方式将变得难以操作。但若用户希望输入一个数字后打印1到该数之间的所有数值，由于用户输入在编译时无法预知，就需要循环的解决方案。  

while语句  
----------------  

**while语句**（也称while循环）是C++提供的三种循环类型中最简单的一种，其语法结构与if语句相似：  

```cpp
while (条件)
    语句;
```  

while语句使用**while**关键字声明。执行时先评估*条件*表达式，若结果为`true`则执行关联的*语句*。  

与if语句不同，while语句在执行完语句后会再次评估条件。只要条件保持`true`，循环就会持续执行。  

观察以下打印1到10的while循环示例：  

```cpp
#include <iostream>

int main()
{
    int count{ 1 };
    while (count <= 10)
    {
        std::cout << count << ' ';
        ++count;
    }

    std::cout << "done!\n";
    return 0;
}
```  

输出结果：  

```
1 2 3 4 5 6 7 8 9 10 done!
```  

详细流程：  

1. 初始化`count`为1  
2. 检查条件`count <= 10`为`true`，执行代码块  
3. 打印当前`count`值并递增  
4. 重复步骤2-3，直到`count`为11时条件为`false`，循环终止  

若将初始值设为15，则条件`15 <= 10`立即为`false`，循环体不会执行。  

无限循环  
----------------  

当条件始终为`true`时，循环将无限执行。例如：  

```cpp
#include <iostream>

int main()
{
    int count{ 1 };
    while (count <= 10) // 此条件永远不可能为false
    {
        std::cout << count << ' '; // 此行将重复执行
    }

    std::cout << '\n'; // 永远不会执行
    return 0; // 永远不会执行
}
```  

由于`count`未递增，程序将无限输出`1 1 1 1...`。  

### 有意设计的无限循环  
可通过以下方式声明：  

```cpp
while (true)
{
  // 此循环将无限执行
}
```  

退出方式包括：return语句、break语句、exit语句、goto语句、抛出异常或用户终止程序。示例：  

```cpp
#include <iostream>

int main()
{
    while (true) // 无限循环
    {
        std::cout << "继续循环（y/n）？ ";
        char c{};
        std::cin >> c;

        if (c == 'n')
            return 0;
    }
}
```  

此类循环常见于持续处理请求的服务器程序。  

> **最佳实践**  
> 有意设计的无限循环推荐使用`while(true)`  

### 无意导致的无限循环  
在while条件后误加分号是常见错误：  

```cpp
#include <iostream>

int main()
{
    int count{ 1 };
    while (count <= 10); // 注意此处分号
    {
        std::cout << count << ' ';
        ++count;
    }

    std::cout << "done!\n";
    return 0;
}
```  

等效于：  

```cpp
while (count <= 10) // 无限循环
    ;               // 空语句作为循环体
```  

由于`count`未更新，程序将无限空转。  

> **警告**  
> 注意while条件后的分号，除非条件能变为`false`，否则会导致无限循环  

循环变量与命名  
----------------  

**循环变量（loop variable）**用于控制循环执行次数，如`count`。虽然常用`int`类型，但偶尔也使用其他类型（如`char`）。  

传统上使用`i`、`j`、`k`作为循环变量名，但更推荐具有描述性的名称（如`userCount`）。  

> **最佳实践**  
> 整型循环变量应使用有符号类型  

考虑以下错误示例：  

```cpp
unsigned int count{ 10 };
while (count >= 0) // 无限循环
{
    --count;
}
```  

当`count`为0时，`--count`会使其变为4294967295（32位无符号整型），条件永远成立。  

迭代控制  
----------------  

每个循环执行周期称为**迭代（iteration）**。使用取余运算符可实现每N次迭代执行特定操作，例如每10次换行：  

```cpp
if (count % 10 == 0)
{
    std::cout << '\n';
}
```  

嵌套循环  
----------------  

循环可嵌套使用。示例：  

```cpp
#include <iostream>

int main()
{
    int outer{ 1 };
    while (outer <= 5)
    {
        int inner{ 1 };
        while (inner <= outer)
        {
            std::cout << inner << ' ';
            ++inner;
        }
        std::cout << '\n';
        ++outer;
    }
    return 0;
}
```  

输出：  

```
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5
```  

测验  
----------------  

**问题1**  
为什么inner变量声明在while块内部？  
<details><summary>答案</summary>确保每次外部循环时重新初始化为1，符合最小作用域原则</details>  

**问题2**  
打印字母a-z及其ASCII码：  
<details><summary>答案</summary>  

```cpp
char myChar{ 'a' };
while (myChar <= 'z')
{
    std::cout << myChar << ' ' << static_cast<int>(myChar) << '\n';
    ++myChar;
}
```  
</details>  

**问题3**  
倒序打印数字：  
<details><summary>答案</summary>  

```cpp
int outer{ 5 };
while (outer >= 1)
{
    int inner{ outer };
    while (inner >= 1)
        std::cout << inner-- << ' ';
    std::cout << '\n';
    --outer;
}
```  
</details>  

**问题4**  
金字塔式打印：  
<details><summary>答案</summary>  

```cpp
int outer{ 1 };
while (outer <= 5)
{
    int inner{ 5 };
    while (inner >= 1)
    {
        if (inner <= outer)
            std::cout << inner << ' ';
        else
            std::cout << "  ";
        --inner;
    }
    std::cout << '\n';
    ++outer;
}
```  
</details>  

[下一课 8.9 do-while语句](Chapter-8/lesson8.9-do-while-statements.md)  
[返回主页](/)  
[上一课 8.7 goto语句](Chapter-8/lesson8.7-goto-statements.md)