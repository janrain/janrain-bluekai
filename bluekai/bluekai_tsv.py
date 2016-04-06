import re
from itertools import groupby

def fromRecords(records, paths=[]):
    return str.join('', fromRecordsIterator(records, paths))

def fromRecordsIterator(records, paths=[]):
    for record in records:
        yield fromRecord(record, paths)

def fromRecord(record, paths=None):

    def mapPath(path):
        try:
            return paths[path]
        except TypeError:
            return path

    # Compile (path, regex) for each path
    regex_mappings = [
        (path, re.compile(path.replace('.', r'(?:\.|\.\d+\.)')))
        for path in (paths or [])
    ]

    try:

        walked_record = walk(record)

        # (path, walked_path, value) of each walked_record that matches a
        # regex and add path from regex_mapping.
        walked_record = (
            (path, walked_path, value)
            for (walked_path, value) in walked_record
            for (path, regex) in regex_mappings
            if regex.fullmatch(walked_path)
        )

        # Group by path
        groups = groupby(walked_record, key=lambda each: each[0])

        # Join groups values with ','.
        attributes = (
            (path, str.join(',', [ value for (_, _, value) in group if value is not None ]))
            for (path, group) in groups
        )

        # Join attributes keys and values with "=".
        attributes = (
           "{}={}".format(mapPath(path), value)
           for (path, value) in attributes
        )

        # Join attributes with '|'.
        attributes = str.join('|', attributes)

        # Create row by joining uuid and attributes.
        row = "{}\t{}\n".format(record['uuid'], attributes)

    except TypeError:
        raise TypeError("Plural, Object and JSON value types are not supported")

    return row

def walk(obj, path=''):
    """
    Iterate over a JSON-compatible Python object.  Behavior with incompatible
    objects is undefined.
    >>> tuple(walk([0, 1]))
    (('', [0, 1]), ('0', 0), ('1', 1))
    >>> tuple(walk([0, 1], 'foo'))
    (('foo', [0, 1]), ('foo.0', 0), ('foo.1', 1))
    >>> tuple(walk({'foo': 'bar', 'baz': [0, 1]}))
    (('', {'foo': 'bar', 'baz': [0, 1]}), ('baz', [0, 1]), ('baz.0', 0), ('baz.1', 1), ('foo', 'bar'))
    >>> tuple(walk("wat"))
    (('', 'wat'),)
    """
    yield path, obj
    dot = '.' if path != '' else ''
    for key, value in _json_iter(obj):
        # these yield chains have got to be inefficient
        # but fixing that would mean losing recursion and simple iteration
        for pair in walk(value, path + dot + str(key)):
            yield pair


def _json_iter(obj):
    if isinstance(obj, dict):
        return sorted(obj.items())
    if isinstance(obj, list):
        return enumerate(obj)
    return ()
