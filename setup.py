try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from distutils.extension import Extension
from xml.etree.ElementInclude import include
from Cython.Build import cythonize
from torch.utils.cpp_extension import BuildExtension
import numpy

# Get the numpy include directory.
numpy_include_dir = numpy.get_include()

# simplify (efficient mesh simplification)
simplify_mesh_module = Extension(
    'utils.libsimplify.simplify_mesh',
    sources=[
        'utils/libsimplify/simplify_mesh.pyx'
    ],
    include_dirs=[numpy_include_dir]
)

# Gather all extension modules
ext_modules = [
    simplify_mesh_module,
]

setup(
    ext_modules=cythonize(ext_modules),
    cmdclass={
        'build_ext': BuildExtension
    }
)
