import argparse

cli_parser = argparse.ArgumentParser(description='videalize')
subparsers = cli_parser.add_subparsers(dest='command')

_listen_parser = subparsers.add_parser(
    'listen', help='starts a worker to listen on a redis queue'
)

process_parser = subparsers.add_parser(
    'process', help='process a video'
)
process_parser.add_argument('video', help='the file to process')
process_parser.add_argument('-o', '--output',
                            dest='output',
                            default='output.mp4',
                            help='the processed file output')
