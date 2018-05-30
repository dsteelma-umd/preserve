#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import argparse
from preserve.commands.bytecount import bytecount as bytecount
from preserve.commands.compare import compare as compare
from preserve.commands.inventory import inventory as inventory
from preserve.commands.verify import verify as verify
from preserve.batch import list_files as list_files

#============================================================================
# HELPER FUNCTIONS 
#============================================================================

def print_header(subcommand):
    '''Format and print a common header for each subcommand.'''
    title = 'preserve.py {0}'.format(subcommand)
    print('\n' + title)
    print('=' * len(title))


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
                            title='subcommands', 
                            description='valid subcommands', 
                            help='-h additional help', 
                            metavar='{bc,inv,comp,ver}',
                            dest='cmd'
                            )
    parser.add_argument('-v', '--version', 
                        action='version', 
                        help='Print version number and exit',
                        version='%(prog)s 0.1'
                        )
    subparsers.required = True

    # parser for the "bytecount" sub-command
    bc_parser = subparsers.add_parser(
                            'bytecount', aliases=['bc'], 
                            help='Count files and sizes in bytes',
                            description='Count files by type and sum bytes.'
                            )
    bc_parser.add_argument( 'path',
                            help='path to search',
                            action='store'
                            )
    bc_parser.add_argument( '-r', '--recursive', 
                            help='Recurse through subdirectories',
                            action='store_true'
                            )
    bc_parser.add_argument( '-H', '--human', 
                            help='Human-readable size',
                            action='store_true'
                            )
    bc_parser.set_defaults(func=bytecount)

    # parser for the "inventory" sub-command
    inv_parser = subparsers.add_parser(
                            'inventory', aliases=['inv'],
                            help='Create inventory of files with checksums',
                            description='Create dirlisting with file metadata.'
                            )
    inv_parser.add_argument('path',
                            help='path to search',
                            action='store'
                            )
    inv_parser.add_argument('-o', '--outfile',
                            help='path to (new) output file',
                            action='store'
                            )
    inv_parser.add_argument('-e', '--existing',
                            help='path to (existing) output file',
                            action='store'
                            )
    inv_parser.set_defaults(func=inventory)

    # parser for the "compare" sub-command
    comp_parser = subparsers.add_parser(
                            'compare', aliases=['comp'],
                            help='Compare two or more inventories',
                            description='Compare contents of file inventories.'
                            )
    comp_parser.add_argument('first', 
                            help='first file'
                            )
    comp_parser.add_argument('other', nargs='+',
                            help='one or more files to compare'
                            )
    comp_parser.set_defaults(func=compare)

    # parser for the "verify" sub-command
    ver_parser = subparsers.add_parser(
                            'verify', aliases=['ver'],
                            help='Verify checksums for two sets of files',
                            description='Verify checksums.'
                            )
    ver_parser.add_argument('first', 
                            help='first file or path'
                            )
    ver_parser.add_argument('second', 
                            help='second file or path'
                            )
    ver_parser.set_defaults(func=verify)

    # parse the args and call the default sub-command function
    args = parser.parse_args()
    print_header(args.func.__name__)
    args.func(args)

if __name__ == "__main__":
    main()
