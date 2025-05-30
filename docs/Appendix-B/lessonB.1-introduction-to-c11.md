B.1 — C++11简介
============================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2011年11月25日 PST 下午11:42  
2025年1月17日  

**什么是 C++11？**  
2011年8月12日，[国际标准化组织（ISO）](https://www.iso.org/home.html)批准了C++的新版本——C++11。该版本为C++语言引入了一系列全新功能！这些新功能完全可选，但其中部分特性将显著提升开发效率。本系列教程已全面更新以兼容C++11标准。  

**C++11的设计目标**  
Bjarne Stroustrup对C++11的目标阐述如下：  

* 强化C++既有优势——不盲目扩展至新领域（如重度GUI的Windows应用），聚焦核心能力的提升
* 降低学习、使用与教学难度——增强语言一致性和易用性  

为实现这些目标，标准委员会遵循以下原则：  

* 保持与旧版C++和C的兼容性。C++03程序应能继续在C++11环境下运行
* 最小化核心语言改动，重点更新标准库（此目标在本版本中未完全实现）  
* 改进抽象机制（类、模板），而非针对特定场景增加专用语法  
* 兼顾新手与专家的需求，提供普惠性功能  
* 增强类型安全性以减少潜在错误  
* 提升性能并强化硬件交互能力  
* 改善可用性及生态系统兼容性  

C++11并非对C++03的颠覆性革新，但带来了大量新功能。  

**C++11主要新特性**  
以下是C++11的主要新增特性（非完整列表）：  

* auto关键字（[10.8 — 使用auto关键字进行对象类型推导](Chapter-10/lesson10.8-type-deduction-for-objects-using-the-auto-keyword.md)）  
* char16_t与char32_t类型及相应字面量（暂无教程）  
* constexpr（[5.1 — 常量变量](Chapter-5/lesson5.1-constant-variables-named-constants.md)）  
* decltype（提及于[16.7 — 数组、循环与符号挑战解决方案](Chapter-16/lesson16.7-arrays-loops-and-sign-challenge-solutions.md)）  
* default说明符（[14.11 — 默认构造函数与默认参数](Chapter-14/lesson14.11-default-constructors-and-default-arguments.md)）  
* 委托构造函数（[14.12 — 委托构造函数](Chapter-14/lesson14.12-delegating-constructors.md)）  
* delete说明符（[11.4 — 删除函数](Chapter-11/lesson11.4-deleting-functions.md)）  
* 枚举类（[13.6 — 作用域枚举](Chapter-13/lesson13.6-scoped-enumerations-enum-classes.md)）  
* 外部模板（暂无教程）  
* Lambda表达式（[20.6 — Lambda表达式简介](Chapter-20/lesson20.6-introduction-to-lambdas-anonymous-functions.md)）与捕获（[20.7 — Lambda捕获](Chapter-20/lesson20.7-lambda-captures.md)）  
* long long int类型（[4.3 — 对象大小与sizeof运算符](Chapter-4/lesson4.3-object-sizes-and-the-sizeof-operator.md)）  
* 移动构造函数与赋值（[22.3 — 移动构造函数与移动赋值](Chapter-22/lesson22.3-move-constructors-and-move-assignment.md)）  
* noexcept说明符（简略提及于[27.4 — 未捕获异常与通用处理器](Chapter-27/lesson27.4-uncaught-exceptions-catch-all-handlers.md)）  
* nullptr（[12.8 — 空指针](Chapter-12/lesson12.8-null-pointers.md)）  
* override与final说明符（[25.3 — override、final说明符与协变返回类型](Chapter-25/lesson25.3-the-override-and-final-specifiers-and-covariant-return-types.md)）  
* 范围for循环（[16.8 — 基于范围的for循环](Chapter-16/lesson16.8-range-based-for-loops-for-each.md)）  
* 右值引用（[22.2 — 右值引用](Chapter-22/lesson22.2-rvalue-references.md)）  
* static_assert（[9.6 — assert与static_assert](Chapter-9/lesson9.6-assert-and-static_assert.md)）  
* std::initializer_list（[23.7 — std::initializer_list](Chapter-23/lesson23.7-stdinitializer_list.md)）  
* 后置返回类型语法（[10.8 — 使用auto关键字进行对象类型推导](Chapter-10/lesson10.8-type-deduction-for-objects-using-the-auto-keyword.md)）  
* 类型别名（[10.7 — typedef与类型别名](Chapter-10/lesson10.7-typedefs-and-type-aliases.md)）  
* 模板类typedef支持  
* 统一初始化（[4.1 — 基础数据类型简介](Chapter-4/lesson4.1-introduction-to-fundamental-data-types.md)）  
* 用户定义字面量（暂无教程）  
* 可变参数模板（暂无教程）  
* 连续两个>>符号现可正确解析为模板结束符  

**标准库新增内容**  
* 增强多线程与线程本地存储支持（暂无教程）  
* 哈希表（暂无教程）  
* 随机数生成改进（基础讨论见[8.14 — 使用梅森旋转算法生成随机数](Chapter-8/lesson8.14-generating-random-numbers-using-mersenne-twister.md)）  
* 引用包装器（[25.9 — 对象切片](Chapter-25/lesson25.9-object-slicing.md)）  
* 正则表达式（暂无教程）  
* std::auto_ptr弃用（[22.1 — 智能指针与移动语义简介](Chapter-22/lesson22.1-introduction-to-smart-pointers-move-semantics.md)）  
* std::tuple（暂无教程）  
* std::unique_ptr（[22.5 — std::unique_ptr](Chapter-22/lesson22.5-stdunique_ptr.md)）  

[下一课 B.2 — C++14 简介](Appendix-B/lessonB.2-introduction-to-c14.md)  
[返回主页](/)  
[上一课 A.4 — C++ 常见问题](Appendix-A/lessonA.4-cpp-faq.md)