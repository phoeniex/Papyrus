#!/usr/bin/osascript

on run argv
	set theFilePath to POSIX file (item 1 of argv)
	set theSaveFilePath to POSIX file (item 2 of argv)
	set theFilePathAlias to theFilePath as alias

	set aDoc to theFilePathAlias as text
	tell application "Numbers"
		open aDoc
		log "opening " & aDoc
		delay 3 -- may need to adjust this higher
		
		tell front document
			save in theSaveFilePath
			close without saving
		end tell
	end tell
end run