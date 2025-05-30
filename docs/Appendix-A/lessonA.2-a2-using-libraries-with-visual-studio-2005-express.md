A.2 — 在Visual Studio中使用库  
========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月30日 上午10:01（PDT）  
2024年8月22日  

 

使用库的完整流程回顾：  

每个库只需执行一次的操作：  

1. **获取库（Acquire the library）**：从网站下载或通过包管理器获取  
2. **安装库（Install the library）**：解压到某个目录或通过包管理器安装  


每个项目需执行的操作：  

3. 告知编译器库的头文件（header file）位置  
4. 告知链接器预编译库文件（precompiled library file）的位置（如有）  
5. 告知链接器需要链接的静态库（static library）或导入库（import library）文件（如有）  
6. 在程序中通过`#include`包含库的头文件  
7. 确保程序能找到使用的动态库（dynamic library）  


**步骤1和2 — 获取并安装库**  

将库下载并安装到硬盘。更多信息参见教程：[静态库与动态库（static and dynamic libraries）](Appendix-A/lessonA.1-a1-static-and-dynamic-libraries.md)  


**步骤3和4 — 告知编译器头文件与库文件的位置**  

A) 进入项目菜单选择：项目 → 属性（通常在底部）  

B) 在"配置（Configuration）"下拉菜单中，确保选择"所有配置（All configurations）"  

C) 在左侧窗格选择：配置属性（Configuration Properties） → VC++目录（VC++ Directories）  

D) 在"包含目录（Include Directories）"行，添加库的.h文件路径（确保用分号与已有条目分隔）  

E) 在"库目录（Library Directories）"行，添加库文件（.lib）路径（如有）  

F) 点击"确定（OK）"  


**步骤5 — 告知链接器项目使用的库**  

（如有.lib文件需执行此步骤，否则可跳过）  

A) 进入项目菜单选择：项目 → 属性  

B) 在"配置（Configuration）"下拉菜单中，确保选择"所有配置（All configurations）"  

C) 左侧窗格选择：配置属性（Configuration Properties） → 链接器（Linker） → 输入（Input）  

D) 在"附加依赖项（Additional Dependencies）"列表中添加.lib文件名（用分号分隔已有条目）  

E) 点击"确定（OK）"  


**步骤6和7 — 包含头文件与确保程序找到DLL**  

按常规方式在项目中通过`#include`包含库的头文件。  

关于步骤7的详细信息，参见教程：[A1 — 静态库与动态库（Static and dynamic libraries）](Appendix-A/lessonA.1-a1-static-and-dynamic-libraries.md)  


**vcpkg包管理器（package manager）**  

vcpkg是微软开发的包管理器（package manager），可简化C++库的下载、安装、管理和使用流程，并与Visual Studio集成。安装和使用指南请参见[此页面](https://learn.microsoft.com/en-us/vcpkg/get_started/get-started-msbuild?pivots=shell-cmd)。  

[下一课 A.3 — 在Code::Blocks中使用库](Appendix-A/lessonA.3-a3-using-libraries-with-codeblocks.md)  
[返回主页](/)  
[上一课 A.1 — 静态库与动态库](Appendix-A/lessonA.1-a1-static-and-dynamic-libraries.md)