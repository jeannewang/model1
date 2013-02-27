#!/usr/bin/env python
import optparse
import sys
from collections import defaultdict

optparser = optparse.OptionParser()
optparser.add_option("-d", "--data", dest="train", default="train", help="Data filename prefix (default=data)")
optparser.add_option("-e", "--english", dest="english", default="english", help="Suffix of English filename (default=english)")
optparser.add_option("-c", "--chinese", dest="chinese", default="chinese", help="Suffix of Chinese filename (default=chinese)")
optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="Threshold for aligning with Dice's coefficient (default=0.5)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (opts.train, opts.chinese)
e_data = "%s.%s" % (opts.train, opts.english)


sys.stderr.write("Training with dice...")
bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
f_count = defaultdict(int)
e_count = defaultdict(int)
fe_count = defaultdict(int)
for (n, (f, e)) in enumerate(bitext):
  for f_i in set(f):
    f_count[f_i] += 1
    for e_j in set(e):
      fe_count[(f_i,e_j)] += 1
  for e_j in set(e):
    e_count[e_j] += 1
  if n % 500 == 0:
    sys.stderr.write(".")
'''
dice = defaultdict(int)
for (k, (f_i, e_j)) in enumerate(fe_count.keys()):
  dice[(f_i,e_j)] = 2.0 * fe_count[(f_i, e_j)] / (f_count[f_i] + e_count[e_j])
  if k % 5000 == 0:
    sys.stderr.write(".")
'''

sys.stderr.write("\n")
sys.stderr.write("Training with model 1...")
#initialize t(e|f) uniformly
t = defaultdict(int)
for (n, (f, e)) in enumerate(bitext):
  for e_i in set(e):
    for f_j in set(f):
		t[(e_i,f_j)] = 1.0/len(fe_count)

old_t = t.copy()
converged=False
epsilon=0.00001
iterations=0
while(not converged):
	#set count(e|f) to 0 for all e,f
	count= defaultdict(int)
	#set total(f) to 0 for all f
	total = defaultdict(int)
	for (n, (f, e)) in enumerate(bitext):
		for e_i in e:
			total_s = 0
			for f_j in f:
				total_s += t[(e_i,f_j)]
		for e_i in e:
			for f_j in f:
				count[(e_i,f_j)] += t[(e_i,f_j)] / total_s
				total[f_j] += t[(e_i,f_j)] / total_s
	# for all f in domain( total(.) )
	# for all e in domain( count(.|f) )
	for (n, (f, e)) in enumerate(bitext):
		for f_i in f:
			def getFirstWhereSecondEqualsFI(x):
				if x[1]==f_i:
					return x[0]
			for e_j in map(getFirstWhereSecondEqualsFI,count):
				t[(e_i,f_j)] = count[(e_i,f_j)] / total[f_j]
	if iterations % 5000 == 0:
		sys.stderr.write(".")
	# until convergence
	if t != old_t:
		for (n,(f,e)) in enumerate(bitext):
			for e_i in e:
				for f_j in f:
					if t[(e_i,f_j)]-old_t[(e_i,f_j)] <= epsilon:
						converged=True
					else:
						converged=False
	iterations+=1				
sys.stderr.write("\n")

print 'init', 1.0/len(fe_count)
for (f, e) in bitext:
  for (i, f_i) in enumerate(f): 
    for (j, e_j) in enumerate(e):
      if t[(f_i,e_j)] >= opts.threshold:
        sys.stdout.write("%i-%i " % (i,j))
  sys.stdout.write("\n")
