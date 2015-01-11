from __future__ import unicode_literals, absolute_import

from fuse import FUSE, Operations

from beets import ui
from beets.plugins import BeetsPlugin


class BeetsFilesystem(BeetsPlugin, Operations):
    def __init__(self):
        super(BeetsFilesystem, self).__init__()

    def commands(self):
        cmd = ui.Subcommand('mount', help='mount the library as a filesystem')
        cmd.parser.add_option('-r', '--root', dest='root',
                              help='Filesystem root location')
        cmd.func = self.mount
        return [cmd]

    def mount(self, lib, opts, args):
        root = opts.root or self.config['root'].get()
        # check that root exists and is an empty directory
        if not root:
            raise ValueError("Misconfiguration: no root folder given")
        try:
            self._log.info("Mounting the library on {0}", root)
            FUSE(self, root, foreground=True)
        except KeyboardInterrupt:
            pass
        except RuntimeError:
            self._log.exception("Problem happened!")
