#!/usr/bin/env python3

# SNIP: included termcolor.py from http://pypi.python.org/pypi/termcolor/1.0.0
########################################################################
# Copyright (c) 2008-2011 Volvox Development Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Author: Konstantin Lepa <konstantin.lepa@gmail.com>

"""ANSII Color formatting for output in terminal."""

import os


__ALL__ = [ 'colored' ]

VERSION = (1, 0, 0)

ATTRIBUTES = dict(
        list(zip([
            'bold',
            'dark',
            '',
            'underline',
            'blink',
            '',
            'reverse',
            'concealed'
            ],
            list(range(1, 9))
            ))
        )
del ATTRIBUTES['']


HIGHLIGHTS = dict(
        list(zip([
            'on_grey',
            'on_red',
            'on_green',
            'on_yellow',
            'on_blue',
            'on_magenta',
            'on_cyan',
            'on_white'
            ],
            list(range(40, 48))
            ))
        )


COLORS = dict(
        list(zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            ],
            list(range(30, 38))
            ))
        )


RESET = '\033[0m'


def colored(text, color=None, on_color=None, attrs=None):
    """Colorize text.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
        colored('Hello, World!', 'green')
    """
    if not text:
      return text
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)

        if on_color is not None:
            text = fmt_str % (HIGHLIGHTS[on_color], text)

        if attrs is not None:
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)

        text += RESET
    return text

########################################################################
# SNIP: end of termcolor.py from http://pypi.python.org/pypi/termcolor/1.0.0
# GPLv3 License applies from this line on.

import sys, random, time, copy

small_board = False

large_digits = (
    (
     '     ',
     '     ',
     '  0  ',
     '     ',
     '     ',
    ),
    (
     '  11 ',
     ' 111 ',
     '  11 ',
     '  11 ',
     '  11 ',
    ),
    (
     '2222 ',
     '   22',
     '  22 ',
     '22   ',
     '22222',
    ),
    (
     '33333',
     '   33',
     '  33 ',
     '   33',
     '3333 ',
    ),
    (
     '44   ',
     '44 44',
     '44444',
     '   44',
     '   44',
    ),
    (
     '55555',
     '55   ',
     '5555 ',
     '   55',
     '5555 ',
    ),
    (
     ' 66  ',
     '66   ',
     '6666 ',
     '66 66',
     ' 666 ',
    ),
    (
     '77777',
     '   77',
     '  77 ',
     ' 77  ',
     '77   ',
    ),
    (
     ' 888 ',
     '8   8',
     ' 888 ',
     '8   8',
     ' 888 ',
    ),
    (
     ' 999 ',
     '99 99',
     ' 9999',
     '   99',
     ' 999 ',
    ),
    (
     ' aaa ',
     '   aa',
     ' aaaa',
     'aa aa',
     ' aaaa',
    ),
    (
     '0x :D',
     'bb   ',
     'bbbb ',
     'bb bb',
     'bbbb ',
    ),
  )
  


def shove(items, zero_items=lambda l:[0]*l, reverse=False):
  was_len = len(items)
  if reverse:
    items = list(reversed(items))
  items = [copy.deepcopy(i) for i in items if i]
  i = 0
  while i < (len(items) - 1):
    if items[i] == items[i + 1]:
      items[i + 1] += 1
      del items[i]
    i += 1
  items.extend(zero_items(was_len - len(items)))
  if reverse:
    items = list(reversed(items))
  return items


class Cell:
  last_cell_color = 0
  colors = ('red', 'green', 'yellow', 'blue', 'magenta', 'cyan', )

  def __init__(c, val=0, col=None):
    c.val = val
    if col is None:
      Cell.last_cell_color += 1
      col = Cell.last_cell_color
    c.col = col

  def __repr__(c):
    return '<%d,%d>'%(c.val, c.col)

  def __bool__(c):
    return bool(c.val)

  def __int__(c):
    return c.val

  def __iadd__(c, other):
    c.val += int(other)
    return c

  def __eq__(c, other):
    if other is None:
      return False
    return c.val == int(other)

  def __str__(c):
    if not c.val:
      return '.'
    else:
      s = hex(c.val)[2:]
      return c.colored(s)

  def colored(c, txt):
    if not c.val:
      return txt
    return colored(txt, Cell.colors[c.col % len(Cell.colors)])

  def colored_large_digit(c):
    digit = large_digits[c.val]
    return [c.colored(digit_row) for digit_row in digit]



def new_cells(n):
  c = []
  for i in range(n):
    c.append(Cell())
  return c

def draw_small(rows):
  for r in rows:
    print(''.join([str(c) for c in r]))

def draw_large(rows):
  for row in rows:
    colored_digits = [c.colored_large_digit() for c in row]
    lines = '\n'.join([ '  '.join(line_parts) for line_parts in zip(*colored_digits)])
    print(lines + '\n')

def islist(x):
  return isinstance(x, list) or isinstance(x, tuple)

def same(a, b):
  if islist(a):
    if (not islist(b)) or (len(a) != len(b)):
      return False
    for i in range(len(a)):
      if not same(a[i], b[i]):
        return False
    return True
  return a == b


class Board:
  START = '' #
  LEFT = '<'
  RIGHT = '>'
  UP = '^'
  DOWN = 'v'

  def __init__(b, w=4, h=4, gamenr=None):
    b.W = w
    b.H = h
    b.moves = []
    b.undo_count = 0
    b.r = random.Random()
    if gamenr is not None:
      b.seed = gamenr
    else:
      b.seed = random.randint(0, 42e8)
    rows = [new_cells(w) for y in range(h)]
    b.record_move(b.START, rows)

  def choice(b, l):
    seed = b.seed + len(b.moves) - b.undo_count
    b.r.seed(seed)
    return b.r.choice(l)

  def get_state(b):
    step = len(b.moves) - b.undo_count
    direction, rows = b.moves[step - 1]
    return step, direction, rows

  def get_rows(b):
    step, direction, rows = b.get_state()
    return rows

  def draw(b):
    step, direction, rows = b.get_state()
    print('0xb #%d   %3d: %s   \n' % (b.seed, step, direction))
    if small_board:
      draw_small(rows)
    else:
      draw_large(rows)
    print()

  def left(b):
    rows = [shove(r, new_cells) for r in b.get_rows()]
    b.record_move(b.LEFT, rows)

  def right(b):
    rows = [shove(r, new_cells, True) for r in b.get_rows()]
    b.record_move(b.RIGHT, rows)

  def up(b):
    cols = [shove(c, new_cells) for c in list(zip(*b.get_rows()))]
    rows = list(zip(*cols))
    b.record_move(b.UP, rows)

  def down(b):
    cols = [shove(c, new_cells, True) for c in list(zip(*b.get_rows()))]
    rows = list(zip(*cols))
    b.record_move(b.DOWN, rows)

  def drop(b, rows):
    '''drop a new value into one of the cells in <rows>,
    return False if there was no space left to drop, True otherwise.
    Use b's rewindable random contraption to choose a position.'''
    def cell(x, y):
      return rows[y][x]
    coords = []
    for y in range(b.H):
      for x in range(b.W):
        if not cell(x, y):
          coords.append((x, y))
    if coords:
      x, y = b.choice(coords)
      rows[y][x].val = b.choice((1, 2))
      return True
    return False

  def record_move(b, direction, rows):
    assert direction in (b.START, b.UP, b.DOWN, b.LEFT, b.RIGHT)
    # don't count moves that had no effect,
    # and discard undone moves
    if b.moves:
      step = len(b.moves) - b.undo_count
      if b.undo_count:
        b.moves = b.moves[:-b.undo_count]
        b.undo_count = 0
      lastdir, lastrows = b.moves[-1]
      if same(rows, lastrows):
        return
    b.drop(rows)
    b.moves.append((direction, rows))

  def undo(b):
    if b.undo_count < (len(b.moves) - 1):
      b.undo_count += 1

  def redo(b):
    if b.undo_count > 0:
      b.undo_count -= 1


def usage():
  print('Usage:\n  %s [--small] [<width> [<height> [<game-nr>]]]' % sys.argv[0])
  exit(0)

if __name__ == '__main__':
  args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
  opts = [arg for arg in sys.argv[1:] if arg.startswith('-')]

  for o in opts:
    if o == '--small':
      small_board = True
    else:
      usage()

  import termios, fcntl, sys, os
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  try:
    w = 4
    h = 4
    gamenr = None

    try:
      if len(args) > 0:
        w = int(args[0])
        h = w

      if len(args) > 1:
        h = int(sys.argv[1])

      if len(args) > 2:
        gamenr = int(args[2])
    except:
      usage()

    b = Board(w, h, gamenr)
    key = None
    while True:
      print('\n\n\n\n\n')
      b.draw()
      key = None
      while True:
        c = sys.stdin.read(1)
        if c:
          print(c)
          if c == '\x1b':
            rest = sys.stdin.read(2)
            if rest == '[A':
              key = '^'
            elif rest == '[D':
              key = '<'
            elif rest == '[B':
              key = 'v'
            elif rest == '[C':
              key = '>'
          elif c in 'wk^':
            key = '^'
          elif c in 'ah<':
            key = '<'
          elif c in 'sjv':
            key = 'v'
          elif c in 'dl>':
            key = '>'
          elif c in 'bzyup,':
            key = 'u'
          elif c in 'fZYrn.':
            key = 'r'
          break;
        else:
          time.sleep(.1)

      if key:
        if key == '^':
          b.up()
        elif key == 'v':
          b.down()
        elif key == '<':
          b.left()
        elif key == '>':
          b.right()
        elif key == 'u':
          b.undo()
        elif key == 'r':
          b.redo()
      else:
        print('use arrow keys to shove, ctrl-c to quit, u to undo, r to redo')
  finally:
      termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
      fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

# vim: shiftwidth=2 tabstop=2 expandtab
