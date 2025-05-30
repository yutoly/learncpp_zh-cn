0.9 — 配置编译器：生成配置  
======================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年9月5日（首次发布于2015年2月17日）  

**生成配置（build configuration）**（也称**生成目标（build target）**）是决定集成开发环境（IDE）如何构建项目的设置集合。该配置通常包含可执行文件命名规则、IDE搜索代码/库文件的目录结构、调试信息保留策略、编译器优化等级等设置。除非有特殊需求，建议保持默认设置。  

创建新项目时，多数IDE会预设两种生成配置：**发布配置（release configuration）**与**调试配置（debug configuration）**。  

**调试配置（debug configuration）**专为程序调试设计，通常是开发阶段的首选配置。该配置关闭所有优化并包含调试信息，虽然会增大程序体积、降低运行速度，但极大提升调试便利性。默认情况下，IDE通常选择调试配置作为活动配置。我们将在后续课程详细探讨调试技巧。  

**发布配置（release configuration）**用于程序公开发布版本。该版本通常针对体积和性能进行优化，且不含额外调试信息。由于启用了全部优化选项，此模式也适用于代码性能测试（本教程后续章节将演示具体方法）。  

对比[0.7 — 编译首个程序](Chapter-0/lesson0.7-compiling-your-first-program.md)中的"Hello World"程序：使用Visual Studio调试配置生成的可执行文件为65KB，而发布版本仅12KB。差异主要源于调试配置保留的额外调试信息。  

尽管可以创建自定义生成配置，但除非需要对比不同编译器设置的效果，通常无需自定义配置。  

> **最佳实践**  
> 开发阶段使用*调试*配置，发布可执行文件或性能测试时切换至*发布*配置。  

部分IDE（如Visual Studio）还会为不同平台创建独立生成配置。例如，Visual Studio会为x86（32位）和x64（64位）平台分别创建配置。  

切换生成配置  
----------------  

**Visual Studio用户**  
通过*标准工具栏选项*中的*解决方案配置*下拉菜单直接切换：  
![VS解决方案配置下拉菜单](https://www.learncpp.com/images/CppTutorial/Chapter0/VS-BuildTarget-min.png)  
建议当前阶段选择*调试*。  

也可通过*生成菜单 > 配置管理器*访问配置管理对话框，修改*活动解决方案配置*。*解决方案配置*下拉菜单右侧的*解决方案平台*菜单支持x86（32位）与x64（64位）平台切换。  

**Code::Blocks用户**  
在*编译器工具栏*的*生成目标*下拉菜单中选择：  
![Code::Blocks生成目标下拉菜单](https://www.learncpp.com/images/CppTutorial/Chapter0/CB-BuildTarget-min.png)  
建议当前阶段选择*调试*。  

**gcc与Clang用户**  
调试构建添加`-ggdb`参数，发布构建使用`-O2 -DNDEBUG`参数。当前阶段请使用调试配置。  

对于GCC/Clang，`-O#`选项控制优化等级：  
* `-O0`：调试构建推荐等级（禁用优化），默认设置  
* `-O2`：发布构建推荐等级（启用普适性优化）  
* `-O3`：在`-O2`基础上增加可能提升性能的额外优化（需实测验证效果）  

详见[GCC优化选项文档](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)。  

**VS Code用户**  
首次运行程序时，资源管理器面板的*.vscode*文件夹下会生成*tasks.json*文件。找到*"args"*字段中的*"${file}"*行：  
- 调试构建：在*"${file}"*上方添加`"-ggdb",`  
- 发布构建：添加：  
  `"-O2",`  
  `"-DNDEBUG",`  

修改生成配置  
----------------  

后续课程将演示如何调整生成配置设置。修改项目设置时，建议在所有配置中进行相同变更，这能避免误改错误配置，并确保切换配置时设置仍生效。  

> **重要提示**  
> 更新项目设置时，请对所有生成配置进行相同修改（除非存在特殊原因）。  

[下一课 0.10 — 配置编译器：编译器扩展](Chapter-0/lesson0.10-configuring-your-compiler-compiler-extensions.md)  
[返回主页](/)  
[上一课 0.8 — 常见C++问题](Chapter-0/lesson0.8-a-few-common-cpp-problems.md)