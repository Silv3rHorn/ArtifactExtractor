# ArtifactExtractor
ArtifactExtractor is a script that extracts common Windows artifacts from source images and VSCs.

Artifacts in VSCs will be checked (via hash) if they are different from a later VSC/image copy before extraction.


## Dependencies
None if using **release executable** on Windows.

Else:
1. Install backports.lzma from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#backports.lzma) (or on Linux using a package manager, e.g. `sudo apt install liblzma-dev`)
2. Install libewf: following testing conducted in February 2019, [libewf-legacy](https://github.com/libyal/libewf-legacy) should be installed rather than [libewf (experimental)](https://github.com/libyal/libewf) or Python bindings libewf-python (as these newer experimental releases have a [file corruption issue](https://github.com/log2timeline/dfvfs/issues/230)). The requirements listed in [requirements_unix.txt](requirements_unix.txt) have been tested successfully using [libewf-legacy build 20140806](https://github.com/libyal/libewf-legacy/releases/tag/20140806) - this build was tested in February 2019 using a [NIST reference E01 image](https://www.cfreds.nist.gov/data_leakage_case/data-leakage-case.html) ("Personal Computer (PC) – 'EnCase' Image"), and confirmed to extract identical data to a raw image equivalent. As libewf is updated regularly, it is recommended to perform similar comparison testing prior to deployment to ensure this advice is still correct.
3. Install remaining requirements: use either [requirements_windows.txt](requirements_windows.txt) or [requirements_unix.txt](requirements_unix.txt) depending on your host OS. Install using pip: `pip install -r requirements_windows.txt` or `pip install -r requirements_unix.txt`

## Usage on Windows
1. Download latest release from [Releases](https://github.com/Silv3rHorn/ArtifactExtractor/releases)
2. Create destination directory
3. `artifact_extractor.exe <source image> <dest dir> [-a <selected artifacts>]` or `artifact_extractor.exe -h` for more options

## Credits
Joachim Metz and his libraries
