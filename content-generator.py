import tkinter
import sys
import csv
from urllib.request import urlopen
from html.parser import HTMLParser


class ParagraphParser(HTMLParser):
    '''
    Custom HTMLParser class used for parsing data
    inside of <p> tags from Wikipedia pages.
    '''

    def __init__(self):
        super().__init__()
        self.in_paragraph = False
        self.paragraphs = ['']
        self.index = 0

    def handle_starttag(self, tag, attrs):
        '''Set in_paragraph when a <p> tag is found.'''
        if tag == 'p':
            self.in_paragraph = True

    def handle_data(self, data):
        '''Read all data found inside <p> tags.'''
        if self.in_paragraph:
            self.paragraphs[self.index] += data

    def handle_endtag(self, tag):
        '''Handle when a closing </p> tag is found.'''
        if tag == 'p':
            self.in_paragraph = False
            self.index += 1
            self.paragraphs.append('')


def get_wiki_page(keyword):
    '''Downloads the contents of the specified keywords Wikipedia page.'''
    # Open the Wiki page of the keyword
    url = f'https://en.wikipedia.org/wiki/{keyword}'
    wiki = urlopen(url)
    wiki_contents = wiki.read().decode('utf-8')
    return wiki_contents


def find_keywords(wiki_contents, primary, secondary):
    '''Finds the pargraph containing the primary and secondary keywords.'''
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
    return f'No paragraph found containing {primary} and {secondary}.'


def read_csv(file_name):
    '''Reads keywords from a CSV file.'''
    # Open the file
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Read the contents
        for keywords in csv_reader:
            return keywords['input_keywords'].split(';')


def csv_output(primary, secondary, paragraph):
    '''Writes the output to a CSV file named output.csv.'''
    # Open the file
    with open('output.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write contents to file
        headers = ['input_keywords', 'output_content']
        output = [f'{primary};{secondary}', paragraph]
        csv_writer.writerows([headers, output])


if __name__ == '__main__':
    primary = 'coat'
    secondary = 'capes'
    if len(sys.argv) == 2:
        primary, secondary = read_csv(sys.argv[1])
    wiki_contents = get_wiki_page(primary)
    paragraph = find_keywords(wiki_contents, primary, secondary)
    csv_output(primary, secondary, paragraph)
