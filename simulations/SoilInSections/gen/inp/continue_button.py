### WARNING: This script will overwrite the first line of each input file in the input directory with "continue"

import pandas as pd

filenames = pd.read_csv('filenames.csv')
filenames = filenames['name'].tolist()


for filename in filenames:
    filename = '../../compute/input/' + filename + '.inp'
    # if the first line is not "continue", replace it with "continue"
    with open(filename, 'r') as file:
        lines = file.readlines()
    text = ''.join(lines)
    text = text.split('\n\n')[-1]
    text = ['continue\n'] + text.split('\n')
    with open(filename, 'w') as file:
        file.writelines(text)

