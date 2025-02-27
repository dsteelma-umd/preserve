#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import argparse
import sys
from .bagcheck import bagcheck
from .bytecount import bytecount
from .compare import compare
from .inventory import inventory
from .verify import verify


#============================================================================
# HELPER FUNCTIONS 
#============================================================================

def print_header(subcommand):
    '''Format and print a common header for each subcommand.'''
    title = 'preserve.py {0}'.format(subcommand)
    sys.stderr.write(
        '\n{0}\n{1}\n'.format(title, '=' * len(title))
        )


#============================================================================
# MAIN FUNCTION
#============================================================================

def main():
    '''Parse args and set the chosen sub-command as the default function.'''

    # main parser for command line arguments
    parser = argparse.ArgumentParser(
        description='Digital preservation utilities.'
        )
    subparsers = parser.add_subparsers(
        title='subcommands', description='valid subcommands', 
        help='-h additional help', metavar='{bc,inv,comp,ver}', dest='cmd'
        )
    parser.add_argument(
        '-v', '--version', action='version', help='Print version number and exit',
        version='%(prog)s 0.5'
        )
    subparsers.required = True

    # parser for the "bagcheck" sub-command
    bagcheck_parser = subparsers.add_parser(
        'bagcheck', aliases=['bck'],
        help='Compare an inventory file against a bagit bag',
        description='Checks relpath & checksum against bag manifest.'
        )
    bagcheck_parser.add_argument(
        '-i', '--inventory', help='Inventory CSV to compare', action='store'
        )
    bagcheck_parser.add_argument(
        '-b', '--bag', help='Path to BagIt bag', action='store'
        )
    bagcheck_parser.set_defaults(func=bagcheck)

    # parser for the "bytecount" sub-command
    bc_parser = subparsers.add_parser(
        'bytecount', aliases=['bc'], help='Count files and sizes in bytes',
        description='Count files by type and sum bytes.'
        )
    bc_parser.add_argument(
        'path', help='path to search', action='store'
        )
    bc_parser.add_argument(
        '-r', '--recursive', help='Recurse through subdirectories', action='store_true'
        )
    bc_parser.add_argument(
        '-H', '--human', help='Human-readable size', action='store_true'
        )
    bc_parser.set_defaults(func=bytecount)

    # parser for the "inventory" sub-command
    inv_parser = subparsers.add_parser(
        'inventory', aliases=['inv'], help='Create inventory of files with checksums',
        description='Create dirlisting with file metadata.'
        )
    inv_parser.add_argument('path', help='path to search', action='store')
    inv_parser.add_argument(
        '-o', '--outfile', help='path to (new) output file', action='store'
        )
    inv_parser.add_argument(
        '-e', '--existing', help='path to (existing) output file', action='store'
        )
    inv_parser.add_argument(
        '-a', '--algorithms', help='hash algorithms to run', action='store'
        )
    inv_parser.set_defaults(func=inventory)

    # parser for the "compare" sub-command
    comp_parser = subparsers.add_parser(
        'compare', aliases=['comp'], help='Compare two or more inventories',
        description='Compare contents of file inventories.'
        )
    comp_parser.add_argument(
        '-r', '--relpath', help='compare by relative paths', action='store_true'
        )
    comp_parser.add_argument('first', help='first file')
    comp_parser.add_argument('other', nargs='+', help='one or more files to compare')
    comp_parser.set_defaults(func=compare)

    # parser for the "verify" sub-command
    ver_parser = subparsers.add_parser(
        'verify', aliases=['ver'], help='Verify two sets of files',
        description='Verify checksums, relpaths, filenames.'
        )
    ver_parser.add_argument(
        '-c', '--checksums', help='Verify files by checksum', action='store_true'
        )
    ver_parser.add_argument(
        '-r', '--relpaths', help='Verify files by relative path', action='store_true'
        )                        
    ver_parser.add_argument(
        '-f', '--filenames', help='Verify files by filename', action='store_true'
        )
    ver_parser.add_argument('first', help='first file or path')
    ver_parser.add_argument('second', help='second file or path')
    ver_parser.set_defaults(func=verify)

    # parse the args and call the default sub-command function
    args = parser.parse_args()
    print_header(args.func.__name__)
    result = args.func(args)
    if result:
        sys.stderr.write(result)
        sys.stderr.write('\n\n')

if __name__ == "__main__":
    main()
