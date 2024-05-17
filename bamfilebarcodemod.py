import argparse
import sys
import builtins
import os
import pysam

# sys.stdout = open("OutBam.bam", "w", buffering=1)
def print(text):
    builtins.print(text, end="\n")
    os.fsync(sys.stdout)
    
parser = argparse.ArgumentParser(description='Modify bamfile for Parse v2 barcode names')
parser.add_argument('--input', type=str, default=None, help="Input Bamfile")
parser.add_argument('--output', type=str, default=None, help="Output file name")
args = parser.parse_args()

global infile,outbam
infile = args.input
outbam = args.output

bamfile = pysam.AlignmentFile(infile, "rb")
outfile = pysam.AlignmentFile(outbam, "wb", template = bamfile)

for line in bamfile:
    readname = line.query_name
    sublib = str.split(readname, '+')
    columns = line.to_string().split()
    # outfile.write(columns)
    bcpattern = "CB:Z:"
    barcode = [i for i in columns if bcpattern in i]
    barcode = str(barcode)
    barcode2 = barcode.replace("[","").replace("]","").replace("'","").replace("CB:Z:","")
    if sublib[1] == 'ATGTGAAG':
        barcode3 = str(barcode2) + "_s1"
        line.set_tag('CB',barcode3)
        outfile.write(line)
    elif sublib[1] == 'GTCCAACC':
        barcode3 = str(barcode2) + "_s2"
        line.set_tag('CB',barcode3)
        outfile.write(line)

# file1 = pysam.AlignmentFile("ex1.bam", "rb")
# lines = file1.readlines()

# with open(infile, 'r') as file:
    # for line in file:       
        # columns = str.split(line)
        # sublib = str.split(columns[0], '+')
        # bcpattern = "CB:Z:"
        # barcode = [i for i in columns if bcpattern in i]
        # barcode = str(barcode)
        # barcode2 = barcode.replace("[","").replace("]","").replace("'","")
        # if sublib[1] == 'ATGTGAAG':
            # barcode3 = "NEW:" + str(barcode2) + "_s1"
            # print(line + str(barcode3))
        # elif sublib[1] == 'GTCCAACC':
            # barcode3 = "NEW:" + str(barcode2) + "_s2"
            # print(line + str(barcode3))
