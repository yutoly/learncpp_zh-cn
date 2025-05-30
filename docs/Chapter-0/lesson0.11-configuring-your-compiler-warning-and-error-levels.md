0.11 — 配置编译器：警告与错误等级  
===========================================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2018年9月19日上午9:58（太平洋夏令时）  
2025年3月17日  

编写程序时，编译器会检查您是否遵守C++语言的规则（假设已按课程[0.10 — 配置编译器：编译器扩展](Chapter-0/lesson0.10-configuring-your-compiler-compiler-extensions.md)关闭了编译器扩展）。若您的代码明确违反语言规则，则程序属于**病态形式（ill-formed）**。  

当编译器检测到问题时，通常会发出**诊断信息（diagnostic message）**（简称**诊断（diagnostic）**）。C++标准未规定诊断信息的分类、措辞或这些问题对程序编译的影响方式。但现代编译器普遍遵循以下惯例：  

* **诊断错误（diagnostic error）**（简称**错误（error）**）：编译器决定中止编译，可能因无法继续或认为错误严重需要停止。编译器生成的诊断错误常被称为**编译错误（compilation errors）**、**编译器错误（compiler errors）**或**编译错误（compile errors）**。  
* **诊断警告（diagnostic warning）**（简称**警告（warning）**）：编译器决定不中止编译，仅忽略问题继续编译。  

> **关键洞察**  
> 编译器决定非阻塞性问题归类为警告还是错误。虽多数情况下分类一致，但不同编译器可能对同一问题采取不同处理——某编译器报错而另一编译器仅警告。  

诊断信息通常包含文件名、行号及问题描述，帮助定位问题。实际错误可能出现在该行或前几行。修复问题后重新编译即可验证诊断信息是否消失。  

某些情况下，编译器可能发现代码虽未违反语言规则，但疑似存在问题。此时会发出警告提醒程序员。可通过修复警告指出的问题或重构代码来消除警告。  

> **进阶阅读**  
> 我们将在课程[7.7 — 外部链接与变量前向声明（external linkage and variable forward declarations）](Chapter-7/lesson7.7-external-linkage-and-variable-forward-declarations.md)中展示合法但编译器认为可疑的语句示例。  
>  
> 极少数情况下，需明确告知编译器忽略特定警告。C++无官方支持方式，但许多编译器（如Visual Studio和GCC）通过非标准#pragma指令提供临时禁用警告的解决方案。  

> **最佳实践**  
> 勿让警告堆积。发现警告应立即处理（如同处理错误），否则严重警告可能淹没在非关键警告中。  

链接器（linker）在链接过程中遇到不可修复的问题时，也可能生成诊断错误。  

 
提升警告等级  
----------------  

默认情况下，多数编译器仅生成最明显问题的警告。但可要求编译器更积极地提供警告，这对学习阶段尤其重要。  

> **最佳实践**  
> 提升警告等级，学习阶段更应如此。额外的诊断信息有助于发现导致程序故障的错误。  

  
**Visual Studio用户**  
右击*解决方案资源管理器*中的项目名，选择*属性*：  

![解决方案资源管理器属性](https://www.learncpp.com/images/CppTutorial/Chapter0/VS-SolutionExplorerProperties-min.png)  
在*项目属性*对话框中：  
1. 确保*配置*字段设为*所有配置*  
2. 选择*C/C++ > 常规*标签页  
3. 设置*警告等级*为*等级4 (/W4)*  

![启用等级4警告](https://www.learncpp.com/images/CppTutorial/Chapter0/VS-EnableAllWarnings-min.png)  
注意：勿选*启用所有警告 (/Wall)*，否则会收到大量C++标准库生成的警告。  

Visual Studio默认禁用有符号/无符号转换警告，建议启用：  
1. 在*C/C++ > 命令行*标签页的*附加选项*中添加`/w44365`  
2. 在*C/C++ > 外部包含*标签页设置*外部头文件警告等级*为*等级3 (/external:W3)*  

配置正确时，编译以下程序应生成C4365警告：  

```cpp
void foo(int)
{  
}

int main()
{
    unsigned int x { 5 };
    foo(x);
    return 0;
}
```  

若未看到警告，请检查*输出*和*错误列表*标签页。  

**Code::Blocks用户**  
通过*设置菜单 > 编译器 > 编译器设置*标签页勾选：  
* \-Wall  
* \-Weffc++  
* \-Wextra  

![启用所有警告](https://www.learncpp.com/images/CppTutorial/Chapter0/CB-EnableAllWarnings-min.png)  
在*其他编译器选项*标签页添加：  
`-Wconversion -Wsign-conversion`  

![添加-Wsign-conversion](https://www.learncpp.com/images/CppTutorial/Chapter0/CB-OtherCompilerFlags-min.png)  

**gcc用户**  
命令行添加标志：  
`-Wall -Weffc++ -Wextra -Wconversion -Wsign-conversion`  

**VS Code用户**  
在tasks.json文件中找到"args"部分，在`"${file}"`行前添加：  

```json
"-Wall",
"-Weffc++",
"-Wextra",
"-Wconversion",
"-Wsign-conversion",
```  


将警告视为错误  
----------------  

可配置编译器将所有警告视为错误（发现警告即停止编译）。这有助于强制解决所有警告问题。  

> **最佳实践**  
> 启用"将警告视为错误"，强制解决所有警告问题。  

**Visual Studio用户**  
右击项目选择*属性*，在*C/C++ > 常规*标签页设置*将警告视为错误*为*是 (/WX)*。  

![将警告视为错误](https://www.learncpp.com/images/CppTutorial/Chapter0/VS-WarningsAsErrors-min.png)  

**Code::Blocks用户**  
在*其他编译器选项*标签页添加`-Werror`。  

**gcc用户**  
命令行添加标志：`-Werror`  

**VS Code用户**  
在tasks.json的`"${file}"`行前添加：  

```json
"-Werror",
```  

[下一课 0.12 — 配置编译器：选择语言标准](Chapter-0/lesson0.12-configuring-your-compiler-choosing-a-language-standard.md)  
[返回主页](/)  
[上一课 0.10 — 配置编译器：编译器扩展](Chapter-0/lesson0.10-configuring-your-compiler-compiler-extensions.md)