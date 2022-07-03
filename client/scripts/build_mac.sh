pyinstaller \
    --clean --noconfirm --onefile --windowed \
    --log-level=WARN \
    --name="chat_mac" \
    --osx-bundle-identifier="fr.epoc.python.chat" \
    run.py