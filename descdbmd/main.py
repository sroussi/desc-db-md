import sys

from descdbmd.driver import drivers
from descdbmd.writer import writers
from descdbmd.writers import markdown
from descdbmd.drivers import glue


def main():
    args = sys.argv[1:]
    driver = drivers[args[0]]()
    result = driver.get_result()

    writer = writers[args[1]]()
    print(writer.print_result(result))

