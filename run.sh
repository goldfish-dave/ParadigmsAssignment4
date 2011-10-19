#!/bin/bash
BUILD_DIR=build
ANTLR_DIR=antlr-3.1.3

ANTLR_JAR=${ANTLR_DIR}/lib/antlr-3.1.3.jar
ANTLR_PY=${ANTLR_DIR}/runtime/Python

rm -rf ${BUILD_DIR}
mkdir -p ${BUILD_DIR}
touch ${BUILD_DIR}/__init__.py
java -cp ${ANTLR_JAR} org.antlr.Tool -o ${BUILD_DIR} Jump.g

PYTHONPATH=${ANTLR_JAR}:. python run.py ${1}
