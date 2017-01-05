## Getting Started

To start, you will need either Python 2.7 or Python 3.5.2 or later

## Building the Documentation

To build the documentation, execute the following command at the command line in the directory this file is contained:

    make documentation

You will need [pdflatex](https://www.tug.org/texlive/ "PDFLaTeX"), [pandoc](http://pandoc.org/ "Pandoc"), [jupyter](https://jupyter.org/ "Jupyter") and [sphinx](http://www.sphinx-doc.org/ "Sphinx") installed.

If this is successful, you can view a PDF of the documentation in the directory:
    
    ./doc/build/latex/HTTM.pdf

## Running Tests

To start, make sure the `virtualenv` python module is installed.

To run the unit tests for this software, execute the following command at the command line in the directory this file is contained:

    make test