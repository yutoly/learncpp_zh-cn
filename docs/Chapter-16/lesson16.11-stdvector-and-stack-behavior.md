16.11 — std::vector 与栈行为  
=======================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日 下午2:51（太平洋夏令时间）  
2024年10月6日修订  

假设您正在编写一个需要用户输入数值列表（例如多个测试分数）的程序。这种情况下，用户要输入的数值数量在编译时是未知的，且每次运行程序都可能不同。您需要将这些值存储在`std::vector`中以便显示和处理。基于目前所学知识，您可能有以下几种实现思路：  

首先，可以询问用户条目总数，创建对应长度的向量，然后让用户逐个输入。这种方法虽可行，但要求用户预先准确知道条目数量且不出错。手动统计超过十或二十个项目会十分繁琐——既然程序应该自动统计，何必让用户自行计数？  

其次，可以假设用户输入不会超过某个数值（如30），创建（或调整）具有该容量的向量。然后让用户持续输入直到完成（或达到30个值）。由于向量长度表示已使用元素数量，我们随后可将向量调整为实际输入数量。这种方法的缺点是用户被限制只能输入30个值，且我们无法判断该限制是否合理。  

为解决此问题，可以添加在用户达到最大值时自动扩展向量容量的逻辑。但这意味着需要将数组大小管理与程序逻辑混合，这会显著增加程序复杂性（必然导致错误）。  

核心问题在于我们试图猜测用户可能输入的元素数量，从而适当管理向量大小。对于元素数量确实无法预知的情况，存在更好的解决方案。  

在深入讨论之前，需要先理解栈的概念。  

什么是栈？  
以自助餐厅的餐盘栈类比。由于餐盘较重且只能逐个移动，栈的修改只能通过两种方式：  
1. 将新餐盘置于栈顶（遮盖下方餐盘）  
2. 移除栈顶餐盘（暴露下方餐盘）  

禁止从栈中间或底部增删餐盘，因为这需要同时移动多个餐盘。  

栈的增删顺序遵循**后进先出（LIFO）**原则。最后入栈的元素最先被移除。  

编程中的栈  
在编程中，**栈（stack）**是按LIFO方式操作元素的容器数据类型，通常通过**压入（push）**和**弹出（pop）**操作实现：  

| 操作名称 | 栈操作         | 是否必需 | 备注                      |  
|----------|----------------|----------|---------------------------|  
| Push     | 元素入栈       | 是       |                           |  
| Pop      | 移除栈顶元素   | 是       | 可能返回被移除元素或void |  

许多栈实现还支持其他可选操作：  

| 操作名称 | 功能               | 是否必需 | 备注                     |  
|----------|--------------------|----------|--------------------------|  
| Top/Peek | 获取栈顶元素       | 可选     | 不删除元素               |  
| Empty    | 判断是否空栈       | 可选     |                          |  
| Size     | 获取栈中元素数量   | 可选     |                          |  

栈在编程中十分常见。在课程[3.9 — 集成调试器：调用栈](Chapter-3/lesson3.9-using-an-integrated-debugger-the-call-stack.md)中讨论的调用栈正是栈结构。函数调用时，相关信息被压入调用栈；函数返回时，信息从栈顶弹出。  

示例操作序列：  
```
       (栈：空)  
压入1 (栈：1)  
压入2 (栈：1 2)  
压入3 (栈：1 2 3)  
弹出   (栈：1 2)  
压入4 (栈：1 2 4)  
弹出   (栈：1 2)  
弹出   (栈：1)  
弹出   (栈：空)  
```  

C++中的栈实现  
C++通过在现有标准库容器（`std::vector`、`std::deque`和`std::list`）中添加栈操作成员函数来实现栈行为。这使得这些容器在保持原有功能的同时可作为栈使用。  

类比说明：  
将栈视为堆叠的邮箱列，每个邮箱容纳一个元素。使用标记（如便利贴）跟踪栈顶位置（最低空邮箱）。压入元素时放入标记位置并上移标记；弹出元素时下移标记并清空当前邮箱。  

`std::vector`的栈行为  
`std::vector`通过以下成员函数实现栈操作：  

| 函数名称     | 栈操作         | 行为                        | 备注                          |  
|--------------|----------------|-----------------------------|-------------------------------|  
| push_back()  | 压入           | 在向量末尾添加元素          |                               |  
| pop_back()   | 弹出           | 移除末尾元素                | 返回void                      |  
| back()       | 查看栈顶       | 获取末尾元素                | 不删除元素                    |  
| emplace_back() | 压入（优化版） | 在末尾直接构造元素          | 比push_back()更高效（见下文） |  

示例程序：  
```cpp
#include <iostream>
#include <vector>

void printStack(const std::vector<int>& stack) {
    if (stack.empty())
        std::cout << "空";

    for (auto element : stack)
        std::cout << element << ' ';

    std::cout << "\t容量：" << stack.capacity() << "  长度：" << stack.size() << "\n";
}

int main() {
    std::vector<int> stack{}; // 空栈

    printStack(stack);

    stack.push_back(1);
    printStack(stack);

    stack.push_back(2);
    printStack(stack);

    stack.push_back(3);
    printStack(stack);

    std::cout << "栈顶：" << stack.back() << '\n';

    stack.pop_back();
    printStack(stack);

    stack.pop_back();
    printStack(stack);

    stack.pop_back();
    printStack(stack);

    return 0;
}
```  

输出示例（GCC/Clang）：  
```
空      容量：0  长度：0  
1       容量：1  长度：1  
1 2     容量：2  长度：2  
1 2 3   容量：4  长度：3  
栈顶：3  
1 2     容量：4  长度：2  
1       容量：4  长度：1  
空      容量：4  长度：0  
```  

关键洞察：  
- `push_back()`和`emplace_back()`会增加向量长度，容量不足时触发重新分配  
- 重新分配通常分配额外容量以减少未来分配次数（不同编译器策略不同）  

容量预分配  
使用`reserve()`成员函数可预分配容量而不改变当前长度：  
```cpp
std::vector<int> stack{};
stack.reserve(6); // 预分配6元素容量
```  

最佳实践：  
- 通过索引访问向量时使用`resize()`  
- 使用栈操作时使用`reserve()`  

`push_back()` vs `emplace_back()`  
两者均用于压入元素。当压入已存在对象时，优先使用`push_back()`。需要创建临时对象时，`emplace_back()`更高效（避免拷贝）：  
```cpp
std::vector<Foo> stack;
stack.emplace_back("a", 2); // 直接构造，无拷贝
```  

解决初始挑战  
使用栈操作处理未知数量输入的示例：  
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> scoreList{};

    while (true) {
        std::cout << "输入分数（-1结束）：";
        int x{};
        std::cin >> x;

        if (x == -1) break;
        scoreList.push_back(x);
    }

    std::cout << "分数列表：";
    for (const auto& score : scoreList)
        std::cout << score << ' ';

    return 0;
}
```  

测验  
问题1：实现指定操作序列的程序  
  
```cpp
#include <iostream>
#include <vector>

void printStackValues(const std::vector<int>& v) {
    std::cout << "\t(栈：";
    for (auto e : v) std::cout << ' ' << e;
    if (v.empty()) std::cout << " 空";
    std::cout << ")\n";
}

void pushAndPrint(std::vector<int>& v, int val) {
    v.push_back(val);
    std::cout << "压入 " << val;
    printStackValues(v);
}

void popAndPrint(std::vector<int>& v) {
    v.pop_back();
    std::cout << "弹出 ";
    printStackValues(v);
}

int main() {
    std::vector<int> v{};
    printStackValues(v);

    pushAndPrint(v, 1);
    pushAndPrint(v, 2);
    pushAndPrint(v, 3);
    popAndPrint(v);
    pushAndPrint(v, 4);
    popAndPrint(v);
    popAndPrint(v);
    popAndPrint(v);

    return 0;
}
```  

[下一课 16.12 — std::vector\<bool\>](Chapter-16/lesson16.12-stdvector-bool.md)  
[返回主页](/)  
[上一课 16.10 — std::vector容量调整](Chapter-16/lesson16.10-stdvector-resizing-and-capacity.md)