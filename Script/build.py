import os

libs = ["requests",
        "pytube",
        "bs4",
        "ctype",
        "html",
        "pornhub_api",
        "pydantic",
        "selenium",
        "soupsieve",
        "xml",
        "youtube_dl",
        "_markupbase",
        "colorsys",
        "fileinput",
        "typing_extensions",
        "uuid"]

append_string = ''
for module in libs:
    append_string += f' --exclude-module={module}'

os.system(f'pyinstaller uwvp.py --onefile --console --noconfirm --paths "C://Ultimate-Web-Video-Parser//Script//SupportedSites"{append_string}'.replace('/', os.sep))