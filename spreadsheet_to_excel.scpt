#!/usr/bin/osascript

on run argv
	set theFilePath to POSIX file (item 1 of argv)
	set theExportFilePath to POSIX file (item 2 of argv)
	set theFilePathAlias to theFilePath as alias
    set theFileName to name of (info for theFilePath)
    set theFileExtension to name extension of (info for theFilePath)
    set xtsLength to count of theFileExtension
    set theFileNameWithoutExtension to text 1 thru -(xtsLength + 2) of theFileName

	-- ensureUTF8Encoding
	do shell script "/usr/bin/defaults write com.apple.iWork.Numbers CSVExportEncoding -int 4"
	
	set exportName to (theExportFilePath as text) & ":" & theFileNameWithoutExtension & ".xlsx"
    log exportName
	set aDoc to theFilePathAlias as text
	tell application "Numbers"
		open aDoc
		delay 3 -- may need to adjust this higher
		
		tell front document
			export to file exportName as Microsoft Excel
			close
		end tell
	end tell
end run