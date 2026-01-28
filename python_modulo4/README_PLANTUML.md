# PlantUML en VS Code (rápido) — Linux / macOS / Windows

## 1) Qué necesitas (mínimo)
- VS Code
- Extensión **PlantUML (jebbs)**
- **Java** (obligatorio)
- **Graphviz (dot)** (recomendado)

---

## 2) Instalar la extensión
En VS Code → **Extensions** → busca **PlantUML** → instala **PlantUML (jebbs)**.

---

## 3) Instalar Java + Graphviz

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y default-jre graphviz
java -version
dot -V

macOS (con Homebrew)

brew install openjdk graphviz
java -version
dot -V

Windows (PowerShell con winget)

winget install --id EclipseAdoptium.Temurin.17.JRE -e
winget install --id Graphviz.Graphviz -e
java -version
dot -V

4) Probar un diagrama

Crea demo.puml:

@startuml
Alice -> Bob: Hola
Bob --> Alice: Hola
@enduml

5) Ver preview en VS Code

Con el archivo abierto:

    Ctrl+Shift+P (Windows/Linux) o Cmd+Shift+P (macOS)

    Ejecuta: PlantUML: Preview Current Diagram