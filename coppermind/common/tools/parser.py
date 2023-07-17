import os
import sys
import struct
import hashlib
import xmltodict
from zipfile import ZipFile


__supported_formats__ = ['EPUB']  # TODO: Should pick from installed parsers


class MissingEbookFile(Exception):
    pass

class InvalidEbookFile(Exception):
    pass


def file_hash(path):
    sha256 = hashlib.sha256()
    with open(path, 'rb') as data:
        for chunk in iter(lambda: data.read(4096), b""):
                sha256.update(chunk)
    return sha256.hexdigest()


def ebook_parser(ebook_file, fmt='EPUB'):
    """
    Given an ebook file, parse metadata and return as dict
    """
    if os.path.exists(ebook_file):
        if fmt.upper() not in __supported_formats__:
            raise NotImplementedError('{} not yet implemented'.format(fmt.upper()))
        fmt_parser = getattr(sys.modules[__name__], '_{}_parser'.format(fmt.lower()))
        return fmt_parser(ebook_file)
    else:
        raise MissingEbookFile("{} was not found, current path: {}".format(ebook_file, os.curdir))
    raise Exception("Why did I get here?")


def _epub_parser(epub):
    """
    Handle EPUB specific parsing
    Return dict of ebook metadata

    An EPUB must contain META-INF/container.xml, which contains the path to
    the EPUB metadata file.
    """
    sha256 = file_hash(epub)
    zf = ZipFile(epub)
    xml = xmltodict.parse(zf.read('META-INF/container.xml'))
    # TODO: validate this is true for all EPUBs
    metadata_path = xml['container']['rootfiles']['rootfile']['@full-path']
    raw_metadata = xmltodict.parse(zf.read(metadata_path))
    metadata = {'format': 'epub'}
    for k, v in raw_metadata['package']['metadata'].items():
        if 'dc:' in k:
            if 'creator' in k:  # Required element, needs additional parsing
                k = 'author'
                v = v['#text']
            if 'identifier' in k:  # Required element, needs additional parsing
                k = 'identifiers'
                if not isinstance(v, list):
                    v = [v]  # Just in case we get a single element
                identifiers = []
                for i in v:
                    # Support multiple identifiers
                    identifiers.append({'identifier': i['@opf:scheme'], 'value': i['#text']})
                v = identifiers
            metadata[k.split('dc:')[-1]] = v
    metadata['identifiers'].append({'identifier': 'sha256', 'value': sha256})
    return metadata

def _mobi_parser(mobi):
    """
    MOBI specific parsing
    Check first if valid Mobipocket file, then parse out metadata

    Easiest method is to seek to byte 60 and read the next 8 bytes
    Should be the string 'BOOKMOBI'
    """
    with open(mobi, 'rb') as f:
        f.seek(60)
        file_type = f.read(8)
        if file_type.decode() != 'BOOKMOBI':
            raise InvalidEbookFile('File at {} is not a valid MOBI'.format(mobi))
        # Check header length
        f.seek(0)
        header = f.read(1024)
        length = struct.unpack_from('>L', header, 0x14)[0]
        exth = header[(length + 16):]
        ext_length, num_items = struct.unpack('>LL', exth[4:12])
        print(exth)
