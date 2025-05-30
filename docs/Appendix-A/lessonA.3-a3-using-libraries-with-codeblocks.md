A.3 — 在Code::Blocks中使用库  
=======================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2007年7月3日 PDT下午6:20  
2024年8月22日  

使用库的基本流程回顾：  

每个库只需配置一次：  

1. 获取库：从官网下载或通过包管理器（package manager）安装  
2. 安装库：解压至目录或通过包管理器安装  
3. 告知编译器库的头文件（header file）所在路径  
4. 告知链接器库文件（library file）所在路径（若有）  

每个项目需配置：  

5. 告知链接器需链接的静态库（static library）或导入库（import library）文件（若有）  
6. 在程序中\#include库的头文件  
7. 确保程序能找到使用的动态库（dynamic library）  

**步骤1和2 — 获取与安装库**  
将库下载并安装至硬盘。详情参见[静态与动态库教程](Appendix-A/lessonA.1-a1-static-and-dynamic-libraries.md)。  

**步骤3和4 — 配置头文件与库文件路径**  
以下全局配置将使库对所有项目可用，每个库只需配置一次：  

A) 进入"Settings（设置）"菜单，选择"Compiler（编译器）"  
![](https://www.learncpp.com/images/CppTutorial/AppendixA/CB-SettingsMenu.png)  

B) 点击"Directories（目录）"标签页（默认选中编译器标签）  
C) 点击"Add（添加）"按钮，添加库头文件路径。Linux用户若通过包管理器安装库，需确保已包含*/usr/include*目录  
![](https://www.learncpp.com/images/CppTutorial/AppendixA/CB-CompilerDirectory.png)  

D) 切换至"Linker（链接器）"标签页。点击"Add（添加）"按钮，添加库文件路径（若有）。Linux用户需确保已包含*/usr/lib*目录  
![](https://www.learncpp.com/images/CppTutorial/AppendixA/CB-LinkerDirectory.png)  

E) 点击"OK"确认  

**步骤5 — 配置项目链接库**  
为项目添加库文件（若无则跳过）：  

A) 右击工作区（workspace）中的粗体项目名（默认为"Console application"），选择"Build options（构建选项）"  
![](https://www.learncpp.com/images/CppTutorial/AppendixA/CB-BuildOptions.png)  

B) 切换至"Linker settings（链接器设置）"标签页。在"Link libraries（链接库）"窗口点击"Add（添加）"，选择要链接的库  
![](https://www.learncpp.com/images/CppTutorial/AppendixA/CB-Library.png)  

C) 点击"OK"确认  

**步骤6和7 — 包含头文件与配置动态库路径**  
在项目中\#include库的头文件即可。  

关于步骤7的详细信息，请参考[静态与动态库教程](Appendix-A/lessonA.1-a1-static-and-dynamic-libraries.md)。  

[下一课 A.4 — C++常见问题](Appendix-A/lessonA.4-cpp-faq.md)  
[返回主页](/)  
[上一课 A.2 — 在Visual Studio中使用库](Appendix-A/lessonA.2-a2-using-libraries-with-visual-studio-2005-express.md)