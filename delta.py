#!/bin/bash

cp wireworld-original.c wireworld-original.c.bak

for patch_number in "$@"; do
    patch wireworld-original.c < "patch.$patch_number"
done

gcc -c wireworld-original.c

if [ $? -ne 0 ]; then
    echo "Patch induced a failure."
    result=1
else
    echo "Patch did not induce a failure."
    result=0
fi

mv wireworld-original.c.bak wireworld-original.c

exit $result
