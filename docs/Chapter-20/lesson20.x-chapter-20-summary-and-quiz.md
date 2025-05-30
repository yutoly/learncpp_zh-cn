20.x — 第20章小结与测验  
===================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2015年12月4日下午7:31（PST）｜2025年2月8日  

本章回顾  
----------------  

又完成一章！只需通过最后的测验即可...  

函数参数可通过值传递（pass by value）、引用传递（pass by reference）或地址传递（pass by address）。基础数据类型和枚举类型建议使用值传递。结构体（struct）、类（class）或需要修改参数时使用引用传递。指针或内置数组使用地址传递。尽可能将引用和地址参数声明为const。  

返回值可通过值返回（return by value）、引用返回（return by reference）或地址返回（return by address）。多数情况下值返回即可，但在处理动态分配数据、结构体或类时引用/地址返回更有效。使用引用或地址返回时，确保不会返回即将超出作用域的对象。  

函数指针（function pointer）允许将函数传递给其他函数，可用于调用方自定义函数行为（如排序方式）。  

动态内存（dynamic memory）分配在堆（heap）上。  

调用栈（call stack）追踪程序启动到当前执行点之间所有活跃函数（已调用未终止的函数）。局部变量分配在栈（stack）上。栈空间有限，可用std::vector实现类似栈的行为。  

递归函数（recursive function）是调用自身的函数，必须包含终止条件（termination condition）。  

命令行参数（command line argument）允许用户或程序在启动时传入数据。这些参数始终为C风格字符串（C-style string），需要数值时应进行转换。  

省略号（ellipsis）允许传递可变数量参数，但会暂停类型检查且不记录参数数量，需程序自行跟踪细节。  

Lambda函数（lambda function）可嵌套在其他函数中，无需名称，与算法库（algorithms library）结合使用效果显著。  

测验时间  
----------------  

**问题1**  
为以下情况编写函数原型（必要时使用const）：  

a) 函数max()接收两个double参数，返回较大值  
  
<details><summary>答案</summary>  
```cpp  
double max(double x, double y);  
```  
</details>  

b) 函数swap()交换两个整数  
  
<details><summary>答案</summary>  
```cpp  
void swap(int& x, int& y);  
```  
</details>  

c) 函数getLargestElement()接收动态分配的整型数组，返回最大元素的引用（允许调用方修改）  
  
<details><summary>答案</summary>  
```cpp  
int& getLargestElement(int* array, int length);  
```  
</details>  

**问题2**  
找出以下程序错误：  

a) 返回局部变量的引用  
  
<details><summary>答案</summary>  
doSomething()返回了函数终止后即销毁的局部变量引用  
</details>  

b) 递归函数缺少终止条件  
  
<details><summary>答案</summary>  
sumTo()无终止条件，value会变为负数导致无限递归直至栈溢出  
</details>  

c) 函数重载冲突  
  
<details><summary>答案</summary>  
两个divide()函数参数相同导致重载冲突，且存在除零风险  
</details>  

d) 栈数组过大  
  
<details><summary>答案</summary>  
过大的栈数组应改为动态分配  
</details>  

e) 命令行参数转换错误  
  
<details><summary>答案</summary>  
未验证argv[1]是否存在，且错误地将字符串赋给整型变量  
</details>  

**问题3**  
实现二分查找算法：  

a) 迭代版本  
  
<details><summary>答案</summary>  
```cpp  
int binarySearch(const int* array, int target, int min, int max)  
{  
    while (min <= max)  
    {  
        int midpoint{ std::midpoint(min, max) };  
        if (array[midpoint] > target)  
            max = midpoint - 1;  
        else if (array[midpoint] < target)  
            min = midpoint + 1;  
        else  
            return midpoint;  
    }  
    return -1;  
}  
```  
</details>  

b) 递归版本  
  
<details><summary>答案</summary>  
```cpp  
int binarySearch(const int* array, int target, int min, int max)  
{  
    if (min > max) return -1;  
    int midpoint{ std::midpoint(min, max) };  
    if (array[midpoint] > target)  
        return binarySearch(array, target, min, midpoint - 1);  
    else if (array[midpoint] < target)  
        return binarySearch(array, target, midpoint + 1, max);  
    return midpoint;  
}  
```  
</details>  

> **提示**  
> 标准库提供[std::binary_search](https://en.cppreference.com/w/cpp/algorithm/binary_search)检查存在性，[std::equal_range](https://en.cppreference.com/w/cpp/algorithm/equal_range)获取元素范围。日常开发建议使用这些函数。  

[下一课 21.1 — 运算符重载简介](Chapter-21/lesson21.1-introduction-to-operator-overloading.md)  
[返回主页](/)  
[上一课 20.7 — Lambda捕获](Chapter-20/lesson20.7-lambda-captures.md)