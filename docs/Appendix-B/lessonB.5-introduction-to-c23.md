B.5 — C++23简介
=============================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月17日  
2024年1月25日（太平洋标准时间下午1:33）  

什么是 C++23？  
----------------  

2023年2月，ISO（国际标准化组织）批准了C++的新版本——C++23。  

C++23 主要改进  
----------------  

以下是C++23引入的主要变化（非完整清单，重点展示关键改进）：  

* **constexpr化的\<cmath\>**（例如`std::abs()`）与\<cstdlib\>（参见课程[6.7 — 关系运算符与浮点数比较](Chapter-6/lesson6.7-relational-operators-and-floating-point-comparisons.md)）  
* **constexpr化的`std::unique_ptr`**（暂无对应课程）  
* **显式`this`参数**（explicit this parameter）（暂无对应课程）  
* **固定精度浮点类型**（通过\<stdfloat\>实现）（暂无对应课程）  
* **格式化输出函数`std::print`与`std::println`**（暂无对应课程）  
* **`std::size_t`及其符号类型的字面量后缀**（参见课程[5.2 — 字面量](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)）  
* **多维下标`operator[]`**（在课程[17.13 — 多维std::array](Chapter-17/lesson17.13-multidimensional-stdarray.md)中提及）  
* **多维视图`std::mdspan`**（参见课程[17.13 — 多维std::array](Chapter-17/lesson17.13-multidimensional-stdarray.md)）  
* **预处理指令`#elifdef`与`#elifndef`**（暂无对应课程）  
* **预处理指令`#warning`**（暂无对应课程）  
* **堆栈追踪库**（stacktrace library）（暂无对应课程）  
* **标准库模块`std`与`std.compat`**（暂无对应课程）  
* **静态`operator()`与`operator[]`**（暂无对应课程）  
* **`std::bitset`完全constexpr化**  
* **`std::expected`**（暂无对应课程）  
* **`std::ranges`算法`starts_with`、`ends_with`、`contains`**（暂无对应课程）  
* **`std::string::contains`与`std::string_view::contains`**（暂无对应课程）  
* **`std::to_underlying`枚举底层类型转换**（参见课程[13.6 — 限定作用域枚举（枚举类）](Chapter-13/lesson13.6-scoped-enumerations-enum-classes.md)）  
* **`std::unreachable()`**（暂无对应课程）  
* **在常量表达式中使用未知指针和引用**（参见课程[17.2 — std::array的长度与索引](Chapter-17/lesson17.2-stdarray-length-and-indexing.md)）  

[下一课 C.1 终点？](Appendix-C/lessonC.1-appendix-c-the-end.md)  
[返回主页](/)  
[  
[上一课 B.4 C++20简介](Appendix-B/lessonB.4-introduction-to-c20.md)