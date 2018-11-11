from jinja2 import Environment, FileSystemLoader
import json_lines
import webbrowser
import argparse
from pathlib import Path
from urllib.parse import urljoin

THIS_DIR = str(Path(__file__).resolve().parent)


def get_items_from_json_file(file):
    items = []
    with open(file, mode="r") as file:
        for item in json_lines.reader(file):
            items.append(item)

    # We need to put the full URL in to be able to display it nicely.
    for item in items:
        item["internal_links"] = [
            (internal_url, urljoin(item["url"], internal_url)) for internal_url
            in
            item["internal_links"]]

    return items


def get_html(input_file):
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)

    return j2_env.get_template("template.html").render(
        items=get_items_from_json_file(input_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="display.py: renders a JSON \
    lines file in Crawlit format to HTML. Optionally also opens it in your \
    default web browser.")
    parser.add_argument("file", help="JSON lines file of items to render")
    parser.add_argument("-ob", "--open-browser", action='store_true',
                        help="Open the rendered HTML file in your default \
                        browser")
    args = parser.parse_args()

    input_file = Path(args.file)
    if not input_file.exists():
        print("Input file: {} not found.".format(args.file))
        exit(1)
    else:
        input_file = input_file.resolve()

    output_file = Path("{}/{}.html".format(input_file.parent, input_file.stem))

    output_string = get_html(input_file)

    with open(output_file, mode="w") as file:
        file.write(output_string)

    if args.open_browser:
        webbrowser.open_new_tab("file://{}".format(str(output_file)))
