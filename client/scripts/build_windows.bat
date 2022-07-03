@ECHO off
pyinstaller ^
    --clean --noconfirm --onefile --windowed ^
    --log-level=WARN ^
    --name="chat_windows" ^
    run.py