import os
from collections import namedtuple

DBInfos = namedtuple('infos', 'dbname dbpath dbfile')

class NazeDB:
    def __init__(self, dbname=None):
        self.root = os.getcwd()
        self.dbname = dbname
        self.dbfile = None
        self.dbpath = None
        if dbname is None:
            return
        for parent, dirnames, filenames in os.walk(self.root):
            for dirname in dirnames:
                if dirname == dbname:
                    return
        os.makedirs(dbname)

    def open(self, dbname):
        for parent, dirnames, filenames in os.walk(self.root):
            for dirname in dirnames:
                if dirname == dbname:
                    self.dbname = dbname
                    os.chdir(os.path.join(parent, dbname))
                    return
        os.makedirs(dbname)
        self.dbname = dbname
        os.chdir(os.path.join(self.root, dbname))

    @property
    def dbinfos(self) -> DBInfos:
        if self.dbname is None:
            return
        for parent, dirnames, filenames in os.walk(self.root):
            for dirname in dirnames:
                if dirname == self.dbname:
                    dbpath = os.path.join(parent, dirname)
                    self.dbfile = ".index.db"
                    self.dbpath = "." + dbpath[len(self.root): ]
                    return DBInfos._make([self.dbname, self.dbpath, self.dbfile])

    @staticmethod
    def listdb() -> [DBInfos]:
        root = os.getcwd()
        res = []
        for parent, dirnames, filenames in os.walk(root):
            for dirname in dirnames:
                rootdir = os.path.join(parent, dirname)
                if os.path.exists(os.path.join(rootdir, '.index.db')):
                    dbpath = "." + rootdir[len(root): ]
                    res.append(DBInfos._make([dirname, dbpath, '.index.db']))
        return res




