# LearnCpp_zh-cn

C++教程LearnCpp.com的中文翻译。翻译方式为LLM翻译，再人工校对。人工校对完成的部分，文件头添加`edited`标记。

完成翻译的文件存储在`translated/`下，为Markdown格式；通过[Docsify](https://github.com/docsify/docsify)部署在GitHub Pages上。[访问网站](https://yutoly.github.io/learncpp_zh-cn/)

## 源码结构

```
.
├── configs.json
├── examples/       # 翻译样例
├── .git
├── .gitignore
├── LICENSE
├── original/       # 存储原网站数据
├── README.md
├── spider.py       # 获取原网站数据
├── translated/     # 存储翻译结果
├── translate.py    # 翻译脚本
├── utils/          # 工具脚本
└── venv/           # Python虚拟环境

```