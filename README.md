# bamfilemanipulation
Scripts for modifying and splitting bamfiles.
This has been designed with python 3.7.12
Requires pysam

The first script (barcodemod.py) can be used for modifying the barcode information containted within the CB:Z: tag of a bamfile based on sequence information contained within the read header. This is built to specifically for preparing bamfiles from Parse Biosciences single-cell sequencing kit (WT Mini, v2 chemistry) for using the Bullseye pipeline to identify m6A methylation using single-cell DART-seq. It finds the sublibrary barcode sequence in the read header and adds either "_s1" or "_s2".

Usage of barcodemod.py
python barcodemod.py --input [inbam.bam] --output [outbam.bam]


The second script (bamsplit.py) can be used for splitting out reads within a bamfile using information with in the tags. The most common use may be to split based on barcodes contained within the CB:Z: tag, though if there are many barcodes to check, this will take a long time.

Usage of bamsplit.py
python bamsplit.py --input [inbam.bam] --output [outbam.bam] [options]

Optional arguments
--barcodeFile [file.txt]
This should be a file consisting of a single column of information (such as a list of barcodes). Reads in the bamfile being split matching these values will be split into the output.

--field [tag name]
This indicates the sam tag to be used for splitting. Use the 2-character indicator (e.g. CB:Z: should be listed as CB).

--singleValue [string]
If you only have a single value you want split (e.g. a single barcode or experiment/replicate indicator), use this value and provide the string of interest.

The third script (bamfilechrommod.py) is used to remove a prefix from the chromosome column within bamfiles. Generally this can be used to remove the "chr", but also any provided prefix

Usage of bamfilechrommod.py
python bamfilechrommod.py --input [inbam.bam] --output [outbam.bam] [options]

Optional arguments
--prefix A string at the front of the chromosome name to be removed

--addPrefix A string to add to the front of the chromosome name

--suffix A string at the end of the chromosome name to be removed
