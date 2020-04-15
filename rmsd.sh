#!/bin/bash
for i in {1..2}
do
	for j in {1..5}
	do
		cp *pdb s${i}/neutral${j}
		cd s${i}/neutral${j}
		echo 4 | gmx_mpi trjconv -s all.pdb -f all.pdb -o all_backbone.pdb
		echo 4 4 | gmx_mpi rms -s SESE.pdb -f all_backbone.pdb -o rmsdHotLoop.xvg -nomw
		echo 4 4 | gmx_mpi rms -s SESEG4.pdb -f all_backbone.pdb -o rmsdCluster.xvg -nomw
		cd ../../
	done
done
cat s1/neutral1/rmsdHotLoop.xvg s1/neutral2/rmsdHotLoop.xvg s1/neutral3/rmsdHotLoop.xvg s1/neutral4/rmsdHotLoop.xvg s1/neutral5/rmsdHotLoop.xvg > s1rmsdHotLoop.xvg
cat s2/neutral1/rmsdHotLoop.xvg s2/neutral2/rmsdHotLoop.xvg s2/neutral3/rmsdHotLoop.xvg s2/neutral4/rmsdHotLoop.xvg s2/neutral5/rmsdHotLoop.xvg > s2rmsdHotLoop.xvg


cat s1/neutral1/rmsdCluster.xvg s1/neutral2/rmsdCluster.xvg s1/neutral3/rmsdCluster.xvg s1/neutral4/rmsdCluster.xvg s1/neutral5/rmsdCluster.xvg > s1rmsdCluster.xvg
cat s2/neutral1/rmsdCluster.xvg s2/neutral2/rmsdCluster.xvg s2/neutral3/rmsdCluster.xvg s2/neutral4/rmsdCluster.xvg s2/neutral5/rmsdCluster.xvg > s2rmsdCluster.xvg

cat s1/neutral1/result.txt s1/neutral2/result.txt s1/neutral3/result.txt s1/neutral4/result.txt s1/neutral5/result.txt > s1result.txt
cat s2/neutral1/result.txt s2/neutral2/result.txt s2/neutral3/result.txt s2/neutral4/result.txt s2/neutral5/result.txt > s2result.txt

cat s1rmsdHotLoop.xvg s2rmsdHotLoop.xvg > rmsdHotLoop.xvg
cat s1rmsdCluster.xvg s2rmsdCluster.xvg > rmsdCluster.xvg
cat s1result.txt s2result.txt > result.txt
