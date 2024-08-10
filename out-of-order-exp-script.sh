#REF_COUNT
${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/FS_MESI/medium/1/huron-ref-count configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-ref-count" --options="18" > ref-count-repair-ooo-micro-semode-topology.log 2>&1
${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/FS_MESI/medium/1/huron-ref-count configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-ref-count" --options="18" > ref-count-repair-inorder-micro-semode-topology.log 2>&1

${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/MESI_Nonblocking/medium/1/huron-ref-count configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-ref-count" --options="18" > ref-count-baseline-ooo-micro-semode-topology.log 2>&1
${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/MESI_Nonblocking/medium/1/huron-ref-count configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-ref-count" --options="18" > ref-count-baseline-inorder-micro-semode-topology.log 2>&1

#LINEAR_REG
${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/MESI_Nonblocking/large/1/huron-linear-reg configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-linear-reg" --options="${MICRO_BENCH}/bench_input/huron/linear_reg/key_file_8MB.txt" > linear-reg-baseline-ooo-micro-semode-topology.log 2>&1
${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/MESI_Nonblocking/large/1/huron-linear-reg configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-linear-reg" --options="${MICRO_BENCH}/bench_input/huron/linear_reg/key_file_8MB.txt" > linear-reg-baseline-inorder-micro-semode-topology.log 2>&1

${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/FS_MESI/large/1/huron-linear-reg configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-linear-reg" --options="${MICRO_BENCH}/bench_input/huron/linear_reg/key_file_8MB.txt" > linear-reg-repair-ooo-micro-semode-topology.log 2>&1
${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/FS_MESI/large/1/huron-linear-reg configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-linear-reg" --options="${MICRO_BENCH}/bench_input/huron/linear_reg/key_file_8MB.txt" > linear-reg-repair-inorder-micro-semode-topology.log 2>&1

#STRING_MATCH
${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/MESI_Nonblocking/large/1/huron-string-match configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-string-match" --options="${MICRO_BENCH}/bench_input/huron/linear_reg/key_file_8MB.txt" > string-match-baseline-ooo-micro-semode-topology.log 2>&1
${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/MESI_Nonblocking/large/1/huron-string-match configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-string-match" --options="${MICRO_BENCH}/bench_input/huron/linear_reg/key_file_8MB.txt" > string-match-baseline-inorder-micro-semode-topology.log 2>&1

${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/FS_MESI/large/1/huron-string-match configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-string-match" --options="${MICRO_BENCH}/bench_input/huron/linear_reg/key_file_8MB.txt" > string-match-repair-ooo-micro-semode-topology.log 2>&1
${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/FS_MESI/large/1/huron-string-match configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-string-match" --options="${MICRO_BENCH}/bench_input/huron/linear_reg/key_file_8MB.txt" > string-match-repair-inorder-micro-semode-topology.log 2>&1

#LOCKLESS_TOY
${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/FS_MESI/small/1/huron-lockless-toy configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-lockless-toy" --options="16" > lockless-repair-ooo-micro-semode-topology.log 2>&1
${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/FS_MESI/small/1/huron-lockless-toy configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-lockless-toy" --options="16" > lockless-repair-inorder-micro-semode-topology.log 2>&1

${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/MESI_Nonblocking/small/1/huron-lockless-toy configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-lockless-toy" --options="16" > lockless-toy-baseline-ooo-micro-semode-topology.log.log 2>&1
${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/MESI_Nonblocking/small/1/huron-lockless-toy configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-lockless-toy" --options="16" > lockless-toy-baseline-inorder-micro-semode-topology.log.log 2>&1

#LOCKED_TOY
${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/FS_MESI/medium/1/huron-locked-toy configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-locked-toy" --options="18" > locked-toy-repair-ooo-micro-semode-topology.log 2>&1
${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/FS_MESI/medium/1/huron-locked-toy configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-locked-toy" --options="18" > locked-toy-repair-inorder-micro-semode-topology.log 2>&1

${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/MESI_Nonblocking/medium/1/huron-locked-toy configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-locked-toy" --options="18" > locked-toy-baseline-ooo-micro-semode-topology.log 2>&1
${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/MESI_Nonblocking/medium/1/huron-locked-toy configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-locked-toy" --options="18" > locked-toy-baseline-inorder-micro-semode-topology.log 2>&1

#BOOST_SPINLOCK
${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/FS_MESI/small/1/huron-boost-spinlock configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-boost-spinlock" --options="10000" > boost-spinlock-repair-ooo-micro-semode-topology.log 2>&1
${MICRO_GEM5}/build/X86_FS_MESI/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/FS_MESI/small/1/huron-boost-spinlock configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-boost-spinlock" --options="10000" > boost-spinlock-repair-inorder-micro-semode-topology.log 2>&1

${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-o3/MESI_Nonblocking/small/1/huron-boost-spinlock configs/example/se.py --ruby --cpu-type=DerivO3CPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-boost-spinlock" --options="10000" > boost-spinlock-baseline-ooo-micro-semode-topology.log 2>&1
${MICRO_GEM5}/build/X86_MESI_Nonblocking/gem5.opt  --outdir=${MICRO_OUT}/micro-se-inorder/MESI_Nonblocking/small/1/huron-boost-spinlock configs/example/se.py --ruby --cpu-type=TimingSimpleCPU --mem-size=3GB --num-cpus=8 --cacheline_size=64 --l1d_assoc=8 --l1i_assoc=8 --l1d_size=32kB --l1i_size=32kB  --l2_assoc=16 --l2_size=2MB --num_l2caches=8 --tracking_width=1 --inv_threshold=16 --fetch_threshold=16 --global_act_size=128 --assoc_act=16 --size_own=512 --reset_tick=10000 --sys-clock=2GHz --cpu-clock=3GHz --router-latency=4 --link-latency=1 --topology=Ring --cmd="${MICRO_BENCH}/build/bin/huron-boost-spinlock" --options="10000" > boost-spinlock-baseline-inorder-micro-semode-topology.log 2>&1
