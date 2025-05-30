9.1 — 代码测试简介  
========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2016年9月8日下午2:06（PDT）首次发布，2024年4月30日更新  

当你编写完一个程序，它成功编译并看似正常运行时，接下来该做什么？

这取决于具体情况。若程序只需运行一次即可丢弃，那么任务已完成。此时即使程序不能处理所有用例也无妨——只要满足当前需求即可。  

若程序完全线性（无条件分支如if语句或switch语句），无需输入且输出正确，则可能已完成开发。通过运行程序并验证输出即完成整体测试。建议在不同系统上编译运行以确保行为一致性（若结果不同，可能存在未定义行为（undefined behavior）恰好在初始系统上正常工作的情况）。  

但多数情况下，程序需多次运行，包含循环与条件逻辑，并接收用户输入。可能编写了可在未来复用的函数，甚至经历了范围蔓延（scope creep）——添加了超出初始规划的功能。若需分发程序给他人（可能尝试你未曾想到的操作），则必须验证程序在各种条件下的行为符合预期——这需要主动测试。  

程序在某组输入下正常工作，并不代表所有情况都能正确处理。  

**软件测试**（software testing，亦称软件验证（software validation））是确认软件是否按预期工作的过程。  

测试挑战  
----------------  

在讨论实用测试方法前，先了解为何全面测试程序具有挑战性。  

考虑这个简单程序：  

```cpp
#include <iostream>

void compare(int x, int y)
{
    if (x > y)
        std::cout << x << " 大于 " << y << '\n'; // 情况1
    else if (x < y)
        std::cout << x << " 小于 " << y << '\n'; // 情况2
    else
        std::cout << x << " 等于 " << y << '\n'; // 情况3
}

int main()
{
    std::cout << "输入数字：";
    int x{};
    std::cin >> x;

    std::cout << "输入另一数字：";
    int y{};
    std::cin >> y;

    compare(x, y);

    return 0;
}
```  

假设使用4字节整型，穷举测试所有输入组合需要运行程序18,446,744,073,709,551,616次（约180亿亿次），显然不可行！  

每次请求用户输入或代码包含条件分支时，程序可能的执行路径数量呈指数级增长。除最简程序外，穷举测试所有输入组合几乎立即变得不可行。  

直觉告诉我们无需执行180亿亿次测试。若情况1在某个x > y的用例中有效，则应对所有x > y的用例均有效。由此，实际只需运行程序三次（分别触发compare()函数的三种情况）即可获得高置信度。类似技巧可大幅减少必要测试次数。  

测试方法论内容丰富，但因其非C++专属主题，我们仅从开发者角度简要介绍。后续章节将讨论测试代码时的实用考量。  

模块化测试  
----------------  

设想汽车制造商建造概念车时选择哪种方案：  
a) 单独测试每个部件，验证后集成并重测，最后整体测试  
b) 直接组装所有部件，最后统一测试  

显然选项a更优，但许多新手程序员却采用b方式！  

在情况b中，任何部件故障都需全车诊断——问题可能存在于任何位置。症状可能对应多种原因（如无法启动可能是火花塞、电池或燃油泵故障）。这导致大量时间浪费在定位问题，且改动可能引发连锁反应。  

情况a通过逐步测试将问题控制在最小范围。部件集成前已通过独立测试，集成后立即重测，问题可被早期发现。整车组装完成后，已有足够信心正常运行，意外问题风险被最小化。  

此类比适用于编程。编写小函数（或类）后立即编译测试更为高效。若出错，只需检查最近改动的小段代码，节省调试时间。  

将代码单元隔离测试以确保正确性的过程称为**单元测试（unit testing）**。每个**单元测试用例（unit test case）**旨在验证代码单元的特定行为。  

> **最佳实践**  
> 以定义明确的小单元（函数或类）编写程序，频繁编译并持续测试。  

短程序接受用户输入时，尝试多种输入可能足够。但随着程序增长，需在集成前测试单个函数或类。  

非正式测试  
----------------  

可在编码时进行非正式测试。编写代码单元（函数、类等）后，添加测试代码并在通过后删除。例如测试isLowerVowel()函数：  

```cpp
#include <iostream>

// 待测试函数（为简化忽略'y'有时作为元音的情况）
bool isLowerVowel(char c)
{
    switch (c)
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
        return true;
    default:
        return false;
    }
}

int main()
{
    // 临时测试代码
    std::cout << isLowerVowel('a') << '\n'; // 应输出1
    std::cout << isLowerVowel('q') << '\n'; // 应输出0

    return 0;
}
```  

若输出1和0则通过。可推断函数能处理其他元音（'e','i','o','u'），删除测试代码后继续开发。  

测试代码留存  
----------------  

临时测试虽便捷，但无法满足未来重测需求。修改函数后需确保原有功能正常，建议将测试代码移至专用函数：  

```cpp
#include <iostream>

bool isLowerVowel(char c) { /* 同上 */ }

// 当前未调用，供未来重测
void testVowel()
{
    std::cout << isLowerVowel('a') << '\n';
    std::cout << isLowerVowel('q') << '\n';
}

int main()
{
    return 0;
}
```  

新增测试用例时，只需添加到testVowel()函数。  

自动化测试  
----------------  

手动验证结果存在缺陷，改进方案：  

```cpp
#include <iostream>

bool isLowerVowel(char c) { /* 同上 */ }

// 返回失败测试编号（全部通过时返回0）
int testVowel()
{
    if (!isLowerVowel('a')) return 1;
    if (isLowerVowel('q')) return 2;

    return 0;
}

int main()
{
    int result { testVowel() };
    if (result != 0)
        std::cout << "testVowel()测试" << result << "失败\n";
    else
        std::cout << "testVowel()测试通过\n";

    return 0;
}
```  

随时调用testVowel()可验证代码完整性，返回0表示通过，非零值指示失败用例。这对修改旧代码尤为重要！  

> **进阶技巧**  
> 使用断言（assert）可在测试失败时中止程序并报错，避免处理测试编号：  

```cpp
#include <cassert> // assert
#include <cstdlib> // std::abort
#include <iostream>

bool isLowerVowel(char c) { /* 同上 */ }

// 测试失败时中止程序
int testVowel()
{
#ifdef NDEBUG
    // 若NDEBUG定义（断言被禁用），终止程序
    std::cerr << "测试需启用断言";
    std::abort();
#endif

    assert(isLowerVowel('a'));
    assert(isLowerVowel('e'));
    // 更多断言...
    assert(!isLowerVowel('z'));

    return 0;
}

int main()
{
    testVowel();
    std::cout << "所有测试通过\n";
    return 0;
}
```  

断言（assert）详见课程[9.6 — 断言与静态断言](Chapter-9/lesson9.6-assert-and-static_assert.md)。  

单元测试框架  
----------------  

由于编写测试函数十分常见，**单元测试框架**（unit testing frameworks）应运而生，可简化测试用例的编写、维护和执行。因涉及第三方软件，此处不作详述。  

集成测试  
----------------  

各单元通过独立测试后，需集成到程序中重测以确保整合正确，此过程称为**集成测试（integration testing）**。集成测试更复杂——目前通过运行程序并抽查集成单元的行为即可。  

测验时间  
----------------  

**问题1**  
应何时开始测试代码？  
  
<details><summary>答案</summary>在编写完任何非平凡函数后立即开始测试。</details>  

[下一课 9.2 代码覆盖率](Chapter-9/lesson9.2-code-coverage.md)  
[返回主页](/)  
[上一课 8.x 第8章总结与测验](Chapter-8/lesson8.x-chapter-8-summary-and-quiz.md)