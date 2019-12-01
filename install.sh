#!/bin/sh

platform='unknown'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
	pyVersion=`which python3`
	if [ -z "$pyVersion" ]; then
		sudo apt-get update ; sudo apt-get install python3.6 ;
	fi
	pipVersion=`which pip`
	if [ -z "$pipVersion" ]; then
		sudo apt-get update ; sudo apt-get install python3-pip ;
	fi
#	pip install random;
#	pip install heapq;
elif [[ "$unamestr" == 'Darwin' ]]; then
	pyVersion=`which python3`
	if [ -z "$pyVersion" ]; then
		brew install python3;
	fi
#	CFLAGS=-I$(brew --prefix)/include LDFLAGS=-L$(brew --prefix)/lib pip install random;
#	CFLAGS=-I$(brew --prefix)/include LDFLAGS=-L$(brew --prefix)/lib pip install heapq;
elif [[ "$unamestr" == 'WindowsNT' ]]; then
	echo "You are on your own here";
	echo "install python3 and pip";
fi
