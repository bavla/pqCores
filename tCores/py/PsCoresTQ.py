gdir = 'c:/users/batagelj/work/python/graph/Nets'
wdir = 'c:/users/batagelj/work/python/graph/Nets/bib'
# wdir = 'c:/users/batagelj/work/python/graph/JSON/SN5'
import sys, os, datetime, json
sys.path = [gdir]+sys.path; os.chdir(wdir)
from Nets import Network as N
import TQ
# fJSON = 'ConnectivityWeighted.json'
# fJSON = "violenceE.json"
# fJSON = 'stem.json'
# fJSON = 'CcCtest.json'
# fJSON = 'Terror news 50.json'
# fJSON = 'CcCSN5.json'
fJSON = 'CcTest.json'
# S = N.loadNetJSON(fJSON); G = S.pairs2edges()
G = N.loadNetJSON(fJSON)
# G.saveNetJSON(file="Terror50E",indent=1)
# fJSON = 'ConnectivityTest.json'
# fJSON = 'ExampleB.json'
# fJSON = 'PathfinderTest.json'
# G = N.Graph.loadNetJSON(fJSON)
G.delLoops()
print("Temporal Ps cores in: ",fJSON)
t1 = datetime.datetime.now()
print("started: ",t1.ctime(),"\n")
Tmin,Tmax = G._info['time']
D = { u: G.TQnetSum(u) for u in G._nodes }
# print("Sum =",D,"\n")
Core = { u: [d for d in D[u] if d[2]==0] for u in G.nodes() }
# core number = 0
D = { u: [d for d in D[u] if d[2]>0] for u in G.nodes() }
D = { u: d for u,d in D.items() if d!=[] }
Dmin = { u: min([e[2] for e in d]) for u,d in D.items() }
step = 0
while len(D)>0:
   step += 1
   dmin,u = min( (v,k) for k,v in Dmin.items() )
   if step % 100 == 1:
      print("{0:3d}. dmin={1:10.4f}   node={2:4d}".format(step,dmin,u))
   cCore = TQ.TQ.complement(Core[u],Tmin,Tmax+1)
   core = TQ.TQ.extract(cCore,[d for d in D[u] if d[2] == dmin])
   if core!=[]:
      Core[u] = TQ.TQ.sum(Core[u],core)
      D[u] = TQ.TQ.cutGE(TQ.TQ.sum(D[u],TQ.TQ.minus(core)),dmin) 
      for link in G.star(u):
         v = G.twin(u,link)
         if not(v in D): continue
         chLink = TQ.TQ.minus(TQ.TQ.extract(core,G.getLink(link,'tq')))
         if chLink==[]: continue
         diff = TQ.TQ.cutGE(TQ.TQ.sum(D[v],chLink),0)  
         D[v] = [ (sd,fd,max(vd,dmin)) for sd,fd,vd in diff ]
         if len(D[v])==0: del D[v]; del Dmin[v]
         else: Dmin[v] = min([e[2] for e in D[v]])
   if len(D[u])==0: del D[u]; del Dmin[u]
   else: Dmin[u] = min([e[2] for e in D[u]])
print("{0:3d}. dmin={1:10.4f}   node={2:4d}".format(step,dmin,u))
# print("\n-----\nCore =",Core)
t2 = datetime.datetime.now()
print("\nfinished: ",t2.ctime(),"\ntime used: ", t2-t1)


