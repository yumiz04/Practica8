# Practica 8 (Chunking)

La idea general es hacer el chunking por número de renglones,
'4' por cada chunk, sin solapar.

La segunda idea es hacer chunks por palabras, '100' palabras
por cada chunk, con solapamientos. La idea para esto es tomar
inicialmente 100 palabras para el primer chunk, el segundo
chunk comprenderá desde (100 - 50) hasta 200, el tercero desde
(200 - 50) hasta 300, y así sucesivamente.

## Preguntas de ejemplo
    "¿Cuántos días de vacaciones me tocan después de 3 años?",
    "¿Cuándo me pagan el aguinaldo?",
    "¿Puedo trabajar desde mi casa?",
    "¿Cuántos minutos tengo para llegar tarde?",
    "Falleció un familiar, ¿Qué puedo hacer?"

## Guía de instalación
Abrir una terminal (CMD o Git Bash) y navegar hasta la ruta deseada
```bash
cd Practicas
```

Clonar el repo
```bash
git clone https://github.com/yumiz04/Practica8.git
```

Entrar a la carpeta del proyecto
```bash
cd Practica8
```

Crear el entorno virtual de Python
```bash
python -m venv venv
```

Abrir VS Code
```bash
code .
```

Activar el entorno virtual (si no está activo)
```bash
.\venv\Scripts\activate
```

Instalar ependencias del proyecto
```bash
pip install supabase sentence-transformers python-dotenv
```