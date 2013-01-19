# Dropbox Recovery Tools

http://movieos.org/code/dropbox-tools/

A collection of little utilities I'm building as and when I need them to fix
things that are wrong with my Dropbox. Dropbox is great and I could not live without
it, but this is the Real World and things break.

Just to be clear - you should _NOT_ use these tools without reading and
understanding them. They're 30 lines of code each, and full of comments, but
they perform potentially destructive changes to your Dropbox folder.

# tools

## `zero_length.py`

Recover truncated files.

Usage:

    $ python zero_length.py <Dropbox folder>

Something weird happened to a shared dropbox I'm part of, and lots of files
became replaced by zero-length versions of themselves. Clearly this is annoying.
This script walks through the Dropbox folder, finds zero-length files, and
recovers them to the first state in their history where they were _not_ zero
length.

## `bulk_undelete.py`

Bulk-undelete files

Usage:

    zero_length.py <recovery folder> [<root path>]

eg:

    $ python zero_length.py ~/DropboxRecovery/ /SharedThings/

This was my first tool. I managed to delete 18,000 files from the shared work
Dropbox folder. Although in theory Dropbox lets you undelete files, in practice
you need to do this one at a time. Not going to happen. This script will walk
the remote Dropbox repository, and download the most recent version of any
file that was deleted in the last 5 days into the recovery folder. If the file
already exists in the target folder, it won't be overwritten, so the script will
only create new files.

I suggest you recover into a new, empty folder, then copy the files back into
dropbox once you're happy that it worked.


# instructions

Install requirements.

    $ pip install -r requrements.txt

Run script.

    # python zero_length.py ~/Dropbox

Eat bacon.


