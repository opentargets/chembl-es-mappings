#!/bin/bash

oldRelease="27"
newRelease="28"

indexes=(drug_indication mechanism molecule target)

for idx in "${indexes[@]}"
do
    echo "Index $idx"
    diff --side-by-side --suppress-common-lines \
        chembl_${oldRelease}_${idx}_structure.json \
        chembl_${newRelease}_${idx}_structure.json
done

