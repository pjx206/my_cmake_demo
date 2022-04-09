# Demo: Use Cython

This demo project shows how do we use CMake to build cython modules, 
which is built from cython generated C source.

Thanks to Qt, I modified the `pyside_config.py` file from an official sample project of PySide6.
Now we can use our `py_config.py` to get Python's include directory and link libraries.