-- Export originals (with Live Photo clips) from Photos, by UUID.
-- Usage: osascript photos_export.applescript /path/to/folder /path/to/uuids.txt
-- uuids.txt has one Photos UUID per line (ZASSET.ZUUID in Photos.sqlite). Fetches from iCloud as needed.
on run argv
  set dest to POSIX file (item 1 of argv)
  set ids to paragraphs of (read POSIX file (item 2 of argv))
  tell application "Photos"
    repeat with u in ids
      try
        set m to media item id ((u as text) & "/L0/001")
        with timeout of 300 seconds
          export {m} to dest with using originals
        end timeout
      on error e
        log "fail " & u & " " & e
      end try
    end repeat
  end tell
end run
