#!/bin/bash
#
# exlude all __MACOSX__ files by matching if being with _
# exclude all . files (e.g. .git)
# exclude all .zip files
zip -r grader.zip . -x .\* -x _\* -x \*.zip -x zip.sh -x calculator.py
