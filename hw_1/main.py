import ast
import graphviz


class Style:
    def __init__(self, label, shape=None, color=None):
        self.label = label if not isinstance(label, str) else lambda x: label
        self.shape = shape
        self.color = color


styles = {
    'Module':       Style('Module', 'house', '#ff948d'),
    'FunctionDef':  Style('Function', 'diamond', '#ffbaba'),
    'arg':          Style(lambda node: f'{str(ast.unparse(node))}', 'box', '#71f596'),
    'arguments':    Style('arguments', 'box', '#5ff7ae'),
    'Name':         Style(lambda node: f'var: {str(ast.unparse(node))}', 'box', '#c9ffba'),
    'Constant':     Style(lambda node: f'const: {str(ast.unparse(node))}', 'box', '#fffcb3'),
    'List':         Style(lambda node: f'List: {str(ast.unparse(node))}', 'tab', '#f5d070'),
    'Subscript':    Style('Subscript', 'invhouse', '#f5d070'),
    'If':           Style('If', 'pentagon', '#bae5ff'),
    'For':          Style('For', 'pentagon', '#bae5ff'),
    'Add':          Style('Add', 'circle', '#c4baff'),
    'USub':         Style('USub', 'circle', '#c4baff'),
    'Sub':          Style('Sub', 'circle', '#c4baff'),
    'BinOp':        Style('BinOp', 'ellipse', '#a4aaff'),
    'UnaryOp':      Style('UnaryOp', 'ellipse', '#a4aaff'),
    'Compare':      Style('Compare', 'ellipse', '#a4aaff'),
    'Eq':           Style('Eq', 'circle', '#c4baff'),
    'Return':       Style('Return', 'rarrow', '#ff6262'),
    'Assign':       Style('Assign', 'Mcircle', '#ffade9'),
    'Call':         Style('Call', 'Mdiamond', '#629ae0'),
    'Expr':         Style('Body', 'hexagon', '#94d6fe'),
    'Attribute':    Style(lambda node: f'Attribute: {str(ast.unparse(node)).split(".")[1]}', 'oval', '#cb94ff'),
    '_default':     Style(lambda node: type(node).__name__)
}


class Walker(ast.NodeVisitor):
    def __init__(self):
        self.stack = []
        self.graph = graphviz.Graph(format='png')
        self.counter = 0

    def generic_visit(self, node):
        node_name = type(node).__name__
        style = styles.get(node_name, styles['_default'])

        parent = None
        if self.stack:
            parent = self.stack[-1]

        if node_name != 'Load' and node_name != 'Store':
            num = 'n' + str(self.counter)
            self.stack.append(num)
            self.graph.node(num, label=style.label(node), shape=style.shape, fillcolor=style.color, style='filled')
            if parent:
                self.graph.edge(parent, num)
            self.counter += 1

        super(self.__class__, self).generic_visit(node)

        if node_name != 'Load' and node_name != 'Store':
            self.stack.pop()


def main():
    filename = 'fibonacci.py'
    with open(filename, 'r') as fin:
        src = fin.read()
    root = ast.parse(src)
    mw = Walker()
    mw.visit(root)
    mw.graph.render("AST")


if __name__ == "__main__":
    main()
