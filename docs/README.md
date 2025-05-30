# LearnCpp\.com 中文翻译

欢迎来到本站！

如你所见，本站是[LearnCpp.com](https://learncpp.com/)的中文翻译站。在我看来，原网站的文章有如下优点：
- 持续更新：不仅有专门一章介绍自C++11以来每一个C++标准的主要变化（目前更新到C++23），你还能看到两章正在建设、以及一章收集弃用的文章；
- 讲授风格：以问题为导向，介绍在什么场景下会遇到什么样的问题，并介绍某个C++特性是如何解决它的；
- 及时练习：不少文章都附有习题，大部分章节也包含章节回顾与测试，部分章节还包含一个小项目；
- 开源在线：知识不应当收费，且应该容易获取。

目前网站的翻译基本都是LLM（deepseek-r1）翻译的，之后~~有时间~~我会人工校对；翻译原则是尽量保持原文的行文，同时减少冗余。不过我随机看了几篇文章，感觉翻译质量还是不错的，有些句子我的翻译还比它的要繁杂难解，所以目前的状态应该~~大部分~~ ~~除了部分格式不统一/不太对头之外~~都是可接受的。

任何有关本站的问题/建议/意见欢迎[提issue](https://github.com/yutoly/learncpp_zh-cn/issues/)！

## 原网站前言

> LearnCpp.com is a free website devoted to teaching you how to program in modern C++. The lessons on this site will walk you through all the steps needed to write, compile, and debug your C++ programs. No prior programming experience is necessary, but programmers of all levels will benefit from our best practices, tips, and insights.
> 
> Becoming an expert won’t happen overnight, but with a bit of patience, you’ll get there. And LearnCpp.com will show you the way.

LearnCpp\.com是一个致力于教你如何用现代C++编程的免费的网站。这个网站的课程将带领你走过编写、编译以及调试你的C++程序的必要步骤。无需编程经验，任何水平的程序员都能从我们的最佳实践、提示与观点中受益。

成为专家无法一蹴而就，但是只要有恒心，你就能做到。LearnCpp\.com会指引你的方向。

~~浓浓翻译腔。。翻译与编程都道阻且长啊~~

## 目录

- 第0章：介绍/起步
  - [0.1 — 本教程简介](Chapter-0/lesson0.1-introduction-to-these-tutorials.md)
  - [0.2 — 程序与编程语言简介](Chapter-0/lesson0.2-introduction-to-programming-languages.md)
  - [0.3 — C/C++简介](Chapter-0/lesson0.3-introduction-to-cplusplus.md)
  - [0.4 — C++开发入门](Chapter-0/lesson0.4-introduction-to-cpp-development.md)
  - [0.5 — 编译器、链接器与库简介](Chapter-0/lesson0.5-introduction-to-the-compiler-linker-and-libraries.md)
  - [0.6 — 安装集成开发环境（Integrated Development Environment，IDE）](Chapter-0/lesson0.6-installing-an-integrated-development-environment-ide.md)
  - [0.7 — 编译你的第一个程序](Chapter-0/lesson0.7-compiling-your-first-program.md)
  - [0.8 — 常见C++问题解析](Chapter-0/lesson0.8-a-few-common-cpp-problems.md)
  - [0.9 — 配置编译器：生成配置](Chapter-0/lesson0.9-configuring-your-compiler-build-configurations.md)
  - [0.10 — 配置编译器：编译器扩展](Chapter-0/lesson0.10-configuring-your-compiler-compiler-extensions.md)
  - [0.11 — 配置编译器：警告与错误等级](Chapter-0/lesson0.11-configuring-your-compiler-warning-and-error-levels.md)
  - [0.12 — 配置编译器：选择语言标准](Chapter-0/lesson0.12-configuring-your-compiler-choosing-a-language-standard.md)
  - [0.13 — 我的编译器使用什么语言标准？](Chapter-0/lesson0.13-what-language-standard-is-my-compiler-using.md)

- 第1章：C++基础
  - [1.1 — 语句与程序结构](Chapter-1/lesson1.1-statements-and-the-structure-of-a-program.md)
  - [1.2 — 注释](Chapter-1/lesson1.2-comments.md)
  - [1.3 — 对象与变量简介](Chapter-1/lesson1.3-introduction-to-objects-and-variables.md)
  - [1.4 — 变量赋值与初始化](Chapter-1/lesson1.4-variable-assignment-and-initialization.md)
  - [1.5 — 输入/输出流库（iostream）简介：cout、cin与endl](Chapter-1/lesson1.5-introduction-to-iostream-cout-cin-and-endl.md)
  - [1.6 — 未初始化变量与未定义行为](Chapter-1/lesson1.6-uninitialized-variables-and-undefined-behavior.md)
  - [1.7 — 关键字与标识符命名](Chapter-1/lesson1.7-keywords-and-naming-identifiers.md)
  - [1.8 — 空白符与基础格式](Chapter-1/lesson1.8-whitespace-and-basic-formatting.md)
  - [1.9 — 字面量与运算符简介](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)
  - [1.10 — 表达式简介](Chapter-1/lesson1.10-introduction-to-expressions.md)
  - [1.11 — 开发第一个程序](Chapter-1/lesson1.11-developing-your-first-program.md)
  - [1.x — 第一章总结与测验](Chapter-1/lesson1.x-chapter-1-summary-and-quiz.md)

- 第2章：C++基础之函数与文件
  - [2.1 — 函数入门](Chapter-2/lesson2.1-introduction-to-functions.md)
  - [2.2 — 函数返回值（值返回函数）](Chapter-2/lesson2.2-function-return-values-value-returning-functions.md)
  - [2.3 — void函数（非值返回函数）](Chapter-2/lesson2.3-void-functions-non-value-returning-functions.md)
  - [2.4 — 函数形参与实参入门](Chapter-2/lesson2.4-introduction-to-function-parameters-and-arguments.md)
  - [2.5 — 局部作用域入门](Chapter-2/lesson2.5-introduction-to-local-scope.md)
  - [2.6 — 函数的优势及高效使用方法](Chapter-2/lesson2.6-why-functions-are-useful-and-how-to-use-them-effectively.md)
  - [2.7 — 前向声明（forward declarations）与定义](Chapter-2/lesson2.7-forward-declarations.md)
  - [2.8 — 多代码文件程序](Chapter-2/lesson2.8-programs-with-multiple-code-files.md)
  - [2.9 — 命名冲突与命名空间简介](Chapter-2/lesson2.9-naming-collisions-and-an-introduction-to-namespaces.md)
  - [2.10 — 预处理器简介](Chapter-2/lesson2.10-introduction-to-the-preprocessor.md)
  - [2.11 — 头文件（Header Files）](Chapter-2/lesson2.11-header-files.md)
  - [2.12 — 头文件守卫（Header Guards）](Chapter-2/lesson2.12-header-guards.md)
  - [2.13 — 如何设计首个程序](Chapter-2/lesson2.13-how-to-design-your-first-programs.md)
  - [2.x — 第2章总结与测验](Chapter-2/lesson2.x-chapter-2-summary-and-quiz.md)

- 第3章：调试C++程序
  - [3.1 — 语法错误与语义错误](Chapter-3/lesson3.1-syntax-and-semantic-errors.md)
  - [3.2 — 调试流程](Chapter-3/lesson3.2-the-debugging-process.md)
  - [3.3 — 调试策略](Chapter-3/lesson3.3-a-strategy-for-debugging.md)
  - [3.4 — 基础调试策略](Chapter-3/lesson3.4-basic-debugging-tactics.md)
  - [3.5 — 进阶调试策略](Chapter-3/lesson3.5-more-debugging-tactics.md)
  - [3.6 — 使用集成调试器：单步执行](Chapter-3/lesson3.6-using-an-integrated-debugger-stepping.md)
  - [3.7 — 使用集成调试器：运行与断点](Chapter-3/lesson3.7-using-an-integrated-debugger-running-and-breakpoints.md)
  - [3.8 — 使用集成调试器：监视变量](Chapter-3/lesson3.8-using-an-integrated-debugger-watching-variables.md)
  - [3.9 — 使用集成调试器：调用栈](Chapter-3/lesson3.9-using-an-integrated-debugger-the-call-stack.md)
  - [3.10 — 在问题显现前发现隐患](Chapter-3/lesson3.10-finding-issues-before-they-become-problems.md)
  - [3.x — 第3章 总结与测验](Chapter-3/lesson3.x-chapter-3-summary-and-quiz.md)

- 第4章：基础数据类型
  - [4.1 — 基础数据类型简介](Chapter-4/lesson4.1-introduction-to-fundamental-data-types.md)
  - [4.2 — void类型](Chapter-4/lesson4.2-void.md)
  - [4.3 — 对象尺寸与sizeof操作符](Chapter-4/lesson4.3-object-sizes-and-the-sizeof-operator.md)
  - [4.4 — 有符号整数（Signed integers）](Chapter-4/lesson4.4-signed-integers.md)
  - [4.5 — 无符号整数及其规避原因](Chapter-4/lesson4.5-unsigned-integers-and-why-to-avoid-them.md)
  - [4.6 — 固定宽度整数与 size_t](Chapter-4/lesson4.6-fixed-width-integers-and-size-t.md)
  - [4.7 — 科学记数法简介](Chapter-4/lesson4.7-introduction-to-scientific-notation.md)
  - [4.8 — 浮点数](Chapter-4/lesson4.8-floating-point-numbers.md)
  - [4.9 — 布尔值](Chapter-4/lesson4.9-boolean-values.md)
  - [4.10 — if语句简介](Chapter-4/lesson4.10-introduction-to-if-statements.md)
  - [4.11 — 字符（Characters）](Chapter-4/lesson4.11-chars.md)
  - [4.12 — 类型转换与static_cast简介](Chapter-4/lesson4.12-introduction-to-type-conversion-and-static_cast.md)
  - [4.x — 第4章 小结与测验](Chapter-4/lesson4.x-chapter-4-summary-and-quiz.md)

- 第5章：常量与字符串
  - [5.1 — 常量变量（constant variables，具名常量）](Chapter-5/lesson5.1-constant-variables-named-constants.md)
  - [5.2 — 字面量（Literals）](Chapter-5/lesson5.2-literals.md)
  - [5.3 — 数值系统（十进制、二进制、十六进制与八进制）](Chapter-5/lesson5.3-numeral-systems-decimal-binary-hexadecimal-and-octal.md)
  - [5.4 — as-if规则与编译期优化](Chapter-5/lesson5.4-the-as-if-rule-and-compile-time-optimization.md)
  - [5.5 — 常量表达式](Chapter-5/lesson5.5-constant-expressions.md)
  - [5.6 — constexpr变量](Chapter-5/lesson5.6-constexpr-variables.md)
  - [5.7 — std::string简介](Chapter-5/lesson5.7-introduction-to-stdstring.md)
  - [5.8 — std::string_view 简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)
  - [5.9 — std::string_view（下篇）](Chapter-5/lesson5.9-stdstring_view-part-2.md)
  - [5.x — 第5章总结与测验](Chapter-5/lesson5.x-chapter-5-summary-and-quiz.md)

- 第6章：运算符
  - [6.1 — 运算符优先级与结合性](Chapter-6/lesson6.1-operator-precedence-and-associativity.md)
  - [6.2 — 算术运算符](Chapter-6/lesson6.2-arithmetic-operators.md)
  - [6.3 — 取余与幂运算](Chapter-6/lesson6.3-remainder-and-exponentiation.md)
  - [6.4 — 递增/递减运算符与副作用](Chapter-6/lesson6.4-increment-decrement-operators-and-side-effects.md)
  - [6.5 — 逗号运算符](Chapter-6/lesson6.5-the-comma-operator.md)
  - [6.6 — 条件运算符](Chapter-6/lesson6.6-the-conditional-operator.md)
  - [6.7 — 关系运算符与浮点数比较](Chapter-6/lesson6.7-relational-operators-and-floating-point-comparisons.md)
  - [6.8 — 逻辑运算符](Chapter-6/lesson6.8-logical-operators.md)
  - [6.x — 第6章总结与测验](Chapter-6/lesson6.x-chapter-6-summary-and-quiz.md)

- O：位操作（选读）
  - [O.1 — 位标志（bit flags）与通过std::bitset进行位操作（bit manipulation）](Chapter-O/lessonO.1-bit-flags-and-bit-manipulation-via-stdbitset.md)
  - [O.2 — 位操作符](Chapter-O/lessonO.2-bitwise-operators.md)
  - [O.3 — 使用位运算符和位掩码进行位操作](Chapter-O/lessonO.3-bit-manipulation-with-bitwise-operators-and-bit-masks.md)
  - [O.4 — 二进制与十进制整数的相互转换](Chapter-O/lessonO.4-converting-integers-between-binary-and-decimal-representation.md)

- 第7章：作用域、生命周期及链接
  - [7.1 — 复合语句（块）](Chapter-7/lesson7.1-compound-statements-blocks.md)
  - [7.2 — 用户自定义命名空间（user-defined namespaces）与作用域解析运算符（scope resolution operator）](Chapter-7/lesson7.2-user-defined-namespaces-and-the-scope-resolution-operator.md)
  - [7.3 — 局部变量](Chapter-7/lesson7.3-local-variables.md)
  - [7.4 — 全局变量简介](Chapter-7/lesson7.4-introduction-to-global-variables.md)
  - [7.5 — 变量遮蔽（名称隐藏）](Chapter-7/lesson7.5-variable-shadowing-name-hiding.md)
  - [7.6 — 内部链接](Chapter-7/lesson7.6-internal-linkage.md)
  - [7.7 — 外部链接与变量前向声明](Chapter-7/lesson7.7-external-linkage-and-variable-forward-declarations.md)
  - [7.8 — 为何（非常量）全局变量是万恶之源](Chapter-7/lesson7.8-why-non-const-global-variables-are-evil.md)
  - [7.9 — 内联函数与变量](Chapter-7/lesson7.9-inline-functions-and-variables.md)
  - [7.10 — 跨多文件共享全局常量（使用内联变量）](Chapter-7/lesson7.10-sharing-global-constants-across-multiple-files-using-inline-variables.md)
  - [7.11 — 静态局部变量](Chapter-7/lesson7.11-static-local-variables.md)
  - [7.12 — 作用域、持续时间与链接性总结](Chapter-7/lesson7.12-scope-duration-and-linkage-summary.md)
  - [7.13 — using声明与using指令](Chapter-7/lesson7.13-using-declarations-and-using-directives.md)
  - [7.14 — 未命名（匿名）与内联命名空间](Chapter-7/lesson7.14-unnamed-and-inline-namespaces.md)
  - [7.x — 第7章总结与测验](Chapter-7/lesson7.x-chapter-7-summary-and-quiz.md)

- 第8章：控制流
  - [8.1 — 控制流简介](Chapter-8/lesson8.1-control-flow-introduction.md)
  - [8.2 — if语句（if statements）与语句块（blocks）](Chapter-8/lesson8.2-if-statements-and-blocks.md)
  - [8.3 — 常见if语句问题](Chapter-8/lesson8.3-common-if-statement-problems.md)
  - [8.4 — constexpr if语句](Chapter-8/lesson8.4-constexpr-if-statements.md)
  - [8.5 — Switch语句基础](Chapter-8/lesson8.5-switch-statement-basics.md)
  - [8.6 — Switch 的贯穿现象与作用域](Chapter-8/lesson8.6-switch-fallthrough-and-scoping.md)
  - [8.7 — goto语句](Chapter-8/lesson8.7-goto-statements.md)
  - [8.8 — 循环与while语句入门](Chapter-8/lesson8.8-introduction-to-loops-and-while-statements.md)
  - [8.9 — do-while 语句](Chapter-8/lesson8.9-do-while-statements.md)
  - [8.10 — for语句](Chapter-8/lesson8.10-for-statements.md)
  - [8.11 — break 与 continue](Chapter-8/lesson8.11-break-and-continue.md)
  - [8.12 — 终止（提前退出程序）](Chapter-8/lesson8.12-halts-exiting-your-program-early.md)
  - [8.13 — 随机数生成简介](Chapter-8/lesson8.13-introduction-to-random-number-generation.md)
  - [8.14 — 使用梅森旋转算法生成随机数](Chapter-8/lesson8.14-generating-random-numbers-using-mersenne-twister.md)
  - [8.15 — 全局随机数（Random.h）](Chapter-8/lesson8.15-global-random-numbers-random-h.md)
  - [8.x — 第八章总结与测验](Chapter-8/lesson8.x-chapter-8-summary-and-quiz.md)

- 第9章：错误检测与处理
  - [9.1 — 代码测试简介](Chapter-9/lesson9.1-introduction-to-testing-your-code.md)
  - [9.2 — 代码覆盖率](Chapter-9/lesson9.2-code-coverage.md)
  - [9.3 — C++中的常见语义错误](Chapter-9/lesson9.3-common-semantic-errors-in-c.md)
  - [9.4 — 错误检测与处理](Chapter-9/lesson9.4-detecting-and-handling-errors.md)
  - [9.5 — std::cin与无效输入处理](Chapter-9/lesson9.5-stdcin-and-handling-invalid-input.md)
  - [9.6 — 断言（assert）与静态断言（static_assert）](Chapter-9/lesson9.6-assert-and-static_assert.md)
  - [9.x — 第9章总结与测验](Chapter-9/lesson9.x-chapter-9-summary-and-quiz.md)

- 第10章：类型转换、类型别名与类型推导
  - [10.1 — 隐式类型转换](Chapter-10/lesson10.1-implicit-type-conversion.md)
  - [10.2 — 浮点提升（Floating-point promotion）与整数提升（Integral promotion）](Chapter-10/lesson10.2-floating-point-and-integral-promotion.md)
  - [10.3 — 数值转换（Numeric conversions）](Chapter-10/lesson10.3-numeric-conversions.md)
  - [10.4 — 窄化转换（narrowing conversions）、列表初始化（list initialization）与constexpr初始化器（constexpr initializers）](Chapter-10/lesson10.4-narrowing-conversions-list-initialization-and-constexpr-initializers.md)
  - [10.5 — 算术转换](Chapter-10/lesson10.5-arithmetic-conversions.md)
  - [10.6 — 显式类型转换（casting）与 static_cast](Chapter-10/lesson10.6-explicit-type-conversion-casting-and-static-cast.md)
  - [10.7 — 类型别名（typedefs）与类型别名](Chapter-10/lesson10.7-typedefs-and-type-aliases.md)
  - [10.8 — 使用auto关键字进行对象类型推导](Chapter-10/lesson10.8-type-deduction-for-objects-using-the-auto-keyword.md)
  - [10.9 — 函数的类型推导](Chapter-10/lesson10.9-type-deduction-for-functions.md)
  - [10.x — 第10章总结与测验](Chapter-10/lesson10.x-chapter-10-summary-and-quiz.md)

- 第11章：函数重载与函数模板
  - [11.1 — 函数重载简介](Chapter-11/lesson11.1-introduction-to-function-overloading.md)
  - [11.2 — 函数重载的区分](Chapter-11/lesson11.2-function-overload-differentiation.md)
  - [11.3 — 函数重载解析与歧义匹配](Chapter-11/lesson11.3-function-overload-resolution-and-ambiguous-matches.md)
  - [11.4 — 删除函数](Chapter-11/lesson11.4-deleting-functions.md)
  - [11.5 — 默认参数](Chapter-11/lesson11.5-default-arguments.md)
  - [11.6 — 函数模板（Function Templates）](Chapter-11/lesson11.6-function-templates.md)
  - [11.7 — 函数模板实例化](Chapter-11/lesson11.7-function-template-instantiation.md)
  - [11.8 — 支持多模板类型的函数模板](Chapter-11/lesson11.8-function-templates-with-multiple-template-types.md)
  - [11.9 — 非类型模板参数](Chapter-11/lesson11.9-non-type-template-parameters.md)
  - [11.10 — 在多个文件中使用函数模板](Chapter-11/lesson11.10-using-function-templates-in-multiple-files.md)
  - [11.x — 第11章总结与测验](Chapter-11/lesson11.x-chapter-11-summary-and-quiz.md)

- F：常量表达式函数
  - [F.1 — 常量表达式函数（Constexpr functions）](Chapter-F/lessonF.1-constexpr-functions.md)
  - [F.2 — Constexpr函数（第二部分）](Chapter-F/lessonF.2-constexpr-functions-part-2.md)
  - [F.3 — constexpr函数（第三部分）与consteval](Chapter-F/lessonF.3-constexpr-functions-part-3-and-consteval.md)
  - [F.4 — Constexpr函数（第四部分）](Chapter-F/lessonF.4-constexpr-functions-part-4.md)
  - [F.X — 章节F总结与测验](Chapter-F/lessonF.X-chapter-f-summary-and-quiz.md)

- 第12章：复合类型：引用与指针
  - [12.1 — 复合数据类型简介](Chapter-12/lesson12.1-introduction-to-compound-data-types.md)
  - [12.2 — 值类别（左值与右值）](Chapter-12/lesson12.2-value-categories-lvalues-and-rvalues.md)
  - [12.3 — 左值引用（Lvalue references）](Chapter-12/lesson12.3-lvalue-references.md)
  - [12.4 — 对const的左值引用](Chapter-12/lesson12.4-lvalue-references-to-const.md)
  - [12.5 — 按左值引用传递](Chapter-12/lesson12.5-pass-by-lvalue-reference.md)
  - [12.6 — 常量左值引用传参](Chapter-12/lesson12.6-pass-by-const-lvalue-reference.md)
  - [12.7 — 指针简介](Chapter-12/lesson12.7-introduction-to-pointers.md)
  - [12.8 — 空指针](Chapter-12/lesson12.8-null-pointers.md)
  - [12.9 — 指针与const](Chapter-12/lesson12.9-pointers-and-const.md)
  - [12.10 — 按地址传递（Pass by address）](Chapter-12/lesson12.10-pass-by-address.md)
  - [12.11 — 传地址（下）](Chapter-12/lesson12.11-pass-by-address-part-2.md)
  - [12.12 — 返回引用与返回地址](Chapter-12/lesson12.12-return-by-reference-and-return-by-address.md)
  - [12.13 — 输入参数与输出参数](Chapter-12/lesson12.13-in-and-out-parameters.md)
  - [12.14 — 指针、引用与const的类型推导](Chapter-12/lesson12.14-type-deduction-with-pointers-references-and-const.md)
  - [12.15 — std::optional](Chapter-12/lesson12.15-stdoptional.md)
  - [12.x — 第12章 小结与测验](Chapter-12/lesson12.x-chapter-12-summary-and-quiz.md)

- 第13章：复合类型：枚举与结构体
  - [13.1 — 程序定义类型（program-defined types）简介](Chapter-13/lesson13.1-introduction-to-program-defined-user-defined-types.md)
  - [13.2 — 无作用域枚举](Chapter-13/lesson13.2-unscoped-enumerations.md)
  - [13.3 — 非限定作用域枚举的整型转换](Chapter-13/lesson13.3-unscoped-enumerator-integral-conversions.md)
  - [13.4 — 枚举类型与字符串的相互转换](Chapter-13/lesson13.4-converting-an-enumeration-to-and-from-a-string.md)
  - [13.5 — 运算符重载入门：I/O 运算符重载](Chapter-13/lesson13.5-introduction-to-overloading-the-i-o-operators.md)
  - [13.6 — 限定作用域枚举（enum classes）](Chapter-13/lesson13.6-scoped-enumerations-enum-classes.md)
  - [13.7 — 结构体（struct）、成员（member）与成员选择（member selection）入门](Chapter-13/lesson13.7-introduction-to-structs-members-and-member-selection.md)
  - [13.8 — 结构体的聚合初始化](Chapter-13/lesson13.8-struct-aggregate-initialization.md)
  - [13.9 — 默认成员初始化](Chapter-13/lesson13.9-default-member-initialization.md)
  - [13.10 — 结构体的传递与返回](Chapter-13/lesson13.10-passing-and-returning-structs.md)
  - [13.11 — 结构体杂项](Chapter-13/lesson13.11-struct-miscellany.md)
  - [13.12 -- 指针和引用的成员选择](Chapter-13/lesson13.12-member-selection-with-pointers-and-references.md)
  - [13.13 — 类模板](Chapter-13/lesson13.13-class-templates.md)
  - [13.14 — 类模板实参推导（CTAD）与推导指引](Chapter-13/lesson13.14-class-template-argument-deduction-ctad-and-deduction-guides.md)
  - [13.15 — 别名模板（alias templates）](Chapter-13/lesson13.15-alias-templates.md)
  - [13.x — 第13章总结与测验](Chapter-13/lesson13.x-chapter-13-summary-and-quiz.md)
  - [13.y — 使用语言参考](Chapter-13/lesson13.y-using-a-language-reference.md)

- 第14章：类简介
  - [14.1 — 面向对象编程简介](Chapter-14/lesson14.1-introduction-to-object-oriented-programming.md)
  - [14.2 — 类简介](Chapter-14/lesson14.2-introduction-to-classes.md)
  - [14.3 — 成员函数（Member functions）](Chapter-14/lesson14.3-member-functions.md)
  - [14.4 — 常量类对象与常量成员函数](Chapter-14/lesson14.4-const-class-objects-and-const-member-functions.md)
  - [14.5 — 公有成员与私有成员及访问说明符](Chapter-14/lesson14.5-public-and-private-members-and-access-specifiers.md)
  - [14.6 — 访问函数](Chapter-14/lesson14.6-access-functions.md)
  - [14.7 — 成员函数返回数据成员的引用](Chapter-14/lesson14.7-member-functions-returning-references-to-data-members.md)
  - [14.8 — 数据隐藏（封装）的优势](Chapter-14/lesson14.8-the-benefits-of-data-hiding-encapsulation.md)
  - [14.9 — 构造函数简介](Chapter-14/lesson14.9-introduction-to-constructors.md)
  - [14.10 — 构造函数成员初始化列表](Chapter-14/lesson14.10-constructor-member-initializer-lists.md)
  - [14.11 — 默认构造函数与默认参数](Chapter-14/lesson14.11-default-constructors-and-default-arguments.md)
  - [14.12 — 委托构造函数（Delegating Constructors）](Chapter-14/lesson14.12-delegating-constructors.md)
  - [14.13 — 临时类对象](Chapter-14/lesson14.13-temporary-class-objects.md)
  - [14.14 — 拷贝构造函数简介](Chapter-14/lesson14.14-introduction-to-the-copy-constructor.md)
  - [14.15 — 类初始化与拷贝省略（copy elision）](Chapter-14/lesson14.15-class-initialization-and-copy-elision.md)
  - [14.16 — 转换构造函数与explicit关键字](Chapter-14/lesson14.16-converting-constructors-and-the-explicit-keyword.md)
  - [14.17 — constexpr 聚合体与类](Chapter-14/lesson14.17-constexpr-aggregates-and-classes.md)
  - [14.x — 第14章总结与测验](Chapter-14/lesson14.x-chapter-14-summary-and-quiz.md)

- 第15章：类深入
  - [15.1 — 隐藏的“this”指针与成员函数链式调用](Chapter-15/lesson15.1-the-hidden-this-pointer-and-member-function-chaining.md)
  - [15.2 — 类（class）与头文件（header file）](Chapter-15/lesson15.2-classes-and-header-files.md)
  - [15.3 — 嵌套类型（成员类型）](Chapter-15/lesson15.3-nested-types-member-types.md)
  - [15.4 — 析构函数（destructor）简介](Chapter-15/lesson15.4-introduction-to-destructors.md)
  - [15.5 — 带有成员函数的类模板](Chapter-15/lesson15.5-class-templates-with-member-functions.md)
  - [15.6 — 静态成员变量](Chapter-15/lesson15.6-static-member-variables.md)
  - [15.7 — 静态成员函数](Chapter-15/lesson15.7-static-member-functions.md)
  - [15.8 — 友元非成员函数](Chapter-15/lesson15.8-friend-non-member-functions.md)
  - [15.9 — 友元类与友元成员函数](Chapter-15/lesson15.9-friend-classes-and-friend-member-functions.md)
  - [15.10 — 引用限定符](Chapter-15/lesson15.10-ref-qualifiers.md)
  - [15.x — 第15章总结与测验](Chapter-15/lesson15.x-chapter-15-summary-and-quiz.md)

- 第16章：动态数组：std::vector
  - [16.1 — 容器与数组入门](Chapter-16/lesson16.1-introduction-to-containers-and-arrays.md)
  - [16.2 — std::vector与列表构造函数简介](Chapter-16/lesson16.2-introduction-to-stdvector-and-list-constructors.md)
  - [16.3 — std::vector与无符号长度及下标问题](Chapter-16/lesson16.3-stdvector-and-the-unsigned-length-and-subscript-problem.md)
  - [16.4 — 传递std::vector](Chapter-16/lesson16.4-passing-stdvector.md)
  - [16.5 — 返回std::vector与移动语义简介](Chapter-16/lesson16.5-returning-stdvector-and-an-introduction-to-move-semantics.md)
  - [16.6 — 数组与循环](Chapter-16/lesson16.6-arrays-and-loops.md)
  - [16.7 — 数组、循环与符号挑战解决方案](Chapter-16/lesson16.7-arrays-loops-and-sign-challenge-solutions.md)
  - [16.8 — 范围for循环（for-each）](Chapter-16/lesson16.8-range-based-for-loops-for-each.md)
  - [16.9 — 使用枚举项进行数组索引与长度管理](Chapter-16/lesson16.9-array-indexing-and-length-using-enumerators.md)
  - [16.10 — std::vector 的调整大小与容量](Chapter-16/lesson16.10-stdvector-resizing-and-capacity.md)
  - [16.11 — std::vector 与栈行为](Chapter-16/lesson16.11-stdvector-and-stack-behavior.md)
  - [16.12 — std::vector\<bool\>](Chapter-16/lesson16.12-stdvector-bool.md)
  - [16.x — 第16章总结与测验](Chapter-16/lesson16.x-chapter-16-summary-and-quiz.md)

- 第17章：定长数组：std::array和C风格数组
  - [17.1 — std::array简介](Chapter-17/lesson17.1-introduction-to-stdarray.md)
  - [17.2 — std::array的长度与索引](Chapter-17/lesson17.2-stdarray-length-and-indexing.md)
  - [17.3 — 传递与返回 std::array](Chapter-17/lesson17.3-passing-and-returning-stdarray.md)
  - [17.4 — 类类型的std::array与花括号省略](Chapter-17/lesson17.4-stdarray-of-class-types-and-brace-elision.md)
  - [17.5 — 通过std::reference_wrapper实现引用数组](Chapter-17/lesson17.5-arrays-of-references-via-stdreference_wrapper.md)
  - [17.6 — std::array 与枚举类型](Chapter-17/lesson17.6-stdarray-and-enumerations.md)
  - [17.7 — C风格数组简介](Chapter-17/lesson17.7-introduction-to-c-style-arrays.md)
  - [17.8 — C 风格数组退化](Chapter-17/lesson17.8-c-style-array-decay.md)
  - [17.9 — 指针算术与下标操作](Chapter-17/lesson17.9-pointer-arithmetic-and-subscripting.md)
  - [17.10 — C风格字符串（C-style strings）](Chapter-17/lesson17.10-c-style-strings.md)
  - [17.11 — C风格字符串符号常量](Chapter-17/lesson17.11-c-style-string-symbolic-constants.md)
  - [17.12 — 多维C风格数组](Chapter-17/lesson17.12-multidimensional-c-style-arrays.md)
  - [17.13 — 多维std::array](Chapter-17/lesson17.13-multidimensional-stdarray.md)
  - [17.x — 第17章总结与测验](Chapter-17/lesson17.x-chapter-17-summary-and-quiz.md)

- 第18章：迭代器与算法（建设中）
  - [18.1 — 使用选择排序对数组排序](Chapter-18/lesson18.1-sorting-an-array-using-selection-sort.md)
  - [18.2 — 迭代器（iterator）简介](Chapter-18/lesson18.2-introduction-to-iterators.md)
  - [18.3 — 标准库算法简介](Chapter-18/lesson18.3-introduction-to-standard-library-algorithms.md)
  - [18.4 — 代码计时](Chapter-18/lesson18.4-timing-your-code.md)

- 第19章：动态分配（建设中）
  - [19.1 — new与delete动态内存分配](Chapter-19/lesson19.1-dynamic-memory-allocation-with-new-and-delete.md)
  - [19.2 — 动态分配数组](Chapter-19/lesson19.2-dynamically-allocating-arrays.md)
  - [19.3 — 析构函数](Chapter-19/lesson19.3-destructors.md)

- 第20章：函数
  - [20.1 — 函数指针（Function Pointers）](Chapter-20/lesson20.1-function-pointers.md)
  - [20.2 — 栈与堆](Chapter-20/lesson20.2-the-stack-and-the-heap.md)
  - [20.3 — 递归（Recursion）](Chapter-20/lesson20.3-recursion.md)
  - [20.4 — 命令行参数](Chapter-20/lesson20.4-command-line-arguments.md)
  - [20.5 — 省略号（及避免使用的原因）](Chapter-20/lesson20.5-ellipsis-and-why-to-avoid-them.md)
  - [20.6 — Lambda表达式（匿名函数）简介](Chapter-20/lesson20.6-introduction-to-lambdas-anonymous-functions.md)
  - [20.7 — Lambda捕获](Chapter-20/lesson20.7-lambda-captures.md)
  - [20.x — 第20章小结与测验](Chapter-20/lesson20.x-chapter-20-summary-and-quiz.md)

- 第21章：操作符重载
  - [21.1 — 操作符重载（operator overloading）简介](Chapter-21/lesson21.1-introduction-to-operator-overloading.md)
  - [21.2 — 使用友元函数重载算术运算符](Chapter-21/lesson21.2-overloading-the-arithmetic-operators-using-friend-functions.md)
  - [21.3 — 使用普通函数重载运算符](Chapter-21/lesson21.3-overloading-operators-using-normal-functions.md)
  - [21.4 — 重载I/O操作符](Chapter-21/lesson21.4-overloading-the-io-operators.md)
  - [21.5 — 使用成员函数重载运算符](Chapter-21/lesson21.5-overloading-operators-using-member-functions.md)
  - [21.6 — 重载一元运算符 +, -, 和 !](Chapter-21/lesson21.6-overloading-unary-operators.md)
  - [21.7 — 比较运算符的重载](Chapter-21/lesson21.7-overloading-the-comparison-operators.md)
  - [21.8 — 递增与递减运算符的重载](Chapter-21/lesson21.8-overloading-the-increment-and-decrement-operators.md)
  - [21.9 — 重载下标运算符（subscript operator）](Chapter-21/lesson21.9-overloading-the-subscript-operator.md)
  - [21.10 — 重载括号运算符（parenthesis operator）](Chapter-21/lesson21.10-overloading-the-parenthesis-operator.md)
  - [21.11 — 重载类型转换运算符](Chapter-21/lesson21.11-overloading-typecasts.md)
  - [21.12 — 重载赋值运算符](Chapter-21/lesson21.12-overloading-the-assignment-operator.md)
  - [21.13 — 浅拷贝与深拷贝](Chapter-21/lesson21.13-shallow-vs-deep-copying.md)
  - [21.14 — 运算符重载与函数模板](Chapter-21/lesson21.14-overloading-operators-and-function-templates.md)
  - [21.x — 第21章总结与测验](Chapter-21/lesson21.x-chapter-21-summary-and-quiz.md)
  - [21.y — 第21章项目](Chapter-21/lesson21.y-chapter-21-project.md)

- 第22章：移动语义与智能指针
  - [22.1 — 智能指针与移动语义入门](Chapter-22/lesson22.1-introduction-to-smart-pointers-move-semantics.md)
  - [22.2 — 右值引用](Chapter-22/lesson22.2-rvalue-references.md)
  - [22.3 — 移动构造函数与移动赋值](Chapter-22/lesson22.3-move-constructors-and-move-assignment.md)
  - [22.4 — std::move](Chapter-22/lesson22.4-stdmove.md)
  - [22.5 — std::unique_ptr（唯一指针）](Chapter-22/lesson22.5-stdunique_ptr.md)
  - [22.6 — std::shared_ptr（std::shared_ptr）](Chapter-22/lesson22.6-stdshared_ptr.md)
  - [22.7 — 使用 std::shared_ptr 时的循环依赖问题与 std::weak_ptr 解决方案](Chapter-22/lesson22.7-circular-dependency-issues-with-stdshared_ptr-and-stdweak_ptr.md)
  - [22.x — 第22章总结与测验](Chapter-22/lesson22.x-chapter-22-summary-and-quiz.md)

- 第23章：对象关系
  - [23.1 — 对象关系](Chapter-23/lesson23.1-object-relationships.md)
  - [23.2 — 组合](Chapter-23/lesson23.2-composition.md)
  - [23.3 — 聚合（Aggregation）](Chapter-23/lesson23.3-aggregation.md)
  - [23.4 — 关联](Chapter-23/lesson23.4-association.md)
  - [23.5 — 依赖关系](Chapter-23/lesson23.5-dependencies.md)
  - [23.6 — 容器类](Chapter-23/lesson23.6-container-classes.md)
  - [23.7 — std::initializer_list（初始化列表）](Chapter-23/lesson23.7-stdinitializer_list.md)
  - [23.x — 第23章总结与测验](Chapter-23/lesson23.x-chapter-23-summary-and-quiz.md)

- 第24章：继承
  - [24.1 — 继承简介](Chapter-24/lesson24.1-introduction-to-inheritance.md)
  - [24.2 — C++中的基础继承](Chapter-24/lesson24.2-basic-inheritance-in-c.md)
  - [24.3 — 派生类的构造顺序](Chapter-24/lesson24.3-order-of-construction-of-derived-classes.md)
  - [24.4 — 派生类的构造函数与初始化](Chapter-24/lesson24.4-constructors-and-initialization-of-derived-classes.md)
  - [24.5 — 继承与访问说明符](Chapter-24/lesson24.5-inheritance-and-access-specifiers.md)
  - [24.6 — 向派生类添加新功能](Chapter-24/lesson24.6-adding-new-functionality-to-a-derived-class.md)
  - [24.7 — 调用继承函数与重写行为](Chapter-24/lesson24.7-calling-inherited-functions-and-overriding-behavior.md)
  - [24.8 — 隐藏继承功能](Chapter-24/lesson24.8-hiding-inherited-functionality.md)
  - [24.9 — 多重继承](Chapter-24/lesson24.9-multiple-inheritance.md)
  - [24.x — 第24章总结与测验](Chapter-24/lesson24.x-chapter-24-summary-and-quiz.md)

- 第25章：虚函数
  - [25.1 — 基类指针与派生类对象的引用](Chapter-25/lesson25.1-pointers-and-references-to-the-base-class-of-derived-objects.md)
  - [25.2 — 虚函数与多态](Chapter-25/lesson25.2-virtual-functions.md)
  - [25.3 — override与final说明符，及协变返回类型](Chapter-25/lesson25.3-the-override-and-final-specifiers-and-covariant-return-types.md)
  - [25.4 — 虚析构函数、虚赋值与覆盖虚化](Chapter-25/lesson25.4-virtual-destructors-virtual-assignment-and-overriding-virtualization.md)
  - [25.5 — 早期绑定与晚期绑定](Chapter-25/lesson25.5-early-binding-and-late-binding.md)
  - [25.6 — 虚表](Chapter-25/lesson25.6-the-virtual-table.md)
  - [25.7 — 纯虚函数、抽象基类与接口类](Chapter-25/lesson25.7-pure-virtual-functions-abstract-base-classes-and-interface-classes.md)
  - [25.8 — 虚基类（virtual base classes）](Chapter-25/lesson25.8-virtual-base-classes.md)
  - [25.9 — 对象切片](Chapter-25/lesson25.9-object-slicing.md)
  - [25.10 — 动态转换（dynamic_cast）](Chapter-25/lesson25.10-dynamic-casting.md)
  - [25.11 — 使用operator<<打印继承类](Chapter-25/lesson25.11-printing-inherited-classes-using-operator.md)
  - [25.x — 第25章总结与测验](Chapter-25/lesson25.x-chapter-25-summary-and-quiz.md)

- 第26章：模板与类
  - [26.1 — 模板类（Template classes）](Chapter-26/lesson26.1-template-classes.md)
  - [26.2 — 模板非类型参数](Chapter-26/lesson26.2-template-non-type-parameters.md)
  - [26.3 — 函数模板特化](Chapter-26/lesson26.3-function-template-specialization.md)
  - [26.4 — 类模板特化（class template specialization）](Chapter-26/lesson26.4-class-template-specialization.md)
  - [26.5 — 偏特化（partial template specialization）](Chapter-26/lesson26.5-partial-template-specialization.md)
  - [26.6 — 指针的部分模板特化](Chapter-26/lesson26.6-partial-template-specialization-for-pointers.md)
  - [26.x — 第26章 小结与测验](Chapter-26/lesson26.x-chapter-26-summary-and-quiz.md)

- 第27章：异常
  - [27.1 — 异常处理的必要性](Chapter-27/lesson27.1-the-need-for-exceptions.md)
  - [27.2 — 基本异常处理](Chapter-27/lesson27.2-basic-exception-handling.md)
  - [27.3 — 异常处理、函数与栈展开](Chapter-27/lesson27.3-exceptions-functions-and-stack-unwinding.md)
  - [27.4 — 未捕获异常（uncaught exceptions）与全捕获处理程序（catch-all handlers）](Chapter-27/lesson27.4-uncaught-exceptions-catch-all-handlers.md)
  - [27.5 — 异常、类与继承](Chapter-27/lesson27.5-exceptions-classes-and-inheritance.md)
  - [27.6 — 重新抛出异常（Rethrowing exceptions）](Chapter-27/lesson27.6-rethrowing-exceptions.md)
  - [27.7 — 函数try块（Function try blocks）](Chapter-27/lesson27.7-function-try-blocks.md)
  - [27.8 — 异常机制的隐患与缺点](Chapter-27/lesson27.8-exception-dangers-and-downsides.md)
  - [27.9 — 异常规范与noexcept](Chapter-27/lesson27.9-exception-specifications-and-noexcept.md)
  - [27.10 — std::move_if_noexcept](Chapter-27/lesson27.10-stdmove_if_noexcept.md)
  - [27.x — 第27章总结与测验](Chapter-27/lesson27.x-chapter-27-summary-and-quiz.md)

- 第28章：输入与输出（I/O）
  - [28.1 — 输入与输出（I/O）流](Chapter-28/lesson28.1-input-and-output-io-streams.md)
  - [28.2 — 使用istream进行输入](Chapter-28/lesson28.2-input-with-istream.md)
  - [28.3 — 使用ostream与ios进行输出](Chapter-28/lesson28.3-output-with-ostream-and-ios.md)
  - [28.4 — 字符串流类](Chapter-28/lesson28.4-stream-classes-for-strings.md)
  - [28.5 — 流状态与输入验证](Chapter-28/lesson28.5-stream-states-and-input-validation.md)
  - [28.6 — 基础文件输入/输出](Chapter-28/lesson28.6-basic-file-io.md)
  - [28.7 — 随机文件I/O](Chapter-28/lesson28.7-random-file-io.md)

- 附录A：杂项
  - [A.1 — 静态库与动态库](Appendix-A/lessonA.1-a1-static-and-dynamic-libraries.md)
  - [A.2 — 在Visual Studio中使用库](Appendix-A/lessonA.2-a2-using-libraries-with-visual-studio-2005-express.md)
  - [A.3 — 在Code::Blocks中使用库](Appendix-A/lessonA.3-a3-using-libraries-with-codeblocks.md)
  - [A.4 — C++ 常见问题解答](Appendix-A/lessonA.4-cpp-faq.md)

- 附录B：C++的更新
  - [B.1 — C++11简介](Appendix-B/lessonB.1-introduction-to-c11.md)
  - [B.2 — C++14简介](Appendix-B/lessonB.2-introduction-to-c14.md)
  - [B.3 — C++17简介](Appendix-B/lessonB.3-introduction-to-c17.md)
  - [B.4 — C++20简介](Appendix-B/lessonB.4-introduction-to-c20.md)
  - [B.5 — C++23简介](Appendix-B/lessonB.5-introduction-to-c23.md)

- 附录C：终点
  - [C.1 — 结束了？](Appendix-C/lessonC.1-appendix-c-the-end.md)

- 附录D：废弃文章（即将移除）
  - [21.1 — 标准库](Appendix-D/lesson21.1-the-standard-library.md)
  - [21.2 — STL容器概览](Appendix-D/lesson21.2-stl-containers-overview.md)
  - [21.3 — STL迭代器（STL iterators）概览](Appendix-D/lesson21.3-stl-iterators-overview.md)
  - [21.4 — STL算法概述](Appendix-D/lesson21.4-stl-algorithms-overview.md)
  - [22.1 — std::string（标准字符串）与std::wstring（宽字符串）](Appendix-D/lesson22.1-stdstring-and-stdwstring.md)
  - [22.2 — std::string 的构造与析构](Appendix-D/lesson22.2-stdstring-construction-and-destruction.md)
  - [22.3 — std::string的长度与容量](Appendix-D/lesson22.3-stdstring-length-and-capacity.md)
  - [22.4 — std::string的字符访问及与C风格数组的转换](Appendix-D/lesson22.4-stdstring-character-access-and-conversion-to-c-style-arrays.md)
  - [22.5 — std::string 赋值与交换](Appendix-D/lesson22.5-stdstring-assignment-and-swapping.md)
  - [22.6 — std::string 追加操作](Appendix-D/lesson22.6-stdstring-appending.md)
  - [22.7 — std::string的插入操作](Appendix-D/lesson22.7-stdstring-inserting.md)
