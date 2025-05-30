19.2 — 动态分配数组  
=====================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2015年8月18日 下午1:52（太平洋夏令时）  
2023年11月20日更新  

除了动态分配单个值外，我们还可以动态分配变量数组。与固定数组（其大小必须在编译时确定）不同，动态分配数组允许我们在运行时选择数组长度（即长度无需是constexpr）。  

> **作者注**  
> 本系列课程主要讨论动态分配C风格数组（C-style arrays），这是最常见的动态数组类型。  
>  
> 虽然可以动态分配`std::array`，但通常更推荐使用非动态分配的`std::vector`。  



要动态分配数组，我们使用数组形式的new和delete（通常称为new\[]和delete\[]）：
```cpp
#include <cstddef>
#include <iostream>

int main()
{
    std::cout << "请输入一个正整数：";
    std::size_t length{};
    std::cin >> length;

    int* array{ new int[length]{} }; // 使用数组new。注意length无需是常量！

    std::cout << "已成功分配长度为" << length << "的整型数组\n";

    array[0] = 5; // 将元素0设为5

    delete[] array; // 使用数组delete释放内存

    // 此处无需将array设为nullptr/0，因为变量即将离开作用域

    return 0;
}
```  
由于分配的是数组，C\+\+会自动调用数组版本的new而非标量版本。本质上，即使\[]没有紧跟在new关键字后，new\[]运算符仍会被调用。  

动态数组的长度类型应为`std::size_t`。若使用非常量整型，需要通过`static_cast`转换为`std::size_t`，否则编译器会因窄化转换发出警告。  

注意由于动态数组内存分配位置与固定数组不同，其尺寸可以非常大。您可运行上述程序尝试分配长度为1,000,000（甚至100,000,000）的数组。因此需要大量内存的C\+\+程序通常采用动态分配。  

**动态删除数组**  
删除动态数组时，必须使用数组版本的delete（即delete\[]）。  

该操作通知CPU需要清理多个变量而非单个变量。新手常见错误是在删除动态数组时使用delete而非delete\[]。对数组使用标量delete会导致未定义行为（undefined behavior），如数据损坏、内存泄漏、崩溃等问题。  

关于数组delete\[]的常见疑问是："如何确定要删除的内存大小？" 答案在于数组new\[]会记录分配的内存大小，使delete\[]能正确释放。遗憾的是这个大小值对程序员不可见。  

**动态数组与固定数组几乎相同**  
在课程[17.8 — C风格数组退化](Chapter-17/lesson17.8-c-style-array-decay.md)中，我们学习到固定数组保存首元素地址，且可退化为指向首元素的指针。退化形式下无法获取数组长度（因此也无法通过sizeof获取大小），除此之外两者差异甚微。  

动态数组初始即是指向首元素的指针，因此具有相同限制（无法获知自身长度或大小）。动态数组功能与退化的固定数组完全相同，区别在于程序员需通过delete\[]手动释放内存。  

**初始化动态数组**  
若要将动态数组初始化为0，语法非常简单：
```cpp
int* array{ new int[length]{} };
```  
在C\+\+11之前，没有简便方法初始化非零动态数组（初始化列表仅适用于固定数组），必须通过循环逐个赋值：
```cpp
int* array = new int[5];
array[0] = 9;
array[1] = 7;
array[2] = 5;
array[3] = 3;
array[4] = 1;
```  
自C\+\+11起，可使用初始化列表初始化动态数组：
```cpp
int fixedArray[5] = { 9, 7, 5, 3, 1 }; // C++11前初始化固定数组
int* array{ new int[5]{ 9, 7, 5, 3, 1 } }; // C++11起初始化动态数组
// 为避免重复类型声明，可使用auto（常用于长类型名）
auto* array{ new int[5]{ 9, 7, 5, 3, 1 } };
```  
注意数组长度与初始化列表间没有赋值运算符。  

为保持一致性，固定数组也可使用统一初始化：
```cpp
int fixedArray[]{ 9, 7, 5, 3, 1 }; // C++11初始化固定数组
char fixedArray[]{ "Hello, world!" }; // C++11初始化固定数组
```  
显式声明数组尺寸是可选的。  

**调整数组大小**  
动态分配数组时可在分配时指定长度，但C\+\+未提供内置的数组大小调整功能。可通过分配新数组、复制元素、删除旧数组实现，但当元素类型是类（具有特殊构造规则）时容易出错。  

因此建议避免手动实现，改用`std::vector`。  

**测验时间**  
**问题1**  
编写程序实现：  
* 询问用户输入姓名数量  
* 动态分配`std::string`数组  
* 获取每个姓名  
* 调用`std::sort`排序（参考[18.1 — 使用选择排序数组](sorting-an-array-using-selection-sort/#stdsort)及[17.9 — 指针算术与下标](Chapter-17/lesson17.9-pointer-arithmetic-and-subscripting.md)）  
* 打印排序结果  

`std::string`支持通过\<和\>比较字符串，无需手动实现。输出应匹配：
```
需要输入多少个姓名？5
输入姓名 #1: Jason
输入姓名 #2: Mark
输入姓名 #3: Alex
输入姓名 #4: Chris
输入姓名 #5: John

排序结果：
姓名 #1: Alex
姓名 #2: Chris
姓名 #3: Jason
姓名 #4: John
姓名 #5: Mark
```  
**提示**  
* 使用`std::getline()`读取含空格的姓名（见课程[5.7 — std::string简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)）  
* 对数组指针使用`std::sort()`时需手动计算起止：
```cpp
std::sort(array, array + arrayLength);
```

  
```cpp
#include <algorithm> // std::sort
#include <cstddef>
#include <iostream>
#include <string>

std::size_t getNameCount()
{
    std::cout << "需要输入多少个姓名？";
    std::size_t length{};
    std::cin >> length;

    return length;
}

// 获取所有姓名
void getNames(std::string* names, std::size_t length)
{
    for (std::size_t i{ 0 }; i < length; ++i)
    {
        std::cout << "输入姓名 #" << i + 1 << ": ";
        std::getline(std::cin >> std::ws, names[i]);
    }
}

// 打印排序结果
void printNames(std::string* names, std::size_t length)
{
    std::cout << "\n排序结果：\n";

    for (std::size_t i{ 0 }; i < length; ++i)
        std::cout << "姓名 #" << i + 1 << ": " << names[i] << '\n';
}

int main()
{
    std::size_t length{ getNameCount() };

    // 分配姓名数组
    auto* names{ new std::string[length]{} };

    getNames(names, length);

    // 排序数组
    std::sort(names, names + length);

    printNames(names, length);

    // 不要忘记数组delete
    delete[] names;
    // 此处无需设为nullptr/0，变量即将离开作用域

    return 0;
}
```  

[下一课 19.3 析构函数](Chapter-15/lesson15.4-introduction-to-destructors.md)  
[返回主页](/)  
[上一课 19.1 使用new和delete进行动态内存分配](Chapter-19/lesson19.1-dynamic-memory-allocation-with-new-and-delete.md)