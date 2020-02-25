try:
    from .image2pdf import main
except ImportError:
    from logging import error

    def main():
        error('Package requirements not installed')

__all__ = ['main']
