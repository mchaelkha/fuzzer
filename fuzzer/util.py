line_sep = '====================\n{}'
line_double_sep = '====================\n{}\n===================='
space_sep = '    {}'

def read_file(filename, arr):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            arr.append(line)
