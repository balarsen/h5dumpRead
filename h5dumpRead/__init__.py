import functools
import gzip
import os
import re

# get the filename from a line: 'HDF5 "rbspa_hope_eff_2018.h5" {'
hdf5_re = re.compile(r'.*HDF5.*"([A-Za-z0-9_\./\\-]*)"')

# get the group from a line: 'GROUP "/" {',
group_re = re.compile(r'.*GROUP.*"([A-Za-z0-9_\./\\-]*)"')


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
        self.GROUPS = self._get_GROUPS()

    def __repr__(self):
        """
        :return: :class:`str`, __repr__ value
        """
        return '<H5dump: {}>'.format(os.path.basename(self.fname))

    __str__ = __repr__

    def _regex_matcher_top(self, regex, retlist=True):
        """
        method to find top level matches within the file (HDF5, GROUPS)

        :param regex: :class:`re.Pattern`, the regex to use for the match
        :return: :class:`list`, the matched items from the file
        """
        newlist = list(filter(regex.match, self.raw))
        ans = [regex.search(v).groups()[0] for v in newlist]
        if not retlist and len(ans) == 1:
            return ans[0]
        else:
            return ans

    _get_GROUPS = functools.partialmethod(_regex_matcher_top, group_re)
    _get_HDF5 = functools.partialmethod(_regex_matcher_top, hdf5_re)


if __name__ == "__main__":
    h = H5dump('tests/datafiles/file1.dump.gz')
