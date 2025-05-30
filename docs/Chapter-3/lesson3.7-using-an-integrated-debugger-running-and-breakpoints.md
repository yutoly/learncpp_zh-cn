3.7 — 使用集成调试器：运行与断点  
============================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2019年2月1日 下午12:01（首次发布于2023年12月15日）  

 






逐语句调试（见课程[3.6 — 使用集成调试器：逐语句执行](Chapter-3/lesson3.6-using-an-integrated-debugger-stepping.md)）虽能逐行检查代码，但在大型程序中，即使要调试到目标位置都可能耗费大量时间。


现代调试器提供了更高效的工具。本章将介绍能快速定位代码的调试功能。


运行到光标处（Run to cursor）  
----------------  

首推功能是*运行到光标处*（Run to cursor）。该命令让程序执行到光标所在行时暂停，便于从该点开始调试。这是快速定位调试起点的有效方法。



Visual Studio 用户  
----------------  

在Visual Studio中，右键代码行选择*运行到光标处*（Run to Cursor）或按Ctrl-F10组合键。



Code::Blocks 用户  
----------------  

在Code::Blocks中，右键代码行选择*运行到光标处*（Run to cursor），或通过*调试菜单（Debug menu） > 运行到光标处*，或按F4快捷键。



VS Code 用户  
----------------  

在VS Code中，调试时右键代码行选择*运行到光标处*（Run to Cursor）。



以下列程序为例：

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

右键第5行选择"运行到光标处"。

![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-StepInto4-min.png)  
程序将执行到该行暂停。此时可继续逐语句调试或再次使用*运行到光标处*。


继续执行（Continue）  
----------------  

调试中途若想继续运行程序，使用*继续执行*（Continue）命令。该命令让程序正常执行直至终止或触发中断（如遇到断点）。



Visual Studio 用户  
----------------  

通过*调试菜单（Debug menu） > 继续*或按F5。



Code::Blocks 用户  
----------------  

通过*调试菜单（Debug menu） > 启动/继续*或按F8。



VS Code 用户  
----------------  

通过*运行菜单（Run menu） > 继续*或按F5。


以第5行为起点执行*继续*，程序将完成运行。


启动调试（Start）  
----------------  

*启动调试*（Start）与*继续执行*功能相同，但用于启动新的调试会话。


Visual Studio 用户  
----------------  

通过*调试菜单（Debug menu） > 开始调试*或按F5。



Code::Blocks 用户  
----------------  

通过*调试菜单（Debug menu） > 启动/继续*或按F8。



VS Code 用户  
----------------  

通过*运行菜单（Run menu） > 开始调试*或按F5（需注意[之前课程](Chapter-0/lesson0.9-configuring-your-compiler-build-configurations.md)中设置的`stopAtEntry: true`参数会影响初始暂停）。


断点（Breakpoints）  
----------------  

**断点（breakpoint）**是让调试器在指定位置暂停执行的标记。相较于*运行到光标处*，断点会每次命中时暂停，且能长期保留。



Visual Studio 用户  
----------------  

设置/取消断点方法：  
* 菜单：*调试菜单（Debug menu） > 切换断点*  
* 右键菜单：*切换断点*  
* 快捷键：F9  
* 点击行号左侧灰色区域  



Code::Blocks 用户  
----------------  

设置/取消断点方法：  
* 菜单：*调试菜单（Debug menu） > 切换断点*  
* 右键菜单：*切换断点*  
* 快捷键：F5  
* 点击行号右侧区域  



VS Code 用户  
----------------  

设置/取消断点方法：  
* 菜单：*运行菜单（Run menu） > 切换断点*  
* 快捷键：F9  
* 点击行号左侧区域  



在第5行设置断点后，Visual Studio显示红色圆点，Code::Blocks显示红色八角形：  
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-Breakpoint1-min.png)

启动调试后，程序将在断点处暂停：  
![](https://www.learncpp.com/images/CppTutorial/Chapter3/VS-Breakpoint2-min.png)

注意：断点仅在代码执行路径上生效。


对比示例程序：

```cpp
#include <iostream>

void printValue(int value)
{
    std::cout << value << '\n';
}

int main()
{
    printValue(5);
    printValue(6);
    printValue(7);

    return 0;
}
```

使用*运行到光标处*到第5行后*继续*，程序不会再次暂停。而设置断点后每次执行到该行都会暂停。


设置下一条语句（Set next statement）  
----------------  

**设置下一条语句**（Set next statement）命令允许跳转执行点，可跳过代码或重复执行某段代码。



Visual Studio 用户  
----------------  

调试时右键语句选择*设置下一条语句*（Set next statement）或按Ctrl-Shift-F10。



Code::Blocks 用户  
----------------  

通过*调试菜单（Debug menu） > 设置下一条语句*或右键菜单。



VS Code 用户  
----------------  

调试时右键语句选择*跳转到光标处*（Jump to cursor）。


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
    printValue(6);
    printValue(7);

    return 0;
}
```

1. *运行到光标处*到第11行，控制台输出5  
2. 右键第12行选择*设置下一条语句*，跳过`printValue(6)`  
3. *继续*后输出：  
```
5
7
```

反向跳转示例：  
1. *运行到光标处*到第12行  
2. 设置执行点回第11行  
3. *继续*后输出：  
```
5
6
6
7
```


警告  
----------------  

* 该命令不改变程序状态，变量值保持跳转前状态  
* 可能导致非预期结果  
* 禁止跨函数跳转，可能引发未定义行为或崩溃  


结论  
----------------  

掌握调试器的执行控制命令后，下一步将学习如何监视程序状态（见[3.8 — 使用集成调试器：监视变量](Chapter-3/lesson3.8-using-an-integrated-debugger-watching-variables.md)）。这些命令是后续调试技术的基础。

[下一课 3.8 — 使用集成调试器：监视变量](Chapter-3/lesson3.8-using-an-integrated-debugger-watching-variables.md)  
[返回主页](/)  
[上一课 3.6 — 使用集成调试器：逐语句执行](Chapter-3/lesson3.6-using-an-integrated-debugger-stepping.md)