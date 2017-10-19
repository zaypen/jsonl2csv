#!/usr/bin/python

import sys
import argparse
import json


converters = {
    None.__class__: lambda v: '',
    bool: lambda v: str(v).upper(),
}


def escape(value, force=False):
    return '"{}"'.format(value.replace('"', '""')) if force or '"' in list(value) else value


def convert(value):
    t = type(value)
    fn = converters.get(t, lambda v: str(v))
    return escape(fn(value))


def merge_headers(headers, d):
    map(headers.add, d.keys())
    return headers


def make_record(headers, d):
    return ','.join(map(lambda header: convert(d[header]), headers))


def json2csv(infile, outfile):
    lines = infile.readlines()
    dicts = map(json.loads, lines)
    headers = reduce(merge_headers, dicts, set())
    records = map(lambda d: make_record(headers, d), dicts)
    outfile.write(','.join(map(escape, headers)) + '\n')
    map(lambda l: outfile.write(l + '\n'), records)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    json2csv(args.infile, args.outfile)
