# vim: filetype=python ts=2 sw=2 sts=2 et :
from rbest import rbest
from tab  import Tab
import about

def eg1():
  the=about.defaults()
  the.data="data/auto93.csv"
  t=Tab(file=the.data)
  print(the.data)
  for _ in  range(10):
    print("")
    rbest(t,the)

#go()
#go("data/auto93.csv")
#diveg("data/auto93.csv")
#diveg("data/pom_dataset.csv")
#diveg("data/xomo_dataset.csv")

eg1()
