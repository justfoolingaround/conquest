import sys
import platform
import ctypes
import pathlib


machine = platform.machine()
sys_platform = sys.platform


if sys.platform == "darwin":
    if machine == "arm64":
        file_ext = "-arm64.dylib"
    else:
        file_ext = "-x86.dylib"

else:
    if sys.platform in ("win32", "cygwin"):
        is_64bit = sys.maxsize > 2**32

        if is_64bit:
            file_ext = "-64.dll"
        else:
            file_ext = "-32.dll"

    else:
        if machine == "aarch64":
            file_ext = "-arm64.so"
        else:
            if "x86" in machine:
                file_ext = "-x86.so"
            else:
                file_ext = "-amd64.so"


library = pathlib.Path(__file__).resolve() / ("../dependencies/tls-client" + file_ext)

if not library.exists():
    raise FileNotFoundError(f"Could not find the library file for your platform.")

c_lib = ctypes.cdll.LoadLibrary(library.as_posix())

request = c_lib.request
request.argtypes = [ctypes.c_char_p]
request.restype = ctypes.c_char_p

freeMemory = c_lib.freeMemory
freeMemory.argtypes = [ctypes.c_char_p]
freeMemory.restype = ctypes.c_char_p
