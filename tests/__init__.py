#!/usr/bin/python3
# -*- coding: utf-8 -*-

__all__ = []

import unittest
from argparse import Namespace
from pathlib import Path

from manga_py.img2pdf import image2pdf


class TestCreatePdf(unittest.TestCase):
    kwargs = None
    _output = None
    _pdf_one = None
    _pdf_two = None

    @classmethod
    def setUpClass(cls):
        cls.kwargs = {
            'path': 'tests/images',
            'delete_original_archives': False,
            'delete_original_directories': False,
            'rewrite_exist_pdf': False,
            'dont_include_directories': True,
            'archives_extension': 'zip',
            'output_directory': 'tests/output',
        }
        cls._output = cls.kwargs.get('output_directory', 'output')
        cls._pdf_one = Path(cls._output).joinpath('test_directory.pdf')
        cls._pdf_two = Path(cls._output).joinpath('test_archive.pdf')

    @classmethod
    def tearDownClass(cls):
        cls._pdf_one.is_file() and cls._pdf_one.unlink()
        cls._pdf_two.is_file() and cls._pdf_two.unlink()

    def img2pdf_arguments(self) -> Namespace:
        return Namespace(
            **self.kwargs
        )

    def prepare(self, **kwargs):
        self.kwargs.update(kwargs)
        image2pdf.arguments = self.img2pdf_arguments

    def test_make_pdf(self):
        self.prepare()

        image2pdf.main()

        self.assertGreater(self._pdf_one.stat().st_size, 1024)
        self.assertGreater(self._pdf_two.stat().st_size, 1024)

        self.assertAlmostEqual(self._pdf_one.stat().st_size, self._pdf_two.stat().st_size, delta=10)
