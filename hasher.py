### THIS CODE IS COPIED FROM https://web.archive.org/web/20240112182958/https://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes#Python
### PARTICIPANTS NEED NOT WRITE THEIR OWN HASHING ALGORITHM

import struct, os
import urllib

__64k = 65536
__longlong_format_char = "q"
__byte_size = struct.calcsize(__longlong_format_char)


def temp_file():
    import tempfile

    file = tempfile.NamedTemporaryFile()
    filename = file.name
    return filename


def is_local(_str):
    from urllib.parse import urlparse

    if os.path.exists(_str):
        return True
    elif urlparse(_str).scheme in ["", "file"]:
        return True
    return False


def hashFile_url(filepath):
    # https://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
    # filehash = filesize + 64bit sum of the first and last 64k of the file
    name = filepath
    if is_local(filepath):
        local_file = True
    else:
        local_file = False

    if local_file == False:
        from urllib import request

        f = None
        opener = None
        url = name
        request.urlcleanup()

        f = request.urlopen(url)

        filesize = int(f.headers["Content-Length"])
        if filesize < __64k * 2:
            try:
                filesize = int(str(f.headers["Content-Range"]).split("/")[1])
            except:
                pass

        opener = request.build_opener()
        bytes_range = ("bytes=0-%s") % (str(__64k))
        opener.addheaders = [("Range", bytes_range)]

        first_64kb = temp_file()
        last_64kb = temp_file()

        request.install_opener(opener)
        request.urlretrieve(url, first_64kb)
        opener = request.build_opener()

        if filesize > 0:
            opener.addheaders = [
                ("Range", "bytes=%s-%s" % (filesize - __64k, filesize))
            ]
        else:
            f.close()
            os.remove(first_64kb)
            return "SizeError"

        try:
            request.install_opener(opener)
            request.urlretrieve(url, last_64kb)
        except:
            f.close()
            if os.path.exists(last_64kb):
                os.remove(last_64kb)
            os.remove(first_64kb)
            return "IOError"
        f = open(first_64kb, "rb")

    try:

        longlongformat = "<q"  # little-endian long long
        bytesize = struct.calcsize(longlongformat)

        if local_file:
            f = open(name, "rb")
            filesize = os.path.getsize(name)
        hash = filesize

        if filesize < __64k * 2:
            f.close()
            if local_file == False:
                os.remove(last_64kb)
                os.remove(first_64kb)
            return "SizeError"

        range_value = __64k / __byte_size
        range_value = round(range_value)

        for x in range(range_value):
            buffer = f.read(bytesize)
            (l_value,) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

        if local_file:
            f.seek(max(0, filesize - __64k), 0)
        else:
            f.close()
            f = open(last_64kb, "rb")
        for x in range(range_value):
            buffer = f.read(bytesize)
            (l_value,) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        if local_file == False:
            os.remove(last_64kb)
            os.remove(first_64kb)
        returnedhash = "%016x" % hash
        return returnedhash

    except IOError:
        if local_file == False:
            os.remove(last_64kb)
            os.remove(first_64kb)
        return "IOError"
