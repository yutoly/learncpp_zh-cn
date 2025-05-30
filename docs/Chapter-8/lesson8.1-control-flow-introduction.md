8.1 — 控制流简介  
================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2007年6月20日 PDT下午9:37  
2023年12月23日  

程序运行时，CPU从`main()`顶部开始执行，默认按顺序执行若干语句（statement），最后在`main()`结束时终止。CPU执行语句的具体序列称为程序的**执行路径（execution path）**（简称**路径**）。  

考虑以下程序：  

```cpp
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    
    int x{};
    std::cin >> x;

    std::cout << "You entered " << x << '\n';

    return 0;
}
```  

该程序的执行路径包括第5、7、8、10、12行（按此顺序）。这是**直线型程序（straight-line program）**的典型示例。直线型程序每次运行时都遵循相同路径（以相同顺序执行相同语句）。  

然而，这往往不符合实际需求。例如，当用户输入无效值时，理想情况下应要求用户重新选择。这在直线型程序中无法实现。实际上，用户可能反复输入无效数据，因此需要重新提示的次数在运行时才能确定。  

幸运的是，C++提供了多种**控制流语句（control flow statements）**（也称**流程控制语句**），允许程序员改变程序的正常执行路径。您已在[4.10 — if语句简介](Chapter-4/lesson4.10-introduction-to-if-statements.md)中接触过if语句，它允许在条件表达式为真时执行特定语句。  

当控制流语句导致执行点跳转到非顺序语句时，称为**分支（branching）**。  

  
控制流语句分类表  
----------------------------

| 类别        | 含义                     | C++实现方式                |
|-----------|------------------------|-------------------------|
| 条件语句      | 仅在满足条件时执行代码序列         | if、else、switch          |
| 跳转语句      | 指示CPU从其他位置开始执行语句       | goto、break、continue     |
| 函数调用      | 跳转至其他位置执行后返回          | 函数调用、return             |
| 循环语句      | 重复执行代码序列直到满足条件        | while、do-while、for、范围for |
| 终止操作      | 结束程序运行                | std::exit()、std::abort()  |
| 异常处理      | 专为错误处理设计的特殊流程控制结构      | try、throw、catch           |  

本章将详细讲解除异常处理外的所有类别（异常处理将在[第27章](https://www.learncpp.com#Chapter27)专门讨论）。  

至此，您编写的程序功能仍有限制。掌握控制流（尤其是循环）后，您将能实现各种有趣功能！程序不再局限于玩具示例，而是具备实际效用。  

真正的乐趣即将开始，让我们启程吧！  

[下一课 8.2 — if语句与代码块](Chapter-8/lesson8.2-if-statements-and-blocks.md)  
[返回主页](/)  
[上一课 7.x — 第7章总结与测验](Chapter-7/lesson7.x-chapter-7-summary-and-quiz.md)