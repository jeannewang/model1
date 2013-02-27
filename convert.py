#!/usr/bin/env python
import optparse
import sys

optparser = optparse.OptionParser()
optparser.add_option("-d", "--data", dest="train", default="test", help="Data filename prefix (default=data)")
optparser.add_option("-e", "--english", dest="english", default="english", help="Suffix of English filename (default=english)")
optparser.add_option("-c", "--chinese", dest="chinese", default="chinese", help="Suffix of Chinese filename (default=chinese)")
optparser.add_option("-a", "--alignment", dest="alignment", default="test.al", help="The alignments in s-t format")
(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (opts.train, opts.chinese)
e_data = "%s.%s" % (opts.train, opts.english)
a_data = opts.alignment

sys.stderr.write("Converting paired alignments to the binary evaluation format...\n")
bitext_lengths = [[len(sentence.strip().split()) for sentence in pair] for pair in zip(open(f_data), open(e_data))]
index = 0
for (l,alignments) in zip(bitext_lengths,open(a_data)):
  alignment_set = set([tuple(map(lambda x: int(x), pair.split('-'))) for pair in  alignments.split()])
  for s in range(l[0]):
    for t in range(l[1]):
      if (s,t) in alignment_set:
        sys.stdout.write('%d ' % index)
      index += 1
