20.4 — 命令行参数  
================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年6月25日（首次发布于2008年2月15日）  

命令行参数的必要性  
----------------  

在课程[0.5 — 编译器、链接器与库简介](Chapter-0/lesson0.5-introduction-to-the-compiler-linker-and-libraries.md)中已了解，当编译链接程序时，输出结果是可执行文件。程序运行时，执行从main()函数顶部开始。至此我们一直使用以下形式声明main函数：  

```cpp
int main()
```  

此版本的main()不接收参数。然而许多程序需要输入数据才能工作。例如编写名为Thumbnail的程序读取图像文件并生成缩略图时，如何指定要处理的文件？用户需要告知程序目标文件。可采用以下方法：  

```cpp
// 程序：Thumbnail
#include <iostream>
#include <string>

int main()
{
    std::cout << "请输入要生成缩略图的文件名：";
    std::string filename{};
    std::cin >> filename;

    // 打开图像文件
    // 创建缩略图
    // 输出缩略图
}
```  

此方法存在问题：每次运行都需等待用户输入。这在手动运行单次时可行，但批量处理或由其他程序调用时效率低下。  

考虑需要处理目录中所有图像的情况。手动运行数百次显然低效。更好的方案是编写程序遍历目录，对每个文件调用Thumbnail。  

在网站场景中，用户上传图片后需自动生成缩略图。此时程序无法通过控制台接收输入，需让服务器在上传后自动调用Thumbnail。  

这两种情况都需要在程序启动时由外部程序传入文件名，而非运行时等待输入。  

**命令行参数（command line arguments）**是操作系统在程序启动时传递的可选字符串参数。程序可将其作为输入使用或忽略。类似于函数参数，命令行参数允许用户或程序在启动时向程序传递输入。  

传递命令行参数  
----------------  

在命令行中通过名称调用可执行程序。例如在Windows中运行当前目录的"WordCount"可执行文件：  

```
WordCount
```  

类Unix系统中的等效命令：  

```
./WordCount
```  

传递参数时只需在可执行文件名后列出参数：  

```
WordCount Myfile.txt
```  

此时Myfile.txt将作为命令行参数传递给WordCount。程序可接收多个以空格分隔的参数：  

```
WordCount Myfile.txt Myotherfile.txt
```  

在IDE中运行时，需通过特定方式输入参数：  

* Visual Studio：右键解决方案资源管理器中的项目 → 属性 → 配置属性 → 调试 → 命令参数  
* Code::Blocks：项目 → 设置程序参数  

使用命令行参数  
----------------  

要在C++程序中访问命令行参数，需使用以下形式的main()：  

```cpp
int main(int argc, char* argv[])
```  

或等效形式：  

```cpp
int main(int argc, char** argv)
```  

推荐第一种形式，因其更直观。  

* **argc（argument count）**：整数参数，表示传递的参数数量（包含程序自身名称，故至少为1）  
* **argv（argument values）**：存储实际参数值的C风格字符串指针数组，长度为argc  

示例程序"MyArgs"打印所有参数：  

```cpp
// 程序：MyArgs
#include <iostream>

int main(int argc, char* argv[])
{
    std::cout << "共接收 " << argc << " 个参数：\n";
    for (int count{ 0 }; count < argc; ++count)
    {
        std::cout << count << ' ' << argv[count] << '\n';
    }
    return 0;
}
```  

输入参数"Myfile.txt"和"100"时输出：  

```
共接收 3 个参数：
0 C:\MyArgs
1 Myfile.txt
2 100
```  

参数0是程序路径，参数1和2是用户输入的参数。  

处理数值型参数  
----------------  

命令行参数始终以字符串形式传递。要将数值参数转换为数字，需进行类型转换。C++实现方式如下：  

```cpp
#include <iostream>
#include <sstream>
#include <string>

int main(int argc, char* argv[])
{
    if (argc <= 1)
    {
        std::cout << "用法：" << (argv[0] ? argv[0] : "<程序名>") << " <数字>\n";
        return 1;
    }

    std::stringstream convert{ argv[1] };
    int myint{};
    if (!(convert >> myint)) myint = 0;

    std::cout << "转换后的整数：" << myint << '\n';
    return 0;
}
```  

输入"567"时输出：  

```
转换后的整数：567
```  

std::stringstream的用法类似于std::cin，未来章节将详细讨论。  

操作系统先解析参数  
----------------  

操作系统负责解析命令行中的特殊字符：  

* `MyArgs Hello world!` 输出3个参数（"Hello"和"world!"分开）  
* `MyArgs "Hello world!"` 输出2个参数（引号内为整体）  
* `MyArgs \"Hello world!\"` 输出3个参数（转义引号被解析）  

结论  
----------------  

命令行参数为程序启动时接收输入提供了有效方式。建议将必需输入数据设计为命令行参数，若无参数传入再请求用户输入。这种设计使程序能灵活适应不同使用场景。  

[下一课 20.5 — 省略号（及避免使用的原因）](Chapter-20/lesson20.5-ellipsis-and-why-to-avoid-them.md)  
[返回主页](/)  
[上一课 20.3 — 递归](Chapter-20/lesson20.3-recursion.md)