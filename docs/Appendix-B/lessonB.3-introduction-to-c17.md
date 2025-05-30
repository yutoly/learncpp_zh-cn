B.3 — C++17简介  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月17日（首次发布于2018年3月31日）  

**什么是C++17？**  

2017年9月，[ISO（国际标准化组织）](https://www.iso.org/home.html)批准了C++的新版本——C++17。C++17包含相当数量的新增内容。  

**C++17的主要改进**  

以下列出C++17的主要变化，请注意本列表并非详尽无遗，仅重点展示部分关键改进：  

* 类模板参数推导（CTAD）([13.14 — 类模板参数推导（CTAD）与推导指引](Chapter-13/lesson13.14-class-template-argument-deduction-ctad-and-deduction-guides.md))  
* 编译时解析的if语句（constexpr if）([8.4 — constexpr if语句](Chapter-8/lesson8.4-constexpr-if-statements.md))  
* if语句与switch语句中的初始化器（参见[13.y — 使用语言参考](Chapter-13/lesson13.y-using-a-language-reference.md)）  
* 内联变量（inline variables）([7.10 — 通过内联变量在多文件间共享全局常量](Chapter-7/lesson7.10-sharing-global-constants-across-multiple-files-using-inline-variables.md))  
* 折叠表达式（fold expressions）（暂无教程）  
* 强制拷贝消除（部分情况）([14.15 — 类初始化与拷贝消除](Chapter-14/lesson14.15-class-initialization-and-copy-elision.md))  
* 嵌套命名空间支持X::Y语法([7.2 — 用户定义命名空间与作用域解析运算符](Chapter-7/lesson7.2-user-defined-namespaces-and-the-scope-resolution-operator.md))  
* 移除std::auto_ptr及其他已弃用类型  
* static_assert不再需要诊断信息参数([9.6 — assert与static_assert](Chapter-9/lesson9.6-assert-and-static_assert.md))  
* std::any（暂无教程）  
* std::byte（暂无教程）  
* std::filesystem（暂无教程）  
* std::optional([12.15 — std::optional](Chapter-12/lesson12.15-stdoptional.md))  
* std::shared_ptr支持管理C风格数组（但std::make_shared尚未支持）([22.6 — std::shared_ptr](Chapter-22/lesson22.6-stdshared_ptr.md))  
* std::size([11.2 — 数组（第二部分）](arrays-part-ii/))  
* std::string_view([5.8 — std::string_view简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md))  
* 结构化绑定声明（structured binding declarations）（暂无教程）  
* 移除三字符组（trigraphs）  
* 模板模板参数中可用typename替代class  
* UTF-8（u8）字符字面量（暂无教程）  

[下一课 B.4 — C++20简介](Appendix-B/lessonB.4-introduction-to-c20.md)  
[返回主页](/)  
[  
[上一课 B.2 — C++14简介](Appendix-B/lessonB.2-introduction-to-c14.md)