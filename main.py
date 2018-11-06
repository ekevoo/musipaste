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
from logging import getLogger
from os.path import exists, dirname, join
from time import sleep

from git import Repo
from pyperclip import paste

log = getLogger(__name__)
repository_url = 'https://github.com/rg3/youtube-dl.git'
base_path = dirname(__file__)


def ensure_ydl():
    repo_path = join(base_path, 'ydl')

    # Check if it exists
    if not exists(repo_path):
        log.warning('Youtube-dl not found! Dowloading from %s', repository_url)
        Repo.clone_from(repository_url, repo_path)

    # Check if it's old
    else:
        remote = Repo(repo_path).remote()
        log.info('Updating from %s', remote.name)
        remote.pull()

    from ydl.youtube_dl import YoutubeDL
    return YoutubeDL


def pull(items):
    YoutubeDL = ensure_ydl()
    ydl_options = {
        'ignoreerrors': True,
        'outtmpl': join(base_path, '%(title)s %(uploader)s-%(id)s.%(ext)s'),
    }
    with YoutubeDL(ydl_options) as youtube_dl:
        youtube_dl.download(items)


def main():
    clipboard = [i for i in (paste() or '').split() if i]
    print('------------------------------------------------------------------------')
    print('')
    if clipboard:
        print('Nothing on the clipboard.')
    else:
        print('Clipboard contents:')
        for i in clipboard:
            print('-', i)
        pull(clipboard)
    print('')
    print('------------------------------------------------------------------------')
    print('')
    print('Done!')
    sleep(30)


if __name__ == '__main__':
    main()
