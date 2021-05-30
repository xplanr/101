# vim: filetype=python ts=2 sw=2 sts=2 et :
# (c) 2021, tim menzies (timm@ieee.org) unlicense.org
"""Simple greedy  search for contrast sets."""

from lib  import obj,rs
import random,sys
from row import Row

def keys(t,the,r=2):
  rows = t.rows[:]
  random.shuffle(rows)
  rs([col.txt for col in t.cols.y])
  rs(t.y()        + ["baseline", len(rows)])
  n =int(the.train*len(rows))
  train = t.clone(rows[:n])
  test  = t.clone(rows[n:])
  rules = learn(train,the)
  judge(test,the,rules)
 
def judge(t,the,rules):
  now=t
  for n,(s,col) in enumerate(rules):
    less = now.clone()
    for x in selected(now.rows,*col): less.add(x)
    if (len(less.rows)  == len(now.rows)):
       break
    if Row(t,now.mid()) < Row(t,less.mid()): 
      break
    if len(less.rows) < 10:  break
    rs(less.y() + [ f"round{n+1}", len(less.rows),col])
    now=less
  
def learn(t, the):
  rows  = sorted(t.rows)
  n     = int(len(rows)**the.tiny)
  bests = rows[:n]
  rests = rows[n:]
  if len(rests) >= n*4:
    gap = int(len(rests) / (n*the.mostrest))
    rests = rests[::gap]
  best, rest= t.clone(bests), t.clone(rests)
  rs(rest.y()        + ["rest", len(rest.rows)])
  rs(best.y()        + ["best", len(best.rows)])
  return sorted(br(best,rest,the), 
                 reverse=True,
                 key=lambda z:z[0])

def br(best,rest,the):
  bins = best.bins(rest,the)
  for (kl,col),b in  bins.items():
    if kl==True:
      b = b/len(best.rows)
      r = bins.get((False,col),0) / len(rest.rows)
      s= b**2/(b+r)
      if b>r :
          yield s,col

def selected(rows, txt,col,span):
  def has(x,lo,hi):
    return x=="?" or (x==lo if lo==hi else lo <= x <= hi)
  for row in rows:
    if has(row.cells[col],*span):
      yield row
