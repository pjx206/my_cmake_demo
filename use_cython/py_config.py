import sysconfig
import os
import sys
import re

python_link_error = 'Unable to locate the Python library for linking.'
python_include_error = 'Unable to locate the Python include headers directory.'

options = []

# option, function, error, description
options.append(("--python-include-path",
                lambda: get_python_include_path(),
                python_include_error,
                "Print Python include path"))

options.append(("--python-link-flags-cmake", lambda: python_link_flags_cmake(), python_link_error,
                "Print python link flags for cmake"))

options_usage = ''
for i, (flag, _, _, description) in enumerate(options):
    options_usage += f'    {flag:<45} {description}'
    if i < len(options) - 1:
        options_usage += '\n'

usage = f"""
Utility to determine include/link options of shiboken/PySide and Python for qmake/CMake projects
that would like to embed or build custom shiboken/PySide bindings.

Usage: py_config.py [option]
Options:
{options_usage}
    -a                                            Print all options and their values
    --help/-h                                     Print this help
"""

option = sys.argv[1] if len(sys.argv) == 2 else '-a'
if option == '-h' or option == '--help':
    print(usage)
    sys.exit(0)


def is_debug():
    debug_suffix = '_d.pyd' if sys.platform == 'win32' else '_d.so'
    return any([s.endswith(debug_suffix) for s in import_suffixes()])

def import_suffixes():
    import importlib.machinery
    return importlib.machinery.EXTENSION_SUFFIXES

def python_version():
    return str(sys.version_info[0]) + '.' + str(sys.version_info[1])

def get_python_include_path():
    return sysconfig.get_path('include')

def python_link_data():
    # @TODO Fix to work with static builds of Python
    libdir = sysconfig.get_config_var('LIBDIR')
    if libdir is None:
        libdir = os.path.abspath(os.path.join(
            sysconfig.get_config_var('LIBDEST'), "..", "libs"))
    version = python_version()
    version_no_dots = version.replace('.', '')

    flags = {}
    flags['libdir'] = libdir
    if sys.platform == 'win32':
        suffix = '_d' if is_debug() else ''
        flags['lib'] = f'python{version_no_dots}{suffix}'

    elif sys.platform == 'darwin':
        flags['lib'] = f'python{version}'

    # Linux and anything else
    else:
        flags['lib'] = f'python{version}{sys.abiflags}'

    return flags


def python_link_flags_cmake():
    flags = python_link_data()
    libdir = flags['libdir']
    lib = re.sub(r'.dll$', '.lib', flags['lib'])
    return f'{libdir};{lib}'


print_all = option == "-a"
for argument, handler, error, _ in options:
    if option == argument or print_all:
        handler_result = handler()
        if handler_result is None:
            sys.exit(error)

        line = handler_result
        if print_all:
            line = f"{argument:<40}: {line}"
        print(line)
