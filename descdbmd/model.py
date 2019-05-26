import json


class Table:
    def __init__(self, name, database, type):
        self.name = name
        self.database = database
        self.category = ''
        self.type = type
        self.columns = []
        self.description = ''

        self.show_partition = False
        self.show_pkey = True
        self.show_nullable = True

    def __str__(self):
        d = self.__dict__
        d['columns'] = [c.__dict__ for c in self.columns]
        return json.dumps(d)

    def extendedtype(self):
        return ''


class Column:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.nullable = False
        self.partition = False
        self.pkey = False
        self.comment = ''

    def __str__(self):
        return json.dumps(self.__dict__)
