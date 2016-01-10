.. _Glossary:

############
Glossary
############

:ref:`B` - :ref:`M` - :ref:`R` - :ref:`S`

.. _B:

****
B
****

.. _Backup:

**Backup**

  A single backup containing refence to all objects needed to reassemble a disk
  image. A backup would reference all `Segment`_ and a `Manifest`_. A backup
  is part of a `Backupset`_.

.. _Backupset:

**Backupset**

  A backupset is a uuid used to provide a unique identifier to a collection of
  backups allowing for thier location in storage to be non-conflicting with
  other backupsets. A backupset references a single disk in an instance. When a
  `Restore`_ is preformed and a new `Backup`_ is started and new backupset uuid
  would be generated.

.. _M:

****
M
****

.. _Manifest:

**Manifest**

  A manifest is a file that tracks metadata and information about a single
  `Backup`_. It has enough information to locate each `Segment`_ that is
  required to bit-for-bit reassemble the block device the `Backup`_ was taken
  from.

.. _R:

****
R
****

.. _Restore:

**Restore**

  A restore refers to reassembling a `Backup`_ from it's backing storage into
  an image that can then be booted or otherwise attached to an instance. It
  reads the `Manifest`_ of the `Backup`_ that you want to restore and pulls all
  of the appropriate objects and then unencrypts and uncompresses them before
  reassembling the final image and uploading it to Glance.

.. _S:

****
S
****

.. _Segment:

**Segment**

  A segment is a section of the block device. It is typially 4MiB in size. A
  `Manifest`_ contains a list of segments that, when combined, would produce a
  bit-for-bit copy of the original block device the `Backup`_ was taken from.
