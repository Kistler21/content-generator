import sys
import csv
import subprocess
import tkinter as tk
from backend import read_csv


def generate(primary, secondary, output_txt):
    """Function that is called when the generate button is pressed."""
    # Enable the textbox and delete the old contents
    output_txt['state'] = 'normal'
    output_txt.delete('1.0', tk.END)

    # Call the backend process to get results
    output_file = 'output.csv'
    child = subprocess.Popen(
        ['python', 'backend.py', primary, secondary, output_file])
    child.wait()

    # Write output to output text box
    output = read_csv(output_file, 'output_content')
    error_messages = [
        'Primary and secondary keywords can only contain letters, numbers, spaces, and cannot be empty.',
        'No Wikipedia page for specified primary keyword.',
        f'No paragraph was found containing {primary} and {secondary}.',
    ]
    # Set text color
    if output in error_messages:
        output_txt['fg'] = 'red'
    else:
        output_txt['fg'] = 'black'
    output_txt.insert('1.0', output)
    output_txt['state'] = 'disabled'


def get_census_data(year, state, output_txt):
    """
    Communicates with a population generator project to get the
    census data for the specified state and year
    """
    # Enable the textbox and delete the old contents
    output_txt['state'] = 'normal'
    output_txt.delete('1.0', tk.END)

    # Call the backend of the population generator
    output_file = '../populationgenerator/output_content'
    child = subprocess.Popen(
        ['python', '../populationgenerator/backend.py', year, state, output_file])
    child.wait()

    # Write output to output text box
    output = read_csv(output_file, 'output_population_size')
    output_txt['fg'] = 'black'
    output_txt.insert('1.0', output)
    output_txt['state'] = 'disabled'


def create_main_window(title):
    """
    Creates the main window for the GUI.
    All other widgets will be a child of the window.
    """
    # Open the main menu for the GUI
    window = tk.Tk()
    window.title(title)

    # Configure rows and columns of window
    window.rowconfigure(4, weight=1)
    window.columnconfigure(1, weight=1)

    return window


def creat_widgets(window):
    """Creates all widgets needed for the GUI."""
    widgets = dict()
    widgets['labels'] = create_labels(window)
    widgets['entries'] = create_entries(window)
    widgets['texts'] = create_texts(window)
    widgets['buttons'] = create_buttons(window, widgets)
    return widgets


def create_labels(window):
    """Creates all labels needed for the GUI."""
    labels = dict()
    labels['primary'] = create_label(
        window,
        'Primary Keyword (or State):',
        {
            'row': 0,
            'column': 0,
            'sticky': 'e',
            'pady': 10,
            'padx': (5, 0)
        }
    )
    labels['secondary'] = create_label(
        window,
        'Secondary Keyword (or Year):',
        {
            'row': 1,
            'column': 0,
            'sticky': 'e',
            'padx': (5, 0)
        }
    )
    labels['output'] = create_label(
        window,
        'Generated Output:',
        {
            'row': 4,
            'column': 0,
            'sticky': 'ne',
            'padx': (5, 0),
        }
    )
    return labels


def create_entries(window):
    """Creates all entries needed for the GUI."""
    entries = dict()
    entries['primary'] = create_entry(
        window,
        {
            'row': 0,
            'column': 1,
            'padx': (0, 5),
            'sticky': 'ew'
        }
    )
    entries['secondary'] = create_entry(
        window,
        {
            'row': 1,
            'column': 1,
            'padx': (0, 5),
            'sticky': 'ew'
        }
    )
    return entries


def create_texts(window):
    """Creates all text boxes needed for the GUI."""
    texts = dict()
    texts['output'] = tk.Text(
        window,
        height=15,
        width=50,
        wrap=tk.WORD,
        state='disabled'
    )
    texts['output'].grid(
        row=4,
        column=1,
        sticky='nsew',
        padx=(0, 5),
        pady=(0, 10)
    )
    return texts


def create_buttons(window, widgets):
    """Creates all buttons needed for the GUI."""
    buttons = dict()
    buttons['generate'] = tk.Button(
        window,
        text='Generate',
        bg='lightgray',
        command=lambda: generate(
            widgets['entries']['primary'].get(), widgets['entries']['secondary'].get(), widgets['texts']['output'])
    )
    buttons['generate'].grid(
        row=2,
        column=0,
        pady=20,
        ipady=10,
        ipadx=10,
        columnspan=2
    )
    buttons['population'] = tk.Button(
        window,
        text='Get Population',
        bg='lightgray',
        command=lambda: get_census_data(
            widgets['entries']['secondary'].get(), widgets['entries']['primary'].get(), widgets['texts']['output'])
    )
    buttons['population'].grid(
        row=3,
        column=0,
        pady=(0, 20),
        ipady=10,
        ipadx=10,
        columnspan=2
    )
    return buttons


def create_label(parent, text, grid_args):
    """
    Creates a label with the specified parent and text.
    Label is placed using grid by unpacking grid_args.
    """
    lbl = tk.Label(parent, text=text)
    lbl.grid(**grid_args)
    return lbl


def create_entry(parent, grid_args):
    """
    Creates a label with the specified parent.
    Label is placed using grid by unpacking grid_args.
    """
    ent = tk.Entry(parent)
    ent.grid(**grid_args)
    return ent


def main():
    """Contains all the functionality of the GUI."""
    window = create_main_window('Content Generator')
    widgets = creat_widgets(window)

    # Check if csv is passed on command line
    if len(sys.argv) == 2:
        primary, secondary = read_csv(sys.argv[1], 'input_keywords')
        widgets['entries']['primary'].insert(0, primary)
        widgets['entries']['secondary'].insert(0, secondary)
        generate(primary, secondary, widgets['texts']['output'])

    window.mainloop()


if __name__ == '__main__':
    main()
