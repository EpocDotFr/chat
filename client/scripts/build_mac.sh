pyinstaller \
    --clean --noconfirm --onefile --windowed \
    --log-level=WARN \
    --name="chat_mac" \
    --icon="resources/images/icon.icns" \
    --add-data="resources:resources" \
    --osx-bundle-identifier="fr.epoc.python.chat" \
    run.py