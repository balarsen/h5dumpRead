# h5dumpRead
Python code to parse h5dump output

Follows the language
https://support.hdfgroup.org/HDF5/doc/ddl.html

## Current status:
- 2020-09-10 Very early, parse to look for compression amount of a h5


## Example
```python
    import h5dumpRead
    h = h5dumpRead.H5dump('tests/datafiles/file1.dump.gz')
    print(h.get_dataset_compression_ratio())
    # {'/ele_eff': 1.169,
    # '/energy_ele': 0.963,
    # '/energy_ion': 0.963,
    # '/epoch': 8.986,
    # '/ion_eff': 1.126,
    # '/pixel': 1.818}      
```




