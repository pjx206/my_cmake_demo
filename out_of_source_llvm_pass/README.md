# Out of source LLVM Pass

Tested on Linux.


[llvm documentation](https://llvm.org/docs/CMake.html#cmake-out-of-source-pass)

```bash
cmake -GNinja -B build .
cmake --build ./build --target all
clang -flegacy-pass-manager -Xclang -load -Xclang ./build/HelloWorld/HelloWorld.so a.c
```

The output will be:

```bash
Hello: main
```