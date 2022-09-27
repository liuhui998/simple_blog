from pprint import pprint
from pathlib import Path
import marko


class PeterMarkdownParser:

    def __init__(self, text):
        self.text = text.strip()
        self.title = ""
        self.categories = []
        self.html_body = ""
        self.markdown_body = ""

    def load_from_file(self, path):
        self.text = Path(path).read_text().strip()

    def parse(self):
        if len(self.text) == 0:
            return
        blog_lines = self.text.split("\n")
        hr_lines = list(1 if (line == "---") else 0
                        for line in blog_lines[0:30])
        if 2 != sum(hr_lines):  # 表示有 Markdown 头
            return
        second_occur_hr = -1
        for index in range(1, 30):
            if "---" == blog_lines[index]:
                second_occur_hr = index
                break

        self.markdown_body = "\n".join(blog_lines[second_occur_hr + 1:])
        self.html_body = marko.convert(self.markdown_body)


if __name__ == "__main__":
    p = PeterMarkdownParser("")
    p.load_from_file(
        "/Users/peter/code/django/simple_blog/blog/data/markdown/2020-08-28-do-not-be-anxious.markdown"
    )
    p.parse()
    pprint(p.title)
    pprint(p.categories)
    pprint(p.html_body)
    pprint(p.markdown_body)