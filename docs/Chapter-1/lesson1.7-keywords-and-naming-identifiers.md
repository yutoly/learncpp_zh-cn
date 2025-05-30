1.7 — 关键字与标识符命名  
======================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月18日（首次发布于2007年6月5日）  

**关键字**  
C\+\+（截至C\+\+23标准）保留了92个词汇供语言内部使用，这些词汇称为**关键字（keywords）**或保留字，每个关键字在C\+\+中都有特殊含义。  

以下是C\+\+23标准的关键字列表：  
* alignas  
* alignof  
* and  
* and_eq  
* asm  
* auto  
* bitand  
* bitor  
* bool  
* break  
* case  
* catch  
* char  
* char8_t（C\+\+20新增）  
* char16_t  
* char32_t  
* class  
* compl  
* concept（C\+\+20新增）  
* const  
* consteval（C\+\+20新增）  
* constexpr  
* constinit（C\+\+20新增）  
* const_cast  
* continue  
* co_await（C\+\+20新增）  
* co_return（C\+\+20新增）  
* co_yield（C\+\+20新增）  
* decltype  
* default  
* delete  
* do  
* double  
* dynamic_cast  
* else  
* enum  
* explicit  
* export  
* extern  
* false  
* float  
* for  
* friend  
* goto  
* if  
* inline  
* int  
* long  
* mutable  
* namespace  
* new  
* noexcept  
* not  
* not_eq  
* nullptr  
* operator  
* or  
* or_eq  
* private  
* protected  
* public  
* register  
* reinterpret_cast  
* requires（C\+\+20新增）  
* return  
* short  
* signed  
* sizeof  
* static  
* static_assert  
* static_cast  
* struct  
* switch  
* template  
* this  
* thread_local  
* throw  
* true  
* try  
* typedef  
* typeid  
* typename  
* union  
* unsigned  
* using  
* virtual  
* void  
* volatile  
* wchar_t  
* while  
* xor  
* xor_eq  

标注（C\+\+20）的关键字是该版本新增内容。若编译器未完全支持C\+\+20标准，这些关键字可能不可用。  

C\+\+还定义了特殊标识符：*override*、*final*、*import*和*module*。这些标识符在特定上下文中有特殊含义，但不属于保留字。  

您已接触过部分关键字（如`int`和`return`）。这些关键字与运算符共同构成了C\+\+语言的核心（预处理指令除外）。在集成开发环境中，关键字通常以特殊颜色突出显示。  

完成本系列教程后，您将掌握这些词汇的绝大多数用法！  

**标识符命名规则**  
变量、函数、类型等实体的名称统称为**标识符（identifier）**。C\+\+对标识符命名有以下硬性规定：  
* 不可使用关键字  
* 只能包含字母（大小写）、数字和下划线  
* 不能包含符号（下划线除外）或空白字符  
* 必须以字母或下划线开头  
* 区分大小写（`nvalue`、`nValue`、`NVALUE`为不同标识符）  

**标识符命名最佳实践**  
1. **变量名首字母小写**：  
```cpp
int value; // 符合惯例
int Value; // 不符合（首字母应小写）
int VALUE; // 不符合（应全小写）
int VaLuE; // 不符合（建议心理辅导）;)
```  

**函数名**通常也以小写字母开头（C\+\+标准库函数均遵循此规范）。**用户自定义类型**（结构体、类、枚举等）通常以大写字母开头。  

2. **多单词命名惯例**：  
* 下划线分隔（蛇形命名法）  
* 驼峰式命名法（camelCase）  

```cpp
int my_variable_name;   // 符合惯例（下划线）
int my_function_name(); // 符合惯例（下划线）

int myVariableName;     // 符合惯例（驼峰式）
int myFunctionName();   // 符合惯例（驼峰式）

int my variable name;   // 无效（含空格）
int MyVariableName;     // 不符合（首字母应小写）
```  

本教程采用驼峰式以提高可读性（下划线在密集代码中易被误认为空格）。C\+\+标准库多使用下划线法，实际项目中两种风格可能混合使用。  

> **最佳实践**  
> 参与现有项目时，应遵循项目原有命名规范。新建项目时采用现代最佳实践。  

3. **避免以下划线开头**：此类名称通常保留给操作系统、库和编译器使用。  

4. **名称应清晰表达含义**（尤其是单位不明确时）：  
* 短作用域标识符可用简短名称  
* 全局访问标识符适用较长名称  
* 通用数值可用短名称  
* 特定值应使用详细名称  

| 不良命名 | 推荐命名 | 说明 |  
| --- | --- | --- |  
| `int ccount` | `int customerCount` | 明确计数对象 |  
| `int data` | `int minutesElapsed` | 避免模糊描述 |  
| `int _count` | `int numApples` | 下划线开头不推荐 |  

5. **避免非常用缩写**：常见无歧义缩写（如`num`、`cm`、`idx`）可接受。  

> **核心洞见**  
> 代码阅读频率远高于编写频率。使用编辑器自动补全功能提升编码效率，而非依赖缩写。  

6. **变量声明注释**：对非显性内容添加注释说明。例如：  
```cpp
// 统计文本字符数（含空格和标点）
int numChars {};
```  

**测验时间**  
**问题1**  
判断以下变量名是否符合规范：  
`int sum {};`（假设用途明确）  
<details><summary>答案</summary>符合规范</details>  

`int _apples {};`  
<details><summary>答案</summary>不符合规范（避免下划线开头）</details>  

`int VALUE {};`  
<details><summary>答案</summary>不符合规范（应全小写）</details>  

`int my variable name {};`  
<details><summary>答案</summary>无效（含空格）</details>  

`int TotalCustomers {};`  
<details><summary>答案</summary>不符合规范（首字母应小写）</details>  

`int void {};`  
<details><summary>答案</summary>无效（void是关键字）</details>  

`int numFruit {};`  
<details><summary>答案</summary>符合规范</details>  

`int 3some {};`  
<details><summary>答案</summary>无效（数字开头）</details>  

`int meters_of_pipe {};`  
<details><summary>答案</summary>符合规范</details>  

[下一课 1.8 — 空格与基础格式](Chapter-1/lesson1.8-whitespace-and-basic-formatting.md)  
[返回主页](/)  
[上一课 1.6 — 未初始化变量与未定义行为](Chapter-1/lesson1.6-uninitialized-variables-and-undefined-behavior.md)