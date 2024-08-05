
echo "arg: workload_name size thres"
echo  "Running experiment with" $1

if [ $1 ];
then 
    python3 src/main.py --tasks run --trials $2 --bench huron-ref-count-manual --verbose 1 --protocol MESI_Nonblocking --workloadSize medium --outputDir micro-manual-fix --benchmark_type custom
    echo "baseline protocol for ref-count completed"
    python3 src/main.py --tasks run --trials $2 --bench huron-linear-reg-manual --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-manual-fix --benchmark_type custom
    echo "baseline protocol for linear-reg completed"
    python3 src/main.py --tasks run --trials $2 --bench huron-string-match-manual --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-manual-fix --benchmark_type custom
    echo "baseline protocol for string-match completed"
    python3 src/main.py --tasks run --trials $2 --bench huron-boost-spinlock-manual --verbose 1 --protocol MESI_Nonblocking --workloadSize small --outputDir micro-manual-fix --benchmark_type custom 
    echo "baseline protocol for boost-spinlock completed"
    python3 src/main.py --tasks run --trials $2 --bench huron-lockless-toy-manual --verbose 1 --protocol MESI_Nonblocking --workloadSize small --outputDir micro-manual-fix --benchmark_type custom 
    echo "baseline protocol for lockless-toy completed"
    python3 src/main.py --tasks run --trials $2 --bench huron-locked-toy-manual --verbose 1 --protocol MESI_Nonblocking --workloadSize medium --outputDir micro-manual-fix --benchmark_type custom
    echo "baseline protocol for locked-toy completed"
    python3 src/main.py --tasks run --trials $2 --bench ESTM-specfriendly-tree-man --verbose 1 --protocol MESI_Nonblocking --workloadSize medium --outputDir micro-manual-fix --benchmark_type custom
    echo "baseline protocol for estm-specfriendly-tree  completed"
    python3 src/main.py --tasks run --trials $2 --bench streammanual --verbose 1 --protocol MESI_Nonblocking --workloadSize large --outputDir micro-manual-fix --benchmark_type parsec
    echo "baseline protocol for streamcluster  completed"
    echo "Baseline protocol run completed for the manual fix"
else
    echo "arg not provided"
fi

cd /home/prospar/prospar-micro-result/micro-manual-fix
mv MESI_Nonblocking MESI_Nonblocking_manual
cd MESI_Nonblocking_manual

for loop in $(seq 1 $2)
do
    mv medium/$loop/huron-ref-count-manual medium/$loop/huron-ref-count
    mv large/$loop/huron-linear-reg-manual large/$loop/huron-linear-reg
    mv large/$loop/huron-string-match-manual large/$loop/huron-string-match
    mv small/$loop/huron-boost-spinlock-manual small/$loop/huron-boost-spinlock
    mv small/$loop/huron-lockless-toy-manual small/$loop/huron-lockless-toy
    mv medium/$loop/huron-locked-toy-manual medium/$loop/huron-locked-toy
    mv medium/$loop/ESTM-specfriendly-tree-man medium/$loop/ESTM-specfriendly-tree
    mv large/$loop/streammanual large/$loop/streamcluster
done
# mv medium/1/huron-ref-count-manual medium/1/huron-ref-count
# mv large/1/huron-linear-reg-manual large/1/huron-linear-reg
# mv large/1/huron-string-match-manual large/1/huron-string-match
# mv small/1/huron-boost-spinlock-manual small/1/huron-boost-spinlock
# mv small/1/huron-lockless-toy-manual small/1/huron-lockless-toy
# mv medium/1/huron-locked-toy-manual medium/1/huron-locked-toy
# mv medium/1/ESTM-specfriendly-tree-man medium/1/ESTM-specfriendly-tree
# mv large/1/streammanual large/1/streamcluster
cd /home/prospar/micro-artifact-framework

