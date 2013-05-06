SET INCLUDES= -I ../../common ../../fuzztreeconfiguration ../../simulation 
SET OPTIONS= --enable=style --suppress=duplicateBranch -q ../../common ../../fuzztreeconfiguration ../../simulation
cppcheck %INCLUDES% %OPTIONS% 2> errors.txt