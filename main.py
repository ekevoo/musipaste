# -*- coding: utf-8 -*-
#
# Copyright 2018, Ekevoo.com.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
import logging
import os
import sys
import time
from pathlib import Path

import git
import pyperclip

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)
repository_url = 'https://github.com/rg3/youtube-dl.git'
base_path = Path(__file__).resolve().parent


def ensure_ydl():
    repo_path = base_path.joinpath('ydl')

    # Check if it exists
    if not repo_path.exists():
        log.warning('Youtube-dl not found! Dowloading from %s', repository_url)
        log.warning('This first run takes several minutes. Please distract yourself with something else.')
        git.Repo.clone_from(repository_url, str(repo_path))

    # Check if it's old
    else:
        repo = git.Repo(str(repo_path))
        if repo.is_dirty():
            log.warning('Custom changes detected in Youtube-dl! Not checking for updates.')
        else:
            remote = repo.remote()
            log.info('Checking for Youtube-dl updates from %s. This should only take a few seconds.', remote.name)
            remote.pull()

    sys.path.append(str(base_path))
    from ydl.youtube_dl import YoutubeDL
    return YoutubeDL


class Converter:
    _converter_path = None

    def check(self, filename: str):
        target_path = Path(filename)
        if target_path.suffix == '.mp3':
            return

        log.info(target_path.with_suffix('.mp3'))


def pull(downloader, items):
    ydl_options = {
        'ignoreerrors': True,
        'format': 'bestaudio',
        'outtmpl': os.getcwd() + '/%(title)s %(uploader)s-%(id)s.%(ext)s',
    }
    converter = Converter()
    with downloader(ydl_options) as youtube_dl:
        for item in items:
            result = youtube_dl.extract_info(item, process=True)
            converter.check(result['filename'])


def main():
    clipboard = [i for i in (pyperclip.paste() or '').split() if i]
    log.info('------------------------------------------------------------------------')
    downloader = ensure_ydl()
    log.info('')
    if clipboard:
        log.info('Clipboard contents:')
        for i in clipboard:
            log.info('- %s', i)
        pull(downloader, clipboard)
    else:
        log.info('Nothing on the clipboard.')
    log.info('')
    log.info('------------------------------------------------------------------------')
    log.info('')
    log.info('Done!')
    time.sleep(30)


if __name__ == '__main__':
    main()
