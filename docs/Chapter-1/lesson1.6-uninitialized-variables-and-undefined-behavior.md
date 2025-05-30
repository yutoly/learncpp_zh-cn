1.6 — 未初始化变量与未定义行为  
=====================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年11月29日（首次发布于2019年2月1日）  

未初始化变量（Uninitialized variables）  
----------------  

与某些编程语言不同，C/C++不会自动将大多数变量初始化为给定值（例如零）。当一个未初始化的变量被分配内存地址时，其默认值将是该内存地址中已有的任意（垃圾）值！未通过初始化或赋值获得已知值的变量称为**未初始化变量（uninitialized variable）**。  

术语说明（Nomenclature）  
----------------  

许多读者认为"已初始化（initialized）"和"未初始化（uninitialized）"是严格反义词，但事实并非完全如此：  
* 已初始化 = 对象在定义时被赋予初始值  
* 赋值 = 对象在定义后被赋予已知值  
* 未初始化 = 对象尚未通过任何方式获得已知值  

例如考虑以下变量定义：  
```cpp
int x;
```  
在课程[1.4 — 变量赋值与初始化](Chapter-1/lesson1.4-variable-assignment-and-initialization.md)中我们提到，当未提供初始化式时，变量将默认初始化。大多数情况下（如本例），默认初始化不会执行实际初始化操作。因此我们称`x`为未初始化变量。这里我们关注结果（对象未获得已知值），而非过程。  

扩展阅读（As an aside…）  
----------------  

这种不初始化的特性是从C语言继承的性能优化策略，源于计算机性能较低的历史时期。假设您需要从文件读取100,000个值：  
* 若C++在创建变量时进行默认初始化，将导致100,000次不必要的初始化操作（显著降低性能）  
* 而这些初始值后续都会被覆盖  

现阶段建议始终初始化变量，因为初始化成本远低于其带来的好处。在深入掌握语言后，可针对特定优化场景选择性省略初始化。  

未初始化变量的使用（Using the values of uninitialized variables）  
----------------  

使用未初始化变量会导致意外结果。观察以下程序：  
```cpp
#include <iostream>

int main()
{
    int x; // 未初始化变量
    std::cout << x << '\n'; // 输出未知垃圾值
    return 0;
}
```  
程序运行时：  
1. 计算机会为`x`分配未使用的内存  
2. 将该内存中的现有值发送至`std::cout`  
3. 输出结果不可预测（作者测试时得到过`7177728`和`5277592`）  

警告（Warning）  
----------------  

部分编译器（如Visual Studio）在调试构建配置（debug build configuration）中会将内存初始化为预设值（如`-858993460`）。但在发布构建配置（release build configuration）中不会执行此操作。若要观察真实未初始化行为，请确保使用发布构建配置（参考课程[0.9 — 编译器配置：构建配置](Chapter-0/lesson0.9-configuring-your-compiler-build-configurations.md)）。  

现代编译器通常能检测未初始化变量的使用，并发出警告或错误。例如Visual Studio会提示：  
```
c:\VCprojects\test\test.cpp(11) : warning C4700: 使用了未初始化的局部变量'x'
```  

若编译器阻止程序运行，可使用以下技巧绕过检测：  
```cpp
#include <iostream>

void doNothing(int&) {} // 通过引用假装使用变量x

int main()
{
    int x;          // 未初始化变量
    doNothing(x);   // 欺骗编译器认为x已被赋值
    std::cout << x; // 仍输出垃圾值
    return 0;
}
```  

使用未初始化变量是新手常见错误，且可能难以调试（若内存中恰巧存在合理值如0，程序可能看似正常运行）。这正是"始终初始化变量"最佳实践的主要原因。  

未定义行为（Undefined behavior）  
----------------  

使用未初始化变量值是**未定义行为（undefined behavior，UB）**的典型案例。未定义行为指执行未被C++语言明确定义的代码所导致的结果。此时程序可能表现出以下任意症状：  
* 每次运行结果不同  
* 持续输出错误结果  
* 行为不稳定（时而正确时而错误）  
* 看似正常但后续产生错误  
* 立即或延迟崩溃  
* 编译器兼容性问题  
* 受无关代码变更影响  

也可能碰巧产生正确结果。  

作者提示（Author’s note）  
----------------  

未定义行为就像巧克力盒，你永远不知道会得到什么！  

C++包含许多可能导致未定义行为的情形（后续课程将逐一指出）。请特别注意并避免这些情况。  

规则（Rule）  
----------------  
避免所有导致未定义行为的情形（如使用未初始化变量）。  

作者提示（Author’s note）  
----------------  

常见读者反馈："你说不能做X，但我做了程序却正常运行！为什么？"可能原因：  
1. 程序实际存在未定义行为，但碰巧得到期望结果（未来可能失效）  
2. 编译器作者未严格遵循标准要求（可通过关闭编译器扩展解决，参考课程[0.10 — 编译器配置：编译器扩展](Chapter-0/lesson0.10-configuring-your-compiler-compiler-extensions.md)）  

实现定义行为与未指定行为（Implementation-defined behavior and unspecified behavior）  
----------------  

**实现（implementation）**指特定编译器及其标准库的组合。C++标准允许实现决定某些行为细节，这类行为称为**实现定义行为（implementation-defined behavior）**，必须记录并保持一致性。  

示例：  
```cpp
#include <iostream>

int main()
{
    std::cout << sizeof(int) << '\n'; // 输出int类型占用的字节数
    return 0;
}
```  
多数平台输出`4`，少数可能输出`2`。  

**未指定行为（unspecified behavior）**类似实现定义行为，但实现无需记录具体行为。  

最佳实践（Best practice）  
----------------  
尽量避免实现定义行为和未指定行为，因其可能导致程序在不同编译器或设置下失效。  

相关链接（Related content）  
----------------  
未指定行为示例见课程[6.1 — 运算符优先级与结合性](operator-precedence-and-associativity/#unspecified)。  

测验时间（Quiz time）  
----------------  

**问题1**  
什么是未初始化变量？为何要避免使用？  
  
<details><summary>答案</summary>未初始化变量是未通过初始化或赋值获得已知值的变量。使用其值会导致未定义行为。</details>  

**问题2**  
什么是未定义行为？其可能后果有哪些？  
  
<details><summary>答案</summary>未定义行为是执行未被语言明确定义的代码导致的结果，可能引发任何不可预测的行为。</details>  

[下一课 1.7 — 关键字与标识符命名](Chapter-1/lesson1.7-keywords-and-naming-identifiers.md)  
[返回主页](/)  
[上一课 1.5 — iostream简介：cout、cin与endl](Chapter-1/lesson1.5-introduction-to-iostream-cout-cin-and-endl.md)