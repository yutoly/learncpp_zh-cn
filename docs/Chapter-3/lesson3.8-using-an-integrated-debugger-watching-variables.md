3.8 — 使用集成调试器：监视变量
=======================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")
2007年11月21日 上午9:58（太平洋标准时间）  
2024年1月5日

前两课（[3.6 — 使用集成调试器：单步执行](Chapter-3/lesson3.6-using-an-integrated-debugger-stepping.md)和[3.7 — 使用集成调试器：运行与断点](Chapter-3/lesson3.7-using-an-integrated-debugger-running-and-breakpoints.md)）介绍了如何通过调试器观察程序执行路径。但单步调试仅是调试器功能的一半。调试器还能在逐步执行代码时检查变量值，且无需修改代码。

与前几课相同，本节示例使用 Visual Studio。若使用其他 IDE/调试器，命令名称或位置可能略有差异。

> **警告**  
> 请确保项目使用调试构建配置编译（详见[0.9 — 配置编译器：构建配置](Chapter-0/lesson0.9-configuring-your-compiler-build-configurations.md)）。若使用发布（release）配置编译，调试器功能可能无法正常工作。

监视变量
----------------

**监视变量（Watching a variable）**是在调试模式下检查程序执行时变量值的过程。多数调试器提供多种实现方式。

参考以下示例程序：
```cpp
#include <iostream>

int main()
{
	int x{ 1 };  // 值1
	std::cout << x << ' ';

	x = x + 2;   // 值变为3
	std::cout << x << ' ';

	x = x + 3;   // 值变为6
	std::cout << x << ' ';

	return 0;
}
```
此程序输出数字 1、3 和 6。

首先*运行到光标处（run to cursor）*至第 6 行：
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-Watch1-min.png)
此时变量 x 已创建并初始化为 1，检查 x 值应显示为 1。

检查简单变量（如 x）的最简方法是悬停鼠标至变量 x 上。部分现代调试器支持此方式，这是最直接的检查方法。

> **Code::Blocks 用户注意**  
> Code::Blocks 默认禁用此功能。需手动开启：进入*设置菜单 > 调试器...*，在*GDB/CDB 调试器节点*下选择*Default*配置文件，勾选*Evaluate expression under cursor*选项：  
> ![](https://www.learncpp.com/images/CppTutorial/Chapter3/CB-EvaluateExpression-min.png)

在第 6 行悬停鼠标至变量 x，显示如下：
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-Watch2-min.png)
注意：可悬停检查任意位置的 x（不限于当前行）。例如悬停第 12 行的 x 显示相同值：
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-Watch3-min.png)

Visual Studio 用户还可使用快速监视（QuickWatch）：选中变量名 x 后右击选择"快速监视"：
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-QuickWatch1-min.png)
弹出的子窗口显示变量当前值：
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-QuickWatch2-min.png)
检查后关闭此窗口。

接着通过逐步执行观察变量变化：*逐过程（step over）*两次或*运行到光标处*至第 9 行，此时 x 值应为 3：
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-Watch4-min.png)

监视窗口
----------------
鼠标悬停或快速监视适用于查看变量在特定时刻的值，但不适合观察变量在代码运行中的变化（需反复悬停/选择变量）。

现代集成调试器提供**监视窗口（watch window）**功能，可添加需持续检查的变量，这些变量会在逐步执行时自动更新。进入调试模式时监视窗口可能已显示，若未显示需通过 IDE 的窗口命令调出（通常在"视图"或"调试"菜单中）。

> **IDE 操作指引**  
> - **Visual Studio**：调试模式下进入*调试菜单 > 窗口 > 监视 > 监视1*  
> - **Code::Blocks**：*调试菜单 > 调试窗口 > 监视*（可拖动停靠至主窗口）  
> - **VS Code**：调试模式下监视窗口停靠在左侧调用堆栈上方

窗口显示如下：
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-Watch5-min.png)
（监视窗口内容可能为空）

添加变量到监视窗口的两种方式：
1. 在监视窗口最左侧列输入变量名
2. 代码窗口中右击变量，选择*添加监视（Add Watch）*(Visual Studio) 或*监视 x*(x 为变量名)(Code::Blocks)

若未处于第 9 行的调试会话中，请启动调试并*运行到光标处*至第 9 行。

添加变量 "x" 到监视列表后显示：
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-Watch6-min.png)
接着*逐过程*两次或*运行到光标处*至第 12 行，可见 x 值从 3 变为 6。

超出作用域的变量（如已返回函数中的局部变量）会保留在监视窗口中，但通常标记为"不可用"或显示灰色最后已知值。若变量回到作用域（如函数再次调用），其值将重新显示。因此即使变量超出作用域也可保留在监视窗口中。

监视功能是逐步执行时观察变量值随时间变化的最佳方式。

在监视变量上设置断点
----------------
部分调试器允许在监视变量（而非代码行）上设置断点。当变量值改变时，程序将暂停执行。

例如，在上述程序的变量 `x` 上设置此类断点，调试器将在执行第 8 行和第 11 行（修改 `x` 值的行）后暂停。

> **Visual Studio 用户操作**  
> 确保变量已被监视。进入调试模式后，在监视窗口右击变量并选择"值更改时中断"。  
> **注意**：每次启动调试会话需重新启用此选项。

监视窗口支持表达式求值
----------------
监视窗口可评估简单表达式。若未执行，请*运行到光标处*至第 12 行，在监视窗口输入 `x + 2` 将得到结果 8。

也可在代码中选中表达式，通过悬停或右击添加到监视窗口来检查其值。

> **警告**  
> 监视表达式中的标识符将按其当前值求值。若需查看代码中表达式的实际结果，请先*运行到光标处*至该表达式，确保所有标识符值正确。

局部变量监视
----------------
调试时检查函数内局部变量值很常见，多数调试器提供快速监视*所有*作用域内局部变量的方法。

> **IDE 操作指引**  
> - **Visual Studio**：调试模式下进入*调试菜单 > 窗口 > 局部变量*  
> - **Code::Blocks**：*监视*窗口中的*局部变量*节点（可展开查看）  
> - **VS Code**：调试模式左侧*变量（VARIABLES）*区域的*局部变量（Locals）*节点

若只需监视局部变量，优先查看*局部变量*窗口（通常已自动显示）。

[下一课 3.9 — 使用集成调试器：调用堆栈](Chapter-3/lesson3.9-using-an-integrated-debugger-the-call-stack.md)  
[返回主页](/)    
[上一课 3.7 — 使用集成调试器：运行与断点](Chapter-3/lesson3.7-using-an-integrated-debugger-running-and-breakpoints.md)