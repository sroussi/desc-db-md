# desc-db-md

A tool that turns database description to markdown

example usages:

Single table:

```
descdbmd glue md -t mytable -d mydb
```

Scan all table within somedbs that has a table property wiki=mycat in glue
```
descdbmd glue md -c mycat -d mydb1,mydb2
```
