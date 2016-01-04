==================
Manifest Structure
==================

The manifest is the piece that tracks all of the different objects. It's
structure is comprised of a header and body. The header contains::

    32B         - signature
    4B          - version
    4B unsigned - header checksum
    4B unsigned - body checksum
    4B signed   - utc timestamp
    4B unsigned - incremental in set
    4B unsigned - size of chunk in B
    8B unsigned - number of sectors (512B) for disk geometry
    2B unsigned - number of bases
    14B         - padding
    32B         - signature
    32B         - chunk 0
    32B         - chunk 1
    32B         - chunk n

Or viewed as an ascii template::

    +---------------------------------------------------------------+
    |    32B FILE SIGNATURE (ALWAYS THE SAME FOR ALL FILES)         |
    |                                                               |
    +---------------+-------+-----------------------+---------------+
    |VERSION| HDR   | BODY  | TMSTMP| INCRMT| SZ OF | NUM OF SECTOR |
    |       | CHKSUM| CHKSUM|       | NUM   | SEGMT | ON DISK       |
    +-------+-----------------------+-------+-------+---------------+
    |# OF|       PADDING / FUTURE EXPANSION                         |
    |BASE|                                                          |
    +-------------------------------+-------------------------------+
    |    UUID OF BACKUPSET 0        |    UUID OF BACKUPSET 1        |
    |                               |    (OR PADDING IF NO BACKUP)  |
    +---------------------------------------------------------------+
    |    UUID OF BACKUPSET 2        |    UUID OF BACKUPSET 3        |
    |                               |    (OR PADDING)               |
    +-------------------------------+-------------------------------+

The body contains n number of chunks. Each chunk contains::

    4B unsigned - chunk
    4B unsigned - incremental
    2B unsigned - base
    1B unsigned - encryption
    1B unsigned - compression
    20B         - sha1

Or viewed as an ascii template::

    +---------------------------------------------------------------+
    | SEGMNT| INCRMT|BAS|C|E|        SHA1 HASH OF UNCOMPRESSED      |
    |       |       |   | | |        UNENCRYPTED DATA               |
    +-------+-------+---+-+-+---------------------------------------+
