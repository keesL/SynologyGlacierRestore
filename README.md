# Restore Synology NAS Backup From Glacier to Anywhere

## Introduction

Amazon Glacier is a very cost-effective service to store off-site backups. Older Synology storage devices had a convenient built-in feature that lets users transparently backup to Glacier, and I have used that for quite some time. Newer ones might still have it, but I currently don't have a device to verify that.

Due to some lack of planning on my side, I actually never checked to see HOW that system worked. Turns out that, during the backup process, filenames are rewritten and that the original directory hierarchy is flattened. 

At first glance, the new filenames look somewhat randomly chosen. In reality, I suspect that they are some form of encoded hash that allows the device to only store one copy of files, even if they are located in different directories or if they have different names.

At second glance, the backup process actually created TWO vaults; one containing all the backups and one containing just one file that turned out to be a mapping from Glacier filename to Synology filename.

With this, we have all the pieces we need to solve this and to allow us to restore a Synology Glacier backup to any location.

The mapping file is a Sqlite3 database that contains a bunch of data. For this purpose, I was really only interested in the mapping form Glacier filename ("Archive", in Amazon terms) to the original filename on my NAS. 

I wrote a Python script that reads the mapping and then copies each file (with the hashed filename) to its original filename.

The process requires restoration of both Vaults prior to running my script. To do that, a tool like FastGlacier can be used. 

That leaves us with an overall approach:

1) Download the mapping, and all files that need restoring using a tool like FastGlacier
2) Edit my Python file with a text editor (notepad, WordPad, Notepad++, Sublime, etc.) and set the following three lines to the appropriate values

    frmdir = 'C:/Users/Kees/Downloads/Glacier/'
    dstdir = 'C:/Users/Kees/Pictures/'
    mapping = 'mapping.sqlite3'

3) Run the script. The original directory hierarchy will be recreated under `dstdir`.

NOTE: I have not looked to see if I could change the metadata of the filename to reflect original dates and times. I might do that some other time.
