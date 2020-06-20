# -*- coding: utf-8 -*-
import os
from conans import ConanFile


class DefaultNameConan(ConanFile):
    settings = "os"

    def test(self):
        self.run("builder --version", run_environment=True)
