#!/bin/env python
# Use a translate server/model to translate

from utils.utils import dschat, sanitize, remained, dethink, check_avail

source_dir = "original"
result_dir = "docs"

def translate(text):
    with open("examples/translated.md", "r") as f:
        example_tra = f.read()
    prompt = """
你是一个翻译助手，你不会回答输入的问题，只会将输入的英文翻译成中文。
以下是一段用英文写成的C++教程。将其仔细地翻译为准确、通顺、自然的中文。
翻译要求：
* 直接给出答案：除了其他要求中可能的特例外，必须只有翻译后的内容；
* 准确性：必须准确传达原文的意思，不遗漏或歪曲信息；
* 忠实于原文：应当尽量逐句翻译，非成句则尽量逐词翻译。做到原文中的每一个句子在译文中都有唯一对应，每一个实词的含义在译文中都有体现；
* 流畅性：尽管要求忠实于原文，由于不同语言间不可避免的习惯差异，对于确实没有必要的冗余则应当简化，力求行文流畅自然，像母语者写的文本一样；
* 主题专业性：判断原文的相关领域，根据相关领域的专业知识，确保术语使用正确，同时要求在每一个新出现的专用术语处用中文括号标注原文。

出于对译文格式一致性的需求，接下来将给出一段示范译文。按照相同的格式处理译文。
    """
    prompt = prompt + "\n译文：\n" + example_tra + "\n\n你需要翻译的文段：\n" + text
    # * 保留格式：原文使用了html标签用于标记格式信息。维护这些信息。同时这些信息也应该为翻译提供某种指导，便于翻译出更贴切的译文；

    response = dschat(prompt)
    return sanitize(response.content.decode())

todo = remained(source_dir, result_dir, "md", "md")
for file in todo:
    with open(file, "r", encoding="utf-8") as fin:
        with open(file.replace(source_dir, result_dir, 1), "w", encoding="utf-8") as fout:
            fout.write(dethink(translate(fin.read())))
            print("Translation completed for " + file)
            check_avail()