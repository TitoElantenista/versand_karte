import streamlit as st

# Título principal
st.title('Wie man die App verwendet 📱')

st.write('---')  # Línea separadora

# Paso 1
st.subheader('1. Daten speichern 🛰')
st.write('Aktivieren Sie auf Ihrem Mobilgerät die Option, um die Daten der Koordinaten zu speichern, an denen Fotos aufgenommen werden.')

st.write('---')  # Línea separadora

# Paso 2-3
st.subheader('2-3. Verbindung zum PC und Fotos übertragen 💻📸')
st.write('''
- Schließen Sie Ihr Gerät, mit dem Sie Fotos aufgenommen haben, an Ihren PC an.
- Übertragen Sie die Fotos mithilfe des Windows-Explorers auf Ihren PC.
''')

st.write('---')  # Línea separadora

# Paso 4
st.subheader('4. Fotos hochladen 🔄')
st.write('''
Wählen Sie die Fotos aus, mit denen Sie eine Karte erstellen möchten, und ziehen Sie sie in das Feld mit der Aufschrift "Drag and drop files here". 
Wenn kein Foto die Koordinaten korrekt gespeichert hat, sehen Sie die Nachricht "Kein hochgeladenes Foto enthält GPS-Koordinaten". 
Wenn nur ein Foto Koordinaten hat, wird eine Karten-Vorschau erstellt. 
Wenn Sie mehrere Fotos hinzugefügt haben, sehen Sie die Linie, die die Marker auf der Karte verbindet.
''')

st.write('---')  # Línea separadora

# Paso 5
st.subheader('5. Thumbnail-Größe wählen 🔍')
st.write('''
Wählen Sie die Größe der Bilder in den Vorschaubildern über das Dropdown-Menü "Wählen Sie die Thumbnail-Größe:".
*Hinweis:* Diese Option wird derzeit überprüft, da es möglich ist, dass die PC-Option für alle Geräte geeignet ist. Sie können jedoch gerne mehrere Karten erstellen und die Ergebnisse überprüfen.
''')

st.write('---')  # Línea separadora

# Paso 6
st.subheader('6. Fotos anzeigen und kommentieren 🖼️💬')
st.write('''
Klicken Sie in der Vorschau auf die Marker, um die Fotos anzuzeigen. Sie sehen den Namen des Fotos und den Zeitpunkt der Aufnahme.
Sie können auch Kommentare zu den Fotos hinzufügen, indem Sie das Foto im Dropdown-Menü auswählen, einen Kommentar schreiben und die Schaltfläche "Kommentar einfügen" drücken. Die Enter-Taste oder ähnliche Optionen funktionieren nicht, um den Kommentar einzufügen.
''')

st.write('---')  # Línea separadora

# Paso 7
st.subheader('7. Datei herunterladen ⬇️')
st.write('''
Klicken Sie auf den Button "Datei vorbereiten". Nach einer kurzen Wartezeit erscheint unter dem Button ein blauer Link "Karte herunterladen" und eine Bestätigungsnachricht.
''')

st.write('---')  # Línea separadora

# FAQ
st.title('FAQ ❓')
st.write('''
- **Wie weiß ich, ob die App einen Fehler hat oder funktioniert?**
    - Wenn Sie viele Fotos hochladen, kann die App langsam sein. Wenn Sie in der oberen rechten Ecke die Nachricht "running" sehen, bedeutet dies, dass die App arbeitet und Änderungen aktualisiert / die Karte neu erstellt. Bitte haben Sie Geduld.
- **Was passiert, wenn ich die Seite aktualisiere?**
    - Glückwunsch! Sie müssen von vorne beginnen, denn wie ich bereits erwähnt habe, speichere ich Ihre Informationen nicht und kann daher weder erkennen, wer Sie sind, noch Ihre Sitzung wiederherstellen.
''')


# Puedes añadir más elementos de Streamlit si lo consideras necesario.
