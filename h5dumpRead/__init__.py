import gzip
import os


class H5dump(object):
    def __init__(self, fname):
        """
        Initialize a H5dump object with the file to read

        :param fname: :class:`str`, the filename to parse
        """
        self.fname = fname
        if fname.endswith('gz'):
            with gzip.open(self.fname, 'r') as fp:
                dat = fp.readlines()
        else:
            with open(self.fname, 'r') as fp:
                dat = fp.readlines()
        self.raw = [v.strip().decode(encoding='UTF-8', errors='strict') for v in dat]
        self.HDF5 = self._get_HDF5()

    def __repr__(self):
        """
        :return: :class:`str`, __repr__ value
        """
        return '<H5dump: {}>'.format(os.path.basename(self.fname))

    __str__ = __repr__

    def _get_HDF5(self):
        """
        get the name of the hd5 file that was dumped
        :return: :class:`str`, name of the hdf5 file
        """
        from regex import hdf5_re
        newlist = list(filter(hdf5_re.match, self.raw))
        files = [hdf5_re.search(v).groups()[0] for v in newlist]
        if len(files) == 1:
            return files[0]
        else:
            return files


if __name__ == "__main__":
    h = H5dump('tests/datafiles/file1.dump.gz')
