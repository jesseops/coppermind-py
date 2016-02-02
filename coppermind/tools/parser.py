import os
import xmltodict
from zipfile import ZipFile


class MissingEbookFile(Exception):
    pass


def ebook_parser(ebook_file, fmt='EPUB'):
    """
    Given an ebook file, parse metadata and return as dict
    """
    if os.path.exists(ebook_file):
        if fmt != 'EPUB':
            raise NotImplementedError('EPUB only for now')
        return _epub_parser(ebook_file)
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
    zf = ZipFile(epub)
    xml = xmltodict.parse(zf.read('META-INF/container.xml'))
    metadata_path = xml['container']['rootfiles']['rootfile']['@full-path']  # TODO: validate this is true for all EPUBs
    raw_metadata = xmltodict.parse(zf.read(metadata_path))
    metadata = {'format': 'epub'}
    for k, v in raw_metadata['package']['metadata'].items():
        if 'dc:' in k:
            if 'creator' in k:  # Required element, needs additional parsing
                k = 'author'
                v = v['#text']
            if 'identifier' in k:  # Required element, needs additional parsing
                if not isinstance(v, list):
                    v = [v]  # Just in case we get a single element
                identifiers = {}
                for i in v:
                    identifiers[i['@opf:scheme']] = i['#text']  # Support multiple identifiers
                v = identifiers
            metadata[k.replace('dc:', '')] = v
    return metadata
