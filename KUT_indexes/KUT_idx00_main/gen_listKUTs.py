# -*- coding: utf-8 -*-

import os

directory = "../../KUT_items"
items = os.listdir(directory)


data = []

for item in items:
    item_texfile = directory + '/' + item + '/TeX/' + item + '.tex'

    with open(item_texfile, 'r', encoding='utf-8') as file:
        content = file.read()
        start_marker = '\\begin{flushleft}'
        end_marker = '\\end{flushleft}'
        start_index = content.find(start_marker)
        end_index = content.find(end_marker)
        if start_index != -1 and end_index != -1:
            extracted_string = content[start_index + len(start_marker):end_index].strip()
            data.append([item, extracted_string])
        else:
            data.append([item, " "])



output_file = 'idx00_maintable.tex'

with open(output_file, 'w', encoding='utf-8') as file:
    for item, extracted_string in data:

        extracted_string = extracted_string.replace('\\', '')

        print(item, extracted_string)

        file.write(f"\\href{{run:../../KUT_items/{item}/TeX/{item}.pdf}}{{{item}}} & {extracted_string} \\\\ \\addlinespace[3pt]  \n")



