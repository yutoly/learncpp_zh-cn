8.x — 第八章总结与测验  
=================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2015年7月16日 下午2:29（太平洋夏令时）  
2025年2月4日更新  

本章回顾  
----------------  

CPU在程序中执行的语句特定序列称为程序的**执行路径（execution path）**。**直线程序（straight-line program）**每次运行时都遵循相同路径。  

**控制流语句（control flow statements）**（亦称**流程控制语句**）允许程序员改变正常执行路径。当控制流语句使程序开始执行非顺序指令序列时，称为**分支（branch）**。  

**条件语句（conditional statement）**是决定是否执行相关语句的语句。  

**if语句（if statements）**允许根据条件是否为`true`来执行相关语句。**else语句（else statements）**在关联条件为`false`时执行。可通过链式组合多个if和else语句。  

**悬空else（dangling else）**发生在无法明确else语句所属的if语句时。悬空else会匹配同一代码块中最后一个未配对的if语句。因此，将if语句体置于代码块中可避免悬空else问题。  

**空语句（null statement）**是仅包含分号的语句，不执行任何操作。当语言要求存在语句但无需实际功能时使用。  

**switch语句（switch statements）**为多选项匹配提供更简洁高效的解决方案，仅支持整型类型。**case标签（case labels）**标识匹配条件值，**default标签（default label）**下的语句在所有case不匹配时执行。  

当执行流从某个标签下语句流向后续标签下的语句时，称为**贯穿（fallthrough）**。使用`break语句`或`return语句`可阻止贯穿。`[[fallthrough]]`属性可用于标记有意贯穿。  

**goto语句（goto statements）**允许程序跳转到代码其他位置（前向或后向），通常应避免使用以免产生**面条代码（spaghetti code）**（指执行路径混乱的程序）。  

**while循环（while loops）**在条件为`true`时持续循环，条件在循环前评估。  

**无限循环（infinite loop）**指条件始终为`true`的循环，需其他控制流语句终止。  

**循环变量（loop variable）**（亦称**计数器**）是记录循环次数的整型变量，每次循环执行称为**迭代（iteration）**。  

**do while循环（do while loops）**与while循环类似，但条件在循环后评估。  

**for循环（for loops）**是最常用循环结构，适合固定次数的循环。**差一错误（off-by-one error）**指循环次数多或少一次的情况。  

**break语句（break statements）**可跳出switch、while、do while或for循环（含未介绍的基于范围的for循环）。**continue语句（continue statements）**直接进入下次循环迭代。  

**终止（halts）**用于结束程序。**正常终止（normal termination）**表示程序按预期退出（通过`status code`指示成功与否）。`std::exit()`在main函数末尾自动调用，或显式调用终止程序（清理部分资源但不处理局部变量和调用栈）。  

**异常终止（abnormal termination）**指程序因意外错误被迫关闭，可通过`std::abort`触发。  

**算法（algorithm）**是解决问题的有限指令序列。**有状态（stateful）**算法在调用间保留信息，**无状态（stateless）**算法不存储信息（需在调用时提供全部信息）。算法中的**状态（state）**指状态变量当前值。  

若算法对给定输入（`start`值）始终产生相同输出序列，则称为**确定性（deterministic）**算法。  

**伪随机数生成器（pseudo-random number generator，PRNG）**是生成模拟随机数序列的算法。初始化PRNG时提供的初始值称为**随机种子（random seed）**（简称种子），此时PRNG被**播种（seeded）**。当种子值小于PRNG状态大小时称为**欠播种（underseeded）**。PRNG重复前的序列长度称为**周期（period）**。  

**随机数分布（random number distribution）**将PRNG输出转换为其他数字分布。**均匀分布（uniform distribution）**指在X和Y（含）间等概率生成数字的分布。  

测验时间  
----------------  

**警告：**测验难度从本章开始提升，但相信你能应对！  

**问题1**  
在[4.x — 第四章总结与测验](Chapter-4/lesson4.x-chapter-4-summary-and-quiz.md)中，我们编写了模拟球体下落的程序。由于当时未学习循环，球体最多只能下落5秒。请修改下方程序，使球体持续下落直至触地。更新程序使用所有已学最佳实践（命名空间、constexpr等）。  

原始代码：  
```cpp  
#include <iostream>  

// 获取塔高并返回  
double getTowerHeight() { /*...*/ }  

// 计算seconds秒后球体高度  
double calculateBallHeight(double towerHeight, int seconds) { /*...*/ }  

// 打印球体高度  
void printBallHeight(double ballHeight, int seconds) { /*...*/ }  

// 计算并打印高度的辅助函数  
void calculateAndPrintBallHeight(double towerHeight, int seconds) { /*...*/ }  

int main() { /* 原五次调用 */ }  
```  

解决方案：  
```cpp  
#include <iostream>  

namespace Constants { constexpr double gravity{9.8}; }  

// 函数实现略...  

int main() {  
    const double towerHeight{getTowerHeight()};  
    int seconds{0};  
    while (calculateAndPrintBallHeight(towerHeight, seconds) > 0.0) {  
        ++seconds;  
    }  
    return 0;  
}  
```  

**问题2**  
质数（prime number）是大于1的自然数，只能被1和自身整除。使用for循环完成`isPrime()`函数，成功时程序输出"Success!"。  

初始代码：  
```cpp  
#undef NDEBUG  
#include <cassert>  
#include <iostream>  

bool isPrime(int x) { return false; /*待实现*/ }  

int main() {  
    assert(!isPrime(0)); // 验证非质数  
    // ...其他断言  
    std::cout << "Success!\n";  
    return 0;  
}  
```  

解决方案：  
```cpp  
bool isPrime(int x) {  
    if (x <= 1) return false;  
    for (int test{2}; test < x; ++test) {  
        if (x % test == 0) return false;  
    }  
    return true;  
}  
```  

**附加优化：**  
1. 跳过偶数除数（除2外）  
2. 仅检查至平方根（使用`test * test <= x`优化）  

优化版本：  
```cpp  
bool isPrime(int x) {  
    if (x <= 1) return false;  
    if (x == 2) return true;  
    if (x % 2 == 0) return false;  
    for (int test{3}; test * test <= x; test += 2) {  
        if (x % test == 0) return false;  
    }  
    return true;  
}  
```  

**问题3**  
实现猜数字游戏Hi-Lo：  
1. 程序随机生成1-100的整数  
2. 用户有7次猜测机会  
3. 每次提示过高/过低，猜中即胜，用完次数则败  
4. 游戏结束后询问是否再玩，输入'y'或'n'  

解决方案（使用[Random.h](global-random-numbers-random-h/#RandomH)）：  
```cpp  
#include <iostream>  
#include "Random.h"  

bool playHiLo(int guesses, int min, int max) {  
    const int number{Random::get(min, max)};  
    for (int count{1}; count <= guesses; ++count) {  
        int guess{};  
        std::cin >> guess;  
        // 判断高低并输出提示  
    }  
    return false; // 失败处理  
}  

bool playAgain() {  
    while (true) {  
        char ch{};  
        std::cin >> ch;  
        if (ch == 'y') return true;  
        if (ch == 'n') return false;  
    }  
}  

int main() {  
    constexpr int guesses{7}, min{1}, max{100};  
    do {  
        playHiLo(guesses, min, max);  
    } while (playAgain());  
    std::cout << "Thank you for playing.\n";  
    return 0;  
}  
```  

[下一课 9.1 — 代码测试简介](Chapter-9/lesson9.1-introduction-to-testing-your-code.md)  
[返回主页](/)  
[上一课 8.15 — 全局随机数（Random.h）](Chapter-8/lesson8.15-global-random-numbers-random-h.md)