3.6 — 使用集成调试器：单步执行  
=============================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年11月16日上午11:27（PST）（首次发布于2007年11月16日）  
2024年8月30日  

 

当程序运行时，执行从*main*函数顶部开始，按语句顺序逐条执行直至结束。程序运行时始终跟踪大量信息：使用的变量值、已调用的函数（以便函数返回时知道跳回位置）、以及当前执行点（以确定下条执行语句）。所有这些追踪信息统称为**程序状态（program state）**（简称*状态*）。  

前文我们探讨了通过修改代码辅助调试的方法，包括打印诊断信息或使用日志记录器。这些是检查运行中程序状态的简单方法。虽然有效但仍有缺点：需要修改代码（耗时且可能引入新错误）、使代码臃肿（降低可读性）。  

上述方法隐含一个前提假设：程序一旦运行就将执行完毕（仅暂停接受输入），我们无法在任意点介入检查结果。  

现代集成开发环境（IDE）提供的**集成调试器（integrated debugger）**正是为此而生。  

调试器  
----------------  

**调试器（debugger）**是允许程序员控制程序执行流程、在运行时检查程序状态的工具。例如可逐行执行程序并检查变量值。通过比对变量实际值与预期值，或观察代码执行路径，调试器能极大助力定位语义（逻辑）错误。  

调试器的核心能力体现在两方面：精确控制程序执行、查看（或修改）程序状态。  

早期调试器（如[gdb](https://en.wikipedia.org/wiki/Gdb)）是命令行工具，需输入复杂命令操作。后来调试器（如Borland早期[turbo debugger](https://en.wikipedia.org/wiki/Turbo_Debugger)）虽独立但提供图形界面。现代IDE普遍内置**集成调试器**——即与代码编辑器同界面的调试工具。  

虽然集成调试器便捷且推荐新手使用，命令行调试器在无图形界面环境（如嵌入式系统）中仍广泛使用。  

几乎所有现代调试器都包含相同基础功能，但菜单布局和快捷键差异较大。本文示例使用Visual Studio截图（同时提供Code::Blocks操作说明），读者可自行适配其他IDE。  

> **提示**  
> 调试器快捷键仅在IDE/调试器窗口激活时有效  

本章后续内容将指导调试器使用。  

> **重要提示**  
> 切勿忽视调试器学习。随着程序复杂度提升，学习调试器所耗时间将远低于其节省的排错时间。  

> **警告**  
> 继续本章前，请确保项目使用调试生成配置（详见[0.9 — 编译器配置：生成配置](Chapter-0/lesson0.9-configuring-your-compiler-build-configurations.md)）。  
> 若使用发布配置编译，调试器功能可能异常（如尝试单步进入时直接运行程序）。  

Code::Blocks用户设置  
----------------  
1. 进入*设置菜单 > 调试器...*  
2. 展开左侧*GDB/CDB调试器*树，选择*Default*  
3. 若"Executable path"显示红色条，点击右侧*...*定位"gdb32.exe"（通常位于*C:\Program Files (x86)\CodeBlocks\MinGW\bin\*）  

> **注意**  
> Code::Blocks调试器（GDB）可能无法识别含空格或非英文字符的路径，若调试异常可考虑此因素。  

VS Code用户设置  
----------------  
1. 按*Ctrl+Shift+P*选择"C/C++: 添加调试配置"  
2. 选择"C/C++: g++ 生成并调试活动文件"  
3. 在生成的`launch.json`中将"stopAtEntry"设为true  
4. 打开main.cpp后按*F5*开始调试  

单步执行  
----------------  

**单步执行（Stepping）**是调试器提供的程序流程控制功能集合，允许逐语句执行代码。  

逐语句（Step into）  
----------------  
**逐语句（Step into）**执行下条语句后暂停。若语句含函数调用，则跳转至被调函数顶部暂停。  

示例程序：  
```cpp
#include <iostream>

void printValue(int value)
{
    std::cout << value << '\n';
}

int main()
{
    printValue(5);
    return 0;
}
```  

调试步骤：  
1. 执行首次*逐语句*命令  
   - Visual Studio: F11  
   - Code::Blocks: Shift+F7  
   - VS Code: F11  
2. 程序编译后启动，控制台窗口打开  
3. 黄色箭头标记显示main函数左大括号（第9行）  
4. 继续逐语句执行至printValue调用（第10行）  
5. 再次逐语句进入printValue函数体（第4行）  
6. 逐语句执行输出语句（可能进入operator<<实现，按*跳出*返回）  
7. 执行完printValue后返回main函数  

> **注意**  
> 若未立即看到输出，可添加`std::cout << std::unitbuf;`启用自动刷新（调试后移除）  

逐过程（Step over）  
----------------  
**逐过程（Step over）**执行下条语句，但跳过函数内部细节直接返回结果。  

操作方式：  
- Visual Studio: F10  
- Code::Blocks: F7  
- VS Code: F10  

示例中当箭头位于printValue调用（第10行）时执行逐过程，直接完成函数调用并暂停在return语句。  

跳出（Step out）  
----------------  
**跳出（Step out）**执行当前函数剩余代码，返回调用处后暂停。  

操作方式：  
- Visual Studio: Shift+F11  
- Code::Blocks: Ctrl+F7  
- VS Code: Shift+F11  

示例中在printValue函数内（第4行）执行跳出，直接完成函数执行并返回main函数。  

步退（Step back）  
----------------  
部分调试器（如Visual Studio企业版和[rr](https://github.com/rr-debugger/rr)）支持**步退（step back）**功能，可回退上一步操作。需注意社区版Visual Studio和Code::Blocks暂未支持此功能。  

[下一课 3.7 — 使用集成调试器：运行与断点](Chapter-3/lesson3.7-using-an-integrated-debugger-running-and-breakpoints.md)  
[返回主页](/)  
[上一课 3.5 — 更多调试技巧](Chapter-3/lesson3.5-more-debugging-tactics.md)