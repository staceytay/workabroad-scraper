#!/usr/bin/env python
"""
This script cleans and processes JSON data scraped, using Scrapy, from
workabroad.ph.
"""

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Sanitize workabroad.ph scraped data")
    parser.add_argument("export", help="Export file format, 'csv' or 'json'")
    parser.add_argument("inputfile", help="Text file to be parsed")
    parser.add_argument("outputfile", help="Name of file to export data to")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity, "
                        "use when debugging only", action="store_true")

    global args
    args = parser.parse_args()

    if args.export == "csv":
        pass
    elif args.export == "json":
        pass
    else:
        sys.exit("Invalid export file format: " + args.export + ", only 'csv' and "
                 "'json' is accepted")


if __name__ == '__main__':
    main()
