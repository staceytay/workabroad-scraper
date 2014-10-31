#!/usr/bin/env python
"""
This script cleans and processes JSON data scraped, using Scrapy, from
workabroad.ph and exports them to .csv or .json files.
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import argparse
import codecs
import csv
import os
import json
import sys

CSV_HEADERS = ['agency_address', 'agency_license', 'agency_name',
               'agency_telephone', 'expiry', 'href', 'id', 'info_principal',
               'location', 'qualifications_age', 'qualifications_education',
               'qualifications_experience', 'qualifications_gender',
               'requirements', 'title']

class Sanitizer:
    @staticmethod
    def clean_data(data):
        """
        "Private" function:
        Recursively cleans data. Works for dicts, lists, and strings.
        """
        if isinstance(data, (str, unicode)):
            return data.strip()
        elif isinstance(data, list):
            cleaned = [Sanitizer.clean_data(d) for d in data]
            return [d for d in cleaned if d not in ["", [], {}]]
        elif isinstance(data, dict):
            cleaned = {}
            for key, value in data.iteritems():
                temp = Sanitizer.clean_data(value)
                if temp not in ["", [], {}]:
                    cleaned[key] = temp
            return cleaned
        else:
            raise Exception("clean_data: unsupported data type " + str(type(data)))

    @staticmethod
    def flatten(data, flat={}, prefix=""):
        """
        "Public" method
        Flattens a JSON object to make it store data in csv later. The given
        JSON object cannot contain a list.
        """
        if prefix:
            prefix = prefix + '_'
        for key, value in data.iteritems():
            if isinstance(value, (str, unicode)):
                flat[prefix + key] = value
            elif isinstance(value, dict):
                Sanitizer.flatten(value, flat, prefix + key)
            else:
                raise Exception("flatten: unsupported data type " +
                                str(type(data)))
        return flat

    @staticmethod
    def process_data(data):
        """
        "Public" function:
        1. Remove whitespace and newlines from scraped data;
        2. Join list of strings for a field into a single string.

        Parameters
        ----------
        data: dict
             A single JSON data object
        """
        data = Sanitizer.clean_data(data)
        for field in ["expiry", "location", "requirements", "title"]:
            data[field] = Sanitizer.stringify(data.get(field, [""]))
        for field in ["agency", "info", "qualifications"]:
            for key, value in data[field].iteritems():
                data[field][key] = Sanitizer.stringify(value)
        return data

    @staticmethod
    def stringify(list_of_strings):
        return " ".join(list_of_strings)


def main():
    parser = argparse.ArgumentParser(description="Sanitize workabroad.ph scraped data")
    parser.add_argument("export", help="Export file format, 'csv' or 'json'")
    parser.add_argument("inputfile", help="Raw JSON file to be parsed")
    parser.add_argument("outputfile", help="Name of file to export data to")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity, "
                        "use when debugging only", action="store_true")

    global args
    args = parser.parse_args()

    file_path = os.path.dirname(os.path.abspath(__file__)) + '/' + args.inputfile

    with codecs.open(file_path, 'r', 'utf-8') as json_data,\
         codecs.open(args.outputfile, 'w', 'utf-8') as out:
        items = json.load(json_data)
        processed_items = []
        for i, item in enumerate(items):
            processed_items.append(Sanitizer.process_data(item))
        if args.export == "csv":
            writer = csv.writer(out)
            writer.writerow(CSV_HEADERS)
            for item in processed_items:
                flat = Sanitizer.flatten(item)
                values = [flat[key] for key in CSV_HEADERS]
                writer.writerow(values)
        elif args.export == "json":
            json.dump(processed_items, out)
        else:
            sys.exit("Invalid export file format: " + args.export +
                     ", only 'csv' and 'json' is accepted")


if __name__ == '__main__':
    main()
