# -*- coding: utf-8 -*-

import os

directory = "../../KUT_items"
items = [i for i in os.listdir(directory) if i != 'KUT000']




# -----------------------------------------------------------------------------




def tabgen():

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


    with open(output_file, 'w', encoding='utf-8') as file:
        for item, extracted_string in data:

            if item in selected_KUT_items:

                extracted_string = extracted_string.replace('\\', '')

                print(item, extracted_string)

                file.write(f"\\href{{run:../../KUT_items/{item}/TeX/{item}.pdf}}{{{item}}} & \\href{{run:../../KUT_items/{item}/TeX/{item}.pdf}}{{{extracted_string}}} \\\\ \\addlinespace[3pt]  \n")







# -----------------------------------------------------------------------------
# Opis a vlastnosti
output_file = 'tab01_rows_LMOT.tex'

selected_KUT_items = [
    'KUT014', 
    'KUT018',
]

tabgen()


# -----------------------------------------------------------------------------
# Softvér
output_file = 'tab02_rows_LMOT.tex'

selected_KUT_items = [
    'KUT016', 
]

tabgen()

# -----------------------------------------------------------------------------
# Rôzne
output_file = 'tab03_rows_LMOT.tex'

selected_KUT_items = [
    'KUT013', 
]

tabgen()

# -----------------------------------------------------------------------------








