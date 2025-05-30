8.9 — do-while 语句  
==========================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月25日 PDT时间下午4:54（更新于2025年2月5日）  

考虑这样一个场景：我们需要向用户展示菜单并要求其进行选择——若用户选择无效选项，则再次询问。显然菜单和选择逻辑应置于某种循环结构中（以便持续询问直至输入有效），但应选择何种循环类型？  

由于while循环在循环开始前检查条件，这会导致实现上的不便。我们可采用如下解决方案：  
```
#include <iostream>

int main()
{
    // selection必须声明在while循环外部以便后续使用
    int selection {}; // 值初始化为0

    while (selection < 1 || selection > 4)
    {
        std::cout << "请做出选择：\n";
        std::cout << "1) 加法\n";
        std::cout << "2) 减法\n";
        std::cout << "3) 乘法\n";
        std::cout << "4) 除法\n";
        std::cin >> selection;
    }

    // 在此处处理selection
    // 例如使用switch语句

    std::cout << "您选择了选项#" << selection << '\n';

    return 0;
}
```  
此方案可行的前提是`selection`的初始值`0`不在有效值集合（`1, 2, 3或4`）中。若`0`本身是有效选项怎么办？我们需选择其他初始值来表示"无效"状态——这会导致代码中出现魔数（magic numbers）（详见课程[5.2 — 字面量](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)）。  

另一种方案是添加新变量追踪有效性：  
```
#include <iostream>

int main()
{
    int selection {};
    bool invalid { true }; // 新增变量用于控制循环

    while (invalid)
    {
        std::cout << "请做出选择：\n";
        std::cout << "1) 加法\n";
        std::cout << "2) 减法\n";
        std::cout << "3) 乘法\n";
        std::cout << "4) 除法\n";

        std::cin >> selection;
        invalid = (selection < 1 || selection > 4);
    }

    // 在此处处理selection
    // 例如使用switch语句

    std::cout << "您选择了选项#" << selection << '\n';

    return 0;
}
```  
虽然避免了魔数，但引入了仅用于确保循环执行一次的新变量，增加了复杂性和潜在错误风险。  

do-while 语句  
----------------  
为解决上述问题，C++提供了do-while语句：  
```
do
    statement; // 可以是单条语句或复合语句
while (condition);
```  
**do-while语句（do-while statement）**是一种循环结构，其行为类似于while循环，区别在于语句块至少会执行一次。执行完语句块后，do-while检查条件：若条件为`true`，程序流跳转回do-while顶部再次执行。  

使用do-while重构上述示例：  
```
#include <iostream>

int main()
{
    // selection必须声明在do-while循环外部以便后续使用
    int selection {};

    do
    {
        std::cout << "请做出选择：\n";
        std::cout << "1) 加法\n";
        std::cout << "2) 减法\n";
        std::cout << "3) 乘法\n";
        std::cout << "4) 除法\n";
        std::cin >> selection;
    }
    while (selection < 1 || selection > 4);

    // 在此处处理selection
    // 例如使用switch语句

    std::cout << "您选择了选项#" << selection << '\n';

    return 0;
}
```  
此方案同时避免了魔数和额外变量。  

值得讨论的是，`selection`变量必须声明在do块外部。若在do块内部声明，该变量会在do块终止时销毁（此时尚未执行条件检查）。但由于while条件需要访问该变量——因此`selection`必须声明在do块外部（即使后续函数体中不再使用）。  

实际应用中，do-while循环并不常见。将条件置于循环底部会降低代码可读性，可能引发错误。许多开发者因此建议完全避免使用do-while循环。我们持较温和立场：在同等条件下优先选择while循环。  

最佳实践  
----------------  
**在同等条件下优先选择while循环而非do-while循环**  



[下一课 8.10 — for语句](Chapter-8/lesson8.10-for-statements.md)  
[返回主页](/)  
[上一课 8.8 — 循环与while语句简介](Chapter-8/lesson8.8-introduction-to-loops-and-while-statements.md)