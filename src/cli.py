import os
from logging import INFO, StreamHandler, getLogger

from colorama import init as init_colorama

from src.commands import new, remove
from src.commands.install import install
from src.commands.test import run_test_runner
from src.utils import StandardLogFormatter

init_colorama()
cwd = os.getcwd()


async def cli(args, script_root):
    logger = getLogger()
    logger.setLevel(INFO)
    handler = StreamHandler()
    handler.setFormatter(StandardLogFormatter())
    logger.addHandler(handler)

    if args.command == "install":
        install(args.package, cwd)
    elif args.command == "remove":
        remove(args.package, cwd)
    elif args.command == "new":
        new(args.project_name, script_root)
    elif args.command == "test":
        await run_test_runner(
            getattr(args, "sources-root"),
            omit=args.omit,
            match=args.match,
            cairo_paths=args.cairo_path,
            cairo_paths_recursive=args.cairo_path_recursive,
        )
