28.7 — 随机文件I/O  
================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年4月4日 PDT下午10:04（首次发布于2008年4月4日）  
2024年4月16日  

**文件指针（file pointer）**  

每个文件流类都包含一个文件指针（file pointer），用于跟踪文件当前的读/写位置。进行文件读写操作时，操作总是发生在文件指针的当前位置。默认情况下，以读/写模式打开文件时，文件指针位于文件开头。若以追加模式打开，文件指针则位于文件末尾，确保写入不会覆盖现有内容。  

**使用seekg()和seekp()进行随机文件访问**  

目前我们接触的都是顺序文件访问（sequential file access）——即按顺序读写文件内容。但C++也支持随机文件访问（random file access）——即在文件中跳跃定位到不同位置读取内容。这在处理包含多条记录（record）的文件时非常有用，可以直接定位到目标记录而无需逐条读取。  

通过seekg()（输入流）和seekp()（输出流）函数可操作文件指针实现随机访问。g代表"get"（获取），p代表"put"（放置）。对于文件流而言，读写位置始终同步，因此这两个函数可以互换使用。  

这两个函数接收两个参数：  
- 第一个参数是偏移量（offset），决定移动的字节数  
- 第二个参数是ios定位标志（ios seek flag），指定偏移量基准点  

| ios定位标志 | 含义 |  
| --- | --- |  
| beg | 偏移量相对于文件开头（默认） |  
| cur | 偏移量相对于当前位置 |  
| end | 偏移量相对于文件末尾 |  

正偏移量使指针向文件末尾移动，负偏移量则向文件开头移动。示例：  

```cpp
inf.seekg(14, std::ios::cur); // 向前移动14字节
inf.seekg(-18, std::ios::cur); // 向后移动18字节
inf.seekg(22, std::ios::beg); // 定位至文件第22字节
inf.seekg(24); // 定位至文件第24字节（默认beg）
inf.seekg(-28, std::ios::end); // 定位至文件末尾前28字节
```  

快速定位文件首尾：  

```cpp
inf.seekg(0, std::ios::beg); // 定位至文件开头
inf.seekg(0, std::ios::end); // 定位至文件末尾
```  

> **警告**  
> 在文本文件中进行非起始位置定位可能导致意外行为。  
>  
> 编程中的换行符（newline）是抽象概念：  
> * Windows使用CR（回车）+ LF（换行）两个字节表示  
> * Unix仅使用LF一个字节  
>  
> 跨越换行符的定位会因编码不同产生差异。部分系统可能在文件末尾填充零字节（zero byte），导致基于末尾的定位结果不一致。  

假设使用上节课创建的输入文件：  

```
This is line 1  
This is line 2  
This is line 3  
This is line 4  
```  

示例程序：  

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    std::ifstream inf{ "Sample.txt" };

    if (!inf)
    {
        std::cerr << "无法打开Sample.txt！\n";
        return 1;
    }

    std::string strData;

    inf.seekg(5); // 定位至第5字符
    std::getline(inf, strData); // 读取剩余行（第1行）
    std::cout << strData << '\n';

    inf.seekg(8, std::ios::cur); // 再移动8字节
    std::getline(inf, strData); // 读取第2行剩余
    std::cout << strData << '\n';

    inf.seekg(-14, std::ios::end); // 定位至末尾前14字节
    std::getline(inf, strData); // 可能产生未定义行为
    std::cout << strData << '\n';

    return 0;
}
```  

输出结果：  

```
is line 1  
line 2  
This is line 4  
```  

> **译注**  
> 第三行结果可能因文件编码不同而变化。  

二进制文件更适合seekg()/seekp()操作。可通过以下方式以二进制模式打开文件：  

```cpp
std::ifstream inf{ "Sample.txt", std::ifstream::binary };
```  

tellg()和tellp()函数可获取文件指针的绝对位置，常用于计算文件大小：  

```cpp
std::ifstream inf{ "Sample.txt" };
inf.seekg(0, std::ios::end);
std::cout << inf.tellg(); // 输出文件字节数
```  

在Windows系统可能输出64（包含CR+LF换行），Unix系统则为60（仅LF）。  

**使用fstream同时读写文件**  

fstream类支持同时读写文件，但需注意：  
- 读写操作切换必须通过修改文件位置的操作（如seek）  
- 即使不移动指针，也需要执行定位操作来切换模式  

示例（将文件中的元音替换为#）：  

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    std::fstream iofile{ "Sample.txt", std::ios::in | std::ios::out };

    if (!iofile)
    {
        std::cerr << "无法打开Sample.txt！\n";
        return 1;
    }

    char chChar{};

    while (iofile.get(chChar))
    {
        switch (chChar)
        {
            case 'a': case 'e': case 'i': case 'o': case 'u':
            case 'A': case 'E': case 'I': case 'O': case 'U':
                iofile.seekg(-1, std::ios::cur); // 回退1字节
                iofile << '#'; // 写入#
                iofile.seekg(iofile.tellg(), std::ios::beg); // 保持位置
                break;
        }
    }

    return 0;
}
```  

运行后文件内容变为：  

```
Th#s #s l#n# 1  
Th#s #s l#n# 2  
Th#s #s l#n# 3  
Th#s #s l#n# 4  
```  

**其他实用文件函数**  

- remove()：删除文件  
- is_open()：检查流是否打开  

**关于将指针写入磁盘的警告**  

将指针（pointer）地址写入磁盘存在严重风险：  
- 变量的地址在不同执行过程中可能变化  
- 读取时原地址可能不再有效  

示例：  
将指向nValue（地址0x0012FF7C）的指针pnValue写入磁盘。重新运行时nValue可能位于0x0012FF78，此时读取的pnValue将指向无效地址。  

> **警告**  
> 切勿将内存地址写入文件。变量地址在程序不同执行时可能变化，导致读取的地址失效。  

[下一课 A.1 静态库与动态库](Appendix-A/lessonA.1-a1-static-and-dynamic-libraries.md)  
[返回主页](/)  
[上一课 28.6 基础文件I/O](Chapter-28/lesson28.6-basic-file-io.md)