0.13 — 我的编译器使用什么语言标准？
====================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年4月18日，太平洋夏令时上午10:29  
2024年12月29日  

以下程序用于打印编译器当前使用的C++语言标准名称。您可以通过复制/粘贴、编译和运行该程序来验证编译器是否符合预期的语言标准。  

PrintStandard.cpp：
```cpp
// 本程序打印编译器当前使用的C++语言标准
// 由learncpp.com（what-language-standard-is-my-compiler-using/）免费提供

#include <iostream>

const int numStandards = 7;
// C++26的标准代码是占位符，实际代码需待标准最终确定
const long stdCode[numStandards] = { 199711L, 201103L, 201402L, 201703L, 202002L, 202302L, 202612L};
const char* stdName[numStandards] = { "C++11前版本", "C++11", "C++14", "C++17", "C++20", "C++23", "C++26" };

long getCPPStandard()
{
    // Visual Studio在__cplusplus支持方面不符合标准（除非设置特定编译器标志）
    // 在Visual Studio 2015及以上版本可使用_MSVC_LANG替代
    // 参考https://devblogs.microsoft.com/cppblog/msvc-now-correctly-reports-__cplusplus/
#if defined (_MSVC_LANG)
    return _MSVC_LANG;
#elif defined (_MSC_VER)
    // 若使用旧版Visual Studio则返回错误
    return -1;
#else
    // __cplusplus是查询语言标准代码的规范方式（由语言标准定义）
    return __cplusplus;
#endif
}

int main()
{
    long standard = getCPPStandard();

    if (standard == -1)
    {
        std::cout << "错误：无法确定您的语言标准。\n";
        return 0;
    }
    
    for (int i = 0; i < numStandards; ++i)
    {
        // 若报告版本是已发布的标准代码
        if (standard == stdCode[i])
        {
            std::cout << "您的编译器使用" << stdName[i]
                << "（语言标准代码" << standard << "L）\n";
            break;
        }

        // 若报告版本介于两个已发布标准之间
        // 则可能是下一版本的预览/实验性支持
        if (standard < stdCode[i])
        {
            std::cout << "您的编译器使用" << stdName[i]
                << "的预览版/预发布版（语言标准代码" << standard << "L）\n";
            break;
        }
    }
    
    return 0;
}
```

编译或运行时问题  
----------------  

若编译时遇到错误，可能是项目设置不当。请参考[0.8 — 常见C++问题](Chapter-0/lesson0.8-a-few-common-cpp-problems.md)获取常见问题解决方案。若问题未解决，请复习[0.6 — 安装集成开发环境（IDE）](Chapter-0/lesson0.6-installing-an-integrated-development-environment-ide.md)及后续课程。  

若程序输出"错误：无法确定您的语言标准"，可能您的编译器不符合标准。若使用主流编译器出现此情况，请在下方留言提供相关信息（如编译器名称及版本）。  

若输出与预期语言标准不符：  
* 检查IDE设置确保编译器配置正确。参考[0.12 — 配置编译器：选择语言标准](Chapter-0/lesson0.12-configuring-your-compiler-choosing-a-language-standard.md)了解主流编译器的配置方法。注意避免拼写或格式错误。某些编译器需为每个项目单独设置语言标准（而非全局设置），新建项目时需特别注意。  

* IDE或编译器可能未正确读取配置文件（VS Code用户偶有反馈）。若怀疑此情况，请查阅相关文档。  

问：若编译器使用预览版/预发布版，是否应退回旧版？  
答：若仅为学习语言，无需退回。请注意即将发布版本中的某些功能可能缺失、不完整、存在缺陷或可能微调。  

[下一课 1.1 — 语句与程序结构](Chapter-1/lesson1.1-statements-and-the-structure-of-a-program.md)  
[返回主页](/)  
[上一课 0.12 — 配置编译器：选择语言标准](Chapter-0/lesson0.12-configuring-your-compiler-choosing-a-language-standard.md)