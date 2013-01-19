#!/usr/bin/python

from common import dropbox_client
import sys
import os


if len(sys.argv) != 2:
    print "Usage: zero_length.py <dropbox folder>"
    sys.exit(1)
dropbox_folder = sys.argv[1]

client = dropbox_client()


# walk filesystem of dropbox folder
for root, dirs, files in os.walk(dropbox_folder):
    for name in files:
        # absolute path to the file we're thinking about
        path = os.path.join(root, name)

        # path to the file relative to the dropbox root folder.
        relative = os.path.abspath(path).replace(os.path.abspath(dropbox_folder), "")

        # macos makes all sorts of stupid files that we don't care about
        if '\r' in path:
            continue
        if "/.dropbox.cache" in path:
            # internal dropbox stuff
            continue

        # only consider 0-length files
        size = os.path.getsize(path)
        if size == 0:
            print "%s is zero-length"%relative
            # look in the history for the first non-zero-length version
            for rev in client.revisions(relative, rev_limit=5):
                if rev["bytes"] != 0:
                    print "   found non-zero history record. Rcovering."
                    client.restore(relative, rev['rev'])
                    break
            else:
                # none of the history records had a non-zero length, so it must
                # have been _created_ as zero length. Surprisingly common.
                print "   file was created as zero-length. Skipping."

