27.2 — 基本异常处理
================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年10月4日 下午1:29（PDT）  
2025年1月6日更新  

在上一课[异常处理的必要性](151-the-need-for-exceptions/)中，我们讨论了使用返回码会导致控制流与错误流混杂的问题。C++通过三个协同工作的关键字实现异常处理：**throw**（抛出）、**try**（尝试）和**catch**（捕获）。  

抛出异常  
----------------  

在现实生活中，我们常用信号表示特定事件的发生。例如美式足球比赛中，当球员犯规时，裁判会掷旗并吹停比赛，评估判罚后继续比赛。  

C++中，**throw语句**用于表示异常或错误情况的发生（类似掷出判罚旗）。触发异常的行为通常称为**引发**异常。  

throw语句的语法是`throw`关键字后接任意数据类型的值。常用值包括错误码、问题描述或自定义异常类：  
```
throw -1; // 抛出整数字面量
throw ENUM_INVALID_INDEX; // 抛出枚举值
throw "无法对负数取平方根"; // 抛出C风格字符串字面量
throw dX; // 抛出已定义的双精度变量
throw MyException("致命错误"); // 抛出MyException类对象
```  

每个throw语句都标志着需要处理的异常事件。  

检测异常  
----------------  

抛出异常只是异常处理的第一步。使用**try**关键字定义**try块**（尝试块），该块内的语句若抛出异常会被检测到：  
```
try
{
    // 可能抛出异常的语句
    throw -1; // 简单的throw语句示例
}
```  

try块本身不定义处理逻辑，仅负责捕获块内语句抛出的异常。  

处理异常  
----------------  

**catch块**（捕获块）使用`catch`关键字定义，处理特定数据类型的异常：  
```
catch (int x)
{
    // 处理int类型异常
    std::cerr << "捕获整型异常，值：" << x << '\n';
}
```  

try块后必须紧跟至少一个catch块，可并列多个catch块。异常被处理后，程序从最后一个catch块之后继续执行。  

catch参数类似于函数参数。基本类型建议按值捕获，非基本类型应通过常量引用捕获以避免复制：  
```
catch (double) // 省略未使用的变量名
{
    std::cerr << "捕获双精度类型异常\n";
}
```  

异常匹配不执行类型转换（如int异常不会匹配double参数catch块）。  

完整示例  
----------------  
```
#include <iostream>
#include <string>

int main()
{
    try
    {
        throw -1; // 抛出整型异常
    }
    catch (double)
    {
        std::cerr << "捕获双精度异常\n";
    }
    catch (int x)
    {
        std::cerr << "捕获整型异常，值：" << x << '\n';
    }
    catch (const std::string&)
    {
        std::cerr << "捕获字符串类型异常\n";
    }

    std::cout << "继续执行后续代码\n";
    return 0;
}
```  

输出结果：  
```
捕获整型异常，值：-1
继续执行后续代码
```  

异常处理机制  
----------------  

1. 抛出异常（throw）时，程序查找最近的try块（必要时沿调用栈回溯）  
2. 检查关联的catch块能否处理该类型异常  
3. 找到匹配则跳转执行对应catch块  
4. 若未找到匹配，程序以运行时错误终止  

注意：  
- char异常不匹配int catch块  
- int异常不匹配float catch块  
- 允许派生类到基类的向上转型  

立即处理示例  
----------------  
```
#include <iostream>

int main()
{
    try
    {
        throw 4.5; // 抛出双精度异常
        std::cout << "此语句永不执行\n";
    }
    catch (double x)
    {
        std::cerr << "捕获双精度值：" << x << '\n';
    }
    return 0;
}
```  

输出：  
```
捕获双精度值：4.5
```  

实际应用示例  
----------------  
```
#include <cmath>
#include <iostream>

int main()
{
    std::cout << "输入数字：";
    double x{};
    std::cin >> x;

    try
    {
        if (x < 0.0)
            throw "不能对负数取平方根"; // 抛出const char*异常

        std::cout << x << "的平方根是" << std::sqrt(x) << '\n';
    }
    catch (const char* exception)
    {
        std::cerr << "错误：" << exception << '\n';
    }
}
```  

输入正数时正常计算，输入负数时触发异常处理。  

catch块的常见操作  
----------------  

1. 输出错误日志后继续执行  
2. 向调用者返回错误码  
3. 抛出新异常（由外层try处理）  
4. main()中捕获致命错误并优雅终止  

[下一课 27.3 异常、函数与栈展开](Chapter-27/lesson27.3-exceptions-functions-and-stack-unwinding.md)  
[返回主页](/)  
[上一课 27.1 异常处理的必要性](Chapter-27/lesson27.1-the-need-for-exceptions.md)