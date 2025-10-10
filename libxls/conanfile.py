from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rm, rmdir, save
from conan.tools.files import copy, get, rmdir, rm
from conan.tools.microsoft import is_msvc
from conan.tools.apple import is_apple_os
from conan.tools.scm import Version

import os

required_conan_version = ">=1.54.0"


class LibxlsConan(ConanFile):
    name = "libxls"
    description = "a C library which can read Excel (xls) files."
    license = "BSD-2-Clause"
    homepage = "https://github.com/libxls/libxls/"
    topics = ("excel", "xls")
    package_type = "library"
    version="1.6.3"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_cli": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_cli": False,
    }

    @property
    def _settings_build(self):
        return getattr(self, "settings_build", self.settings)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        #self.settings.rm_safe("compiler.libcxx")
        #self.settings.rm_safe("compiler.cppstd")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        if not is_apple_os(self):
            self.requires("libiconv/1.17")

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.10 <4]")
    
    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination=self.source_folder, strip_root=True)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def _patch_sources(self):
        config_h_content = """
#define HAVE_ICONV 1
#define ICONV_CONST
#define PACKAGE_VERSION "{}"
""".format(self.version)
        if self.settings.os == "Macos":
            config_h_content += "#define HAVE_XLOCALE_H 1\n"
        save(self, os.path.join(self.source_folder, "src", "export", "config.h"), config_h_content)

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "LICENSE", self.source_folder, os.path.join(self.package_folder, "licenses"))

    def package_info(self):
        self.cpp_info.set_property("pkg_config_name", "libxls")
        self.cpp_info.libs = ["xls"]
        if is_apple_os(self):
            self.cpp_info.system_libs.append("iconv")