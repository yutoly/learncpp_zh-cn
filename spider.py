#!/bin/env python
import requests
from bs4 import BeautifulSoup
from html_to_markdown import convert_to_markdown

import code # For debuging

# Toggle from 0:html, 1:markdown, 2:article(tag)
# To elaborate: `html` means the very orignal format and contents on the website;
#   `md` means to use html_to_markdown.convert_to_markdown() to convert the html to markdown;
#   `article` means to extract only the <article>-tag (the primary part) from the html.
flag = 1
formats = ["html", "md", "article"]
output_format = formats[flag]

# Get lesson list
res = requests.get("https://learncpp.com")
soup = BeautifulSoup(res.content.decode(), "html.parser")

# Found a way to filter out <div>s with class=lessontable on stackoverflow.com
# and the result happens to be a list whose indice representing the corresponding chapter No.
chapter_list = soup.find_all("div", {"class": "lessontable"})
for i in range(len(chapter_list)):
    # Find every <a> first
    all_tag_a = chapter_list[i].find_all("a")
    for j in range(len(all_tag_a)):
        tag = all_tag_a[j]
        # Judge whether there is "href" attr in the tag. We don't bother processing those tags without
        if "href" not in tag.attrs.keys():
            continue
        # Then find the No.(denoted as lessontable-row-number in html) and url
        rnumber = tag.parent.parent.find("div", {"class": "lessontable-row-number"}).string
        url = tag["href"]
        # Get lesson content
        lesson = BeautifulSoup(requests.get(url).content.decode(), "html.parser")
        # Filter out comment forms and leave only the main part
        # It takes me quite a lot time to figure out that I only need to extract <article> tag
        # and there will be no need to remove comment-about things manually :|
        # lesson.find(id="wpdcom").decompose() # something like these ww
        main = lesson.find("article")
        # Convert to markdown and save to file
        main = convert_to_markdown(main) if output_format == "md" else main
        # There is a trailing '/' in the end of url.
        chapter_id = rnumber.split('.')[0]
        # Tricky. Stupid way to do.
        chapter_name = ("Chapter-" if chapter_id.isdigit() or chapter_id in {"O", "F"} else "Appendix-") + chapter_id
        filename = "original/" + chapter_name + "/" + "lesson" + rnumber + "-" + url.split('/')[-2] + "." + output_format
        # It should be reasonable to save all contents to html while save only main part to md
        with open(filename, "w") as f:
            f.write([lesson.prettify(), main, main.prettify()][flag])
        print("Write successfully of lesson" + rnumber)

# Only relics saving indice to file facilitating analyse of document format
# with open("original/home.html", "w") as f:
#     f.write(soup.prettify())