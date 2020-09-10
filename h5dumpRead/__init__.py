import functools
import gzip
import os
import re
from collections import namedtuple

# get the filename from a line: 'HDF5 "rbspa_hope_eff_2018.h5" {'
hdf5_re = re.compile(r'.*HDF5.*"([A-Za-z0-9_\./\\-]*)"')

# get the group from a line: 'GROUP "/" {',
group_re = re.compile(r'.*GROUP.*"([A-Za-z0-9_\./\\-]*)"')

# get the datasets from a line: 'DATASET "ele_eff" {',
dataset_re = re.compile(r'.*DATASET.*"([A-Za-z0-9_\./\\-]*)"')

# Extent = namedtuple('Extent', ['start', 'end'])
Boundary = namedtuple('Boundary', ['kind', 'start', 'end'])


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
        self.BOUNDARIES = self._get_group_boundaries()
        self.BOUNDARIES = {**self.BOUNDARIES, **self._get_dataset_boundaries()}

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
        :param retlist :class:`bool`, if False return the answer as a str not a list if possible
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

    def _get_boundary(self, startind):
        """
        Given a start index in `self.raw` find the line with the closing index

        :param startind: :class:`int`, the starting index for the search
        :return: :class:`int`, the ending index of the search where the {} are balanced
        """
        opens = 1
        closed = 0
        for ii in range(startind + 1, len(self.raw)):
            if '{' in self.raw[ii]:
                opens += 1
                print('{', ii, self.raw[ii], opens, closed)
            if '}' in self.raw[ii]:
                closed += 1
                print('}', ii, self.raw[ii], opens, closed)
            if closed == opens:
                break
        return ii

    def _get_group_boundaries(self):
        """
        Return the indices in `self.raw` that contain that group info

        :return: :class:`dict`, the groups and their boundaries
        """
        out = {}
        for g in self.GROUPS:
            ind1 = self.raw.index('GROUP "{}" {{'.format(g))
            ind2 = self._get_boundary(ind1)
            out[g] = Boundary(kind='GROUP', start=ind1, end=ind2)
        return out

    def _regex_matcher_group(self, regex, group):
        """
        method to find dataset matches within a group

        :param regex: :class:`re.Pattern`, the regex to use for the match
        :param group: :class:`str`, the group to use
        :return: :class:`list`, the matched items from the file
        """
        newlist = list(filter(regex.match, self.raw))
        ans = [regex.search(v).groups()[0] for v in newlist]
        return ans

    def _get_dataset_boundaries(self):
        """
        Given a group in the file return the dataset boundaries

        :return: :class:`dict`, the datasets and their boundaries
        """
        out = {}
        for group in self.GROUPS:
            try:
                newlist = list(
                    filter(dataset_re.match, self.raw[self.BOUNDARIES[group].start:self.BOUNDARIES[group].end]))
            except KeyError:
                raise KeyError('Group "{}" not in this file'.format(group))
            # TODO check with a named group here!
            datasets = [os.path.join(group, dataset_re.search(v).groups()[0]) for v in newlist]
            inds = [self.raw.index(v) for v in newlist]
            for ii, ds in zip(inds, datasets):
                ind2 = self._get_boundary(ii)
                out[ds] = Boundary(kind='DATASET', start=ii, end=ind2)
        return out


if __name__ == "__main__":
    h = H5dump('tests/datafiles/file1.dump.gz')
