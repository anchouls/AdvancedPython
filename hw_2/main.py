from advpy_ast_tree import main as ast
import sys


def init_document():
    return r'\documentclass{article}'


def document(data):
    return _gen((r'\begin{document}',
                 _gen(data),
                 r'\end{document}'))


def _gen(lines):
    return '\n'.join(lines)


def generate_table(table_data):
    m = len(table_data[0])
    new_table = filter(lambda x: len(x) == m, table_data)
    return _gen(
        (r'\begin{tabular}{' + '| l ' * m + '| }',
         r'\hline',
         *(' & '.join(list(map(str, i))) + r' \\ \hline' for i in new_table),
         r'\end{tabular}'))


def generate_image_headers():
    return r'\usepackage{graphicx}'


def generate_image(img):
    return _gen((r'\begin{figure}[h]',
                 r'\includegraphics[width=0.8\linewidth]{' + img + '}',
                 r'\end{figure}'))


def main(file_path):
    ast.main()
    content = _gen((init_document(),
                    generate_image_headers(),
                    document((
                        generate_table([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                        generate_image('AST.png')
                    ))))
    with open(file_path, 'w') as fp:
        fp.write(content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        main('artifacts/table.tex')
    else:
        main(sys.argv[1])
