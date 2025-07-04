7.12 — 作用域、持续时间与链接性总结  
============================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2016年4月19日 下午5:05（PDT）  
2024年12月1日  

 

由于作用域（scope）、持续时间（duration）和链接性（linkage）的概念容易混淆，我们特别开设本课进行总结。部分内容尚未涉及，此处仅作完整性参考。

作用域小结  
----------------  
标识符的作用域决定其在源代码中的可访问范围：  

* **块作用域（局部作用域）**的变量：  
  + 从声明点开始至所在代码块结束（包括嵌套块）  
  + 包含：  
    - 局部变量  
    - 函数参数  
    - 块内定义的程序自定义类型（如枚举和类）  

* **全局作用域**的变量与函数：  
  + 从声明点开始至文件结束  
  + 包含：  
    - 全局变量  
    - 函数  
    - 命名空间或全局作用域内定义的程序自定义类型  

持续时间小结  
----------------  
变量的持续时间决定其创建与销毁时机：  

* **自动持续时间**变量：  
  + 在定义时创建，离开所在块时销毁  
  + 包含：  
    - 局部变量  
    - 函数参数  

* **静态持续时间**变量：  
  + 程序启动时创建，程序结束时销毁  
  + 包含：  
    - 全局变量  
    - 静态局部变量  

* **动态持续时间**变量：  
  + 由程序员控制创建与销毁  
  + 包含：  
    - 动态分配变量  

链接性小结  
----------------  
标识符的链接性决定不同作用域中同名声明是否指向同一实体：  

* **无链接性**标识符：  
  + 每个声明指向独立实体  
  + 包含：  
    - 局部变量  
    - 块内定义的程序自定义类型  

* **内部链接性**标识符：  
  + 同一翻译单元内同名声明指向同一实体  
  + 包含：  
    - 静态全局变量（无论是否初始化）  
    - 静态函数  
    - const全局变量  
    - 未命名命名空间及其内部定义项  

* **外部链接性**标识符：  
  + 整个程序中同名声明指向同一实体  
  + 包含：  
    - 非静态函数  
    - 非const全局变量（无论是否初始化）  
    - extern const全局变量  
    - inline const全局变量  
    - 命名空间  

注意：具有外部链接性的标识符若被多个.cpp文件编译定义，通常会导致重复定义链接错误（违反单一定义规则）。例外情况包括类型、模板和内联函数/变量，后续课程将详述。

变量作用域、持续时间与链接性总表  
----------------  

| 类型                | 示例                    | 作用域  | 持续时间 | 链接性   | 备注                        |
|---------------------|-------------------------|---------|----------|----------|-----------------------------|
| 局部变量            | int x;                 | 块      | 自动     | 无       |                             |
| 静态局部变量        | static int s_x;        | 块      | 静态     | 无       |                             |
| 动态局部变量        | int* x { new int{} };  | 块      | 动态     | 无       |                             |
| 函数参数            | void foo(int x)        | 块      | 自动     | 无       |                             |
| 内部非const全局变量 | static int g_x;        | 全局    | 静态     | 内部     | 可初始化或未初始化          |
| 外部非const全局变量 | int g_x;               | 全局    | 静态     | 外部     | 可初始化或未初始化          |
| 内联非const全局变量 | inline int g_x; (C++17)| 全局    | 静态     | 外部     | 可初始化或未初始化          |
| 内部常量全局变量    | constexpr int g_x{1};  | 全局    | 静态     | 内部     | 必须初始化                  |
| 外部常量全局变量    | extern const int g_x{1};| 全局   | 静态     | 外部     | 必须初始化                  |
| 内联常量全局变量    | inline constexpr g_x{1};| 全局   | 静态     | 外部     | 必须初始化                  |

前向声明小结  
----------------  
通过前向声明可访问其他文件的函数或变量，作用域遵循常规规则：  

| 类型                | 示例                    | 备注                        |
|---------------------|-------------------------|-----------------------------|
| 函数前向声明        | void foo(int x);        | 仅原型，无函数体            |
| 非const变量前向声明 | extern int g_x;         | 必须未初始化                |
| const变量前向声明   | extern const int g_x;   | 必须未初始化                |
| constexpr变量前向声明 | extern constexpr int g_x; | 不允许，constexpr不能前向声明 |

注意：constexpr变量（隐式const）可通过const变量前向声明访问，此时变量视为const而非constexpr。

存储类说明符解析  
----------------  
`static`和`extern`作为标识符声明的一部分时称为**存储类说明符（storage class specifier）**，用于设置存储持续时间和链接性。  

C++支持的4种有效存储类说明符：  

| 说明符       | 含义                        | 备注                     |
|--------------|-----------------------------|--------------------------|
| extern       | 静态/线程存储 + 外部链接性  |                          |
| static       | 静态/线程存储 + 内部链接性  |                          |
| thread_local | 线程存储持续时间            |                          |
| mutable      | 允许修改const类对象成员      |                          |
| auto         | 自动存储持续时间            | C++11弃用                |
| register     | 自动存储 + 寄存器存储提示    | C++17弃用                |

术语"存储类说明符"通常仅用于正式文档。

[下一课 7.13 使用声明与使用指令](Chapter-7/lesson7.13-using-declarations-and-using-directives.md)  
[返回主页](/)  
[上一课 7.11 静态局部变量](Chapter-7/lesson7.11-static-local-variables.md)