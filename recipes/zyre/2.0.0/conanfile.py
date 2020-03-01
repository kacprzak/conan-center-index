from conans import ConanFile, CMake, tools
from sys import platform
from packaging import version
import re
import os


class ZyreConan(ConanFile):
    name = "zyre"
    version = "2.0.0"
    license = "MPL-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/zeromq/zyre"
    description = "Local Area Clustering for Peer-to-Peer Applications."
    topics = ("conan", "zyre", "czmq", "zmq", "zeromq",
              "message-queue", "asynchronous")
    exports_sources = ['CMakeLists.txt', 'Findzyre.cmake']
    settings = "os", "compiler", "build_type", "arch"
    requires = "zeromq/4.3.2", "czmq/4.2.0"
    options = {
        "shared": [True],
        "fPIC": [True, False],
        "drafts": [True, False],
    }
    default_options = {
        "shared": True,
        "*:shared": True,
        "fPIC": True,
        "drafts": False,
    }
    generators = ["cmake"]
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def build_requirements(self):
        if not tools.which("ninja") and \
                self.settings.compiler == 'Visual Studio':
            self.build_requires.add('ninja/1.9.0')

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        generator = 'Ninja' if self.settings.compiler == "Visual Studio" \
            else None
        cmake = CMake(self, generator=generator)
        cmake.definitions["ENABLE_DRAFTS"] = self.options.drafts
        cmake.configure(build_dir=self._build_subfolder)
        return cmake

    def build(self):
        tools.replace_in_file(os.path.join(
            self._source_subfolder, "CMakeLists.txt"), "enable_testing()", '')
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy('Findzyre.cmake')
        self.copy(pattern="LICENSE", src=self._source_subfolder,
                  dst='licenses')
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        if self.settings.compiler == 'Visual Studio':
            self.cpp_info.libs = ['zyre']
        else:
            self.cpp_info.libs = ['zyre']
