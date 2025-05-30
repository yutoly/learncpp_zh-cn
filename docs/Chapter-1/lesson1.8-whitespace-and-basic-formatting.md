1.8 — 空白符与基础格式  
======================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月1日 下午5:22（PDT时间）  
2024年1月23日（更新）  

**空白符（whitespace）**指用于格式控制的字符。在C++中主要指空格、制表符（tab）和换行符。C++中的空白符主要有三个用途：分隔特定语言元素、文本内容处理、以及代码格式化。  

必须使用空白符分隔的语言元素  
----------------  

某些语言元素必须通过空白符分隔。这主要出现在两个关键字或标识符（identifier）需要连续出现时，以便编译器区分它们。  

例如变量声明必须使用空白符分隔：  

```cpp
int x; // int与x必须用空白符分隔
```  

若写成`intx`，编译器会将其视为一个标识符并报错。  

另一个例子是函数返回类型与名称必须分隔：  

```cpp
int main(); // int与main必须用空白符分隔
```  

当需要空白符作为分隔符时，编译器不关心具体数量，只需存在即可。以下变量定义均有效：  

```cpp
int x;
int                y;
            int 
z;
```  

某些情况下换行符也作为分隔符。例如单行注释（//）以换行符结束。  

错误示范：  

```cpp
std::cout << "Hello world!"; // 注释内容
这是非注释内容 // 编译错误
```  

预处理指令（如`#include <iostream>`）必须独占一行：  

```cpp
#include <iostream>
#include <string>
```  

文本内容中的空白符处理  
----------------  

引号内的文本会保留所有空白符：  

```cpp
std::cout << "Hello world!";
```  

与以下代码输出不同：  

```cpp
std::cout << "Hello          world!"; // 输出带多个空格的文本
```  

引号内不允许换行：  

```cpp
std::cout << "Hello
     world!"; // 错误！
```  

仅用空白符分隔的多个引号文本会被拼接：  

```cpp
std::cout << "Hello "
     "world!"; // 输出"Hello world!"
```  

使用空白符格式化代码  
----------------  

空白符在其他场景主要用于提高代码可读性。例如以下代码难以阅读：  

```cpp
#include <iostream>
int main(){std::cout<<"Hello world";return 0;}
```  

改进版本：  

```cpp
#include <iostream>
int main() {
std::cout << "Hello world";
return 0;
}
```  

更佳版本：  

```cpp
#include <iostream>

int main()
{
    std::cout << "Hello world";

    return 0;
}
```  

语句可跨多行书写：  

```cpp
#include <iostream>

int main()
{
    std::cout
        << "Hello world"; // 有效写法
    return 0;
}
```  

这对长语句特别有用。  

基础格式规范  
----------------  

C++不强制格式要求，但建议遵循以下规范：  

1. **缩进**：使用制表符或空格缩进（建议设置制表符为4空格宽度）  
2. **函数大括号**：两种常见风格  
   - 开括号跟随语句：`int main() {`  
   - 开括号独立成行（本教程采用）：  
     ```cpp
     int main()
     {
         // 语句
     }
     ```  
3. **语句缩进**：函数体内语句统一缩进一级  
4. **行长限制**：建议不超过80字符，过长时合理换行：  
   ```cpp
   std::cout << "This is a really long line" 
       << " continued here"; // 续行额外缩进
   ```  
5. **运算符位置**：换行时运算符置于行首：  
   ```cpp
   int result = 3 + 4
       + 5 * 6;
   ```  
6. **对齐优化**：通过空格提升可读性：  
   ```cpp
   cost          = 57;    // 对齐赋值符号
   pricePerItem  = 24;
   ```  

自动格式化工具  
----------------  

现代IDE通常提供自动格式化功能：  
- **Visual Studio**：*编辑 > 高级 > 格式化文档*  
- **Code::Blocks**：右键 > *Format use AStyle*  
建议配置快捷键以便快速格式化。外部工具如[clang-format](https://clang.llvm.org/docs/ClangFormat.html)也可使用。  

> **最佳实践**  
> 建议启用自动格式化保持代码风格统一。  

风格指南  
----------------  

**风格指南（style guide）**是包含编程规范的文档，常见C++风格指南包括：  
- [C++核心指南](http://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)（Bjarne Stroustrup与Herb Sutter维护）  
- [Google风格指南](https://google.github.io/styleguide/cppguide.html)  
- [LLVM编码标准](https://llvm.org/docs/CodingStandards.html)  
- [GCC/GNU规范](https://gcc.gnu.org/codingconventions.html)  

本教程推荐遵循C++核心指南。  

> **注意事项**  
> 参与现有项目时，应遵循项目已有风格。  

[下一课 1.9 — 字面量与运算符简介](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)  
[返回主页](/)  
[上一课 1.7 — 关键字与标识符命名](Chapter-1/lesson1.7-keywords-and-naming-identifiers.md)