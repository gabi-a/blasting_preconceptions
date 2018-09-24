# CSIRO C3 : BLASTing away preconceptions in crystallisation trials

### WARNING
What follows are not always clear instructions - they are my notes in case I need to go back to any step.\
Running the steps out of order will likely fail due to files missing which should have been generated\
in a previous step.\
The C6 code is not published, so it will not be possible to run that stage.

## Dependencies
Python 2 and Python 3 are required to execute every stage.\
numpy and matplotlib need to be installed (just install scipy).\
This has been developed on windows, however everything *should* run on linux except C6 with out much modification.\
Some of the code takes a few hours - it is very easy to parallize if you want to run it on multiple cores however\
(in fact I did do this but it is too messy to publish).

(1) PDB data can be downloaded via FTP from ftp://ftp.wwpdb.org/pub/pdb \
(2) BLAST database and executables can be downloaded from https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download
Check that blast is installed by running blastp in a terminal.

## Setup databases
In the db folder, place:
* a folder called pdb, containing the entire current pdb as a list of .ent.gz files. [Download from (1)]
[Only required for running BLAST stages]
* a file called pdb_seqres.txt containing the FASTA sequence of every pdb entry. [Download from (1)]
* a folder called blastdb, containing the current BLAST db for proteins. [Download and extract pdbaa from (2)]
Also create an empty folder in db called blastout.

Resulting directory structure should be:\
db\
|-- blastdb\
|-- blastout\
|-- pdb

## Parsing conditions
1. First we create a text database which will be the input to the parser.\
  `>python make_r280_db.py` (~ 35 mins)
   This generates `r280db.txt` which is a list of all R280 lines in the \
   format required by `parseFile.py`

2. The next step is to parse the REMARK 280 lines to extract chemical conditions.\
   `>cd Parse`\
   `>pipenv --python 2`\
   `>pipenv run python parseFile.py "../db/r280db.txt" > parsereport.txt` (~ 4 hours)\
   This generates a number of files in the Parse folder:
   * `parsereport.txt` has various reports on the parsed chemicals and quality of parsing
   * `output/cond_resolved_out.xml` lists each well and its conditions
   * `output/chem_list.xml` lists all chems found
   * `output/chemfreq_resolved_out.xml` lists the frequency of all chems found
   * `output/chem_alia.xml` lists aliases used if any
   
3. We now convert the parsed xml to a dictionary, and also save a list of all\
   parsed, non empty pdb codes for later use.\
   `>cd ..`\
   `>python make_chems_dict.py`\
   This generates two files in the db folder:
   * `chems_dict.pkl` is a dictionary of wells with format `{pdb code : list of conditions}`
   * `nonempty_pdbcodes.pkl` is a list of all pdb codes with non empty chemical resevoirs

## Running BLAST
At this step we blast every structure in the PDB which has been parsed.
`>python blast_all.py` (run overnight)
This generates a CSV file for each structure in `db/blastout`.
It also saves a list of all codes which could be blasted (i.e. their sequence was available) in 
`db/nonempty_seq_pdbcodes.pkl`

## C6
`>python make_pickle_files.py` to convert pickle3 files to pickle2\
`>pipenv --python 2` to create a python 2 environment\
`>pipenv install numpy` to install numpy to the pipenv environment\
`>pipenv run python correlate_c6.py`

## PEGeq
To calculate the PEGeq slope and intercept, and visualise it:\
`>python pegeq.py`\
This creates `db/pegeq.pkl` which stores the slope.
