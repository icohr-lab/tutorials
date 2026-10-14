#!/bin/bash
# Usage: runtests.sh KEY...   Runs blank and solved scripts for each notebook key (e.g. F1 A3 B2).
# Test scripts are read from generator/tests/ (or $NB_TEST); run the generator scripts first.
HERE="$(cd "$(dirname "$0")" && pwd)"
TEST="${NB_TEST:-$HERE/tests}"
mkdir -p "$TEST/run" && cd "$TEST/run" || exit 1
for k in "$@"; do
  for mode in blank solved; do
    f=$TEST/${k}_${mode}.R
    log=$TEST/${k}_${mode}.log
    Rscript -e 'options(warn=1, width=140); source("'$f'", echo=FALSE, print.eval=TRUE)' > $log 2>&1
    code=$?
    errs=$(grep -c -E "^Error" $log)
    bad=$(grep -c "EXPECTED-ERROR-CELL: FALSE" $log)
    pass=$(grep -c "^PASS" $log); notyet=$(grep -c "^NOT YET" $log)
    echo "$k $mode: exit=$code errors=$errs unexpected_non_errors=$bad PASS=$pass NOTYET=$notyet warnings=$(grep -c -i '^Warning' $log)"
    if [ $code -ne 0 ]; then tail -5 $log; fi
  done
done
