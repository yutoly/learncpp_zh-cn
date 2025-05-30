3.10 — 在问题显现前发现隐患  
==================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年10月14日（首次发布于2019年2月1日）  

当出现语义错误（semantic error）时，可能在程序运行时立即被发现，也可能长期潜伏。新代码的引入或环境变化可能突然触发这些隐患。错误在代码库中存在越久，就越难定位——原本易修复的问题可能演变成耗时费力的调试噩梦。  

应对策略  
----------------  

### 避免错误  
最佳策略是预防错误发生，以下方法可降低出错概率：  
* 遵循最佳实践  
* 避免在疲惫或情绪低落时编程，适当休息  
* 熟悉语言常见陷阱（所有我们警示的注意事项）  
* 控制函数长度  
* 优先使用标准库而非自编代码  
* 充分添加注释  
* 从简单方案入手，逐步增加复杂度  
* 避免晦涩/非直观的解决方案  
* 优先考虑可读性与可维护性，而非性能  

> "调试的难度是初次编写代码的两倍。如果你在编码时竭尽所能地展现聪明才智，将来如何调试？"  
> ——Brian Kernighan，《编程风格要素》第二版  

### 代码重构（refactoring）  
随着程序功能扩展（"行为变更"），某些函数会逐渐变长。冗长的函数会增加复杂性和理解难度。  

解决方案是将长函数拆分为多个短函数。这种在不改变行为的前提下调整代码结构的做法称为**重构（refactoring）**。重构通过提升组织性与模块化来降低复杂度。  

函数长度标准：  
* 超过一屏垂直高度的函数通常过长（需滚动查看会显著降低可读性）  
* 理想长度应小于十行  
* 小于五行的函数更优  

**关键原则**  
修改代码时，单独实施行为变更或结构调整，并重新测试。同时进行两种修改会增加错误风险，且更难定位问题。  

防御性编程（defensive programming）简介  
----------------  

错误不仅源于自身编写（如逻辑错误），也可能因用户非常规操作触发。例如要求输入整数时用户输入字母，若未做错误处理，程序可能表现异常。  

**防御性编程**即预先考虑软件可能被终端用户或其他开发者（包括自身）误用的所有方式，通过检测和缓解措施（如提示用户重新输入错误数据）来应对。  

提升错误发现速度  
----------------  

### 函数测试  
通过编写测试函数验证代码功能是常用方法。以下是示例（演示用途）：  
```cpp
#include <iostream>

int add(int x, int y)
{
	return x + y;
}

void testadd()
{
	std::cout << "预期输出：2 0 0 -2\n";
	std::cout << add(1, 1) << ' ';
	std::cout << add(-1, 1) << ' ';
	std::cout << add(1, -1) << ' ';
	std::cout << add(-1, -1) << ' ';
}

int main()
{
	testadd();
	return 0;
}
```  
`testadd()`通过多组参数测试`add()`函数。若输出符合预期，则函数可信。保留此测试函数可在修改`add`时快速验证功能完整性。  

这是**单元测试（unit testing）**的初级形式——通过测试源代码的最小单元确保正确性。  

### 约束检查（constraints）  
通过添加额外代码（可在非调试版本中移除）验证假设条件。例如计算阶乘的函数应检查参数非负：  
```cpp
int factorial(int n)
{
    // 检查非负参数
    if (n < 0)
        return -1; // 错误码
    
    // 正常计算逻辑
    // ...
}
```  
常用方法包括`assert`和`static_assert`（详见课程[9.6 — Assert与static_assert](Chapter-9/lesson9.6-assert-and-static_assert.md)）。  

### 静态分析工具（static analysis tools）  
程序员常犯特定类型错误，可通过**静态分析工具**（又称linters）检测。这类工具分析源代码寻找潜在语义问题（"静态"指不执行代码的分析）。  

编译器本身即具备基础静态分析功能（如检测未初始化变量）。建议调高编译器告警级别（参见课程[0.11 — 编译器配置：警告与错误级别](Chapter-0/lesson0.11-configuring-your-compiler-warning-and-error-levels.md)）。  

**推荐工具**  
免费：  
* [clang-tidy](https://clang.llvm.org/extra/clang-tidy/)  
* [cpplint](https://github.com/cpplint/cpplint)  
* [cppcheck](https://cppcheck.sourceforge.io/)（已集成至Code::Blocks）  
* [SonarLint](https://www.sonarsource.com/open-source-editions/)  

付费（开源项目可能免费）：  
* [Coverity](https://www.synopsys.com/software-integrity/security-testing/static-analysis-sast.html)  
* [SonarQube](https://www.sonarsource.com/products/sonarqube/)  

**最佳实践**  
在大型项目中使用静态分析工具，可发现数十至数百个潜在问题。  

Visual Studio用户提示  
----------------  
2019版起内置静态分析工具，路径：*生成 > 对解决方案运行代码分析 (Alt+F11)*  

[下一课 3.x — 第3章总结与测验](Chapter-3/lesson3.x-chapter-3-summary-and-quiz.md)  
[返回主页](/)  
[上一课 3.9 — 使用集成调试器：调用栈](Chapter-3/lesson3.9-using-an-integrated-debugger-the-call-stack.md)