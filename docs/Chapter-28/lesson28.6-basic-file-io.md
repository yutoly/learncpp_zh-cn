28.6 — 基础文件输入/输出  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年3月31日（首次发布于2008年3月31日）  
2024年2月27日更新  

C++中的文件输入/输出（file I/O）与标准I/O操作非常相似（仅增加了少量复杂性）。C++包含3个基础文件I/O类（file I/O classes）：ifstream（派生自istream）、ofstream（派生自ostream）和fstream（派生自iostream）。这些类分别处理文件输入、输出和输入/输出操作。使用文件I/O类需要包含fstream头文件。


与可直接使用的cout、cin、cerr和clog流不同，文件流（file streams）必须由程序员显式设置。但操作极其简单：要打开文件进行读/写，只需实例化对应的文件I/O类对象，并将文件名作为参数传入。然后使用插入（<<）或提取（>>）运算符进行文件读写。操作完成后，可通过以下方式关闭文件：显式调用close()函数，或让文件I/O变量离开作用域（文件I/O类析构函数将自动关闭文件）。


**文件输出（File output）**  
以下示例使用ofstream类进行文件输出：  

```cpp
#include <fstream>
#include <iostream>
 
int main()
{
    // ofstream用于写文件
    // 创建名为Sample.txt的文件
    std::ofstream outf{ "Sample.txt" };

    // 检查文件是否成功打开
    if (!outf)
    {
        std::cerr << "无法打开Sample.txt进行写入！\n";
        return 1;
    }

    // 写入两行内容
    outf << "这是第一行\n";
    outf << "这是第二行\n";

    return 0;
    // outf离开作用域时，ofstream析构函数将关闭文件
}
```

在项目目录中可找到生成的Sample.txt文件，用文本编辑器打开可见写入的两行内容。


注意：也可使用put()函数向文件写入单个字符。


**文件输入（File input）**  
现在读取先前创建的文件内容。注意ifstream在到达文件末尾（EOF）时返回0，我们利用此特性控制读取循环：  

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    // ifstream用于读文件
    std::ifstream inf{ "Sample.txt" };

    if (!inf)
    {
        std::cerr << "无法打开Sample.txt进行读取！\n";
        return 1;
    }

    std::string strInput{};
    while (inf >> strInput)
        std::cout << strInput << '\n';
    
    return 0;
    // inf离开作用域时自动关闭文件
}
```

输出结果：  

```
这是
第一行
这是
第二行
```

由于提取运算符（>>）按空白符分隔，需改用getline()读取整行：  

```cpp
while (std::getline(inf, strInput))
    std::cout << strInput << '\n';
```

输出正确结果：  

```
这是第一行
这是第二行
```

**缓冲输出（Buffered output）**  
C++输出可能采用缓冲机制（buffered），即多次输出操作可能被批量处理后再写入磁盘（称为缓冲区刷新，flushing）。关闭文件时会自动刷新缓冲区。程序异常终止（崩溃或调用exit()）时可能丢失缓冲数据，因此建议在调用exit()前显式关闭文件。


可手动刷新缓冲区：使用ostream::flush()函数或输出std::flush。注意std::endl也会刷新缓冲区，频繁使用可能影响性能。建议使用'\n'替代std::endl以避免不必要的刷新。


**文件模式（File modes）**  
文件流构造函数可接受第二个参数指定打开模式（file modes），模式标志定义于ios类：  

| ios文件模式 | 含义 |
| --- | --- |
| app | 追加模式 |
| ate | 初始定位到文件末尾 |
| binary | 二进制模式 |
| in | 读模式（ifstream默认） |
| out | 写模式（ofstream默认） |
| trunc | 若文件存在则清空 |


多个模式可用按位或（\|）组合。fstream默认使用std::ios::in \| std::ios::out模式，但若文件不存在可能失败。创建新文件时建议仅使用std::ios::out模式。


示例：追加内容到已有文件：  

```cpp
std::ofstream outf{ "Sample.txt", std::ios::app };
outf << "这是第三行\n";
outf << "这是第四行\n";
```

最终文件内容：  

```
这是第一行
这是第二行
这是第三行
这是第四行
```

**显式打开文件（Explicitly opening files）**  
可使用open()函数显式打开文件，用法与构造函数相同：  

```cpp
std::ofstream outf{ "Sample.txt" };
outf << "内容";
outf.close();

outf.open("Sample.txt", std::ios::app);
outf << "追加内容";
outf.close();
```

关于open()函数的详细信息可参考[cppreference](https://en.cppreference.com/w/cpp/io/basic_filebuf/open)。

[下一课 28.7 — 随机文件I/O](Chapter-28/lesson28.7-random-file-io.md)  
[返回主页](/)  
[上一课 28.5 — 流状态与输入验证](Chapter-28/lesson28.5-stream-states-and-input-validation.md)