4.2 — void类型  
===================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2015年2月11日（太平洋标准时间下午5:55）  
2023年8月29日更新  

void是所有数据类型中最容易解释的。简而言之，**void**表示"无类型"！  

void是我们遇到的第一个不完整类型（incomplete type）。**不完整类型**是指已声明但未定义的类型。编译器知道这类类型的存在，但没有足够信息来确定该类型对象所需分配的内存大小。`void`被设计为故意不完整的类型，因为它本身代表类型的缺失，因此无法被定义。  

不完整类型不能被实例化：  
```
void value; // 无效操作，变量不能用不完整类型void定义
```  

void通常用于以下几种场景：  

无返回值的函数  
----------------  

最常见的用法是使用*void*表示函数不返回值：  
```
void writeValue(int x) // void在此表示无返回值
{
    std::cout << "x的值为：" << x << '\n';
    // 无return语句，因为此函数不返回值
}
```  

若在此类函数中使用return语句返回值会导致编译错误：  
```
void noReturn(int x) // void在此表示无返回值
{
    std::cout << "x的值为：" << x << '\n';

    return 5; // 错误
}
```  

在Visual Studio 2017中会产生以下错误：  
```
error C2562: 'noReturn': 'void'函数返回了值
```  

已弃用：无参数的函数  
----------------  

在C语言中，void被用于表示函数不接受任何参数：  
```
int getValue(void) // void在此表示无参数
{
    int x{};
    std::cin >> x;

    return x;
}
```  

虽然这段代码在C++中仍可编译（出于向后兼容考虑），但这种void的用法在C++中已被弃用。以下等效代码是C++推荐写法：  
```
int getValue() // 空参数列表隐式表示void
{
    int x{};
    std::cin >> x;

    return x;
}
```  

> **最佳实践**  
> 使用空参数列表代替*void*来表示函数无参数。  

void的其他用途  
----------------  

void关键字在C++中还有第三种（更高级的）用法，我们将在[19.5 — void指针](void-pointers/)章节讨论。由于尚未涉及指针概念，目前无需关注此用法。  

让我们继续学习！  
[下一课 4.3 对象大小与sizeof运算符](Chapter-4/lesson4.3-object-sizes-and-the-sizeof-operator.md)  
[返回主页](/)  
[上一课 4.1 基础数据类型简介](Chapter-4/lesson4.1-introduction-to-fundamental-data-types.md)