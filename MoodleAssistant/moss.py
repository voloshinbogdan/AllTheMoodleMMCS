import sys
import glob
import socket
import argparse
import urllib.request
import os
import os.path
import subprocess
import platform
import json
import pandas as pd
from time import sleep
from sys import exit
from html.parser import HTMLParser
from pywebcopy import save_website

def report():
    return "report.html"

# BEGIN: Check if file is text
ENC = {}
def is_binary(file_name):
  try:
    with open(file_name, 'tr', encoding='cp1251') as check_file:  # try open file in text mode
      check_file.read()
    ENC[file_name] = 'cp1251'
    return False
  except:  # if fail then file is non-text (binary)
    try:
      with open(file_name, 'tr', encoding='utf-8-sig') as check_file:  # try open file in text mode
        check_file.read()
      ENC[file_name] = 'utf-8-sig'
      return False
    except:  # if fail then file is non-text (binary)
      return True
# END: Check if file is text


class TableHTMLParser(HTMLParser):

  def __init__(self):
    self.table = False
    self.data = {
      'Source': [],
      'Compared': [],
      'Percent': [],
      'Lines': [],
      'URL': []
    }
    self.tind = -1
    self.tag = None
    super().__init__()

  def handle_starttag(self, tag, attrs):
    self.tag = tag
    if self.table:
      if tag == 'tr':
        self.tind = -1
      elif tag == 'td':
        self.tind += 1
      elif tag == 'a' and self.tind == 0:
        self.data['URL'].append(attrs[0][1])
    elif tag == 'table':
      self.table = True

  def handle_endtag(self, tag):
    self.tag = ''
    if tag == 'table':
      self.table = False
      self.tind = -1

  def handle_data(self, data):
    if self.table:
      if self.tind == 2 and self.tag == 'td':
        self.data['Lines'].append(int(data))
      elif self.tind == 0 and self.tag == 'a':
        _, p = data.split()
        self.data['Source'].append(data)
        self.data['Percent'].append(int(p[1:-2]))
      elif self.tind == 1 and self.tag == 'a':
        _, p = data.split()
        self.data['Compared'].append(data)
        self.data['Percent'][-1] = max(self.data['Percent'][-1], int(p[1:-2]))

def get_args_parser():
    parser = argparse.ArgumentParser(description='Run MOSS')
    parser.add_argument('files', type=str, nargs='+',
                        help='files to send')
    parser.add_argument('-X', action='store_true',
                        help='use experimental server')
    parser.add_argument('-d', action='store_true',
                        help='specifies that submissions are by directory, not by file')
    parser.add_argument('-uid', type=int, default=939277019,
                        help='ID to login')
    parser.add_argument('-m', type=int, default=100,
                        help='maximum number of times a given passage may appear before it is ignored')
    parser.add_argument('-n', type=int, default=250,
                        help='the number of matching files to show in the results')
    parser.add_argument('-l', type=str, default='c',
                        help='the source language of the tested programs')
    parser.add_argument('-b', type=str, nargs='*', default=[],
                        help='base files - code that appears in the base files is not counted in matches')
    parser.add_argument('-c', type=str, default='',
                        help='comment string that is attached to the generated report')

    return parser


def load_args(fname='moss.json'):
    with open(fname, 'r') as f:
        args = json.load(f)
    return args


def call_moss(**args):
    """
        Arguments same as for argparse. See get args_parser.
    """

    noreq = 'Request not sent.';

    print('Checking files . . .')
    b = []
    for f in args['b']:
      for arg in glob.glob(f, recursive=True):
        if not os.path.isfile(arg):
          print('Base file %s does not exist. %s' % (arg, noreq))
          exit()
        if not os.access(arg, os.R_OK):
          print('Base file %s is not readable. %s' % (arg, noreq))
          exit()
        if is_binary(arg):
          print('Base file %s is not a text file. %s' % (arg, noreq))
          exit()
        b.append(arg)

    files = []
    for f in args['files']:
      for arg in glob.glob(f, recursive=True):
        if not os.path.isfile(arg):
          print('File %s does not exist. %s' % (arg, noreq))
          exit()
        if not os.access(arg, os.R_OK):
          print('File %s is not readable. %s' % (arg, noreq))
          exit()
        if is_binary(arg):
          print('File %s is not a text file. %s' % (arg, noreq))
          exit()
        files.append(arg)

    if not files:
      print('No files submitted.')
      exit()

    print('OK')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(600)
    server_address = ('moss.stanford.edu', 7690) # 171.64.78.49

    try:
      sock.connect(server_address)
    except Exception:
      print('Could not connect to server %s: %s' % server_address)
      exit()


    def upload_file(filename, i, lang):
      name = filename.replace(' ', '_')
      name = os.path.join(
        os.path.basename(os.path.dirname(name)),
        os.path.basename(name)).replace('\\', '/')
      print('Uploading %s ...' % name)
      res = b''
      with open(filename, 'rt', encoding=ENC[filename]) as file:
        v = (file.read() + '\r\n').encode(ENC[filename]) #.decode('utf8').encode('utf8')
        size = len(v)
        res += ('file %s %s %s %s\n' % (i, lang, size, name)).encode('utf8')
        res += v
      print('done')
      return res


    sock.sendall((('moss %s\n' % (args['uid'])) +
                  ('directory %s\n' % (int(args['d']))) +
                  ('directory %s\n' % (int(args['d']))) +
                  ('X %s\n' % (int(args['X']))) +
                  ('maxmatches %s\n' % (args['m'])) +
                  ('show %s\n' % (args['n'])) +
                  ('language %s\n' % (args['l']))).encode('utf8'))

    res = sock.recv(3600)
    if res == b'no\n':
      print('Unrecognized language %s' % (args['l']))
      sock.sendall(b'end\n')
      sock.close()
      exit()

    to_send = b''
    for f in b:
      to_send += upload_file(f, 0, args['l'])

    for i, f in enumerate(files):
      to_send += upload_file(f, i+1, args['l'])

    to_send += ('query 0 %s\n' % (args['c'])).encode('utf8')
    sock.sendall(to_send)
    print("Query submitted.  Waiting for the server's response.")
    url = sock.recv(100).decode('utf-8')
    print(url)
    sock.sendall(b'end\n')
    sock.close()
    return url


def sort_moss(url):
    page = urllib.request.urlopen(url).read().decode('utf8')
    parserHTML = TableHTMLParser()
    parserHTML.feed(page)
    table = pd.DataFrame(parserHTML.data)
    return page, table.sort_values('Percent', ascending=False)
    

def report_moss(page, sortedtable, url):
    prepage = page.split('<TABLE>')[0] + url

    body = '\n<TABLE>\n'
    body += '<TR><TH>Source<TH>Compared<TH>Lines Matched\n'
    for i in range(len(sortedtable)):
      row = sortedtable.iloc[i]
      body += '<TR><TD><A HREF="%s">%s</A>\n' % (row['URL'], row['Source'])
      body += '  <TD><A HREF="%s">%s</A>\n' % (row['URL'], row['Compared'])
      body += '<TD ALIGN=right>%s\n' % (row['Lines'])
    body += '</TABLE>\n'

    postpage = page.split('\n</TABLE>\n')[1]

    with open(report(), "w") as f:
      f.write(prepage + body + postpage)


def download_website(url, download_folder):
    kwargs = {
        'bypass_robots': True,
        'project_name': 'site_folder',
        'over_write': False,
        'allowed_domains': ['moss.stanford.edu'],
        'load_css': True,
        'load_images': True,
        'load_javascript': True,
        'recursive': True,
        'recursion_depth': -1,  # Unlimited recursion depth
    }
    save_website(
        url=url,
        project_folder=download_folder,
        **kwargs
    )


def main():
    args = get_args_parser().parse_args()
    url = call_moss(**vars(args))
    print('Sorting...')
    page, sortedtable = sort_moss(url)
    print('done.')
    print('Creating report')
    report_moss(page, sortedtable, url)
    print('done')
    print(os.path.abspath(report()))
    
    if platform.system() == 'Darwin':       # macOS
      subprocess.call(('open', report()))
    elif platform.system() == 'Windows':    # Windows
      os.startfile(report())
    else:                                   # linux variants
      subprocess.call(('xdg-open', report()))


if __name__ == "__main__":
    main()