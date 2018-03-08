#!/bin/sh 
func() { 
	echo ------ this is func -------- 
	echo "This Script Executable File : $0" 
	echo "Argument Count : $#" 
	echo "Process ID : $$" 
	echo "Argument List \$* : $*" 
	echo "Argument List \$@ : $@" 
	echo "Argument 1 : $1" 
	echo "Argument 2 : $2" 
	echo "Argument 3 : $3" 
} 	
echo ------ this is main -------- 
echo "This Script Executable File : $0" 
echo "Argument Count : $#" 
echo "Process ID : $$" 
echo "Argument List \$* : $*" 
echo "Argument List \$@ : $@" 
echo "Argument 1 : $1" 
echo "Argument 2 : $2" 
echo "Argument 3 : $3" 
echo "Argument 4 : $4" 
func aa bb cc dd
