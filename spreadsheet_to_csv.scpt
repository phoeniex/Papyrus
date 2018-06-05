#!/usr/bin/osascript

on run argv
	set theFilePath to POSIX file (item 1 of argv)
	set theExportFilePath to POSIX file (item 2 of argv)
	set theFilePathAlias to theFilePath as alias

	-- ensureUTF8Encoding
	do shell script "/usr/bin/defaults write com.apple.iWork.Numbers CSVExportEncoding -int 4"
	
	set exportName to theExportFilePath as text
	set aDoc to theFilePathAlias as text
	tell application "Numbers"
		open aDoc
		delay 3 -- may need to adjust this higher
		
		tell front document
			export to file exportName as CSV
			close
		end tell
	end tell
end run