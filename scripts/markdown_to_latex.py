import subprocess
import re
import os

# In this variable is markdown from all jupyternotebook cell
global_markdown = {}

def run_latexx(command, pdftex):

    pdftex="latex/"
    command=["bash", "-c"]

    command.append("pdflatex -shell-escape -interaction=nonstopmode main.tex")
    command[2]=command[2]+" && biber main && "
    command[2]=command[2]+" pdflatex -shell-escape -interaction=nonstopmode main.tex"

    subprocess.call(command, cwd=pdftex, stdout=open(os.devnull, 'wb'))
    subprocess.call(command, cwd=pdftex)

    #set your path to latex folder\n",

    subprocess.call(command, cwd=pdftex, stdout=open(os.devnull, 'wb'))

def run_latex():
    subprocess.call(['python', 'scripts/run.py'])

def save_markdown_files(text: str, dir):
    for key, markdown in text.items():
        file_name = key + '.md'
        file = open(dir + file_name, 'w')

        file.write(markdown)
        file.close()


def add_extra_backslash_to_escapes_codes(t):
    ''' Automatically add extra \\ before python escape characters before
    saving to markdown'''

    t = t.replace('\r', '\\r')
    t = t.replace('\b', '\\b')
    t = t.replace('\t', '\\t')
    t = t.replace('\t', '\\t')
    # t=t.replace('\n', '\\\\n')
    t = t.replace('\a', '\\a')
    t = t.replace('\f', '\\f')
    return t


def count_words(words):
    count = 0
    words = add_extra_backslash_to_escapes_codes(words)

    # words=words
    for word in words.split():
        if not re.match("\\\\", word):
            count += 1
    return count


def count_markdown_words(text: str) -> dict:
    # Split the text into lines
    lines = text.split("\n")

    # Initialize variables to keep track of the number of words in headlines
    # and subheadlines

    headline_words = 0
    subheadline_words = 0

    # Initialize a variable to keep track of the total number of words in tables
    table_words = 0

    # Initialize a variable to keep track of the total number of words in the
    # text

    total_words = 0
    figures_words = 0
    dontskiplines = True

    # Loop through each line in the text
    for line in lines:
        # Check if the line is a headline
        # regex=re.findall(r"[^\\]\w+", line)
        # regex=count_words(line)

        if line.startswith("\begin{equation}"):
            dontskiplines = False

        if line.startswith("\\end{equation}"):
            dontskiplines = True

        if dontskiplines:
            if line.startswith("# "):
                # Split the line into words and add the number of words to the
                # headline_words variable
                headline_words += count_words(line)
            # Check if the line is a subheadline
            elif line.startswith("## "):
                # Split the line into words and add the number of words to the
                # subheadline_words variable
                subheadline_words += count_words(line)
            # Check if the line is part of a table
            elif line.startswith("|"):
                # Split the line into words and add the number of words to the
                # table_words variable
                table_words += count_words(line)
            elif line.startswith("!["):
                # Split the line into words and add the number of words to the
                # figures_caption var
                figures_words += count_words(line)
            # If the line is not a headline, subheadline, or part of a table,
            # add the number of words to the total_words variabl

            else:
                total_words += count_words(line)  # len(re.findall(r"\w+", line))

    # Return the total number of words in headlines, subheadlines, and tables,
    # as well as the total number of words

    return {
        # total words are without tables, headlines, ans subheadlines
        "pure_total_words": total_words,
        "headline_words": headline_words ,
        "subheadline_words": subheadline_words ,
        "table_words": table_words,
        "figures_words": figures_words
    }


def count_markdown_words_dict(markdown: dict) -> dict:

    word_counts = {
        'pure_total_words': 0,
        'headline_words': 0,
        'subheadline_words': 0,
        'table_words': 0,
        'figures_words': 0
    }

    for key, value in markdown.items():
        counts = count_markdown_words(value)
        for key, value in counts.items():
            word_counts[key] += value

    return word_counts


def split_markdown_into_dict(text: str) -> dict:
    ''' You give markdown as a str and it returns markdown in dict'''

    # split the text into lines
    lines = text.split("\n")

    # initialize a dictionary to store the paragraphs and sub-paragraphs
    result = {}

    # initialize the current key and value
    current_key = None
    current_value = []

    # loop over the lines
    for line in lines:
        # if the line starts with "#", it indicates the start of a new paragraph
        # or sub-paragraph. update the current key and value accordingly.
        if line.startswith("#"):
            if current_key is not None:
                result[current_key] = "\n".join(current_value)
            current_key = line
            current_value = []

        # if the line does not start with "#", it is part of the current paragraph
        # or sub-paragraph. append it to the current value.
        else:
            current_value.append(line)

    # add the final paragraph or sub-paragraph to the result
    result[current_key] = "\n".join(current_value)

    return result


def split_markdown_into_dict_level_one(markdown: dict) -> dict:
    ''' Order dict that all the text from headline level 1
    will be in each key '''

    first_level = {}

    for key, value in markdown.items():
        if key.startswith("# "):
            first_level[key] = value
            current_key = key
        else:
            first_level[current_key] = first_level[current_key] + "\n" + key + "\n" + value

    return first_level


def add_wordcount_to_markdown(markdown: dict) -> str:
    ''' Takes markdown and insert word count for every paragraph and subparagraph '''

    # initialize the result string
    result = ""

    # loop over the keys and values in the dictionary
    for title, text in markdown.items():
        # count the number of words in the text
        words = count_markdown_words(text)['pure_total_words']

        time_to_read_str = str(words) + " words, around " + str(round(words / 130, 2)) + " minutes of reading "
        time_on_right = ""
        if words > 0:
            time_on_right = '''
\\begin{flushright}
        %s
\\end{flushright}
    ''' % time_to_read_str

        # add the title, word count, and estimated reading time to the result
        result += title + "\n"
        result += str(time_on_right)
        result += str(text) + "\n"

    return result

def dict_markdown_to_str(global_markdown: dict) -> str:
    markdown_string = ""
    for key, value in global_markdown.items():
        markdown_string += key + value
    return markdown_string

def print_stats(t):
    total = count_markdown_words(t)['pure_total_words']

    # print('Pure total words: ', total)
    # print('Total time to read [minutes] : ', round(total / 130, 2))
    # print("headline_words", count_markdown_words(t)['headline_words'])
    # print("subheadline_words", count_markdown_words(t)['subheadline_words'])
    # print("table_words", count_markdown_words(t)['table_words'])
    # print("figures_words", count_markdown_words(t)['figures_words'])

    print("Cell:", count_markdown_words(t))
    print("All Doc:", count_markdown_words(dict_markdown_to_str(global_markdown)))

# Main function:


def saveText(markdown: str, headline: str):
    # set directory to save md files
    dir = 'latex/md/'
    # create one if it's missing
    if not os.path.exists(dir):
        os.makedirs(dir)
    t = markdown

    markdown = add_extra_backslash_to_escapes_codes(markdown)

    # markdown_from_cell = { headline: markdown }


    markdown = split_markdown_into_dict(markdown)

    global global_markdown
    global_markdown = global_markdown | markdown

    ##check if markdown text is already in cell
    #if markdown not in global_markdown:
    #     global_markdown[headline]=markdown

    # markdown = split_markdown_into_dict(markdown)
    text = {headline: add_wordcount_to_markdown(markdown)}

    save_markdown_files(text, dir)
    file = open(dir + 'global_markdown.md', 'w')
    # Count total words by
    file.write(
        add_wordcount_to_markdown(
            split_markdown_into_dict_level_one(
                global_markdown
            )
        )
    )
    print_stats(t)

    # I would like to compile latex from here but somehow
    # pdf is not rendering correctly
    # run_latex()

