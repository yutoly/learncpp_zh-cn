0.7 — 编译你的第一个程序  
===================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年5月28日 PDT上午10:35  
2025年1月21日更新  

在编写第一个程序之前，我们需要学习如何在集成开发环境（Integrated Development Environment，IDE）中创建新程序。本节将指导您完成这一过程，并最终编译执行首个程序！  

项目（Project）  
----------------  

在IDE中编写C++程序时，通常从创建新项目开始（稍后将演示具体步骤）。**项目**是一个容器，包含生成可执行文件（或库、网站等）所需的所有源代码文件、图像、数据文件等。项目还保存了各种IDE、编译器与链接器设置，以及您的工作进度，以便后续重新打开时能恢复至离开时的状态。编译程序时，项目内所有.cpp文件都将被编译并链接。  

每个项目对应一个程序。当需要创建第二个程序时，需新建项目或覆盖现有项目代码（若无需保留原内容）。项目文件通常与特定IDE绑定，在不同IDE中需重新创建。  

> **最佳实践**  
> 为每个新程序创建独立项目。  

控制台项目（Console Project）  
----------------  

创建新项目时，通常需选择项目类型。本教程所有项目均为**控制台项目**，即创建可在Windows、Linux或Mac控制台中运行的程序。  

以下是Windows控制台截图：  
![Windows控制台](https://www.learncpp.com/images/CppTutorial/Chapter0/WindowsCommandLine-min.png?ezimgfmt=ng%3Awebp%2Fngcb2%2Frs%3Adevice%2Frscb2-1)  

默认情况下，控制台应用程序没有图形用户界面（GUI），通过控制台输出文本、键盘读取输入，并编译为独立可执行文件。这种特性非常适合学习C++，既保持复杂度最低，又确保在各类系统中正常运行。  

若从未使用过控制台或不知如何访问也无需担心，我们将通过IDE编译启动程序（必要时会自动调用控制台）。  

工作区/解决方案（Workspace/Solution）  
----------------  

创建新项目时，许多IDE会自动将项目加入"工作区"或"解决方案"（术语因IDE而异）。工作区/解决方案是容纳一个或多个相关项目的容器。例如开发游戏时，若需分别为单人与多人模式创建可执行文件，就需要两个项目。这些项目显然不应完全独立——毕竟同属一个游戏。通常会将每个项目配置为同一解决方案中的独立项目。  

尽管可以向解决方案添加多个项目，但我们建议为每个程序新建工作区/解决方案（尤其在学习阶段）。这样更简单且减少出错几率。  

编写第一个程序  
----------------  

传统上，程序员在新语言中的第一个程序是著名的[hello world程序](https://en.wikipedia.org/wiki/Hello_world)，我们也将延续这一传统！您以后会感谢这个决定的。或许。  

在Visual Studio 2019（或更新版本）中创建项目  
----------------  

启动Visual Studio 2019（或更新版本）后，您将看到如下对话框：  
![Visual Studio 2019 初始对话框](https://www.learncpp.com/images/CppTutorial/Chapter0/VS2019-GetStarted-min.png)  
选择*创建新项目*。  

随后出现如下对话框：  
![Visual Studio 2019 新建项目对话框](https://www.learncpp.com/images/CppTutorial/Chapter0/VS2019-CreateNewProject-min.png)  
若已打开其他项目，可通过*文件菜单 > 新建 > 项目*访问此对话框。  

选择*Windows桌面向导*并点击*下一步*。若未找到此选项，可能安装Visual Studio时未选择*使用C++的桌面开发*工作负载。此时请返回[0.6节](Chapter-0/lesson0.6-installing-an-integrated-development-environment-ide.md)按指引重新安装（注意：无需完全重装，可运行Visual Studio安装程序修改现有安装以添加C++工作负载）。  

接下来配置新项目：  
![Visual Studio 2019 配置新项目对话框](https://www.learncpp.com/images/CppTutorial/Chapter0/VS2019-ConfigureNewProject-min.png)  
将项目名称替换为`HelloWorld`。  

建议勾选*将解决方案和项目放在同一目录*以减少子目录层级。点击*创建*继续。  

最后设置项目选项：  
![Visual Studio 2019 项目选项对话框](https://www.learncpp.com/images/CppTutorial/Chapter0/VS2019-PrecompiledHeader-min.png)  
确保*应用程序类型*设为*控制台应用程序(.exe)*，取消*预编译头*选项后点击*确定*。  

至此项目创建完成！跳转至下方[Visual Studio解决方案资源管理器](#visual_studio_solution_explorer)继续操作。  

> **问：什么是预编译头？为何禁用？**  
> 在大型项目（含多个代码文件）中，预编译头通过避免冗余编译可提升编译速度。但使用预编译头需额外配置，对小项目（如本教程的示例）提升不明显。因此建议初学者禁用，待编译时间过长时再启用。  

在Visual Studio 2017及更早版本中创建项目  
----------------  

通过*文件菜单 > 新建 > 项目*创建新项目。弹出对话框如下：  
![Visual Studio 2017 新建项目对话框](https://www.learncpp.com/images/CppTutorial/Chapter0/VS2017-NewProject-min.png)  
首先确保左侧选中*Visual C++*。若未显示，请参照前文检查安装配置。  

Visual Studio 2017 v15.3及更新版本用户：在*Visual C++*下选择*Windows桌面*，在主窗口选择*Windows桌面向导*。  

旧版本用户：选择*Win32*及*Win32控制台应用程序*。  

在下方*名称*栏输入`HelloWorld`，位置栏可选不同存储路径。点击*确定*后，旧版本会启动Win32应用程序向导，点击*下一步*。  

设置向导界面：  
![Visual Studio 2017 桌面向导](https://www.learncpp.com/images/CppTutorial/Chapter0/VS2017-DesktopWizard-min.png)  
取消勾选*预编译头*后点击*完成*。  

解决方案资源管理器（Solution Explorer）  
----------------  

窗口左侧或右侧的*解决方案资源管理器*中，Visual Studio已创建解决方案（*解决方案'HelloWorld'*），其内加粗显示的项目即新建的*HelloWorld*。项目中，Visual Studio已生成若干文件，包括*HelloWorld.cpp*（位于*源文件*目录下）。其他.cpp或.h文件可暂时忽略。  
![Visual Studio 2019 初始窗口](https://www.learncpp.com/images/CppTutorial/Chapter0/VS2019-Initial-min.png)  

文本编辑器中，Visual Studio已打开*HelloWorld.cpp*并生成默认代码。请全选删除后输入：  
```cpp
#include <iostream>

int main()
{
	std::cout << "Hello, world!";
	return 0;
}
```  

按*F7*（或*Ctrl+Shift+B*）或通过*生成菜单 > 生成解决方案*编译。成功时输出窗口显示：  
```
1>------ 已启动生成: 项目: HelloWorld, 配置: Debug Win32 ------
1>HelloWorld.cpp
1>HelloWorld.vcxproj -> c:\users\alex\documents\visual studio 2017\Projects\HelloWorld\Debug\HelloWorld.exe
========== 生成: 1 成功，0 失败，0 最新，0 跳过 ==========
```  

> **问：出现C1010错误（"找不到预编译头"）怎么办？**  
> 创建项目时未禁用预编译头。请按前文指引重新创建项目并禁用该选项。  

按*Ctrl+F5*或*调试菜单 > 开始执行(不调试)*运行程序，将看到：  
![程序运行](https://www.learncpp.com/images/CppTutorial/Chapter0/VC2005-Run-min.png)  

> **相关说明**  
> 从Visual Studio直接运行程序时，可能看到额外输出行（如进程退出代码），这属于正常现象。详见[2.2节](Chapter-2/lesson2.2-function-return-values-value-returning-functions.md)。  

在Code::Blocks中创建项目  
----------------  

通过*文件菜单 > 新建 > 项目*创建新项目，选择*控制台应用程序*：  
![Code::Blocks 项目对话框](https://www.learncpp.com/images/CppTutorial/Chapter0/CB-Project-min.png)  
向导中确保选择C++，项目命名为`HelloWorld`，建议保存路径如`C:\CBProjects`。配置默认即可。  

工作区管理窗口显示项目结构：  
![Code::Blocks 工作区](https://www.learncpp.com/images/CppTutorial/Chapter0/CB2017-Save-min.png)  
展开*Sources*目录双击"main.cpp"，替换默认代码为：  
```cpp
#include <iostream>

int main()
{
	std::cout << "Hello, world!";
	return 0;
}
```  

按*Ctrl+F9*或*生成菜单 > 生成*编译。成功时生成日志显示：  
```
-------------- 生成: Debug in HelloWorld (编译器: GNU GCC Compiler)---------------
mingw32-g++.exe -Wall -fexceptions -g -std=c++14  -c C:\CBProjects\HelloWorld\main.cpp -o obj\Debug\main.o
mingw32-g++.exe  -o bin\Debug\HelloWorld.exe obj\Debug\main.o   
输出文件 bin\Debug\HelloWorld.exe 大小1.51 MB
生成状态: 0 (0分0秒)
0错误, 0警告 (0分0秒)
```  

按*Ctrl+F10*或*生成菜单 > 运行*执行程序。  

> **Linux用户注意**  
> 可能需要额外安装软件包，详见[0.6节](Chapter-0/lesson0.6-installing-an-integrated-development-environment-ide.md)。  

在VS Code中创建项目  
----------------  

通过*查看 > 资源管理器*（*Ctrl+Shift+E*）打开资源管理器窗格，点击*打开文件夹*新建`HelloWorld`文件夹作为项目目录。  

新建文件*main.cpp*并输入代码：  
```cpp
#include <iostream>

int main()
{
	std::cout << "Hello, world!";
	return 0;
}
```  

通过*运行 > 启动调试*或点击播放图标旁的下拉箭头选择*运行C/C++文件*，选择*g++生成并调试活动文件*（macOS选*clang++*）。在底部切换至*终端*标签查看输出。  

使用命令行g++编译  
----------------  

将代码保存为HelloWorld.cpp后执行：  
```bash
g++ -o HelloWorld HelloWorld.cpp
./HelloWorld
```  

其他IDE或在线编译器  
----------------  

需自行完成：  
1. 创建控制台项目（仅IDE）  
2. 添加.cpp文件（若未自动生成）  
3. 粘贴代码  
4. 编译运行  

编译失败处理  
----------------  

1. 查看错误信息定位问题行  
2. 参考[0.8节](Chapter-0/lesson0.8-a-few-common-cpp-problems.md)常见问题  
3. 查看对应课程的评论区  
4. 搜索引擎查询错误信息  

程序运行后控制台窗口闪退  
----------------  

在main()函数返回前添加：  
```cpp
#include <limits>
// ...
std::cin.clear();
std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
std::cin.get();
```  

避免使用`system("pause")`等平台相关方案。若杀毒软件拦截程序，可暂时禁用或将项目目录加入白名单。  

编译相关术语解析  
----------------  

* **生成（Build）**：编译修改过的文件并链接  
* **清理（Clean）**：删除缓存文件  
* **重新生成（Rebuild）**：清理后生成  
* **编译（Compile）**：仅编译单个文件  
* **运行/启动（Run/Start）**：执行程序（部分IDE会先自动生成）  

总结  
----------------  

恭喜完成最难部分（安装IDE并编译首个程序）！若对Hello World代码存在疑问，下一章将逐行详解。  

[下一课 0.8 — 常见C++问题](Chapter-0/lesson0.8-a-few-common-cpp-problems.md)  
[返回主页](/)  
[上一课 0.6 — 安装集成开发环境(IDE)](Chapter-0/lesson0.6-installing-an-integrated-development-environment-ide.md)