#!/usr/bin/python

from common import dropbox_client
from dropbox import rest

import sys
import os
import datetime

# dropbox API doesn't return any sensible datestrings.
DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

if len(sys.argv) not in (2, 3):
    print "Usage: recover.py <output folder> [<start walk>]"
    sys.exit(1)
recover_to = sys.argv[1]
try:
    start_walk = sys.argv[2]
except IndexError:
    start_walk = "/"

client = dropbox_client()


def recover_tree(folder = "/", recover_to=recover_to):
    # called recursively. We're going to walk the entire Dropbox
    # file tree, starting at 'folder', files first, and recover anything
    # deleted in the last 5 days.
    print "walking in %s"%folder

    try:
        meta = client.metadata(folder, include_deleted=True, file_limit=10000)
    except rest.ErrorResponse, e:
        print e # normally "too many files". Dropbox will only list 10000 files in
        # a folder. THere is probably a way around this, but I haven't needed it yet.
        return
    
    # walk files first, folders later
    for filedata in filter(lambda f: not f.get("is_dir", False), meta["contents"]):
        # we only care about deleted files.
        if not filedata.get("is_deleted", False):
            continue

        # this is the date the file was deleted on
        date = datetime.datetime.strptime(filedata["modified"], DATE_FORMAT)

        # this is where we'll restore it to.
        target = os.path.join(recover_to, filedata["path"][1:])

        if os.path.exists(target):
            # already recovered
            pass
        elif date < datetime.datetime.now() - datetime.timedelta(days=5):
            # not deleted recently
            pass
        else:
            print "  %s is deleted"%(filedata["path"])

            # fetch file history, and pick the first non-deleted revision.
            revisions = client.revisions(filedata["path"], rev_limit=10)
            alive = filter(lambda r: not r.get("is_deleted", False), revisions)[0]

            # create destination folder.
            try:
                os.makedirs(os.path.dirname(target))
            except OSError:
                pass

            # try to download file.
            # I'm torn here - I could just use the Dropbox API and tell it to 
            # restore the deleted file to the non-deleted version. PRoblem with
            # that is that it might recover too much. THis approach lets me restore
            # to a new folder with _just_ the restored files in, and cherry-pick
            # what I want to copy back into the main dropbox.
            try:
                fh = client.get_file(filedata["path"], rev=alive["rev"])
                with open(target+".temp", "w") as oh:
                    oh.write(fh.read())
                os.rename(target+'.temp', target)
                print "    ..recovered"
            except Exception, e:
                print "*** RECOVERY FAILED: %s"%e


    # now loop over the folders and recursively walk into them. Folders can
    # be deleted too, but don't try to undelete them, we'll rely on them being
    # implicitly reinflated when their files are restored.
    for file in filter(lambda f: f.get("is_dir", False), meta["contents"]):
        recover_tree(file["path"], recover_to)


recover_tree(start_walk)
