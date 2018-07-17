rm *.dat
rm *.q
rm newMeta0.m
rm finalMeta0.m
rm ignoreLines.txt

python 0_removeWarmup.py
python 0_fixAnomalies.py
python 1_getMetadata.py
python 2_findStreak.py
python 3_findChain.py
python 4_correlate.py
python 5_getPartners.py
