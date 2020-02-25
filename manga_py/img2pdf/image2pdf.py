from argparse import ArgumentParser, Namespace
from pathlib import Path
from logging import warning, error
from zipfile import ZipFile
from PIL import Image
from tempfile import gettempdir
from typing import Tuple, List
from shutil import rmtree

_allowed_file_extensions = [
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.webp',
]


def arguments() -> Namespace:
    _args = ArgumentParser()
    _args.add_argument('path', help="Path to archives directory", type=str,)
    _args.add_argument('-d', '--delete-original-archives', action='store_true',)
    _args.add_argument('-D', '--delete-original-directories', action='store_true',)
    _args.add_argument('-r', '--rewrite-exist-pdf', action='store_true',)
    _args.add_argument('-i', '--dont-include-directories', action='store_false',)
    _args.add_argument('-e', '--archives-extension', default='zip')
    _args.add_argument('-o', '--output-directory', help="Path to created pdf", type=str,)
    return _args.parse_args()


def open_img(path, mode: str = 'r') -> Image.Image:
    return Image.open(str(path), mode)


def ext(arg):
    return '.' + arg.archives_extension


def prepare(arg: Namespace) -> Tuple[List[Path], List[Path], Path]:
    path = Path(arg.path).absolute()
    _with_directories = arg.dont_include_directories

    if not path.exists():
        error('Target directory not exists')
        exit(1)

    archives = [i for i in path.iterdir() if i.name.endswith(ext(arg)) and i.is_file()]
    dirs = [i for i in path.iterdir() if i.is_dir()] if _with_directories else []

    if len(archives) == 0 and len(dirs) == 0:
        error('Target files not found')
        exit(1)

    if arg.output_directory is None:
        output = path
    else:
        output = Path(arg.output_directory).absolute()
        output.mkdir(parents=True, exist_ok=True)

    return archives, dirs, output


def temp_dir():
    temp = Path(gettempdir()).joinpath('.manga-py').joinpath('.img2pdf')

    if temp.exists():
        if not temp.is_dir():
            warning('move temporary target to new destination (is file now)')
            temp.rename(temp.parent.joinpath('.img2pdf.backup'))
        rmtree(str(temp))
        return temp_dir()
    else:
        temp.mkdir(parents=True)

    return temp


def make_pdf(cur_temp: Path, pdf_path: Path):
    images = []
    for img in cur_temp.iterdir():
        if img.is_file() and img.name[img.name.rfind('.'):] in _allowed_file_extensions:
            image = open_img(img)
            if 'RGB' != image.mode:
                image = image.convert(mode='RGB', colors=1 << 14)  # 16k
            images.append(image)

    if len(images) > 0:
        try:
            pdf_image = images[0].copy()
            kwargs = {
                'format': 'PDF',
                'resolution': 100.0,
                'save_all': True,
            }
            if len(images) > 1:
                kwargs.setdefault('append_images', images[1:])
            pdf_image.save(str(pdf_path), **kwargs)
            pdf_image.close()
        except Exception as e:
            warning('%s' % e)
            pdf_path.unlink()
        [i.close() for i in images]


def process_archives(archives: List[Path], output: Path, _ext: str, rewrite: bool, temp: Path, _delete_orig: bool):
    for i, arc in enumerate(archives):
        pdf_name = output.joinpath(arc.name[:-1 * len(_ext)] + '.pdf')
        if not rewrite and Path(pdf_name).is_file():
            continue

        cur_temp = temp.joinpath(str(i))
        cur_temp.mkdir()

        zip_file = ZipFile(str(arc), mode='r')
        zip_file.extractall(cur_temp)

        make_pdf(cur_temp, pdf_name)

        rmtree(str(cur_temp))
        zip_file.close()

        if _delete_orig:
            arc.unlink()


def process_directories(directories: List[Path], output: Path, rewrite: bool, _delete_orig: bool):
    for i, directory in enumerate(directories):
        pdf_name = output.joinpath(directory.name + '.pdf')
        if not rewrite and Path(pdf_name).is_file():
            continue

        make_pdf(directory, pdf_name)

        if _delete_orig:
            rmtree(directory)


def main():
    arg = arguments()
    rewrite = arg.rewrite_exist_pdf
    temp = temp_dir()
    archives, dirs, output = prepare(arg)
    _ext = ext(arg)
    _delete_orig_archives = arg.delete_original_archives
    _delete_orig_directories = arg.delete_original_directories
    _with_directories = arg.dont_include_directories

    process_archives(archives, output, _ext, rewrite, temp, _delete_orig_archives)
    if _with_directories:
        process_directories(dirs, output, rewrite, _delete_orig_directories)
