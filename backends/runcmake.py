import os
import subprocess
os.environ["CC"]="C:\Program Files (x86)\Intel\Composer XE 2013\bin\intel64\icl.exe"
os.environ["CXX"]="C:\Program Files (x86)\Intel\Composer XE 2013\bin\intel64\icl.exe"
os.system("cmake-gui .")
os.system("pause")