3.9 — 使用集成调试器：调用栈  
===================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2019年2月1日 下午12:02（太平洋标准时间）  
2023年6月5日  

现代调试器包含一个极为实用的调试信息窗口——调用栈（call stack）窗口。  

当程序调用函数时，系统会记录当前位置、执行函数调用并在返回时恢复。这种机制通过调用栈实现。  

**调用栈（call stack）**是记录当前执行路径中所有活动函数调用的列表。每个被调函数在栈中对应一个条目，包含函数返回时的目标代码行。新函数调用时入栈，函数返回时出栈，控制权交还给栈顶下方的函数。  

**调用栈窗口**是显示当前调用栈的调试界面。若未显示该窗口，需在IDE中手动开启：  

Visual Studio用户  
----------------  
通过*调试菜单 > 窗口 > 调用栈*打开。注意需在调试会话中激活。  

Code::Blocks用户  
----------------  
通过*调试菜单 > 调试窗口 > 调用栈*打开。  

VS Code用户  
----------------  
调试模式下，调用栈窗口停靠在界面左侧。  

以下示例程序演示调用栈：  

```cpp
#include <iostream>

void a()
{
	std::cout << "a() called\n";
}

void b()
{
	std::cout << "b() called\n";
	a();
}

int main()
{
	a();
	b();
	return 0;
}
```  

在第5行和第10行设置断点后启动调试。函数`a`首先被调用，触发第5行断点：  

![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-CallStack1-min.png)  
此时调用栈显示：  
- 底层：`main`函数（第17行）  
- 顶层：`a`函数（第5行）  

注意：不同IDE可能显示差异（如函数名格式、行号偏移或`[外部代码]`标记），这些差异无关紧要。  

继续执行至第10行断点，调用栈更新为：  
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-CallStack2-min.png)  
- 顶层变为`b`函数（第10行）  
- `a`函数已出栈  

再次继续执行，触发`a`函数断点时的调用栈：  
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-CallStack3-min.png)  
- 调用顺序：`main` → `b` → `a`  

调用栈与断点配合使用时，可清晰展示代码执行路径。  

结论  
----------------  
掌握集成调试器的基本操作（单步执行、断点、监视窗口和调用栈）后，您已具备调试各类问题的能力。熟练运用调试器需要实践积累，但投入的学习时间将大幅提升调试效率！  

[下一课 3.10 — 防患于未然的问题检测](Chapter-3/lesson3.10-finding-issues-before-they-become-problems.md)  
[返回主页](/)    
[上一课 3.8 — 使用集成调试器：监视变量](Chapter-3/lesson3.8-using-an-integrated-debugger-watching-variables.md)