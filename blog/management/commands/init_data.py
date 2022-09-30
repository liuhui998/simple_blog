"""
Django command to wait for the database to be available
"""

from ast import parse
import time
import traceback
from sqlite3 import OperationalError  # noqa
from sys import stdout
from blog.data.markdown_parser import PeterMarkdownParser  # noqa
from psycopg2 import OperationalError as Psycopg2OpError  # noqa
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import os
from blog.models import *
from projects.models import *


class Command(BaseCommand):
    """Django command to wait for database."""

    def clean_all_data(self):
        self.stdout.write("start clean all old data...")
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Category.objects.all().delete()
        Project.objects.all().delete()

    def init_projects_data(self):
        p1 = Project(
            title='Git Community Book 中文版',
            description=
            '一本介绍 Git 技术使用及原理的图书. https://github.com/liuhui998/gitbook',
            technology='Git',
            image='img/project1.png')
        p1.save()

        p2 = Project(
            title='Spserver',
            description=
            '一个开源 C++ 高并发网络框架（我只贡献了2个性能 patch. https://github.com/liuhui998/spserver',
            technology='C++',
            image='img/project1.png')
        p2.save()

        p3 = Project(
            title='Python Basic',
            description=
            '一本基础 Python 习题集. https://github.com/liuhui998/python-basic',
            technology='Python Notebook',
            image='img/project1.png')
        p3.save()

    def handle(self, *args, **options):
        self.stdout.write('start init data...')
        # loop all markdown files
        print(settings.BASE_DIR)
        markdown_dir = os.path.join(settings.BASE_DIR, "blog/data/markdown")
        ext = ('.md', '.markdown')

        # iterating over all files
        markdown_files = []
        for file_name in os.listdir(markdown_dir):
            print(file_name)
            if file_name.endswith(ext):
                markdown_files.append(os.path.join(markdown_dir, file_name))

        self.clean_all_data()
        # insert into database
        self.init_projects_data()

        for markdown_file in markdown_files:
            print(">" * 80)
            print(markdown_file)

            parser = PeterMarkdownParser(file_path=markdown_file)
            print(parser.date)
            if parser.date == None:
                print(parser.header_text)
                break

            #print(parser)
            post = Post(title=parser.title,
                        body=parser.html_body,
                        created_on=parser.date)
            #print(post.created_on)
            post.save()

            for category_name in parser.categories:
                category = Category.objects.filter(name="test").first()
                if not category:
                    category = Category(name=category_name)
                    category.save()
                post.categories.add(category)

            Post.objects.filter(id=post.id).update(created_on=parser.date)
