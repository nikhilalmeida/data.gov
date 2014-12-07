import fileinput
import json
from collections import Counter

applicants  = [ json.loads(file_data)  for file_data in fileinput.input()]
counter = Counter()
c_pos = Counter()
for applicant in applicants:
    counter[applicant['pT']]+=applicant['offered_wage']
    c_pos[applicant['pT']]+=1
avgs = sorted([ (counter[pos] / count, pos, count) for pos, count in  c_pos.most_common()],key=lambda tup: tup[0],reverse=True)
for avg in avgs:
     print "{}\t{}\t{}".format(avg[0], avg[1], avg[2])

    # print "{}\t{}\t{}".format(count, pos, avg)