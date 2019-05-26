import argparse

import boto3

from descdbmd import driver
from descdbmd.model import Table,Column


class GlueAthenaTable(Table):
    def __init__(self, descriptor):
        Table.__init__(self, descriptor['Name'], descriptor['DatabaseName'], 'Athena')
        self.descriptor = descriptor
        self.show_nullable = False
        self.show_partition = True
        self.show_pkey = False

        self.description = descriptor.get('Description', '')
        self.columns = \
            [GlueAthenaColumn(column_desc) for column_desc in descriptor['StorageDescriptor']['Columns']] + \
            [GlueAthenaColumn(column_desc) for column_desc in descriptor.get('PartitionKeys',[])]

        self.format = self._infer_format()

    def extendedtype(self):
        return f'Athena ({self.format})'

    def _infer_format(self):

        if 'SerdeInfo' in self.descriptor['StorageDescriptor']\
                and 'SerializationLibrary' in self.descriptor['StorageDescriptor']['SerdeInfo']\
                and self.descriptor['StorageDescriptor']['SerdeInfo']['SerializationLibrary'] == \
                'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe':
            return 'Parquet'

        if 'SerdeInfo' in self.descriptor['StorageDescriptor']\
                and 'SerializationLibrary' in self.descriptor['StorageDescriptor']['SerdeInfo']\
                and self.descriptor['StorageDescriptor']['SerdeInfo']['SerializationLibrary'] == \
                'org.openx.data.jsonserde.JsonSerDe':
            return 'JSON'

        if 'SerdeInfo' in self.descriptor['StorageDescriptor']\
                and 'SerializationLibrary' in self.descriptor['StorageDescriptor']['SerdeInfo']\
                and self.descriptor['StorageDescriptor']['SerdeInfo']['SerializationLibrary'] == \
                'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe':
            return 'CSV'

        return ''


class GlueAthenaColumn(Column):
    def __init__(self, descriptor):
        Column.__init__(self)
        self.name = descriptor['Name']
        self.type = descriptor['Type']
        self.comment = descriptor.get('Comment', '')


class GlueRedshiftTable(Table):
    def __init__(self, descriptor):
        name = descriptor['StorageDescriptor']['Location'].split('.')
        db = '.'.join(name[:-1])
        name = name[-1]
        Table.__init__(self, name, db, 'Redshift')
        self.descriptor = descriptor
        self.show_nullable = False
        self.show_partition = False
        self.show_pkey = False

        self.description = descriptor['Description']
        self.columns = \
            [GlueAthenaColumn(column_desc) for column_desc in descriptor['StorageDescriptor']['Columns']]

    def extendedtype(self):
        return f'Redshift'


class GlueRedshiftColumn(Column):
    def __init__(self, descriptor):
        Column.__init__(self)
        self.name = descriptor['Name']
        self.type = descriptor['Type']
        self.comment = descriptor.get('Comment', '')


class GlueDriver(driver.Driver):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Describe Glue Tables')
        parser.add_argument('driver', help='driver should be glue')
        parser.add_argument('writer', help='driver should be glue')
        parser.add_argument("-t", "--table_name", default=None, help="Describe a specific table")
        parser.add_argument("-d", "--database_names", default=None, help="when describing a specific table, the database it belongs to, when describing all tables, limiting to one or several database, comma separated")
        parser.add_argument("-c", "--category", default=None, help="when describing all tables, limiting to one category")
        cmd_args = parser.parse_args()
        self.table_name = cmd_args.table_name
        self.database_names = [db.strip() for db in cmd_args.database_names.split(',') if db.strip()]
        self.category = cmd_args.category

    def get_result(self):
        glue = boto3.client('glue')
        if self.table_name and self.database_names:
            descriptor = glue.get_table(Name=self.table_name, DatabaseName=self.database_names[0])
            return GlueAthenaTable(descriptor['Table'])

        elif self.category and self.database_names:
            table_descriptors = []
            for db in self.database_names:
                tables = glue.get_tables(DatabaseName=db, MaxResults=1000)['TableList']
                tables = [t for t in tables if 'Parameters' in t and 'wiki' in t['Parameters']
                          and self.category in [w.strip() for w in t['Parameters']['wiki'].split(',')]]
                table_descriptors.extend(tables)
            return [self._tablecls(desc)(desc) for desc in table_descriptors]
        return None

    def _tablecls(self, desc):
        if 'Parameters' in desc and 'classification' in desc['Parameters'] \
                and desc['Parameters']['classification'] == 'redshift':
            return GlueRedshiftTable
        return GlueAthenaTable


driver.drivers['glue'] = GlueDriver
