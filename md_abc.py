import re
import argparse

def sort_headers(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    header_regex = re.compile(r'^(#{1,6})\s*(.*)$')

    sorted_lines = []
    current_level = []
    current_header_level = None

    for line in lines:
        match = header_regex.match(line)
        if match:
            header_level = len(match.group(1))
            header_text = match.group(2)

            if current_header_level is None:
                current_header_level = header_level

            if header_level == current_header_level:
                current_level.append((header_level, header_text))
            else:
                sorted_lines.extend(f'{"#"*level} {text}\n' for level, text in sorted(current_level))
                current_level = [(header_level, header_text)]
                current_header_level = header_level
        else:
            sorted_lines.extend(f'{"#"*level} {text}\n' for level, text in sorted(current_level))
            current_level = []
            current_header_level = None
            sorted_lines.append(line)

    if current_level:
        sorted_lines.extend(f'{"#"*level} {text}\n' for level, text in sorted(current_level))

    with open(filename, 'w') as file:
        file.writelines(sorted_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sort Markdown headers.')
    parser.add_argument('filename', type=str, help='The path to the Markdown file to sort.')

    args = parser.parse_args()

    sort_headers(args.filename)
