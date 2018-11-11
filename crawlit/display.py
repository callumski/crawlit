from jinja2 import Template, Environment, FileSystemLoader
import json_lines
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def load_json_file(file):
    with open(file, mode="r") as file:
        yield next(json_lines.reader(file))


def get_html(input_file):
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    return j2_env.get_template("template.html").render(items=load_json_file(input_file))


if __name__ == '__main__':
    input_file = "output/crawlit.10.11.18-21.10.1541884254.json"
    with open("output/crawlit.10.11.18-21.10.1541884254.html", mode="w") as file:
        file.write(get_html(input_file))
