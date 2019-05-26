from descdbmd import writer
from descdbmd.writer import Writer


class Markdown(Writer):
    def __init__(self):
        pass

    def print_result(self, result):
        if type(result) == list:
            return self._print_list(result)
        return self._print_table(result)

    def _print_list(self, tables):

        mds = '\n\n\n'.join([self._print_table(t) for t in tables])

        anchors = '\n'.join([f'[{t.name}](#{t.name})' for t in tables])

        return anchors+'\n\n'+mds

    def _print_table(self, table):
        output = f'### {table.name}\nDatabase: {table.database}\nType: {table.extendedtype()}\n\n'
        output += f'{table.description}\n\n'

        columns_head = '| name | type |'
        columns_sep = '|-------------|-------------|'
        if table.show_pkey:
            columns_head += ' pkey |'
            columns_sep += '-------------|'
        if table.show_partition:
            columns_head += ' partition |'
            columns_sep += '-------------|'
        if table.show_nullable:
            columns_head += ' nullable |'
            columns_sep += '-------------|'
        columns_head += ' comment |'
        columns_sep += '----------------------------------------------------------------------|'
        output += columns_head
        output += '\n'
        output += columns_sep
        output += '\n'

        for col in table.columns:
            output += self._print_column(table, col)
            output += '\n'

        return output

    def _print_column(self, table, column):
        output = f'| {column.name} | {column.type} |'
        if table.show_pkey:
            output += f' {"Yes" if column.pkey else "No"} |'
        if table.show_partition:
            output += f' {"Yes" if column.partition else "No"} |'
        if table.show_nullable:
            output += f' {"Yes" if column.nullable else "No"} |'

        output += f' {column.comment} |'

        return output


writer.writers['md'] = Markdown