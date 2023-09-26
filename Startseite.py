import streamlit as st

def main():
    st.title("Foto-Ortung")

    markdown_text = """
    

    **Zweck der App:**  
    Diese nicht-professionelle Anwendung ermöglicht das Erstellen eines interaktiven Kartenbilds mit Markierungen und Vorschauen der hochgeladenen Fotos, basierend auf den Metadaten, die Ihr elektronisches Gerät in den Fotos speichert.

    - 📸 Eine Linie auf der Karte verbindet und ordnet die Fotos nach dem Datum und der Uhrzeit ihrer Erstellung. Eine Animation zeigt zudem die Richtung, in der die Fotos aufgenommen wurden.
    - 🌍 Die interaktive Karte wird als HTML-Datei gespeichert, die Sie an andere weiterleiten können, damit sie diese auf ihren Geräten anzeigen können.
    - 📱 Das Konzept der App besteht darin, Benutzern zu ermöglichen, wie gewohnt Fotos zu machen, ohne auf eine zusätzliche App angewiesen zu sein. Anschließend können sie mit wenig Aufwand eine Karte erstellen, ohne die ursprünglichen Fotos zu verändern.
    ![Startbild](https://raw.githubusercontent.com/TitoElantenista/versand_karte/main/resources/startfoto.jpg)

    ---

    # Voraussetzungen

    **Kompatibilität:**  
    Obwohl die App mit Samsung-Geräten getestet wurde, sollte sie auch mit anderen Geräten funktionieren. Nichtsdestotrotz empfehle ich, die App vor einem Projekt zu testen. Bei Problemen können Sie mich unter robertosl.info@gmail.com kontaktieren, damit ich die Kompatibilität Ihres Geräts überprüfen kann.

    **Foto-Metadaten:**  
    Die App benötigt bestimmte Informationen aus Ihren Fotos, um die Karte zu erstellen. Diese Informationen sind in den Metadaten Ihres Fotos eingebettet. Stellen Sie sicher, dass diese Funktion in den Kameraeinstellungen aktiviert ist.  

    ---

    # Aktuelle Limitierungen

    **Metadaten:**  
    Viele mobile Apps löschen aus Sicherheitsgründen die in Dateien eingebetteten Metadaten, wenn sie auf eine Webseite hochgeladen werden. Daher empfehle ich, diese App auf einem Computer zu verwenden und die Anweisungen im Menü unter "So funktioniert's" zu befolgen, um sicherzustellen, dass die App funktioniert.

    ---

    # Datenschutz und allgemeine Informationen

    **Über die App:**  
    Foto-Ortung ist ein Hobbyprojekt und hat keine Firma im Hintergrund. Der Benutzer ist für die Verwendung und Überprüfung der erstellten Karte verantwortlich.

    **Datensicherheit:**  
    Die App liest folgende Daten aus den Bildern: Koordinaten, Name, Datum und Uhrzeit der Aufnahme. Keine persönlichen oder statistischen Daten werden vom App-Ersteller gespeichert oder sind von Interesse.

    **Plattforminformation:**  
    Die App verwendet das Python-Modul Streamlit und wird in dessen Cloud gehostet. Es liegt in der Verantwortung des Benutzers, sich über mögliche gespeicherte Daten des Serviceanbieters zu informieren.
    
    ---
    
    **Kontakt:**
    Wenn Sie mit mir in Kontakt treten möchten, können Sie dies über meine E-Mail tun: [robertosl.info@gmail.com](mailto:robertosl.info@gmail.com) oder über LinkedIn: [Roberto SL](https://www.linkedin.com/in/roberto-sl-8a0b81b0/)

    
    """


    st.markdown(markdown_text)

if __name__ == "__main__":
    main()
