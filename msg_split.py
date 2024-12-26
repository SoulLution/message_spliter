import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './')))

from typing import Generator
from bs4 import BeautifulSoup
import sys
import click
from utils.is_too_long_string import is_too_long_string
from utils.reduce_elements import reduce_start_elements, reduce_last_elements, WHITE_LIST

import argparse

MAX_LEN = 4096

def split_message(source: str, max_len=MAX_LEN) -> Generator[str, None, None]:
    """Splits the original message (`source`) into fragments of the specified length (`max_len`)."""

    soup = BeautifulSoup(source, 'html.parser')
    
    # Check for too long not splited tags
    tags_not_in_whitelist = soup.find_all(lambda tag: tag.name not in WHITE_LIST)
    for element in tags_not_in_whitelist:
        element_len = reduce_start_elements(element.parents) + str(element) + reduce_last_elements(element.parents)
        if(len(element_len) >= max_len):
            click.secho(f"Error:  Tag '{element_len}' is too large for this max length.\n        Max length needed more '{len(str(element_len))}'.", bg='red', fg='white')
            sys.exit(1)
    
    # Check for too long strings
    strings = soup.find_all(string=lambda text: is_too_long_string(
        reduce_start_elements(text.parents) + str(text) + reduce_last_elements(text.parents),
        max_len
    ))
    if(len(strings) > 0):
        max_long_string = max(strings, key=len)
        max_long_string = reduce_start_elements(max_long_string.parents) + str(max_long_string) + reduce_last_elements(max_long_string.parents)
        click.secho(f"Error:  Text '{max_long_string}' is too large for this max length.\n        Max length needed more '{len(str(max_long_string))}'.", bg='red', fg='white')
        sys.exit(1)

    # Run main functionality 
    while len(soup.contents) > 0:
        result = reduce_start_elements([soup])
        result = soap_loop(result, soup, max_len)
        result += reduce_last_elements([soup])
        yield result

def soap_loop(source: str, parent, max_len):
    while len(parent.contents) > 0:
        element = parent.contents[0]
        if (len(source + str(element) + reduce_last_elements(element.parents)) < max_len):
            source += str(element)
            element.extract()
        elif len(source + reduce_start_elements([element]) + reduce_last_elements([element, *element.parents])) < max_len:
            source += reduce_start_elements([element])
            if(element.text.strip() != '' and element.name in WHITE_LIST):
                source = soap_loop(source, element, max_len)
            return source + reduce_last_elements([element])
        else:
            return source
    return source


def main():
    parser = argparse.ArgumentParser(description="Split a HTML file's content into smaller parts.")
    parser.add_argument("--max-len", type=int, default=MAX_LEN, help="Maximum length of each split message.")
    parser.add_argument("file", type=str, help="Path to the HTML file to split.")
    
    args = parser.parse_args()
    for i in range(3):
        print('-')
    try:
        with open(args.file, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        return
    try:
        for i, chunk in enumerate(split_message(content, args.max_len)):
            click.secho(f"fragment #{i + 1}: {len(chunk)} chars", bg='blue', fg='white')
            click.echo(chunk)
            click.echo()
        click.secho("Scrip was ended with success", bg='green', fg='white')
    except FileNotFoundError:
        return

if __name__ == "__main__":
    main()