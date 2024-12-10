# format files

def format_files_to_list(filename: str):

    formatted_ls = []
    line_num = 1

    try:
        read_file = open(filename, "r")
        lines = read_file.readlines()
        while line_num < len(lines):
            line = lines[line_num].strip()
            formatted_ls.append(line.split(','))
            line_num += 1
        read_file.close()
    except:
        print(f"Error: The {filename} is missing or incorrect.")
        quit()
    return formatted_ls

# group Type and Category

def group_cat(file_ls: list, column_no: int):

    group_ls = []
    line = 0
    while line < len(file_ls):
        group_name = file_ls[line][column_no]
        if group_name not in group_ls:
            group_ls.append(group_name)
        line += 1
    return group_ls