import os
import stat
import shutil
from conans import ConanFile, tools
import subprocess

class InstallBuilderConan(ConanFile):
    name = "installbuilder"
    # version = '20.4.0'
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
        if self.settings.os == 'Macos':
            try:
                tools.mkdir('mnt')
                subprocess.check_call([
                    '/usr/bin/hdiutil', 'attach', os.path.join(self.source_folder, self._main_download),
                    '-readonly',
                    # '-verbose',
                    '-mountpoint', os.path.join(self.build_folder, 'mnt')
                ])
                subprocess.check_call([
                    os.path.join('mnt', f'installbuilder-qt-professional-{self.version}-osx-installer.app','Contents','MacOS','osx-x86_64'),
                    # os.path.join('mnt', f'installbuilder-qt-professional-21.6.0-osx-installer.app','Contents','MacOS','osx-x86_64'),
                    '--mode', 'unattended',
                    '--prefix', 'inst', 
                ])
            finally:
                subprocess.check_call([
                    '/usr/bin/hdiutil', 'detach', os.path.join(self.build_folder, 'mnt'),
                    # '-verbose',
                    '-force',
                ])
        else:
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
        if self.settings.os == 'Macos':
            tools.rmdir(os.path.join(self.package_folder, "uninstall.app"))

        # tools.remove_files_by_mask(self.package_folder, 'uninstall*')
        # tools.remove_files_by_mask(self.package_folder, '*.desktop')

    def package_info(self):
        bin_path = os.path.join(self.package_folder, 'bin')
        self.output.info('Appending PATH environment variable: %s' % bin_path)
        self.env_info.PATH.append(bin_path)
        autoupdate_bin_path = os.path.join(self.package_folder, 'autoupdate', 'bin')
        self.output.info('Appending PATH environment variable: %s' % autoupdate_bin_path)
        self.env_info.PATH.append(autoupdate_bin_path)

        if self.settings.os != 'Macos':
            cdrtools_bin_path = os.path.join(self.package_folder, 'tools', 'cdrtools','bin')
            self.output.info('Appending PATH environment variable: %s' % cdrtools_bin_path)
            self.env_info.PATH.append(cdrtools_bin_path)
            dmg_bin_path = os.path.join(self.package_folder, 'tools', 'libdmg-hfsplus','bin')
            self.output.info('Appending PATH environment variable: %s' % dmg_bin_path)
            self.env_info.PATH.append(dmg_bin_path)

        osslsigncode_bin_path = os.path.join(self.package_folder, 'tools', 'osslsigncode','bin')
        self.output.info('Appending PATH environment variable: %s' % osslsigncode_bin_path)
        self.env_info.PATH.append(osslsigncode_bin_path)
        if self.settings.os == 'Macos':
            code_signing_bin_path = os.path.join(self.package_folder, 'tools', 'code-signing','bin')
            self.output.info('Appending PATH environment variable: %s' % code_signing_bin_path)
            self.env_info.PATH.append(code_signing_bin_path)

    def package_id(self):
        if self.settings.os == "Macos":
            del self.info.settings.os.version
