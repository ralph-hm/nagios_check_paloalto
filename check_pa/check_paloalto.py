# -*- coding: utf-8 -*-
import argparse
import sys

import nagiosplugin

import check_pa.user_agent as useragent
import check_pa.certificate as certificate
import check_pa.diskspace as diskspace
import check_pa.load as load
import check_pa.environmental as environmental
import check_pa.sessioninfo as sessioninfo
import check_pa.throughput as throughput
import check_pa.thermal as thermal

@nagiosplugin.guarded
def main():  # pragma: no cover
    args = parse_args(sys.argv[1:])
    check = args.func(args)
    check.main(verbose=args.verbose)


def _diskspace(args):
    return diskspace.create_check(args)


def _certificates(args):
    return certificate.create_check(args)


def _load(args):
    return load.create_check(args)


def _environmental(args):
    return environmental.create_check(args)


def _sessinfo(args):
    return sessioninfo.create_check(args)


def _thermal(args):
    return thermal.create_check(args)


def _throughput(args):
    return throughput.create_check(args)


def _useragent(args):
    return useragent.create_check(args)



def parse_args(args):
    parser = argparse.ArgumentParser(description=__doc__)

    connection = parser.add_argument_group('Connection')
    connection.add_argument('-H', '--host',
                            help='PaloAlto Server Hostname')
    connection.add_argument('-T', '--token',
                            help='Generated Token for REST-API access')

    debug = parser.add_argument_group('Debug')
    debug.add_argument('-v', '--verbose', action='count', default=0,
                       help='increase output verbosity (use up to 3 times)')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Sub-Parser for command 'diskspace'.
    parser_diskspace = subparsers.add_parser('diskspace',
                                             help='Checks used diskspace.',
                                             )
    parser_diskspace.add_argument('-w', '--warn',
                                  metavar='WARN', type=int, default=85,
                                  help='Warning if diskspace is greater. '
                                       '(default: %(default)s)')
    parser_diskspace.add_argument('-c', '--crit',
                                  metavar='CRIT', type=int, default=95,
                                  help='Critical if disksace is greater. '
                                       '(default: %(default)s)')

    parser_diskspace.set_defaults(func=_diskspace)

    # Sub-Parser for command 'certificates'.
    parser_certificates = subparsers.add_parser(
        'certificates',
        help='Checks the certificate store for '
             'expiring certificates: Outputs is a warning, '
             'if a certificate is in range.')
    parser_certificates.add_argument(
        '-ex', '--exclude', default='', help='Exclude certificates from '
                                             'check by name.')
    parser_certificates.add_argument(
        '-r', '--range',
        metavar='RANGE',
        default='0:20',
        help='''
        Warning if days until certificate expiration is in range:
        Represents a threshold range.
        The general format is "[@][start:][end]
        (default: %(default)s)
        ''')
    parser_certificates.set_defaults(func=_certificates)

    # Sub-Parser for command 'load'.
    parser_load = subparsers.add_parser(
        'load',
        help='Checks the CPU load.')
    parser_load.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=85,
        help='Warning if CPU load is greater. (default: %(default)s)')
    parser_load.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=95,
        help='Critical if CPU load is greater. (default: %(default)s)')
    parser_load.set_defaults(func=_load)

    # Sub-Parser for command 'useragent'.
    parser_useragent = subparsers.add_parser(
        'useragent',
        help='Checks for running useragents.')
    parser_useragent.set_defaults(func=_useragent)

    # Sub-Parser for command 'environmental'.
    parser_environmental = subparsers.add_parser(
        'environmental',
        help='Checks if an alarm is found.')
    parser_environmental.set_defaults(func=_environmental)

    # Sub-Parser for command 'sessinfo'.
    parser_sessinfo = subparsers.add_parser(
        'sessinfo',
        help='Checks important session parameters.')
    parser_sessinfo.set_defaults(func=_sessinfo)

    # Sub-Parser for command 'thermal'.
    parser_thermal = subparsers.add_parser(
        'thermal',
        help='Checks the temperature.')
    parser_thermal.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=40,
        help='Warning if temperature is greater. (default: %(default)s)')
    parser_thermal.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=45,
        help='Critical if temperature is greater. (default: %(default)s)')
    parser_thermal.set_defaults(func=_thermal)

    # Sub-Parser for command 'throughput'.
    parser_throughput = subparsers.add_parser(
        'throughput',
        help='Checks the throughput.')

    parser_throughput.add_argument(
        '-i', '--interface',
        help='PA interface name, seperate by comma.',
        nargs='?',
        required=True,
    )
    parser_throughput.set_defaults(func=_throughput)

    return parser.parse_args(args)


if __name__ == '__main__':  # pragma: no cover
    main()
