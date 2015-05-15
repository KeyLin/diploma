#gcc 8speexenc.c -g -lspeex -o 8enc.exe
#gcc 8speexdec.c -g -lspeex -o 8dec.exe

gcc speexenc.c -g -lspeex -o 16enc.exe
gcc speexdec.c -g -lspeex -o 16dec.exe
