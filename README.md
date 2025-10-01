# Schnittstellen Projekt – Ausbildungsbewerbung

Ein Webinterface zur Benutzerverwaltung mit Flask, MySQL und REST-API. Erstellt im Rahmen meiner Bewerbung als Fachinformatiker für Anwendungsentwicklung.

## 🌐 Live-Demo
- [Seite öffnen](https://nbauschat.eu.pythonanywhere.com)

## 🔧 Technologien

- Python 3.11  
- Flask  
- Jinja2 Templates  
- HTML, CSS, JavaScript  
- MySQL  
- dotenv (.env)

## 📦 Setup

1. Repository klonen:
   ```bash
   git clone https://github.com/noelbscht/schnittstellensystem.git
   cd schnittstellensystem
   ```

2. Virtuelle Umgebung erstellen:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. Pakete installieren:
   ```bash
   pip install -r requirements.txt
   ```

4. `.env.template` kopieren und ausfüllen:
   ```bash
   cp .env.template .env
   ```

5. Anwendung starten:
   ```bash
   flask run
   ```

## ⚙️ Optional: WSGI-Konfiguration
- **Datei:** `app.wsgi`  
- **Hinweis:** Die Umgebungsvariable `PROJECT_PATH` muss in der `.env` gesetzt werden und auf das Projektverzeichnis zeigen.

## 📚 Dokumentation

- `static/documentation/authentication_table.ddl` – MySQL Tabellenstruktur  
- `static/documentation/interface.drawio.html` – API-Flussdiagramm  


## 🖼️ Oberfläche

Die Weboberfläche zeigt:
- Verfügbare Endpunkte
- Dropdown zur Schnittstellen-Auswahl
- Fehler- und Erfolgsmeldungen
- API-Klassendiagramm zur Visualisierung

## 🔒 Sicherheit

- `.env` ist in `.gitignore` enthalten  
- `.env.template` zeigt benötigte Variablen ohne sensible Daten

## 📄 Lizenz

Siehe [LICENSE](LICENSE) – Nutzung nur mit Verweis auf mein GitHub-Profil und ausschließlich für nicht-kommerzielle Zwecke.

## 🎯 Zweck

Dieses Projekt dient ausschließlich Demonstrations- und Bewerbungszwecken im Rahmen meiner Ausbildungssuche.
