#!/usr/bin/env python
import sys, random, time

def val2char(val):
  if not val:
    return '.'
  else:
    return hex(val)[2:]

def shove(items, reverse=False):
  was_len = len(items)
  if reverse:
    items = reversed(items)
  items = [i for i in items if i]
  i = 0
  while i < (len(items) - 1):
    if items[i] == items[i + 1]:
      items[i] += 1
      del items[i+1]
    i += 1
  items.extend([0] * (was_len - len(items)))
  if reverse:
    items = list(reversed(items))
  return items


class Board:

  def __init__(b, w=4, h=4):
    b.W = w
    b.H = h
    b.rows = [[0] * w] * h
    b.rows = [list(row) for row in b.rows] # make sure each is a single list

  def cell_char(b, x, y):
    return val2char(b.rows[y][x])

  def cell(b, x, y):
    return b.rows[y][x]

  def draw(b):
    for r in b.rows:
      print ''.join([val2char(v) for v in r])

  def left(b):
    for r in range(len(b.rows)):
      b.rows[r] = shove(b.rows[r])

  def right(b):
    for r in range(len(b.rows)):
      b.rows[r] = shove(b.rows[r], True)

  def up(b):
    cols = [list(col) for col in zip(*b.rows)]
    for c in range(len(cols)):
      cols[c] = shove(cols[c])
    b.rows = [list(row) for row in zip(*cols)]

  def down(b):
    cols = [list(col) for col in zip(*b.rows)]
    for c in range(len(cols)):
      cols[c] = shove(cols[c], True)
    b.rows = [list(row) for row in zip(*cols)]

  def drop(b):
    coords = []
    for y in range(b.H):
      for x in range(b.W):
        if not b.cell(x, y):
          coords.append((x, y))
    if coords:
      x, y = random.choice(coords)
      b.rows[y][x] = random.choice((1, 2))
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
    b = Board(4, 4)
    b.drop()
    while True:
      b.draw()
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
          elif c in 'wk':
            key = '^'
          elif c in 'ah':
            key = '<'
          elif c in 'sj':
            key = 'v'
          elif c in 'dl':
            key = '>'
          break;
        except IOError:
          time.sleep(.1)

      if key:
        print key
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
        print 'use arrow keys!'
  finally:
      termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
      fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    
