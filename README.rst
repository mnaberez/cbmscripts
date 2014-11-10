cbmscripts
==========

Scripts for working with Commodore disk images

d64bad, d80bad
--------------

Read the error map at the end of a disk image and report all bad sectors.

d64diff, d80diff
----------------

Compare every sector of two disk images and report the differences.

d64flag
-------

Check if a D64 (1541, single sided) image has any information that
suggests the disk should have been imaged as a D71 (1571, double sided).
This checks a flag in the directory and also looks for any track/sector
pointers that are outside the 1541 range.

d80adderror
-----------

Add an error to the error map of a D80 image.  If the image does not have
an error map, one will be added.  To clear an error byte in the map, set
it to zero.

d64dir, d80dir
--------------

Read the CBM DOS directory of an image using `c1541` from VICE.  This
script exists because `c1541` will not read a disk image with an error map.
If the disk image has no error map, it will be passed directly to
`c1541`.  If the disk image has an error map, a temp file will be created
of the image without the error map, and it will be passed to `c1541`.

d80offset
---------

Given a track and sector, display its offset in the disk image.  This is
useful when examining an image file in a hex editor.

d64splice, d80splice
--------------------

Copy a sector from the source image into the target image.  If you have two
images of the same disk with different bad sectors, you can use this to
make one good image.  Use `d80adderror` to clear the error in the error map
after splicing.

d64truncate, d80truncate
------------------------

Remove the error map from a disk image.  Use this if you've fixed all errors
on a disk, or if you have to use the image with a program that does not
support images with error maps.

d80zero
-------

Fill a sector will null bytes.
