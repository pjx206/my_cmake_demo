# 将子项目作为动态库使用

使用场景：

在Windows上，我们有一份源码用于生成dll和dll对应的lib文件，我们希望这份源码作为子项目，融入到当前目录进行编译。

文件结构：

```纯文本
cmake-shared-demo
 ├── CMakeLists.txt
 ├── main.cpp
 └── shared
     ├── CMakeLists.txt
     ├── dll.c
     └── include
         └── dll.h
```



我们想要将main.cpp编译成exe，shared目录下的源码编译成dll和lib，将lib连接到顶层CMakeLists.txt中的项目。

大致过程如下：

```Mermaid
flowchart LR
  main.cpp --> main.obj
  dll.c --> dll.obj--> shared_module.lib & shared_module.dll
  main.obj & shared_module.lib --> link --> Demo.exe
  Demo.exe & shared_module.dll --> run:::runclass
  classDef runclass fill:#9f6

```



