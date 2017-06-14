import sys
import codecs
fp = codecs.open(sys.argv[1], 'r', encoding='utf-8')
lines = fp.readlines()
fp.close()
fout = codecs.open('v2_' + sys.argv[1], 'w', encoding = 'utf-8')
for line in lines:
    fout.write(line.lstrip('+'))
fout.close()

