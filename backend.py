import csv
import sys

from urllib.request import urlopen, HTTPError
from html.parser import HTMLParser


class ParagraphParser(HTMLParser):
    """
    Custom HTMLParser class used for parsing data
    inside of <p> tags from Wikipedia pages.
    """

    def __init__(self):
        super().__init__()
        self.in_paragraph = False
        self.paragraphs = ['']
        self.index = 0

    def handle_starttag(self, tag, attrs):
        """Set in_paragraph when a <p> tag is found."""
        if tag == 'p':
            self.in_paragraph = True

    def handle_data(self, data):
        """Read all data found inside <p> tags."""
        if self.in_paragraph:
            self.paragraphs[self.index] += data

    def handle_endtag(self, tag):
        """Handle when a closing </p> tag is found."""
        if tag == 'p':
            self.in_paragraph = False
            self.index += 1
            self.paragraphs.append('')


def get_wiki_page(keyword):
    """
    Downloads the contents of the specified keywords Wikipedia page.
    Return false if the page doesn't exist.
    """
    # Replace space with underscore for Wiki page
    keyword = keyword.replace(' ', '_')

    # Open the Wiki page of the keyword
    try:
        url = f'https://en.wikipedia.org/wiki/{keyword}'
        wiki = urlopen(url)
        wiki_contents = wiki.read().decode('utf-8')
        return wiki_contents
    except HTTPError:
        return False


def find_keywords(wiki_contents, primary, secondary):
    """
    Finds the pargraph containing the primary and secondary keywords.
    Returns False if no pargraph is found containing both keywords.
    """
    # Parse the content for all data inside <p> elements
    parser = ParagraphParser()
    parser.feed(wiki_contents)

    # Find paragraph that contains both keywords
    for paragraph in parser.paragraphs:
        if (
            primary.lower() in paragraph.lower()
            and secondary.lower() in paragraph.lower()
        ):
            return paragraph.strip()

    # No paragraph found with both words
    return False


def read_csv(file_name, key):
    """Reads keywords from a CSV file."""
    # Open the file
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Read the contents
        for keywords in csv_reader:
            if key == 'input_keywords':
                return keywords[key].split(';')
            else:
                return keywords[key]


def csv_output(filename, primary, secondary, paragraph):
    """Writes the output to the given CSV filename."""
    # Open the file
    with open(filename, 'w', newline='') as csv_file:
        headers = ['input_keywords', 'output_content']
        csv_writer = csv.DictWriter(csv_file, fieldnames=headers)

        # Write contents to file
        output = {
            headers[0]: f'{primary};{secondary}',
            headers[1]: paragraph
        }
        csv_writer.writeheader()
        csv_writer.writerow(output)


def get_input():
    """
    Returns the primary keyword, secondary keyword
    based on the arguments passed from the command line.
    """
    # Input file and output file passed
    if len(sys.argv) == 3:
        primary, secondary = read_csv(sys.argv[1], 'input_keywords')
    # Primary keyword, seconary keyword, and output file passed
    elif len(sys.argv) == 4:
        primary = sys.argv[1]
        secondary = sys.argv[2]

    return primary, secondary


def is_valid_keyword(keyword):
    """Validates that a keyword contains only letters, numbers, and spaces."""
    return all(char.isalnum() or char.isspace() for char in keyword)


def generate_output(primary, secondary):
    """
    Validates the primary and secondary keywords and
    parses Wikipedia if they are valid.
    """
    # Validate keywords
    if (not is_valid_keyword(primary) or not is_valid_keyword(secondary)):
        return 'Primary and secondary keywords can only contain letters, numbers, spaces, and cannot be empty.'

    # Download and validate the webpage
    wiki_contents = get_wiki_page(primary)
    if not wiki_contents:
        return 'No Wikipedia page for specified primary keyword.'

    # Parse content
    output = find_keywords(wiki_contents, primary, secondary)
    if not output:
        return f'No paragraph was found containing {primary} and {secondary}.'

    return output


def generate_content():
    """
    Main function that is called when script is called.
    Parses command line arguments for input and output.
    """
    primary, secondary = get_input()
    output_file = sys.argv[-1]
    output = generate_output(primary, secondary)
    csv_output(output_file, primary, secondary, output)


if __name__ == '__main__':
    generate_content()
