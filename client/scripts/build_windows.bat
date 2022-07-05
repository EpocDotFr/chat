@ECHO off
pyinstaller ^
    --clean --noconfirm --onefile --windowed ^
    --log-level=WARN ^
    --name="chat_windows" ^
    --icon="resources/images/icon.ico" ^
    --add-data="resources;resources" ^
    run.py