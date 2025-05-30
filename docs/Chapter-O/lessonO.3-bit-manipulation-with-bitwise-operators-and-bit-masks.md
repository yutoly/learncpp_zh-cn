O.3 — 使用位运算符和位掩码进行位操作  
===========================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2015年9月8日 下午9:12 PDT（首次发布）  
2024年7月21日

 

在前序课程[O.2 — 位运算符](Chapter-O/lessonO.2-bitwise-operators.md)中，我们讨论了各种位运算符如何对操作数中的每个位应用逻辑运算。现在我们已经理解其工作原理，让我们看看它们更常见的应用方式。

位掩码（bit mask）  
----------------  

要操作单个位（例如开启或关闭），我们需要某种方式来标识目标位。但位运算符本身无法直接识别位位置，而是通过**位掩码（bit mask）**来实现。位掩码是一组预定义的位，用于选择后续操作要修改的具体位。

现实场景类比：当粉刷窗框时，使用遮蔽胶带保护玻璃。类似地，位掩码通过屏蔽不需要修改的位，只允许访问目标位。

### C++14中的位掩码定义  
最简单的位掩码是为每个位位置定义单独的掩码。我们使用0屏蔽无关位，1标记目标位。虽然可以是字面量，但通常定义为符号常量以便复用：

```cpp
#include <cstdint>

constexpr std::uint8_t mask0{ 0b0000'0001 }; // 位0
constexpr std::uint8_t mask1{ 0b0000'0010 }; // 位1
// ...其余掩码定义类似
```

### C++11及更早版本的位掩码定义  
对于不支持二进制字面量的版本，有两种常用方法：  
1. 使用十六进制字面量（需熟悉十六进制转二进制）  
2. 使用左移运算符定位：

```cpp
constexpr std::uint8_t mask0{ 1 << 0 }; // 0000 0001
constexpr std::uint8_t mask1{ 1 << 1 }; // 0000 0010
// ...其余掩码定义类似
```

位状态检测  
----------------  
通过位与（&）运算符结合掩码检测位状态：

```cpp
std::uint8_t flags{ 0b0000'0101 };
std::cout << "位0状态：" << (flags & mask0 ? "开启\n" : "关闭\n");
```

置位操作  
----------------  
使用位或赋值（|=）开启特定位：

```cpp
flags |= mask1; // 开启位1
flags |= (mask4 | mask5); // 同时开启位4和位5
```

清除位  
----------------  
使用位与（&）和位非（~）组合清除位：

```cpp
flags &= ~mask2; // 关闭位2
flags &= ~(mask4 | mask5); // 同时关闭位4和位5
```

注意编译器可能提示符号转换警告，可通过强制类型转换解决：

```cpp
flags &= static_cast<std::uint8_t>(~mask2);
```

位翻转  
----------------  
使用异或（^=）翻转位状态：

```cpp
flags ^= mask2; // 翻转位2
flags ^= (mask4 | mask5); // 同时翻转位4和位5
```

std::bitset的位掩码应用  
----------------  
虽然std::bitset提供专用函数，但也可直接使用位运算符：

```cpp
std::bitset<8> flags{0b0000'0101};
flags ^= (mask1 | mask2); // 翻转位1和位2
```

语义化位掩码命名  
----------------  
推荐使用有意义的命名增强代码可读性：

```cpp
constexpr std::uint8_t 饥饿状态{ 1 << 0 };
constexpr std::uint8_t 悲伤状态{ 1 << 1 };
// ...其余状态定义
std::uint8_t 角色状态{};
角色状态 |= 快乐状态; // 设置快乐状态
```

位标志的适用场景  
----------------  
当存在大量相似标志变量时，位操作可显著节省内存。例如100个对象使用8位标志仅需108字节，而布尔数组需要800字节。

函数参数优化案例：

```cpp
// 传统布尔参数列表冗长难读
void 传统函数(bool 选项1, bool 选项2, ..., bool 选项32);

// 使用位掩码更简洁
void 优化函数(std::bitset<32> 选项);
优化函数(选项10 | 选项32); // 设置多个选项
```

多字节位掩码应用  
----------------  
32位RGBA颜色值解析示例：

```cpp
constexpr std::uint32_t 红掩码{ 0xFF000000 };
std::uint32_t 像素值{};
uint8_t 红分量 = (像素值 & 红掩码) >> 24; // 提取红色通道
```

操作总结  
----------------  
- 检测：`if (flags & mask)`  
- 置位：`flags |= mask`  
- 清除：`flags &= ~mask`  
- 翻转：`flags ^= mask`

测验解析  
----------------  
a) 设置文章为已读：  
```cpp
myArticleFlags |= option_viewed;
```

b) 检测删除状态：  
```cpp
if (myArticleFlags & option_deleted)
```

c) 取消收藏：  
```cpp
myArticleFlags &= static_cast<std::uint8_t>(~option_favorited);
```

d) 德摩根定律解释：  
`~(A|B) ≡ ~A & ~B`，故两种写法等效。

[下一课：O.4 — 整数的二进制与十进制转换](Chapter-O/lessonO.4-converting-integers-between-binary-and-decimal-representation.md)  
[返回主页](/)  
[上一课：O.2 — 位运算符](Chapter-O/lessonO.2-bitwise-operators.md)