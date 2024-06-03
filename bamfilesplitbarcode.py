import argparse
import sys
import builtins
import os
import pysam
    

parser = argparse.ArgumentParser(description='Split Bamfile by barcode in CB tag')
parser.add_argument('--input', type=str, default=None, help="Input Bamfile")
parser.add_argument('--output', type=str, default=None, help="Output file name")
parser.add_argument('--barcodeFile', type=str, default=None, help="File with one column consisting of list of valid barcodes to split sequences into out bam file")
parser.add_argument('--field', type=str, default='CB', help="field tag of that you want to split by")
parser.add_argument('--singleValue', type=str, nargs="?", help="Use this tag if you want to input a specific string to filter a specific field by. Provide the string here.", default="multi")
args = parser.parse_args()

def print(text):
    builtins.print(text, end="\n")
    os.fsync(sys.stdout)

global infile,outbam,bcs,field,filtval
infile = args.input
outbam = args.output
bcs = args.barcodeFile
field = args.field
filtval = args.singleValue

if bcs is not None:
	barcodefile = open(bcs, "r")
	bclist = barcodefile.read().splitlines()
else:
	print("No barcode file provided. Hopefully that's OK")

bamfile = pysam.AlignmentFile(infile, "rb")
outfile = pysam.AlignmentFile(outbam, "wb", template = bamfile)

if filtval == "multi":
    for line in bamfile:
        bcval = line.get_tag(field)
        if bcval in bclist:
            outfile.write(line)
else:
    for line in bamfile:
        bcval = line.get_tag(field)
        if bcval == filtval:
            outfile.write(line)    
