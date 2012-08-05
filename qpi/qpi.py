'''qpi: Turn your Raspberry Pi into a badass media machine.'''
import argparse
import display
import multiprocessing
import server

def parse_args(args):
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument(
      '--port', default=5000, type=int, help='The port to listen on')
  return parser.parse_args(args[1:])

def main(args):
  opts = parse_args(args)
  server.run_server(opts.port)

if __name__ == '__main__':
  import sys
  main(sys.argv)
