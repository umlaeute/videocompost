import os

user = "vc"
group = "vc"
basedir = "/home/%s" % user
configdir = os.path.join (basedir, "config")
infilename = os.path.join (basedir, "infile.raw")
chunkdir = os.path.join (basedir, "chunks")
bindir = os.path.join (basedir, "bin")

if __name__ == "__main__":
    pass
