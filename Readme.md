# CSIRO C3 : BLASTing away preconceptions in crystallisation trials
Python 2 and Python 3 are required to execute every stage.

(1) PDB data can be downloaded via FTP from ftp://ftp.wwpdb.org/pub/pdb
(2) BLAST database and executables can be downloaded from https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download

## Setup databases
In the db folder, place:
* a folder called pdb, containing the entire current pdb as a list of .ent.gz files. [Download from (1)]
[Only required for running BLAST stages]
* a file called pdb_seqres.txt containing the FASTA sequence of every pdb entry. [Download from (1)]
* a folder called blastdb, containing the current BLAST db for proteins. [Download and extract pdbaa from (2)]
Also create an empty folder in db called blastout.

Resulting directory structure should be:
db
|-- blastdb
|-- blastout
|-- pdb

## Parsing conditions
1. First we create a text database which will be the input to the parser.
  `>python make_r280_db.py` | ~ 35 mins
   This generates `r280db.txt` which is a list of all R280 lines in the 
   format required by `parseFile.py`

2. The next step is to parse the REMAKR 280 lines to extract chemical conditions.
   `>cd Parse`
   `>pipenv --python 2`
   `>pipenv run python parseFile.py "../db/r280db.txt" > parsereport.txt`
   This generates a number of files in the Parse folder:
   * `parsereport.txt` has various reports on the parsed chemicals and quality of parsing
   * `output/cond_resolved_out.xml` lists each well and its conditions
   * `output/chem_list.xml` lists all chems found
   * `output/chemfreq_resolved_out.xml` lists the frequency of all chems found
   * `output/chem_alia.xml` lists aliases used if any
   
3. We now convert the parsed xml to a dictionary, and also save a list of all
   parsed, non empty pdb codes for later use.
   `>cd ..`
   `>python make_chems_dict.py`
   This generates two files in the db folder:
   * `chems_dict.pkl` is a dictionary of wells with format `{pdb code : list of conditions}`
   * `nonempty_pdbcodes.pkl` is a list of all pdb codes with non empty chemical resevoirs

## Running BLAST
At this step we generate a list of all pdb codes which
* have non empty chemicals
* were succesfully blasted
as well as a dictionary containing numpy arrays with the fromat `{pdb code : blast results}`
`>python make_blast_dict.py`

## C6

## PEGeq
To calculate the PEGeq slope and intercept, and visualise it:
`>python pegeq.py`