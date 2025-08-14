import os

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import get


class libsmb2Recipe(ConanFile):
    name = "libsmb2"
    version = "6.2"

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
        get(self, "https://github.com/sahlberg/libsmb2/archive/refs/tags/libsmb2-6.2.tar.gz", strip_root=True)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["ESP_PLATFORM"] = False
        tc.variables["ENABLE_EXAMPLES"] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["smb2"]
