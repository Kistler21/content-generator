import tkinter as tk
import tkinter.font
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
        headers = ['input_keywords', 'output_content']
        csv_writer = csv.DictWriter(csv_file, fieldnames=headers)

        # Write contents to file
        output = {
            headers[0]: f'{primary};{secondary}',
            headers[1]: paragraph
        }
        csv_writer.writeheader()
        csv_writer.writerow(output)


def main():
    '''Contains all the functionality of the GUI.'''
    # Open the main menu for the GUI
    window = tk.Tk()
    window.title('Content Generator')

    # Create the label and entry for primary keyword
    primary_lbl = tk.Label(window, text='Primary Keyword:')
    primary_ent = tk.Entry(window)

    # Place the primary keyword label and entry
    primary_lbl.grid(
        row=0,
        column=0,
        sticky='e',
        pady=10,
        padx=(5, 0)
    )
    primary_ent.grid(
        row=0,
        column=1,
        padx=(0, 5),
        sticky='ew'
    )

    # Create the label and entry for secondary keyword
    secondary_lbl = tk.Label(window, text='Secondary Keyword:')
    secondary_ent = tk.Entry(window)

    # Place the secondary keyword label and entry
    secondary_lbl.grid(
        row=1,
        column=0,
        sticky='e',
        padx=(5, 0)
    )
    secondary_ent.grid(
        row=1,
        column=1,
        sticky='ew',
        padx=(0, 5)
    )

    # Create and pace the button for generating the output
    generate_btn = tk.Button(window, text='Generate', bg='lightgray')
    generate_btn.grid(
        row=2,
        column=0,
        pady=20,
        ipady=10,
        ipadx=10,
        columnspan=2
    )

    # Create the label and text for output
    output_lbl = tk.Label(window, text='Generated Output:')
    output_txt = tk.Text(window, height=10, width=40, wrap=tk.WORD)

    # Place the output label and text
    output_lbl.grid(
        row=3,
        column=0,
        sticky='ne',
        padx=(5, 0),
    )
    output_txt.grid(
        row=3,
        column=1,
        sticky='ew',
        padx=(0, 5),
        pady=(0, 10)
    )

    # Run the loop to look for events
    window.mainloop()


if __name__ == '__main__':
    primary = 'coat'
    secondary = 'capes'
    if len(sys.argv) == 2:
        primary, secondary = read_csv(sys.argv[1])
    wiki_contents = get_wiki_page(primary)
    paragraph = find_keywords(wiki_contents, primary, secondary)
    csv_output(primary, secondary, paragraph)
    main()
