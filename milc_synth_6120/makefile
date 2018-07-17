MPIPFLAGS= -L/global/u2/i/indrayud/milc/spack-develop/opt/spack/cray-CNL-haswell/gcc-4.9.3/libunwind-1.1-ifr2bxvmo7nv7ndfayoqjeu6fc2vkfyr/lib -L/global/u2/i/indrayud/milc/mpiP-3.4.1/lib -I/global/u2/i/indrayud/milc/spack-develop/opt/spack/cray-CNL-haswell/gcc-4.9.3/libunwind-1.1-ifr2bxvmo7nv7ndfayoqjeu6fc2vkfyr/include -L/global/u2/i/indrayud/milc/spack-develop/opt/spack/cray-CNL-haswell/gcc-4.9.3/libelf-0.8.13-vuty53dga3upuqyn4wik3pphayalpdet/lib -L/global/u2/i/indrayud/milc/spack-develop/opt/spack/cray-CNL-haswell/gcc-4.9.3/libdwarf-20160507-fcrpm5sqp7efbxsc2uskogtjameq54v3/lib -Wl,-Bstatic -ldwarf -Wl, -Bdynamic -lmpiP -lm -lelf -lunwind -lbfd -liberty -lunwind-x86_64 -lz -dynamic -llzma

ARIESFLAGS= -I/global/homes/i/indrayud/org/ariesncl/ -L/global/homes/i/indrayud/org/ariesncl/libariesncl.a -ldl

syn:
	cc -O3 -g -o milc_synth milc_synth_6120.c ${ARIESFLAGS} ${MPIPFLAGS} 

clean:
	rm -f milc_synth ending.log
