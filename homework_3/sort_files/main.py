import re
import os
import sys
from time import sleep
from threading import Thread
from pathlib import Path
import shutil

from colorama import Fore

from .constants import (
    DIR_SUFF_DICT,
    TRANS,
    FOUND_FILES,
    THREAD_POOL,
)


def sort(path: Path) -> None:
    with THREAD_POOL:
        file_extensions = {}
        other_file_extensions = [0, set()]

        for el in path.iterdir():

            if el.is_file():
                folder_name = file_moderation(el, path)

                if folder_name:
                    file_extensions[el.suffix] = (file_extensions[el.suffix] + 1) if file_extensions.get(el.suffix) else 1

                else:
                    other_file_extensions[0] += 1
                    other_file_extensions[1].add(el.suffix)

            else:
                folder_moderation(el)

        report_folder(path, file_extensions, other_file_extensions)


def file_moderation(file: Path, path: Path) -> str | None:
    for folder_name, suffixes in DIR_SUFF_DICT.items():
        if file.suffix.lower() in suffixes:

            FOUND_FILES[folder_name].append(file.name)

            folder = path.joinpath(folder_name)

            folder.mkdir(exist_ok=True)

            file = file.rename(
                f"{folder.joinpath(normalize(file.name.removesuffix(file.suffix)))}{file.suffix}"
            )

            if folder_name == "archives":
                archive_folder = folder.joinpath(file.name.removesuffix(file.suffix))
                archive_folder.mkdir(exist_ok=True)

                try:
                    shutil.unpack_archive(
                        file,
                        archive_folder
                    )
                except (shutil.ReadError, RuntimeError) as e:
                    print(
                        f"{Fore.RED}An error occurred: {e}\n"
                        f"An attempt to extract the archive failed: {Fore.MAGENTA}{file.absolute()}")

            return folder_name

    else:
        FOUND_FILES["unknown"].append(file.name)

        file.rename(
            f"{path.joinpath(normalize(file.name.removesuffix(file.suffix)))}{file.suffix}"
        )


def folder_moderation(folder: Path) -> None:
    if not os.listdir(folder):
        folder.rmdir()

    elif folder.name not in DIR_SUFF_DICT.keys():
        Thread(target=sort,
               args=(
                   folder.rename(
                       f"{str(folder.absolute()).removesuffix(folder.name)}{normalize(folder.name)}"),
               )
        ).start()


def normalize(name: str) -> str:
    return re.sub(r'([^\w\s]+)', lambda match: '_' * len(match.group()), name).translate(TRANS)


def report_folder(path: Path, file_extensions: dict, other_file_extensions: list) -> None:
    print(f"{Fore.GREEN}\nIn directory {Fore.MAGENTA}«{path}»{Fore.GREEN} found files with extension:\n"
          f"{Fore.MAGENTA}{'Extension':^15}{Fore.GREEN}|{Fore.MAGENTA}{'Quantity':>5}")

    for extension, quantity in file_extensions.items():
        print(f"{Fore.CYAN}{str(extension):^15}{Fore.GREEN}|{Fore.CYAN}{str(quantity):>5}")

    if other_file_extensions[0]:
        print(
            f"{Fore.CYAN}{other_file_extensions[0]}{Fore.GREEN} files with an unknown extension: "
            f"{Fore.CYAN}{', '.join(other_file_extensions[1])}\n")


def main() -> None:
    if len(sys.argv) < 2:
        raise Exception("[-] Аргументом при запуску скрипта не передано шлях до директорії")

    root_folder = Path(sys.argv[1])

    if not root_folder.exists():
        raise ValueError("[-] Nonexistent directory")

    elif root_folder.is_file():
        raise ValueError("[-] The file is located at this path")

    while True:
        text = input(
            f"{Fore.CYAN}Confirm the sorting of the files in the directory "
            f"{Fore.MAGENTA}'{root_folder.absolute()}' {Fore.CYAN}(yes/no):{Fore.RESET} ")

        if text.lower() == "yes":
            break
        elif text.lower() == "no":
            return "File sorting canceled"

    extensions = []

    for ext in DIR_SUFF_DICT.values():
        extensions.extend(ext)

    print(f"{Fore.YELLOW}Search for files with the following extensions: {Fore.CYAN}{extensions}")
    sleep(5)

    sort(root_folder)

    print("""\n[!] Sorting is complete
        Found {cyan}{images_len}{yellow} files of category images: {cyan}{images}{yellow}
        Found {cyan}{documents_len}{yellow} files of category documents: {cyan}{documents}{yellow}
        Found {cyan}{audio_len}{yellow} files of category audio: {cyan}{audio}{yellow}
        Found {cyan}{video_len}{yellow} files of category video: {cyan}{video}{yellow}
        Found and unpacked {cyan}{archives_len}{yellow} files of category archives: {cyan}{archives}{yellow}
        Found {cyan}{unknown_len}{yellow} files with unknown extension: {cyan}{unknown}
        """.format(
        cyan=Fore.CYAN,
        yellow=Fore.YELLOW,
        images_len=len(FOUND_FILES['images']),
        documents_len=len(FOUND_FILES['documents']),
        audio_len=len(FOUND_FILES['audio']),
        video_len=len(FOUND_FILES['video']),
        archives_len=len(FOUND_FILES['archives']),
        unknown_len=len(FOUND_FILES['unknown']),
        **FOUND_FILES
    ))


if __name__ == '__main__':
    main()
