#!/usr/bin/env python
import optparse
import sys

optparser = optparse.OptionParser()
optparser.add_option("-r", "--reference", dest="reference", default="test.alignment", help="Reference alignment file")
optparser.add_option("-p", "--prediction", dest="prediction", default="test.prediction", help="Predicted alignments to evaluate")

(opts, _) = optparser.parse_args()
r_data = opts.reference
p_data = opts.prediction

true_positive = 0
false_positive = 0
false_negative = 0
for ref_line,pred_line in zip(open(r_data),open(p_data)):
  ref_alignment_set = set(ref_line.split())
  pred_alignment_set = set(pred_line.split())
  true_positive += len(ref_alignment_set.intersection(pred_alignment_set))
  false_negative += len(ref_alignment_set.difference(pred_alignment_set))
  false_positive += len(pred_alignment_set.difference(ref_alignment_set))

sys.stdout.write('TP = %s, FP = %s, FN = %s\n' \
                 % (true_positive, false_positive, false_negative))
sys.stdout.write('Recall = %f\n' % (true_positive / float(false_negative+true_positive)))
sys.stdout.write('Precision = %f\n' % (true_positive / float(false_positive+true_positive)))
sys.stdout.write('F-score = %f\n' \
                 % (2.0*true_positive / (2.0*true_positive + false_positive + false_negative)))
