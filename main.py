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
import time
from os.path import exists, dirname, join

import git
import pyperclip

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)
repository_url = 'https://github.com/rg3/youtube-dl.git'
base_path = dirname(__file__)


def ensure_ydl():
    repo_path = join(base_path, 'ydl')

    # Check if it exists
    if not exists(repo_path):
        log.warning('Youtube-dl not found! Dowloading from %s', repository_url)
        git.Repo.clone_from(repository_url, repo_path)

    # Check if it's old
    else:
        remote = git.Repo(repo_path).remote()
        log.info('Updating downloader from %s', remote.name)
        remote.pull()

    from ydl.youtube_dl import YoutubeDL
    return YoutubeDL


def pull(downloader, items):
    ydl_options = {
        'ignoreerrors': True,
        'format': 'bestaudio',
        'outtmpl': join(base_path, '%(title)s %(uploader)s-%(id)s.%(ext)s'),
    }
    with downloader(ydl_options) as youtube_dl:
        youtube_dl.download(items)


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
