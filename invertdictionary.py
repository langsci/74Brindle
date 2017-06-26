# -*- coding: utf-8 -*-

import re

class Entry():
  def __init__(self,a):
    sensenr = ''
    self.inverts = []
    poss = ''
    for l in a:
      l = l.strip()
      if l.endswith('%'):
        l = l[:-1]          
      if r'\headword' in l:
        headword=l          
        continue
      if r'\sensenr' in l:
        sensenr = l
        continue
      if l.strip().startswith(r'\synpos') or l.strip().startswith(r'\pos'):
        poss = l
        continue
      if 'lsgloss' in l:         
        gloss = l[9:][:-1]          
        self.inverts.append((gloss, headword, sensenr, poss))
 

       
d = {}

entries = open('chapters/dictionary.tex').read().decode('utf8').split('%------------------------------')
#print len(entries)
for e in entries[1:]:
  #print e
  a = e.split('\n')[1:]
  x = Entry(a)
  try:
    for inv in x.inverts:
      glosses = inv[0]
      for g in glosses.split(';'): 
        try:
          d[g.strip()].append(inv[1:])
        except KeyError:
          d[g.strip()] = [inv[1:]]
        except AttributeError:     
          s =  u"%% no gloss for %s" % x.vernaculars
          print s.encode('utf8')
  except AttributeError:
    continue
      
for k in sorted(d.keys(),key=lambda s: s.lower()):
  print '%'+30*'-'
  print '\\newentry'
  print u'\\lsgloss{%s}' % k.strip().encode('utf8')
  out = []
  for e in d[k]:
    out.append("""%s%%
%s%%
%s%%
"""%e)
  print ';\n'.join(out).encode('utf8')      
  