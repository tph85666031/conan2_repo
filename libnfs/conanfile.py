import os

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import get


class libnfsRecipe(ConanFile):
    name = "libnfs"
    version = "6.0.2"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    options = {"shared": [True, False],
               "fPIC": [True, False]}

    default_options = {"shared": False,
                       "fPIC": True}

    generators = "CMakeDeps"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def source(self):
        # Please, be aware that using the head of the branch instead of an immutable tag
        # or commit is not a good practice in general
        get(self, "https://github.com/tph85666031/libnfs/archive/refs/tags/6.0.2.tar.gz", strip_root=True)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["ENABLE_TESTS"] = False
        tc.variables["ENABLE_DOCUMENTATION"] = False
        tc.variables["ENABLE_UTILS"] = False
        tc.variables["ENABLE_EXAMPLES"] = False
        tc.variables["ENABLE_MULTITHREADING"] = True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["nfs"]
