import os
import stat
import shutil
from conans import ConanFile, tools
import subprocess

class InstallBuilderConan(ConanFile):
    name = "installbuilder"
    version = '20.4.0'
    url = "https://installbuilder.com"
    homepage = "https://installbuilder.com"
    description = "A powerful and easy to use cross platform installer creation tool"
    license = "Proprietary"
    settings = "os"
    topics = ("installer")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _main_download(self):
        return self.conan_data["sources"][self.version][str(self.settings.os)]['filename']

    def source(self):
        tools.download(**self.conan_data["sources"][self.version][str(self.settings.os)])
        if self.settings.os == 'Linux':
            st = os.stat(self._main_download)
            os.chmod(self._main_download, st.st_mode | stat.S_IEXEC)

    def build(self):
        subprocess.check_call([
            os.path.join(self.source_folder, self._main_download),
            '--mode', 'unattended',
            '--prefix', 'inst', 
        ])

    def package(self):
        self.copy("*", src='inst')
        tools.rmdir(os.path.join(self.package_folder, "demo"))
        tools.rmdir(os.path.join(self.package_folder, "docs"))
        tools.rmdir(os.path.join(self.package_folder, "projects"))
        tools.rmdir(os.path.join(self.package_folder, "projects"))
        # tools.remove_files_by_mask(self.package_folder, 'uninstall*')
        # tools.remove_files_by_mask(self.package_folder, '*.desktop')

    def package_info(self):
        bin_path = os.path.join(self.package_folder, 'bin')
        self.output.info('Appending PATH environment variable: %s' % bin_path)
        self.env_info.PATH.append(bin_path)
        cdrtools_bin_path = os.path.join(self.package_folder, 'tools', 'cdrtools','bin')
        self.output.info('Appending PATH environment variable: %s' % cdrtools_bin_path)
        self.env_info.PATH.append(cdrtools_bin_path)
        dmg_bin_path = os.path.join(self.package_folder, 'tools', 'libdmg-hfsplus','bin')
        self.output.info('Appending PATH environment variable: %s' % dmg_bin_path)
        self.env_info.PATH.append(dmg_bin_path)
        osslsigncode_bin_path = os.path.join(self.package_folder, 'tools', 'osslsigncode','bin')
        self.output.info('Appending PATH environment variable: %s' % osslsigncode_bin_path)
        self.env_info.PATH.append(osslsigncode_bin_path)
