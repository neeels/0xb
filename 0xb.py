#!/usr/bin/env python

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

import sys, random, time

large_digits = (
    (
     '     ',
     '     ',
     '  0  ',
     '     ',
     '     ',
    ),
    (
     '   11',
     '   11',
     '   11',
     '   11',
     '   11',
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
     '     ',
     ' aa  ',
     'a  a ',
     'aaaa ',
     'a  a ',
    ),
    (
     'b!you',
     'B!WIN',
     'bBbB!',
     'B!!bB',
     'bBbB!',
    ),
  )
  


def shove(items, zero_items=lambda l:[0]*l, reverse=False):
  was_len = len(items)
  if reverse:
    items = reversed(items)
  items = [i for i in items if i]
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

  def __cmp__(c, other):
    return cmp(c.val, int(other))

  def __repr__(c):
    return '<%d,%d>'%(c.val, c.col)

  def __nonzero__(c):
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

class Board:

  def __init__(b, w=4, h=4):
    b.W = w
    b.H = h
    b.rows = []
    for y in range(h):
      b.rows.append(new_cells(w))

  def cell(b, x, y):
    return b.rows[y][x]

  def draw_small(b):
    for r in b.rows:
      print ''.join([str(c) for c in r])

  def draw_large(b):
    for row in b.rows:

      colored_digits = [c.colored_large_digit() for c in row]
      lines = '\n'.join([ '  '.join(line_parts) for line_parts in zip(*colored_digits)])
      print lines, '\n'

  def draw(b):
    return b.draw_large()

  def left(b):
    for r in range(len(b.rows)):
      b.rows[r] = shove(b.rows[r], new_cells)

  def right(b):
    for r in range(len(b.rows)):
      b.rows[r] = shove(b.rows[r], new_cells, True)

  def up(b):
    cols = [list(col) for col in zip(*b.rows)]
    for c in range(len(cols)):
      cols[c] = shove(cols[c], new_cells)
    b.rows = [list(row) for row in zip(*cols)]

  def down(b):
    cols = [list(col) for col in zip(*b.rows)]
    for c in range(len(cols)):
      cols[c] = shove(cols[c], new_cells, True)
    b.rows = [list(row) for row in zip(*cols)]

  def drop(b):
    coords = []
    for y in range(b.H):
      for x in range(b.W):
        c = b.cell(x,y)
        if not b.cell(x, y):
          coords.append((x, y))
    if coords:
      x, y = random.choice(coords)
      b.rows[y][x].val = random.choice((1, 2))
      return True
    return False



if __name__ == '__main__':
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

    if len(sys.argv) >= 2:
      w = int(sys.argv[1])
      h = w

    if len(sys.argv) >= w:
      h = int(sys.argv[2])

    b = Board(w, h)
    b.drop()
    key = None
    while True:
      print '\n\n\n\n\n'
      b.draw()
      if key:
        print key,
      key = None
      while True:
        try:
          c = sys.stdin.read(1)
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
          break;
        except IOError:
          time.sleep(.1)

      if key:
        old_rows = list(b.rows)
        if key == '^':
          b.up()
        if key == 'v':
          b.down()
        if key == '<':
          b.left()
        if key == '>':
          b.right()
        if b.rows != old_rows:
          b.drop()
      else:
        print 'use arrow keys to shove, ctrl-c to quit'
  finally:
      termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
      fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    
