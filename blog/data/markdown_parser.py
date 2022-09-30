from pprint import pprint
from pathlib import Path
from ast import literal_eval
from datetime import datetime
import marko
import os


class PeterMarkdownParser:

    def __init__(self, text=None, file_path=None):
        self.title = ""
        self.header_text = ""
        self.categories = []
        self.html_body = ""
        self.markdown_body = ""
        self.date = None

        if text:
            self.text = text.strip()
        elif file_path:
            self.load_from_file(file_path)
        else:
            raise Exception("text or file_path should be specified either!")
        self.parse()

    def load_from_file(self, path):
        self.text = Path(path).read_text().strip()

    def parse(self):
        if len(self.text) == 0:
            return
        blog_lines = self.text.split("\n")
        hr_lines = list(1 if (line == "---") else 0
                        for line in blog_lines[0:8])
        if 2 != sum(hr_lines):  # 表示有 Markdown 头
            return
        second_occur_hr = -1
        for index in range(1, 30):
            if "---" == blog_lines[index]:
                second_occur_hr = index
                break
        self.header_text = "\n".join(blog_lines[1:second_occur_hr]).strip()
        self.parse_header()
        self.markdown_body = "\n".join(blog_lines[second_occur_hr + 1:])
        self.html_body = marko.convert(self.markdown_body)

    def parse_header(self):
        arr = list((item.split(": ") for item in self.header_text.split("\n")))
        for index in range(len(arr)):

            if arr[index][0] == "categories:":
                arr[index][0] = "categories"
                arr[index].append("[]")
        res = dict(arr)

        #pprint(res)
        #pprint(res['categories'])
        self.categories = literal_eval(res['categories'])
        self.title = res['title']
        self.date = datetime.strptime(res['date'], '%Y-%m-%d %H:%M')

    def __str__(self):
        msg = """
        title: %s,
        date: %s,
        categories: %s,
        markdown_body: %s,
        html_body: %s
        """ % (self.title, self.date, str(
            self.categories), self.markdown_body[0:50], self.html_body[0:50])
        return msg


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    path = os.path.join(base_dir, "markdown",
                        "2020-11-07-us-political-idols.markdown")
    #2019-11-20-mid-life-crisis.markdown
    p = PeterMarkdownParser(file_path=path)
    print(p)
    print(p.text)
    #pprint(p.html_body)
    #pprint(p.markdown_body)