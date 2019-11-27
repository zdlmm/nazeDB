import os
from nazedb import *
import csv


class NazeTable:
    def __init__(self, tname: str, db: NazeDB):
        root = os.getcwd()
        os.chdir(os.path.join(root, db.dbinfos.dbpath))
        self.db = db
        self.tname = tname + '.csv'
        self.rows = [[]]
        if os.path.exists(self.tname):
            pass
        else:
            f = open('.index.db', 'a', newline='')
            f.write(self.tname + '\n')
            f.close()
            fcsv = open(self.tname, 'wt')
            fcsv.close()
        os.chdir(root)

    def set_header(self, ls: [str]):
        self.rows[0] = ls

    def get_header(self) -> [str]:
        return self.rows[0]

    @property
    def filepath(self) -> str:
        return os.path.join(self.db.dbinfos.dbpath, self.tname)

    @property
    def get_rows(self) -> [[str]]:
        return self.rows

    def add_row(self, **kw):
        Row = namedtuple('Row', self.get_header())
        self.rows.append(Row(**kw))

    def add_row_list(self, list: [str]):
        self.rows.append(list)

    def save(self):
        root = os.getcwd()
        os.chdir(os.path.join(root, self.db.dbinfos.dbpath))
        f = open(self.tname, 'wt', newline='')
        f_csv_w = csv.writer(f)
        f_csv_w.writerows(self.rows)
        f.close()
        os.chdir(root)

    def load(self):
        rs = [[]]
        root = os.getcwd()
        os.chdir(os.path.join(root, self.db.dbinfos.dbpath))
        with open(self.tname) as f:
            f_csv = csv.reader(f)
            for r in f_csv:
                rs.append(r)
        self.rows = rs
        f.close()
        for row in self.rows:
            if len(row) == 0:
                self.rows.remove(row)
        os.chdir(root)

    def clean(self):
        root = os.getcwd()
        os.chdir(os.path.join(root, self.db.dbinfos.dbpath))
        os.remove(self.tname)
        f = open('.index.db', 'r+')
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != self.tname + '\n':
                f.write(i)
        f.truncate()
        f.close()
        os.chdir(root)

    @staticmethod
    def cleanall(dbinfos: DBInfos):
        root = os.getcwd()
        os.chdir(os.path.join(root, dbinfos.dbpath))
        for file in os.listdir(os.path.join(root, dbinfos.dbpath)):
            os.remove(file)
        f = open('.index.db', 'a')
        f.close()
        os.chdir(root)

