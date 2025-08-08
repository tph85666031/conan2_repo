#!/bin/bash

for i in ./*
do
    if test -d $i;then
	    pushd $i
		conan create .
		popd
	fi
done
