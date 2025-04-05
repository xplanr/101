# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, tim menzies (timm@ieee.org) unlicense.org
"""Recursive  call keys on the fastmap cluster,
descend into the subtrees greated by those rules."""

from lib  import obj,rs
import random,sys
from row import Row

def rbest(t,the,cols=None,loud=False):
  rules=[]
  cols = cols or t.cols.x
  tiny = len(t.rows)**the.tiny // 1
  def recurse(rows, lvl=0):
     dist    = lambda r1,r2 : r1.dist(r2,the, cols=cols)
     faraway = lambda r1    : t.far(r1, the, cols=cols, rows=rows)
     if loud: 
       print(f"{'|.. ' * lvl}{len(rows)}")
     if len(rows)>=2*tiny: 
       # find  two distant points, in  linear times
       any   = random.choice(rows)
       left  = faraway(any)
       right = faraway(left)
       c     = dist(left,right)
       # map everyone onto a line between the two distant points
       for row in rows:
         a = dist(row,left)
         b = dist(row,right)
         x = (a**2 + c**2 - b**2)/(2*c+1E-32) # cosine rule
         row.fastmapx = x
       # sort everyone along that line
       rows = sorted(rows, key=lambda row: row.fastmapx)
       mid  = len(rows)//2
       best, rest = (rows[:mid], rows[mid:]) if left < right else (rows[mid:],rows[:mid])
       maybe  = sorted(br( t.clone(best), t.clone(rest), the),
                       reverse=True, key=lambda z:z[0])
       if maybe:
         rule = maybe[0][1]
         if rule not in rules:
           todo = list(selected(rows, *rule))
           if len(todo) <  len(rows):
              rules.append(rule)
              return recurse(todo, lvl+1)  # recurse on the left-hand-side half
     return t.clone(rows), rules


  #-- main ----------
  return recurse(t.rows)

def br(best,rest,the):
  bins = best.bins(rest,the)
  for (kl,col),b in  bins.items():
    if kl==True:
      b = b/len(best.rows)
      r = bins.get((False,col),0) / len(rest.rows)
      s= b**2/(b+r)
      if  b>r :
          yield s,col

def selected(rows, txt,col,span):
  def has(x,lo,hi):
    return x=="?" or (x==lo if lo==hi else lo <= x <= hi)
  for row in rows:
    if has(row.cells[col],*span):
      yield row
