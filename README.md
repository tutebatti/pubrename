# pubrename
This is a simple GUI to conveniently rename pdf files of academic publications.
The general pattern is `author_year_title_subtitle_additions.pdf`, all lower case.
German Umlaute (ä, ö, ü) are changed to ae, oe, ue;
other non-ASCII signs are altered using the python module `unidecode`.

## Requirements
Pubrename was designed and tested with python 3 and PyQT modules for the GUI.
You will need the pdf viewer Evince installed;
in the future, I want to integrate a pdf viewer into the program itself.
The key shortcuts to move the pdf viewer to the right side of the screen are carried out virtually by pubrename.
The program was designed for Linux Mint (Cinnamon) and only tested there as well as on KDE Plasma;
I do not know if it works for other systems but I am happy about any feedback on that.

## Features & How-To
You can either choose an individual file from the menu to rename;
or you can choose a folder from the menu, from which random pdf files will be opened.
This feature allows for conveniently renaming a lot of files that have piled up on your computer.

Generally, author or editor, year, title, subtitle, and additions can be each entered in the respective fields.
The convenience of the GUI comes with drag & drop from a machine-readable pdf:
simply mark the title etc. and drag & drop it to the respective fields.

After clicking "Vorschau" (i.e., preview), the new filename is displayed.
It can be adjusted before submitting.

Filenames that are already close to the intended pattern can be normalized, slightly adapted, and submitted without filling out all the fields.
What is more, the script `normalize_pubfilename.py` can be used stand-alone, for example to batch-process a lot of files in the terminal.

Renamed files are moved to a folder `renamed`;
also, there are two buttons
(1) to move the file to a folder `2edit` for pre-processing such as cropping or OCR
(using OCRed files is recommended to use the benefits of the GUI, see above);
(2) to move the file to a folder `deleted` to move these files later to the trash or delete them immediately.

## To do
- Implement English language, in addition to German
- Look for further bugs
- Improve error handling
- Integrate pdf viewer
- Allow for other file types, such as epub or djvu
- Give more options to the user
