9.6 — 断言（assert）与静态断言（static_assert）
================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年11月2日（首次发布于2017年5月14日）  

在接收参数的函数中，调用者可能传入语法有效但语义无意义的参数。例如前文课程（[9.4 — 错误检测与处理](Chapter-9/lesson9.4-detecting-and-handling-errors.md)）中展示的示例函数：
```
void printDivision(int x, int y)
{
    if (y != 0)
        std::cout << static_cast<double>(x) / y;
    else
        std::cerr << "错误：不能除以零\n";
}
```
该函数显式检查`y`是否为`0`，因为除以零是语义错误，执行会导致程序崩溃。前文课程中讨论过两种处理方式：终止程序或跳过错误语句。但两种方案都有缺陷：跳过语句属于静默失败，这在开发调试阶段尤其不利，因为会掩盖真正问题。即使打印错误信息，也可能淹没在输出中难以定位。

若通过`std::exit`终止程序，将丢失调用栈和调试信息。此时`std::abort`更合适，开发者可调试程序中止点。

前置条件、不变量与后置条件
----------------

**前置条件（precondition）**指代码段执行前必须满足的条件（通常指函数体）。上例中`y != 0`检查就是确保除法运算前`y`非零的前置条件。

函数前置条件的最佳实践是置于函数顶部，未满足时立即返回：
```
void printDivision(int x, int y)
{
    if (y == 0) // 处理前置条件
    {
        std::cerr << "错误：不能除以零\n";
        return; // 返回调用者
    }

    // 此时已知y != 0
    std::cout << static_cast<double>(x) / y;
}
```
（可选阅读）这种模式称为"保镖模式（bouncer pattern）"——检测到错误立即返回。其优势在于：
1. 所有测试条件前置，错误处理集中
2. 减少代码嵌套

**不变量（invariant）**指代码执行期间必须保持为真的条件，常见于循环控制。**后置条件（postcondition）**指代码执行后必须满足的条件，本例无后置条件。

断言（Assert）
----------------

通过条件语句检测无效参数（或验证假设）并终止程序是常见错误检测手段，C++为此提供快捷方式。**断言（assertion）**是程序无bug时应成立的表达式：若表达式为`true`，断言无操作；若为`false`，显示错误信息并终止程序（通过`std::abort`）。错误信息通常包含失败表达式、代码文件和行号，极大辅助调试。

关键洞见：断言用于开发调试阶段的错误检测。断言失败时程序立即停止，可通过调试工具检查程序状态。若未使用断言，错误可能导致后续功能异常且难以定位。

C++运行时断言通过**assert**预处理宏实现，位于\<cassert\>头文件：
```
#include <cassert> // assert()
#include <cmath>   // std::sqrt
#include <iostream>

double calculateTimeUntilObjectHitsGround(double initialHeight, double gravity)
{
  assert(gravity > 0.0); // 仅当重力为正时物体会落地

  if (initialHeight <= 0.0)
    return 0.0;
 
  return std::sqrt((2.0 * initialHeight) / gravity);
}

int main()
{
  std::cout << "耗时：" << calculateTimeUntilObjectHitsGround(100.0, -9.8) << "秒\n";
  return 0;
}
```
调用`calculateTimeUntilObjectHitsGround(100.0, -9.8)`时，`assert(gravity > 0.0)`触发断言失败，输出类似：
```
dropsimulator: src/main.cpp:6: 断言'gravity > 0.0'失败
```
断言虽常用于参数验证，但可应用于任何需要验证条件为真的场景。尽管建议避免预处理宏，但断言是少数推荐使用的特例。

提升断言描述性
----------------
简单断言如`assert(found);`触发时信息有限。可通过逻辑AND添加描述字符串：
```
assert(found && "在数据库中未找到车辆");
```
此技巧有效因为字符串字面值总为`true`，不影响断言逻辑但能增强错误信息：
```
断言失败：found && "在数据库中未找到车辆"，文件Test.cpp第34行
```

未实现功能断言
----------------
断言也可标记未实现的功能分支：
```
assert(moved && "需处理学生换教室的情况");
```
当开发者遇到该情况时，断言失败信息可提示需实现该分支。

NDEBUG宏
----------------
断言检查会产生运行时开销，且正式环境代码应已通过测试。因此通常仅在调试版本启用断言。C++通过`NDEBUG`宏控制断言：若定义该宏，断言失效。

多数IDE在发布配置中默认定义`NDEBUG`。例如Visual Studio的项目预处理器定义包含`NDEBUG`。若需在发布版本启用断言，需手动移除该定义。

提示：可通过在包含头文件前添加`#define NDEBUG`或`#undef NDEBUG`来局部控制断言：
```
#define NDEBUG // 禁用断言（须在#include之前）
#include <cassert>
#include <iostream>

int main()
{
    assert(false); // 已禁用，不会触发
    std::cout << "Hello, world!\n";
    return 0;
}
```

静态断言（static_assert）
----------------
**静态断言（static_assert）**在编译期检查条件，失败导致编译错误。与断言不同，静态断言是关键字，无需包含头文件。其语法：
```
static_assert(条件, 诊断信息);
```
示例：
```
static_assert(sizeof(long) == 8, "long必须为8字节");
static_assert(sizeof(int) >= 4, "int至少4字节");

int main(){ return 0; }
```
编译时将产生错误：
```
错误C2338: long必须为8字节
```
注意事项：
- 条件必须是常量表达式
- 可置于代码任意位置（包括全局命名空间）
- 在发布版本中仍有效
- 无运行时开销

C++17起诊断信息可省略。

断言与错误处理的区别
----------------
断言用于检测开发阶段的编程错误（本不应发生的情况），属程序员责任。断言不处理错误恢复，通常在发布版本被禁用。

错误处理用于应对正式环境中可能出现的（即便罕见）异常情况，需考虑恢复或优雅终止。错误处理涉及运行时开销和开发成本。

最佳实践：
- 断言检测编程错误、错误假设或不应出现的情况
- 错误处理应对正式环境的预期异常
- 二者结合处理不应发生但需优雅失败的情况

断言限制与警告
----------------
1. 断言本身可能编写错误，导致误报或漏报
2. 断言表达式不应有副作用，否则调试版与发布版行为不同
3. `abort()`立即终止程序，不执行清理。因此断言仅适用于终止不会导致数据损坏的场景

[下一课 9.x 第9章总结与测验](Chapter-9/lesson9.x-chapter-9-summary-and-quiz.md)  
[返回主页](/)  
[上一课 9.5 std::cin与无效输入处理](Chapter-9/lesson9.5-stdcin-and-handling-invalid-input.md)