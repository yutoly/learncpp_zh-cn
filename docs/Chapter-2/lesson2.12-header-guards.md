2.12 — 头文件守卫（Header Guards）
====================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")
2024年6月12日（首次发布于2016年4月5日）

重复定义问题
----------------
在课程[2.7 — 前向声明与定义](Chapter-2/lesson2.7-forward-declarations.md)中，我们提到变量或函数标识符只能有一个定义（单一定义规则）。因此，多次定义同一变量标识符将导致编译错误：

```
int main()
{
    int x; // 变量x的定义
    int x; // 编译错误：重复定义
    return 0;
}
```

类似地，多次定义函数也会导致编译错误：

```
#include <iostream>

int foo() // 函数foo的定义
{
    return 5;
}

int foo() // 编译错误：重复定义
{
    return 5;
}

int main()
{
    std::cout << foo();
    return 0;
}
```

虽然这些程序易于修复（移除重复定义），但在头文件中，定义被多次包含的情况极易发生。当头文件\#包含另一个头文件（常见情况）时便会出现此问题。

> **作者提示**  
> 后续示例将在头文件中定义函数。实际开发中通常不应这样做。  
> 此处仅为通过已学功能有效演示概念。

考虑以下示例：  
square.h：
```
int getSquareSides()
{
    return 4;
}
```
wave.h：
```
#include "square.h"
```
main.cpp：
```
#include "square.h"
#include "wave.h"

int main()
{
    return 0;
}
```
这个看似无害的程序无法编译！原因如下：首先，*main.cpp* \#包含*square.h*，将函数*getSquareSides*的定义复制到*main.cpp*。接着*main.cpp* \#包含*wave.h*，而*wave.h*自身又\#包含*square.h*。这导致*square.h*的内容（包括*getSquareSides*的定义）被复制到*wave.h*，进而再复制到*main.cpp*。

解析所有\#包含后，*main.cpp*实际内容如下：
```
int getSquareSides()  // 来自square.h
{
    return 4;
}

int getSquareSides() // 来自wave.h（通过square.h）
{
    return 4;
}

int main()
{
    return 0;
}
```
出现重复定义导致编译错误。每个文件单独看都正确，但因*main.cpp*两次包含*square.h*的内容而引发问题。若*wave.h*需要*getSquareSides()*，且*main.cpp*同时需要*wave.h*和*square.h*，应如何解决？

头文件守卫
----------------
**头文件守卫（header guard）**（也称**包含守卫（include guard）**）可解决此问题。头文件守卫是条件编译指令，格式如下：
```
#ifndef 唯一标识符
#define 唯一标识符

// 此处放置声明（及特定类型定义）

#endif
```
当头文件被\#包含时，预处理器会检查当前翻译单元中是否已定义*唯一标识符*。若是首次包含，*唯一标识符*尚未定义，因此预处理器将定义该标识符并包含文件内容。若同一文件再次包含该头文件，*唯一标识符*已被定义，文件内容会被忽略（因\#ifndef条件不成立）。

所有头文件都应使用头文件守卫。*唯一标识符*可自定义，但惯例是使用头文件全文件名的大写形式（用下划线替代空格和标点）。例如*square.h*的头文件守卫：
square.h：
```
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

#endif
```
标准库头文件也使用头文件守卫。例如Visual Studio的iostream头文件包含：
```
#ifndef _IOSTREAM_
#define _IOSTREAM_

// 内容在此

#endif
```

> **进阶阅读**  
> 大型项目中可能存在同名头文件（位于不同目录）。若仅用文件名作为守卫（如CONFIG_H），这两个文件可能使用相同守卫名。若某文件（直接或间接）包含这两个头文件，第二个头文件的内容将被忽略，导致编译错误。  
> 因此建议使用更复杂的守卫名：项目路径_文件名_H、文件名_随机数_H 或 文件名_创建日期_H。

使用头文件守卫的更新示例
----------------
为*square.h*添加头文件守卫（规范起见也为*wave.h*添加守卫）：
square.h：
```
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

#endif
```
wave.h：
```
#ifndef WAVE_H
#define WAVE_H

#include "square.h"

#endif
```
main.cpp：
```
#include "square.h"
#include "wave.h"

int main()
{
    return 0;
}
```
预处理器解析所有\#包含后程序如下：
main.cpp：
```
// main.cpp包含square.h
#ifndef SQUARE_H // 首次出现
#define SQUARE_H // 定义SQUARE_H

// 包含全部内容
int getSquareSides()
{
    return 4;
}

#endif // SQUARE_H

#ifndef WAVE_H // main.cpp包含wave.h
#define WAVE_H
#ifndef SQUARE_H // wave.h包含square.h，但SQUARE_H已定义
#define SQUARE_H // 因此不包含以下内容

int getSquareSides() // 此部分被排除
{
    return 4;
}

#endif // SQUARE_H
#endif // WAVE_H

int main()
{
    return 0;
}
```
执行过程：  
1. 首次遇到`#ifndef SQUARE_H`时`SQUARE_H`未定义，包含内容至`#endif`（包含函数定义）  
2. 再次遇到`#ifndef SQUARE_H`时`SQUARE_H`已定义，跳过内容至`#endif`  

头文件守卫通过首次包含时定义宏标识符，后续包含时排除内容来防止重复包含。

头文件守卫不阻止跨文件包含
----------------
头文件守卫仅阻止同一文件多次包含同一头文件，而**不阻止**头文件被包含到不同代码文件中。这可能导致新问题：
square.h：
```
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides() // 函数定义
{
    return 4;
}

int getSquarePerimeter(int sideLength); // getSquarePerimeter的前向声明

#endif
```
square.cpp：
```
#include "square.h"  // 此处包含一次

int getSquarePerimeter(int sideLength)
{
    return sideLength * getSquareSides();
}
```
main.cpp：
```
#include "square.h" // 此处也包含一次
#include <iostream>

int main()
{
    std::cout << "正方形有 " << getSquareSides() << " 条边\n";
    std::cout << "边长为5的正方形周长为 " << getSquarePerimeter(5) << '\n';
    return 0;
}
```
此时*square.h*被包含到*square.cpp*和*main.cpp*中，导致两个文件都获得*getSquareSides*的定义。程序可编译但**链接器**会报告*getSquareSides*的重复定义错误！

解决方案是将函数定义移至.cpp文件，头文件仅保留前向声明：
square.h：
```
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides(); // getSquareSides的前向声明
int getSquarePerimeter(int sideLength); // getSquarePerimeter的前向声明

#endif
```
square.cpp：
```
#include "square.h"

int getSquareSides() // 实际定义
{
    return 4;
}

int getSquarePerimeter(int sideLength)
{
    return sideLength * getSquareSides();
}
```
main.cpp：
```
#include "square.h" 
#include <iostream>

int main()
{
    std::cout << "正方形有 " << getSquareSides() << " 条边\n";
    std::cout << "边长为5的正方形周长为 " << getSquarePerimeter(5) << '\n';
    return 0;
}
```
现在*getSquareSides*仅有一个定义（位于*square.cpp*），链接器正常。*main.cpp*通过*square.h*的前向声明调用该函数（链接器将*main.cpp*的调用关联到*square.cpp*的定义）。

避免头文件包含定义的疑问
----------------
虽然我们通常不建议在头文件中定义函数，但未来课程中将展示必须将**非函数定义**（如自定义类型）放入头文件的情况。若无头文件守卫，代码文件可能包含多个相同类型定义，导致编译器报错。

因此即便当前教程中非必需，现在建立良好习惯可避免未来纠正错误习惯。

\#pragma once
----------------
现代编译器支持通过`#pragma`指令实现更简洁的头文件守卫：
```
#pragma once

// 代码在此
```
`#pragma once`与头文件守卫作用相同：避免头文件重复包含。传统守卫需开发者手动实现（\#ifndef/\#define/\#endif），而`#pragma once`由**编译器自动守卫**，具体实现方式由编译器决定。

> **进阶阅读**  
> 当头文件副本存在于文件系统不同位置时，若两个副本都被包含，头文件守卫能正确去重，但`#pragma once`可能失效（因编译器无法识别内容相同）。

多数项目中`#pragma once`运行良好，因其更简洁且不易出错。许多IDE创建新头文件时自动添加`#pragma once`。

> **警告**  
> `#pragma`指令专为编译器实现者设计，其支持范围和含义完全**由编译器决定**。除`#pragma once`外，不同编译器可能不支持相同的pragma指令。  
> 因`#pragma once`非C++标准内容，部分编译器可能未实现。故Google等公司建议使用传统头文件守卫。本教程系列采用最常规的头文件守卫，但现代C++普遍支持`#pragma once`，实际开发中可接受使用。

总结
----------------
头文件守卫确保头文件内容不会多次复制到同一文件中，从而防止重复定义。

重复**声明**无问题——但即使头文件仅含声明（无定义），添加头文件守卫仍是最佳实践。

注意：头文件守卫**不阻止**头文件被复制到不同项目文件中。这是合理设计，因我们常需在不同文件中引用同一头文件内容。

测验时间
----------------

**问题1**  
为此头文件添加头文件守卫：  
add.h：
```
int add(int x, int y);
```
  
<details><summary>答案</summary>
```
#ifndef ADD_H
#define ADD_H

int add(int x, int y);

#endif
```
</details>  

[下一课 2.13 如何设计首个程序](Chapter-2/lesson2.13-how-to-design-your-first-programs.md)  
[返回主页](/)    
[上一课 2.11 头文件](Chapter-2/lesson2.11-header-files.md)