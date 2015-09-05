import io
import re


re_indent = re.compile(r'^\ +')


def get_indent(docstr):
    for lstr in map(str.rstrip, docstr.splitlines()):
        indent_match = re_indent.search(lstr)
        if indent_match is not None:
            return indent_match.group()
    return ''


class DocFile(io.StringIO):

    def __init__(self, existing):
        super().__init__()
        super().write(existing)
        self.indent = get_indent(existing)

    def writeline(self, line):
        super().write(self.indent)
        super().write(line)
        super().write('\n')
