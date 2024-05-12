#!/usr/bin/env python3
import sys
import pathlib
import re
import hashlib

def convert_md_to_html(input_file, output_file):
    """
    Converts a Markdown file to HTML with support for headings, lists, paragraphs, and custom formatting.

    Args:
        input_file (str): Path to the input Markdown file.
        output_file (str): Path to the output HTML file.
    """
    input_path = pathlib.Path(input_file)
    if not input_path.is_file():
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.readlines()

    html_content = []
    in_unordered_list = False
    in_paragraph = False
    for line in markdown_content:
        match_heading = re.match(r'^(#+)\s(.*)', line)
        if match_heading:
            if in_paragraph:
                html_content.append('</p>\n')
                in_paragraph = False
            heading_level = len(match_heading.group(1))
            heading_content = match_heading.group(2).strip()
            html_content.append(f'<h{heading_level}>{heading_content}</h{heading_level}>\n')
            continue

        match_unordered_list_item = re.match(r'^-\s(.*)', line)
        if match_unordered_list_item:
            if in_paragraph:
                html_content.append('</p>\n')
                in_paragraph = False
            if not in_unordered_list:
                html_content.append('<ul>\n')
                in_unordered_list = True
            list_item_content = parse_custom_formatting(match_unordered_list_item.group(1).strip())
            html_content.append(f'<li>{list_item_content}</li>\n')
            continue

        if line.strip() == '':
            if in_paragraph:
                html_content.append('</p>\n')
                in_paragraph = False
            continue
        else:
            if not in_paragraph:
                html_content.append('<p>\n')
                in_paragraph = True
            line_content = parse_custom_formatting(line.strip())
            if line_content:
                html_content.append(f'{line_content}<br/>\n')

    if in_unordered_list:
        html_content.append('</ul>\n')
    elif in_paragraph:
        html_content.append('</p>\n')

    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.writelines(html_content)

def parse_custom_formatting(text):
    """
    Parses Markdown text for custom formatting patterns and applies transformations.

    Args:
        text (str): Text containing custom formatting syntax.

    Returns:
        str: Transformed text based on custom rules.
    """
    text = re.sub(r'\[\[(.*?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), text)
    text = re.sub(r'\(\((.*?)\)\)', lambda match: match.group(1).replace('c', '').replace('C', ''), text)
    return text

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_md_to_html(input_file, output_file)

    sys.exit(0)
