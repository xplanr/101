# vim: filetype=python ts=2 sw=2 sts=2 et :
from rbest import rbest
from tab  import Tab
import about,random
from lib import rs

def eg1():
  the=about.defaults()
  t=Tab(file=the.data)
  print(the.data)
  for _ in range(10):
    cluster,rules=rbest(t,the)
    print(rs(cluster.y(),2),len(cluster.rows),sorted(rules),random.random())

#go()
#go("data/auto93.csv")
#diveg("data/auto93.csv")
#diveg("data/pom_dataset.csv")
#diveg("data/xomo_dataset.csv")

eg1()
