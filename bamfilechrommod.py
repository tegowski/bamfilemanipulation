import argparse
import sys
import builtins
import os
import pysam

# sys.stdout = open("OutBam.bam", "w", buffering=1)
def print(text):
    builtins.print(text, end="\n")
    os.fsync(sys.stdout)
    
parser = argparse.ArgumentParser(description='Modify bamfile to remove the prefix from the chromosome')
parser.add_argument('--input', type=str, default=None, help="Input Bamfile")
parser.add_argument('--output', type=str, default=None, help="Output file name")
parser.add_argument('--prefix', type=str, default=None, help="Prefix to be removed")
args = parser.parse_args()

global infile,outbam
infile = args.input
outbam = args.output
prefix = args.prefix
prefixlen = int(len(prefix))

print(prefix)
print(prefixlen)

bamfile = pysam.AlignmentFile(infile, "rb")
outfile = pysam.AlignmentFile(outbam, "wb", template = bamfile)

#Remove prefix from header
header = bamfile.header.to_dict()
for ref in header['SQ']:
    if ref['SN'].startswith(str(prefix)):
        # Remove the prefix
        ref['SN'] = ref['SN'][prefixlen:]
			
with pysam.AlignmentFile(outbam, "wb", header=header) as outfile:
    for read in bamfile:
        outfile.write(read)