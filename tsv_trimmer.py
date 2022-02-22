import re


def trimmer(filename):
    """초기화"""
    edited_lines = []

    """tsv 파일 읽어오기"""
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            """수정하기"""
            hyperlink = re.compile(r'([a-zA-Z0-9]+.) ([a-zA-Z0-9]+.) ([a-zA-Z0-9]+.) ([a-zA-Z0-9]+)')
            link_ex = hyperlink.search(line)
            if link_ex:
                line = re.sub(hyperlink, f"{link_ex.group(1)}{link_ex.group(2)}{link_ex.group(3)}{link_ex.group(4)}",
                              line)

            edited_lines.append(line)

    """수정된 내용을 쓰기"""
    with open(filename, 'w') as f:
        f.writelines(edited_lines)
