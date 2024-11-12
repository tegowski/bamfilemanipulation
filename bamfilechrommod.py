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
parser.add_argument('--input', type=str, required=True, help="Input Bamfile")
parser.add_argument('--output', type=str, required=True, help="Output file name")
parser.add_argument('--prefix', type=str, default=None, help="Prefix to be removed")
parser.add_argument('--addPrefix', type=str, default=None, help="Prefix to be added")
parser.add_argument('--suffix', type=str,default=None,help="Suffix to be removed")
args = parser.parse_args()

global infile,outbam
infile = args.input
outbam = args.output

bamfile = pysam.AlignmentFile(infile, "rb")
outfile = pysam.AlignmentFile(outbam, "wb", template = bamfile)
header = bamfile.header.to_dict()    

#Remove prefix from header
if args.prefix: 
    prefix = args.prefix
    prefixlen = int(len(prefix))
    for ref in header['SQ']:
        if ref['SN'].startswith(str(prefix)):
            # Remove the prefix
            ref['SN'] = ref['SN'][prefixlen:]

if args.addPrefix:
    addpre = args.addPrefix
    for ref in header['SQ']:
        ref['SN'] = addpre + ref['SN']
        
if args.suffix:
    suff = args.suffix
    sufflen = int(len(suff))
    for ref in header['SQ']:
        if ref['SN'].endswith(str(suff)):
            # Remove the prefix
            ref['SN'] = ref['SN'][:-sufflen]

    
with pysam.AlignmentFile(outbam, "wb", header=header) as outfile:
    for read in bamfile:
        outfile.write(read)
        
bamfile.close()
