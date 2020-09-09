import re

# get the filename from a line: 'HDF5 "rbspa_hope_eff_2018.h5" {'
hdf5_re = re.compile(r'.*HDF5.*"([A-Za-z0-9_\./\\-]*)"')

