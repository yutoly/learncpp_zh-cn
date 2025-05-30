0.6 — 安装集成开发环境（Integrated Development Environment，IDE）  
=============================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月29日（首次发布于2007年5月28日）  

**集成开发环境（Integrated Development Environment，IDE）**是专为简化程序开发、构建和调试而设计的软件。典型的现代IDE包含以下功能：  
* 便捷加载和保存代码文件的机制  
* 具备编程友好功能的代码编辑器，包括行号显示、语法高亮、集成帮助、名称补全和自动代码格式化  
* 基础构建系统，支持将程序编译链接为可执行文件并运行  
* 集成调试器，便于发现和修复软件缺陷  
* 插件安装机制，可扩展IDE功能或添加版本控制等特性  

部分C++ IDE会为您自动安装配置C++编译器（compiler）和链接器（linker），另一些则允许用户自行插入独立安装的编译工具链。虽然这些工具可单独使用，但安装IDE能通过统一界面完成所有操作，大幅提升效率。  

选择IDE  
----------------  

首要问题是"选择哪款IDE？"。许多IDE免费提供，您可同时安装多款进行体验。以下是我们的推荐方案：  

若您有其他心仪IDE也可使用。本教程展示的概念适用于任何现代IDE，但不同IDE的命名、布局和快捷键可能存在差异，您需自行探索等效功能。  

> **重要提示**  
> 为充分发挥本站价值，建议安装支持至少C++17标准的编译器套件。  
> 若受限于C++14标准（教育或商业约束），多数课程示例仍可运行。但遇到使用C++17（或更新）特性的课程时，需跳过或进行代码转换。  
> 切勿使用不支持C++11标准的编译器（C++11被视为现代C++的最低标准）。  
>  
> 支持C++17的最低编译器版本：  
> * GCC/G++ 7  
> * Clang++ 8  
> * Visual Studio 2017 15.7  

Windows平台：Visual Studio  
----------------  

Windows 10/11用户强烈推荐安装[Visual Studio 2022 Community](https://www.visualstudio.com/downloads/)。  

运行安装程序后，在"工作负载（workload）"选择界面勾选**使用C++的桌面开发**。右侧默认选项通常适用，但请确保勾选**Windows 11 SDK**（或仅有的**Windows 10 SDK**）。Windows 11 SDK应用程序可在Windows 10运行。  

![Visual Studio工作负载选择界面](https://www.learncpp.com/images/CppTutorial/Chapter0/VS2019-Installer-min.png)  

Linux/Windows跨平台：Code::Blocks  
----------------  

Linux开发者（或需编写跨平台程序的Windows用户）推荐使用[Code::Blocks](https://www.codeblocks.org/downloads/binaries/)。这款免费开源跨平台IDE支持Linux和Windows系统。  

**Windows用户注意事项**  
* 下载带MinGW的版本（文件名含*mingw-setup.exe*），该版本集成GCC C++编译器的Windows移植版  
* Code::Blocks 20.03自带的MinGW仅支持C++17标准。如需使用C++20：  
  1. 完成常规安装后关闭IDE  
  2. 进入安装目录（通常为C:\Program Files (x86)\CodeBlocks）  
  3. 将"MinGW"目录重命名为"MinGW.bak"（备份）  
  4. 访问<https://winlibs.com/>下载最新MinGW-w64（选择Release Versions → UCRT Runtime → LATEST → Win64 → without LLVM/Clang/LLD/LLDB → Zip archive）  
  5. 解压"mingw64"至安装目录并重命名为"MinGW"  
  6. 确认新编译器工作后删除旧目录  

![Code::Blocks MinGW Windows下载选项](https://www.learncpp.com/blog/wp-content/uploads/images/CppTutorial/ide/CB-MinGWDownload-min.png)  

**Linux用户注意事项**  
* Debian系（Mint/Ubuntu）可能需要安装build-essential包：终端执行`sudo apt-get install build-essential`  
* Arch系需安装base-devel包  
* 首次启动时在"编译器自动检测"对话框选择GNU GCC Compiler作为默认编译器  

![编译器自动检测对话框](https://www.learncpp.com/images/CppTutorial/Chapter0/CompilersAutoDetection-min.png)  

> **常见问题**  
> 问：出现"无法在配置的搜索路径中找到GNU GCC编译器的可执行文件"错误怎么办？  
> 答：  
> 1. Windows用户确认下载的是含MinGW的版本  
> 2. 设置→编译器→恢复默认值  
> 3. 检查工具链可执行文件路径是否指向MinGW目录  
> 4. 完全卸载后重装  
> 5. [尝试其他编译器](http://wiki.codeblocks.org/index.php/Installing_a_supported_compiler)  

高级用户选项：Visual Studio Code  
----------------  

**Visual Studio Code**（简称VS Code，非Visual Studio Community）是面向经验开发者的轻量级编辑器，具备跨平台、多语言支持和插件扩展等优势，但配置复杂度较高。  

> **重要警告**  
> 本教程不提供VS Code完整配置指南。VS Code不适合C++新手，已有用户反馈大量配置问题。除非已有使用经验或具备故障排查能力，否则不建议选择此方案。  

**Linux用户**  
* 通过发行版包管理器安装  
* 遵循[Linux C++配置指南](https://code.visualstudio.com/docs/cpp/config-linux)  

**Mac用户**  
* 按[macOS安装指南](https://code.visualstudio.com/docs/setup/mac)操作  
* 配置参考[Mac C++设置说明](https://code.visualstudio.com/docs/cpp/config-clang-mac)  

**Windows用户**  
* 根据[Windows安装指南](https://code.visualstudio.com/docs/setup/windows)安装  
* 配置参考[Windows C++设置说明](https://code.visualstudio.com/docs/cpp/config-mingw)  

Mac其他选择  
----------------  
* [Xcode](https://developer.apple.com/xcode/)（若可用）  
* [Eclipse](https://www.eclipse.org/)（需手动安装C++组件）  

其他常见问题  
----------------  

**问：可以使用在线编译器吗？**  
答：适用于简单练习，推荐：  
* [TutorialsPoint](https://www.tutorialspoint.com/compile_cpp_online.php)  
* [Wandbox](https://wandbox.org/)（支持多版本GCC/Clang）  
* [Godbolt](https://godbolt.org/)（可查看汇编代码）  

但存在功能限制（多文件创建、交互输入、调试支持不足），建议尽快迁移至完整IDE。  

**问：可以使用命令行编译器（如Linux的g++）吗？**  
答：可行但不推荐新手使用。需自行配置编辑器和命令行调试器。  

**问：可以使用Eclipse/Sublime/Notepad++等其他编辑器吗？**  
答：可行但不推荐。这些工具需额外配置，初学者应选择开箱即用的方案。  

应避免的IDE  
----------------  
* Borland Turbo C++ — 不支持C++11  
* Visual Studio for Mac — 不支持C++  
* Dev C++ — 已停止维护  

故障排除  
----------------  
安装失败时：  
1. 卸载IDE并重启  
2. 暂时禁用杀毒软件  
3. 重新安装  
4. 搜索错误信息寻找解决方案  

若问题持续，建议更换IDE或通过搜索引擎查找解决方案。  

下一步  
----------------  
完成IDE安装（或暂时使用在线编译器）后，即可开始编写第一个程序！  

[下一课 0.7 — 编译首个程序](Chapter-0/lesson0.7-compiling-your-first-program.md)  
[返回主页](/)  
[上一课 0.5 — 编译器、链接器与库简介](Chapter-0/lesson0.5-introduction-to-the-compiler-linker-and-libraries.md)