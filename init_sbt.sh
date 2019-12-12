#!/bin/bash

if [[ $# -eq 0 ]]; then
	echo "Provide Scala project name: \`$0 myProject\`"
	exit 1
fi

proj_name=$1

mkdir $proj_name
cd $proj_name

mkdir -p src/{main,test}/{java,resources,scala}
mkdir lib project target

echo "name := \"$proj_name\"
version := \"1.0\"
scalaVersion := \"2.11.12\"" > build.sbt