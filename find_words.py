from email.policy import strict
import string
from time import sleep
import PyPDF2
import textract
import sys
import glob
import os
from rich import print, pretty
from rich.tree import Tree
from rich.progress import track
from rich.console import Console
from rich.table import Table
import re
import csv
import calendar
import time

pretty.install()

if len(sys.argv) != 3:
    sys.exit('Usage: python find_words.py path words=word1,word2,"word with space"')
if os.path.exists(sys.argv[1]) == False:
    sys.exit("Invalid path")
first_array = sys.argv[2].split('=')
if len(first_array) != 2:
    sys.exit('Invalid words. Usage words=word1,word2,"word with space"')
words = first_array[1].split(',')
tree = Tree("Searching by :")
for word_tree in words:
    tree.add(f'"{word_tree}"')
print (tree)
path = os.path.abspath(sys.argv[1])
pdf_files = glob.glob(f'{path}/**/*.pdf', recursive=True)

table = Table(title="Found")

header = ['File', 'Word', 'Page']
data = []
table.add_column("File", style="cyan", no_wrap=True)
table.add_column("Word", style="magenta")
table.add_column("Page", justify="right", style="green")

def find_in_file(file):
    try:
        pdf_file = open(file,'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file, strict=False)
        num_pages = pdf_reader.numPages
        count = 0
        text = ""
        while count < num_pages:
            page = pdf_reader.getPage(count)
            page_number = count + 1
            text = page.extractText()
            if text == "":
                print(f'page {page_number} from {file} without text. OCR...')
                pdf_writer = PyPDF2.PdfFileWriter()
                pdf_writer.addPage(page)
                new_file = f'{file}_{page_number}.pdf'
                pdf_out = open(new_file, 'wb')
                pdf_writer.write(pdf_out)
                pdf_out.close()
                text = textract.process(new_file, method='tesseract', language='por')
                text = text.decode("utf-8")
                os.remove(new_file)
            for word in words:
                if re.search(word.lower(), text.lower()):
                    data.append([file, word, page_number])
                    table.add_row(file, word, f'{page_number}')
            count +=1
    except:
        data.append([file, "file cannot be opened", "0"])
        table.add_row(file, "file cannot be opened", "0")
    
i = 0
for _ in track(range(len(pdf_files)), description=f'[green]Finding in {len(pdf_files) - i} files'):
    find_in_file(pdf_files[i])
    i = i + 1

console = Console()
console.print(table)
gmt = time.gmtime()
timestamp = calendar.timegm(gmt)
with open(f'{timestamp}.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)