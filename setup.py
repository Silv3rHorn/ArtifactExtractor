from distutils.core import setup
from glob import glob
import py2exe
import sys

sys.path.append("D:\\Dropbox\\git\\msvcr90")
data_files = [("Microsoft.VC90.CRT", glob(r'D:\Dropbox\git\msvcr90\*.*'))]

setup(
    console=['artifact_extractor.py'],
    data_files=data_files
)
