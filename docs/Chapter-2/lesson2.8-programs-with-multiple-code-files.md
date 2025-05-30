2.8 — 多代码文件程序  
========================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月2日 下午8:26（太平洋夏令时）  
2025年2月11日  

向项目添加文件  
----------------  

随着程序规模扩大，通常需要将其拆分为多个文件以实现组织性或可重用性。使用集成开发环境（IDE）的优势在于能简化多文件操作。您已了解如何创建和编译单文件项目，向现有项目添加新文件非常简便。  

> **最佳实践**  
> 向项目添加新代码文件时，请使用.cpp扩展名。  

**Visual Studio用户**  
在解决方案资源管理器窗口中右键点击*源文件*文件夹（或项目名称），选择*添加 > 新建项…*。  
注意：若通过*文件菜单*而非解决方案资源管理器创建文件，需手动将其加入项目。右键点击*源文件*选择*添加 > 现有项*，然后选择文件。  
编译时将在输出中看到文件名。  

**Code::Blocks用户**  
通过*文件 > 新建 > 文件…*创建文件。  
编译时将在输出中看到文件名。  

**gcc用户**  
在命令行中使用编辑器创建附加文件并命名。编译时需在命令行包含所有相关代码文件。例如：*g++ main.cpp add.cpp -o main*，其中*main.cpp*和*add.cpp*是代码文件，*main*是输出文件名。  

**VS Code用户**  
选择*视图 > 资源管理器*打开面板，点击项目名右侧的*新建文件*图标（或通过*文件 > 新建文件*）。命名时保留.cpp扩展名。若文件出现在*.vscode*文件夹内，请将其拖至项目文件夹。  
接着打开*tasks.json*文件，定位到`"${file}",`行：  
- 显式指定编译文件：用文件名替换该行（每行一个），例如：  
  `"main.cpp",`  
  `"add.cpp",`  
- 自动编译目录内所有.cpp文件：  
  - Windows：替换为`"${fileDirname}\\**.cpp"`  
  - Unix系统：替换为`"${fileDirname}/**.cpp"`  

多文件示例  
----------------  
在课程[2.7 — 前向声明与定义](Chapter-2/lesson2.7-forward-declarations.md)中，我们见过无法编译的单文件程序：  
```cpp
#include <iostream>

int main()
{
    std::cout << "3加4的和是: " << add(3, 4) << '\n';
    return 0;
}

int add(int x, int y)
{
    return x + y;
}
```  
当编译器在*main*函数第5行遇到*add*调用时，由于*add*在第9行才定义，会导致编译错误。当时的解决方案是调整函数顺序（将*add*置前）或使用*add*的前向声明。  

现在观察类似的多文件程序：  
add.cpp：  
```cpp
int add(int x, int y)
{
    return x + y;
}
```  
main.cpp：  
```cpp
#include <iostream>

int main()
{
    std::cout << "3加4的和是: " << add(3, 4) << '\n'; // 编译错误
    return 0;
}
```  
无论编译器先编译哪个文件，*main.cpp*都会因相同错误失败：  
```
main.cpp(5) : 错误 C3861: 未找到标识符'add'
```  
原因相同：编译器处理*main.cpp*第5行时不认识标识符*add*。  

编译器独立编译每个文件，既不感知其他文件内容，也不记忆已编译文件的信息。即使先前编译过*add.cpp*（若其先被编译），编译器也不会保留*add*函数的定义。这种有限的可见性和短暂记忆是刻意设计的：  
1. 允许项目源文件按任意顺序编译  
2. 修改源文件时仅需重新编译该文件  
3. 降低不同文件标识符命名冲突的可能性  

命名冲突问题将在下节探讨（[2.9 — 命名冲突与命名空间简介](Chapter-2/lesson2.9-naming-collisions-and-an-introduction-to-namespaces.md)）。  

解决方案与前文相同：将*add*函数定义置于*main*函数前，或通过前向声明满足编译器。由于函数*add*位于不同文件，调整顺序不可行，故采用前向声明：  
main.cpp（含前向声明）：  
```cpp
#include <iostream>

int add(int x, int y); // 告知main.cpp add()是在别处定义的函数

int main()
{
    std::cout << "3加4的和是: " << add(3, 4) << '\n';
    return 0;
}
```  
add.cpp（保持不变）：  
```cpp
int add(int x, int y)
{
    return x + y;
}
```  
现在编译器处理*main.cpp*时能识别*add*标识符。链接器（linker）会将*main.cpp*中的*add*调用关联到*add.cpp*的函数定义。  
尝试自行编译含前向声明的*main.cpp*和*add.cpp*。若遇链接错误，请检查是否已将*add.cpp*正确加入项目或编译命令。  

> **提示**  
> 编译器独立编译各文件（且不保留记忆），因此每个使用`std::cout`或`std::cin`的代码文件都需`#include <iostream>`。  
> 若上例中`add.cpp`使用了这些对象，则必须包含该头文件。  

> **关键洞察**  
> 当标识符在表达式中使用时，必须连接到其定义：  
> - 若编译器在当前文件既未见前向声明也未见定义，将在使用点报错  
> - 若同文件存在定义，编译器直接关联标识符  
> - 若定义位于不同文件（且对链接器可见），链接器负责关联  
> - 否则链接器将报"未找到标识符定义"错误  

故障排查  
----------------  
首次处理多文件时可能遇到以下问题：  
1. 若编译器报*main*中未定义*add*：可能忘记在*main.cpp*添加函数*add*的前向声明  
2. 若链接器报*add*未定义（如`unresolved external symbol "int __cdecl add(int,int)"`）：  
   a) 最常见原因：*add.cpp*未正确加入项目。编译时应看到*main.cpp*和*add.cpp*同时被处理。若仅见*main.cpp*，说明*add.cpp*未被编译。在Visual Studio或Code::Blocks中，检查*add.cpp*是否显示在IDE侧边栏的解决方案资源管理器/项目面板中。若未显示，请右键项目添加文件后重新编译。命令行编译时需在命令中同时包含*main.cpp*和*add.cpp*  
   b) 可能将*add.cpp*添加到了错误项目  
   c) 文件可能被设置为不编译/不链接。检查文件属性确保其配置为参与编译/链接。Code::Blocks中需勾选编译和链接复选框；Visual Studio中"排除生成"选项应为"否"或留空。注意分别检查各生成配置（如调试版和发布版）  
3. **切勿**在*main.cpp*中`#include "add.cpp"`。虽然本例能编译，但包含.cpp文件会增加命名冲突等意外风险（尤其当程序变复杂时）。详细讨论见课程[2.10 — 预处理器简介](Chapter-2/lesson2.10-introduction-to-the-preprocessor.md)  

小结  
----------------  
C++设计允许各源文件独立编译且无需知晓其他文件内容，因此文件编译顺序无关紧要。进入面向对象编程后我们将频繁使用多文件，请确保掌握多文件项目的添加和编译方法。  

> **提醒**  
> 创建新代码(.cpp)文件后，必须将其加入项目以参与编译。  

测验时间  
----------------  
**问题#1**  
将以下程序拆分为两个文件（main.cpp和input.cpp）。main.cpp包含main函数，input.cpp包含getInteger函数。  
[查看提示](javascript:void(0))  
提示：勿忘在main.cpp中对getInteger()进行前向声明。  
```cpp
#include <iostream>

int getInteger()
{
	std::cout << "输入整数: ";
	int x{};
	std::cin >> x;
	return x;
}

int main()
{
	int x{ getInteger() };
	int y{ getInteger() };

	std::cout << x << " + " << y << " = " << x + y << '\n';
	return 0;
}
```  
  
input.cpp：  
```cpp
#include <iostream> // 此文件需包含iostream

int getInteger()
{
	std::cout << "输入整数: ";
	int x{};
	std::cin >> x;
	return x;
}
```  
main.cpp：  
```cpp
#include <iostream> // 此文件同样需要iostream

int getInteger(); // getInteger函数的前向声明

int main()
{
	int x{ getInteger() };
	int y{ getInteger() };

	std::cout << x << " + " << y << " = " << x + y << '\n';
	return 0;
}
```  
若链接器报`getInteger()`未定义错误，可能忘记编译*input.cpp*。  

[下一课 2.9 命名冲突与命名空间简介](Chapter-2/lesson2.9-naming-collisions-and-an-introduction-to-namespaces.md)  
[返回主页](/)  
[上一课 2.7 前向声明与定义](Chapter-2/lesson2.7-forward-declarations.md)