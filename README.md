# desc-db-md

A tool that turns database description to markdown

install:
```
pip install git+https://github.com/sroussi/desc-db-md
```

example usages:

Single table:

```
descdbmd glue md -t mytable -d mydb
```

Scan all table within somedbs that has a table property wiki=mycat in glue
```
descdbmd glue md -c mycat -d mydb1,mydb2
```
