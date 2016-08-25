from setuptools import setup, find_packages

setup(
    name="ts-python",
    version="0.1.0",
    author="Zachary W. Graham",
    description="A library for interacting with TS-7250-v2\
        hardware features.",
    license="BSD",
    packages=find_packages(exclude=["test"]),
    platforms=["Linux"],
    install_requires=[
        "pyserial >= 2.7",
        "cffi>=1.2.1"
    ],
    setup_requires=['cffi>=1.2.1'], #'pycparser >= 2.14']
    extras_require={
        "develop": ["mock >= 1.3.0", "nose >= 1.3.7"]
    },
    cffi_modules=["ts7250v2/_mmio.py:ffi"]
)
