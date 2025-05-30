27.x — 第27章总结与测验  
===================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2017年2月11日 下午12:18（首次发布于2023年10月7日）  

**本章回顾**  

异常处理机制将错误或特殊情况的处理与常规代码控制流解耦，为不同场景提供灵活的错误处理方式，从而避免返回码（return codes）导致的混乱问题。  

**throw**语句用于抛出异常。**try块**检测其内部代码抛出的异常，这些异常会被路由到**catch块**——后者捕获特定类型的异常（若匹配）并进行处理。默认情况下，被捕获的异常视为已处理。  

异常会立即处理：当异常抛出时，控制流跳转至最近的try块，寻找能处理该异常的catch处理器。若找到匹配的try/catch，则执行栈展开（stack unwinding）至catch块位置，控制流在匹配的catch块顶部恢复。若未找到try块或匹配的catch块，程序将调用std::terminate终止并提示未处理异常错误。  

可抛出任意数据类型的异常（包括类）。  

catch块可配置为捕获特定数据类型，或通过省略号（…）设置全能捕获处理器。捕获基类引用的catch块也会捕获派生类异常。标准库抛出的所有异常均派生自std::exception类（位于exception头文件），因此通过引用捕获std::exception可捕获所有标准库异常。可通过what()成员函数确定std::exception的具体类型。  

在catch块内部可抛出新异常。由于新异常在关联的try块外抛出，不会被当前catch块捕获。使用单独throw关键字可重新抛出（rethrown）当前异常。避免通过已捕获的异常变量重新抛出，否则可能导致对象切片（object slicing）。  

函数try块（Function try blocks）用于捕获函数内或关联成员初始化列表中的异常，通常仅用于派生类构造函数。  

切勿从析构函数抛出异常。  

**noexcept**异常说明符（exception specifier）用于声明函数不抛出/不失败（no-throw/no-fail）。  

若对象具有noexcept移动构造函数，std::move_if_noexcept返回可移动的右值（r-value），否则返回可复制的左值（l-value）。结合noexcept说明符与std::move_if_noexcept，可在存在强异常保证（strong exception guarantee）时使用移动语义（move semantics），否则使用复制语义（copy semantics）。  

异常处理存在开销：多数情况下使用异常的代码运行稍慢，且处理异常成本极高。异常应仅用于处理特殊情况，而非常规错误处理（如无效输入）。  

**章节测验**  

1. 编写Fraction类：其构造函数接收分子（numerator）和分母（denominator）。若分母为0，则抛出std::runtime_error异常（位于stdexcept头文件）。在主程序中要求用户输入两个整数：若分数有效则打印该分数；若无效则捕获std::exception并提示无效分数。  

程序运行示例如下：  

```
输入分子：5  
输入分母：0  
无效分母
```  

  

```cpp
#include <iostream>
#include <stdexcept> // 用于 std::runtime_error
#include <exception> // 用于 std::exception

class Fraction
{
private:
    int m_numerator = 0;
    int m_denominator = 1;

public:
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }
        , m_denominator{ denominator }
    {
        if (m_denominator == 0)
            throw std::runtime_error("无效分母");
    }

    friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);
};

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
    out << f1.m_numerator << '/' << f1.m_denominator;
    return out;
}

int main()
{
    std::cout << "输入分子：";
    int numerator{};
    std::cin >> numerator;

    std::cout << "输入分母：";
    int denominator{};
    std::cin >> denominator;

    try
    {
        Fraction f{ numerator, denominator };
        std::cout << "您输入的分数为：" << f << '\n';
    }
    catch (const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }

    return 0;
}
```  

[下一课 28.1 输入输出流](Chapter-28/lesson28.1-input-and-output-io-streams.md)  
[返回主页](/)  
[上一课 27.10 std::move_if_noexcept](Chapter-27/lesson27.10-stdmove_if_noexcept.md)