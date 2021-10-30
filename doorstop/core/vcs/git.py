# SPDX-License-Identifier: LGPL-3.0-only

"""Plug-in module to store requirements in a Git repository."""

import os

import gitignorant

from doorstop import common
from doorstop.core.vcs.base import BaseWorkingCopy

log = common.logger(__name__)


class WorkingCopy(BaseWorkingCopy):
    """Git working copy."""

    DIRECTORY = '.git'
    IGNORES = ('.gitignore',)

    def lock(self, path):
        log.debug("`git` does not support locking: %s", path)
        self.call('git', 'pull')

    def edit(self, path):
        self.call('git', 'add', self.relpath(path))

    def add(self, path):
        self.call('git', 'add', self.relpath(path))

    def delete(self, path):
        self.call('git', 'rm', self.relpath(path), '--force', '--quiet')

    def commit(self, message=None):
        message = message or input("Commit message: ")
        self.call('git', 'commit', '--all', '--message', message)
        self.call('git', 'push')

    @property
    def ignores(self):
        """Yield Gitignorant rules to ignore."""
        if self._ignores_cache is None:
            self._ignores_cache = []
            log.debug("reading and caching the gitignore patterns...")
            for filename in self.IGNORES:
                path = os.path.join(self.path, filename)
                if os.path.isfile(path):
                    self._ignores_cache = list(
                        gitignorant.parse_gitignore_file(common.read_lines(path))
                    )
        yield from self._ignores_cache

    def ignored(self, path):
        """Determine if a path matches a gitignored pattern."""
        for pattern in self.ignores:
            if pattern.matches(path):
                return True
        return False
