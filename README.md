**Papyrus: An extrodinary localize solution for mobile platform**

...

# Requirement

This script running on MacOS terminal with sheel script. Drive with Python 3.0 and Applesctipt.
- **openpyxl**: python library for edit Microsoft Excel file format.
- **appscript**: python library for running Apple Script via python.

# Usage

```
> ./papyrus -h
Usage:
    ./papyrus [-f|--file FILE] [-j|--jira JIRA] [--(no-)dry-run] [--(no-)silent] [-v|--version] [-h|--help] <project> <platform> <business-unit>

Options:
	<project>		name of project, use for export/import correct file in iCloud.
	<platform>		type of operation to use (ios, and/android, bu).
	<business-unit>		business unit to use to export/import

	-f,--file		file path use for import (supported "bu" platform only) (no default)
	-j,--jira		jira reference number for import (supported "bu" platform only) (default: "-")
	--dry-run,--no-dry-run	run command with no result (off by default)
	--silent,--no-silent	run command with no print (off by default)
	-v,--version		Prints version
	-h,--help		Prints help

Platforms:
	bu			Convert localization Numbers to .xlsx file for translators
	ios			Convert localization Numbers to .strings files for iOS
	and/android		Convert localization Numbers to .xml files for Android
```