# ArtifactExtractor
![](https://img.shields.io/badge/python-2.7-blue.svg)

ArtifactExtractor is a script that extracts common Windows artifacts from source images and VSCs.

Artifacts in VSCs will be checked (via hash) if they are different from a later VSC/image copy before extraction.


## Dependencies
None if using [release executable](https://github.com/Silv3rHorn/ArtifactExtractor/releases) on Windows.

Else:
1. Install backports.lzma
    * Windows: Use latest wheel file available from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#backports.lzma)
    * Linux: Use a package manager, e.g. `sudo apt install liblzma-dev`
2. Install libewf
    * [libewf-legacy](https://github.com/libyal/libewf-legacy) should be installed rather than [libewf (experimental)](https://github.com/libyal/libewf) - Newer experimental releases have a [file corruption issue](https://github.com/log2timeline/dfvfs/issues/230). 
    * Windows: Use the MSI installer available from [here](https://mega.nz/#!qU9yUQCa!EWpwiZvjGtUIUxldKSGdQkdvLCwJ7t3PGinymU8TfQc)
    * Linux: Use [libewf-legacy build 20140806](https://github.com/libyal/libewf-legacy/releases/tag/20140806)
3. (Windows ONLY) Install pywin32: `pip install pywin32`
4. Install remaining requirements: use [requirements.txt](requirements.txt)
    * Use pip: `pip install -r requirements.txt`

## Usage
1. Create destination directory
2. `artifact_extractor.exe <source image> <dest dir> [-a <selected artifacts>]` or `artifact_extractor.exe -h` for more options

## Credits
Joachim Metz and his libraries

John Corcoran for Unix Compatibility
