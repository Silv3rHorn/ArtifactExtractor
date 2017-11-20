# ArtifactExtractor
ArtifactExtractor is a script that extracts common Windows artifacts from source images and VSCs.

Artifacts in VSCs will be checked (via hash) if they are different from a later VSC/image copy before extraction.


## Dependencies
None if using release executable. 

Else, install from [requirements](https://github.com/Silv3rHorn/ArtifactExtractor/blob/master/requirements.txt) - `pip -r requirements.txt`. Install dependencies with errors separately:
1. Install backports.lzma from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#backports.lzma)
2. Install stable version (i.e. not experimental) of libewf only (see [here](https://github.com/log2timeline/dfvfs/issues/230))

## Usage
1. Download latest release from [Releases](https://github.com/Silv3rHorn/ArtifactExtractor/releases)
2. Create destination directory
3. `artifact_extractor.exe <source image> <dest dir>`

## Credits
Joachim Metz and his libraries
