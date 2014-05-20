import sys
from cx_Freeze import setup, Executable

# After running the setup file (python setup.py build) the scrapy/VERSION file has to be manually put into the
# library.zip, also the FourmiCrawler map has to be copied to both the library and the exe.win32-2.7 folder. after
# putting the files in the library the library has to be zipped and replace the old library.
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "scrapy", "lxml", "w3lib", "pkg_resources", "zope.interface"], "excludes": []}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

setup(  name = "Scrapy",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("fourmi.py", base=base)])