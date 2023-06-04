__app_name__ = "moderaitor"
__version__ = "0.1.0"

from moderaitor.cli import cli

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()