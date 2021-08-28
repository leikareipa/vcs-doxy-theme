# VCS's Doxygen theme

This repo provides an app that converts Doxygen's XML output into the HTML documentation of [VCS](https://github.com/leikareipa/vcs).

## Usage

Follow these steps to build the VCS HTML docs.

First, generate VCS's XML documentation:

1. Obtain the contents of VCS's [main repo](https://github.com/leikareipa/vcs)
2. Run Doxygen on that repo as per instructions there - it'll generate VCS's documentation in XML format

Then, build the HTML docs:

3. Copy the generated XML into a directory called `xml` in the root of this repo
4. Navigate to this repo's root and run `$ python3 vcs.py` (Python ~3.3+ required)
5. The generated HTML docs should now be in the `output` directory, from which you can copy them to be hosted

Note: The built docs require a browser with JavaScript enabled.
