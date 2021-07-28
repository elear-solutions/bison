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
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "bison-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    @contextmanager
    def _build_context(self):
        yield

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        self._autotools = AutoToolsBuildEnvironment(self)
        args = [
            "--enable-relocatable",
            "--disable-nls",
            "--datarootdir={}".format(os.path.join(self.package_folder, "bin", "share").replace("\\", "/")),
        ]
        host, build = None, None
        self._autotools.configure(args=args, configure_dir= "..", host=host, build=build)
        return self._autotools

    def build(self):
        with self._build_context():
            env_build = self._configure_autotools()
            env_build.make()

    def package(self):
        with self._build_context():
            env_build = self._configure_autotools()
            env_build.install()
            self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = ["y"]

        self.output.info('Setting BISON_ROOT environment variable: {}'.format(self.package_folder))
        self.env_info.BISON_ROOT = self.package_folder.replace("\\", "/")

        bindir = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: {}'.format(bindir))
        self.env_info.PATH.append(bindir)
        pkgdir = os.path.join(bindir, 'share', 'bison')
        self.output.info('Setting the BISON_PKGDATADIR environment variable: {}'.format(pkgdir))
        self.env_info.BISON_PKGDATADIR = pkgdir

        # yacc is a shell script, so requires a shell (such as bash)
        self.user_info.YACC = os.path.join(self.package_folder, "bin", "yacc").replace("\\", "/")
