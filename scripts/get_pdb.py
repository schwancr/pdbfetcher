
import argparse
from pdbfetcher import PDBFetcher

def main(args):

    fetcher = PDBFetcher(temp_dir=args.temp_dir)
    pdb = fetcher.get('1hv4')

    return pdb


def entry_point():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='temp_dir', default=None,
        help='temporary directory to save PDB files')
    parser.add_argument('-p', dest='pdb_id', help='PDB ID to fetch')
    args = parser.parse_args()
    main(args)
