from conans import ConanFile, AutoToolsBuildEnvironment, tools
from contextlib import contextmanager
import os


class BisonLibConan(ConanFile):
    name = "bison"
    version = "0.0.1"
    url = "https://github.com/elear-solutions/bison"
    homepage = "https://www.gnu.org/software/bison/"
    description = "Bison is a general-purpose parser generator"
    topics = ("conan", "bison", "parser")
    license = "GPL-3.0-or-later"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "fPIC": [True, False],
    }
    default_options = {
        "fPIC": True,
    }

    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        extracted_dir = "bison"
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        self._autotools = AutoToolsBuildEnvironment(self)
        self._autotools.configure(configure_dir= "..")
        return self._autotools

    def build(self):
        self.run("cd .. && touch aclocal.m4 Makefile.am configure Makefile.in")
        env_build = self._configure_autotools()
        env_build.make()

    def package(self):
        env_build = self._configure_autotools()
        env_build.install()

    def package_info(self):
        self.cpp_info.libs = ["y"]

