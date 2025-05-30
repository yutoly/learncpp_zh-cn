0.10 — 配置编译器：编译器扩展  
================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2018年9月19日 PDT上午9:57  
2024年10月25日  

C++标准定义了程序在特定场景下的行为规则。大多数情况下，编译器会遵循这些规则。然而，许多编译器会对语言进行自定义修改（通常用于增强与其他语言版本的兼容性，如C99，或出于历史原因）。这些编译器特有的行为称为**编译器扩展（compiler extensions）**。  

使用编译器扩展编写的程序可能导致与C++标准不兼容。依赖非标准扩展的程序通常无法在其他编译器（不支持相同扩展）上编译，即使编译成功也可能运行异常。  

令人困扰的是，编译器扩展往往默认启用。这对新手尤其不利，他们可能误认为某些有效行为属于官方C++标准，而实际上只是编译器过于宽松。  

由于编译器扩展并非必需，且会导致程序不符合C++标准，我们建议禁用编译器扩展。  

最佳实践  
----------------  
禁用编译器扩展以确保程序（及编码实践）符合C++标准，并能在任意系统上运行。  

禁用编译器扩展  
----------------  

Visual Studio用户  
----------------  
1. 在*解决方案资源管理器*窗口中右键单击项目名称，选择*属性*  
![解决方案资源管理器属性](https://www.learncpp.com/images/CppTutorial/Chapter0/VS-SolutionExplorerProperties-min.png)  
2. 在项目对话框中，确保*配置*字段设为*所有配置*  
3. 导航至*C/C++ > 语言*标签页  
4. 将*符合性模式*设为*是 (/permissive-)*（若非默认值）  
![禁用语言扩展](https://www.learncpp.com/images/CppTutorial/Chapter0/VS-DisableExtensions-min.png)  

Code::Blocks用户  
----------------  
1. 通过*设置菜单 > 编译器 > 编译器标志*标签页  
2. 查找并勾选*-pedantic-errors*选项  
![禁用语言扩展](https://www.learncpp.com/images/CppTutorial/Chapter0/CB-Pedantic-min.png)  

gcc与Clang用户  
----------------  
在编译命令行中添加*-pedantic-errors*标志  

VS Code用户  
----------------  
1. 打开tasks.json文件，定位到`"args"`部分  
2. 在`"${file}"`行上方添加新行：  
```json
"-pedantic-errors",
```  
3. 启用自动添加文件末尾换行符：  
   - 进入*文件（Mac系统为Code）> 首选项 > 设置*  
   - 搜索`insert final newline`  
   - 在*工作区设置*和*用户设置*标签页勾选*Files: Insert Final Newline*  

相关内容  
----------------  
Xcode用户可参考[Rory的评论](configuring-your-compiler-compiler-extensions/comment-page-1/#comment-446983)获取配置指南  

重要提示  
----------------  
这些设置基于项目单独生效。每次创建新项目时需重新配置，或创建包含这些设置的模板项目以供复用。  

[下一课 0.11 — 配置编译器：警告与错误等级](Chapter-0/lesson0.11-configuring-your-compiler-warning-and-error-levels.md)  
[返回主页](/)  
[上一课 0.9 — 配置编译器：生成配置](Chapter-0/lesson0.9-configuring-your-compiler-build-configurations.md)