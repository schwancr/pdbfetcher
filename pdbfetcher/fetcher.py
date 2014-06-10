import ftplib
import gzip
import os
import mdtraj

class PDBFetcher(object):
    def __init__(self, temp_dir='.', just_files=False):
        self.temp_dir = temp_dir
        self.just_files = just_files
        self.open()


    def __del__(self):
        self.close()


    def open(self):
        self.conn = ftplib.FTP('ftp.wwpdb.org')
        self.conn.login()


    def close(self):
        self.conn.quit()


    def get(self, pdbid):
        pdbid = pdbid.lower()

        if len(pdbid) != 4:
            raise Exception("pdb id must be four characters long")

        filename = os.path.join(self.temp_dir, '%s.pdb.gz' % pdbid)
        with open(filename, 'wb') as filehandler:
            self.conn.retrbinary('RETR pub/pdb/data/structures/divided/pdb/%s/pdb%s.ent.gz' % (pdbid[1:3], pdbid),
                filehandler.write)

        if self.just_files:
            return filename

        else:
            # then we actually want to load it as a pdb file object and return an mdtraj trajectory
            with gzip.open(filename) as filehandler:
                text = filehandler.read()

            with open(filename[:-3], 'w') as filehandler:
                filehandler.write(text)

            pdb = mdtraj.load_pdb(filename[:-3])

            return pdb
