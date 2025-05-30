8.7 — goto语句  
======================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年10月14日（首次发布于2007年6月21日）  

接下来要介绍的控制流语句是无条件跳转（unconditional jump）。无条件跳转会直接跳转到代码的其他位置执行。所谓"无条件"意味着跳转必然发生（与if语句或switch语句不同，后者的跳转取决于条件表达式的结果）。  

在C++中，无条件跳转通过**goto语句（goto statement）**实现，跳转目标通过**语句标签（statement label）**标识。与switch的case标签类似，语句标签通常不进行缩进。  

以下示例演示了goto语句和语句标签的用法：  
```
#include <iostream>
#include <cmath> // 包含sqrt()函数

int main()
{
    double x{};
tryAgain: // 这是语句标签
    std::cout << "输入非负数: "; 
    std::cin >> x;

    if (x < 0.0)
        goto tryAgain; // 这是goto语句

    std::cout << x << "的平方根是" << std::sqrt(x) << '\n';
    return 0;
}
```  
该程序要求用户输入非负数。若输入负数，程序使用goto语句跳转回`tryAgain`标签，重新要求输入。通过这种方式，程序可以持续请求有效输入。  

运行示例：  
```
输入非负数: -4
输入非负数: 4
4的平方根是2
```  

语句标签的函数作用域（function scope）  
----------------  
在对象作用域章节（第7章）中，我们介绍了局部（块）作用域和文件（全局）作用域。语句标签使用第三种作用域：**函数作用域（function scope）**，即标签在函数内全局可见（包括声明前的位置）。goto语句与其对应的`语句标签`必须位于同一函数内。  

上述示例展示了向后跳转（跳转到函数前面的位置），但goto也可以向前跳转：  
```
#include <iostream>

void printCats(bool skip)
{
    if (skip)
        goto end; // 向前跳转：由于函数作用域，'end'标签在此可见
    
    std::cout << "cats\n";
end:
    ; // 语句标签必须关联实际语句
}

int main()
{
    printCats(true);  // 跳过打印语句，无输出
    printCats(false); // 输出"cats"

    return 0;
}
```  
输出结果：  
```
cats
```  

该程序有三点值得注意：  
1. 语句标签必须关联实际语句。函数末尾无语句时需使用空语句（null statement）  
2. 由于函数作用域，可以在声明前跳转到标签  
3. 此例使用goto跳过打印语句并非最佳实践，使用if语句更合适  

跳转限制  
----------------  
跳转存在两个主要限制：  
1. 只能在同一函数内跳转（不可跨函数）  
2. 向前跳转时，不能跳过仍在作用域内的变量初始化  

例如：  
```
int main()
{
    goto skip;   // 错误：该跳转非法...
    int x { 5 }; // 该初始化变量在'skip'标签处仍在作用域内
skip:
    x += 3;      // 若x未初始化，此表达式如何求值？
    return 0;
}
```  
注意：向后跳转经过变量初始化时，变量会在初始化执行时被重新初始化。  

避免使用goto  
----------------  
C++（及其他现代高级语言）中通常避免使用`goto`。著名计算机科学家[艾兹格·迪杰斯特拉](https://en.wikipedia.org/wiki/Edsger_Dijkstra)在论文[《Go To 语句有害论》](http://www.cs.utexas.edu/users/EWD/ewd02xx/EWD215.PDF)中阐述了避免goto的理由。主要问题在于goto允许代码随意跳转，导致**面条式代码（spaghetti code）**——执行路径如意大利面般缠绕，难以追踪逻辑。  

如迪杰斯特拉所言："程序员素质与其程序中goto语句的密度成反比"。  

几乎所有使用goto的代码都能用if语句或循环结构更清晰地表达。一个例外情况是需要退出嵌套循环但不想退出整个函数时，goto可能是最简洁的解决方案。  

进阶示例  
----------------  
以下示例演示用goto退出嵌套循环而不退出函数：  
```
#include <iostream>

int main()
{
    for (int i = 1; i < 5; ++i)
    {        
        for (int j = 1; j < 5; ++j)
        {
            std::cout << i << " * " << j << " = " << i*j << '\n';
            
            // 若乘积能被9整除，跳转到"end"标签
            if (i*j % 9 == 0)
            {
                std::cout << "发现可被9整除的乘积。提前终止。\n";
                goto end;
            }
        }

        std::cout << "递增第一个因子。\n";
    }

end:
    std::cout << "操作完成。" << '\n';

    return 0;
}
```  

作者注  
----------------  
来自[xkcd](https://xkcd.com/292/)的友情提醒：  
![https://imgs.xkcd.com/comics/goto.png](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20width=%22740%22%20height=%22201%22%3E%3C/svg%3E)  

最佳实践  
----------------  
避免使用goto语句（除非其他方案会显著降低代码可读性）。  

[下一课 8.8 — 循环与while语句简介](Chapter-8/lesson8.8-introduction-to-loops-and-while-statements.md)  
[返回主页](/)  
[上一课 8.6 — switch贯穿与作用域](Chapter-8/lesson8.6-switch-fallthrough-and-scoping.md)