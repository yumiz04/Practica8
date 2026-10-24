# Practica 8 (Chunking)

## Dirección del proyecto
La idea general del chunking es comparar dos enfoques distintos:

El primer enfoque es hacer el chunking por número de renglones,
'4' por cada chunk, sin solapamiento.

El segundo enfoque es hacer chunks por número de palabras con un
margen de solapamiento. En concreto de '100' palabras por cada
chunk. La idea es tener una ventana de '100' con pasos de '50':
Por ejemplo, de 0 a 100, 50 a 150, 100 a 200, 150 a 250, etc.

Se mantiene el método original de chunking visto en clase. Se le
llamó por artículo, debido a que segmenta por cada uno.

## Golden Set
Preguntas sin respuesta: 8 y 20
```markdown
    "¿Cuántos días de vacaciones me tocan después de 3 años?",
    "¿Cuándo me pagan el aguinaldo?",
    "¿Puedo trabajar desde mi casa?",
    "Se murió mi tío, ¿me dan permiso?",
    "¿Cuál es el código de vestimenta?",
    "¿Cuántos minutos tengo para llegar tarde?",
    "Falleció un familiar, ¿Qué puedo hacer?",
    "Llegué tarde varias veces, ¿qué pasa?",
    "¿Cuando se realiza el depósito de la gratificación anual de fin de año?",
    "En caso del fallecimiento de un familiar, ¿cuántos días de permiso con goce tengo?",
    "¿Tengo la posibilidad de trabajar a distancia desde mi hogar?",
    "Si acumulo retrasos de forma constante, ¿cuáles son las consecuencias?",
    "¿Cómo se retribuye económicamente si presto mis servicios durante un día festivo?",
    "¿Es factible monetizar los días de vacaciones en lugar de disfrutarlos físicamente?",
    "¿Cuál es el código de vestimenta para asistir de forma presencial a las oficinas?",
    "¿Cuál es el margen de tolerancia permitido al llegar al corporativo?",
    "Si muere un pariente cercano, ¿cuál es el procedimiento y plazo para notificarlo?",
    "¿Cuántos días libres con goce de salario corresponden por contraer nupcias?",
    "¿Cuál es el monto mensual que otorga la empresa para cubrir gastos en esquema remoto?",
    "¿Existe alguna restricción sobre el uso de smartphones durante las horas laborales?"
```

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

## Guía de uso
Ejecutar
```bash
python ingesta.py
```
Muestra la estrategia de chunking y el número de chunks.
Cronometra los tiempos de los embeddings en segundos.

```bash
python bench.py
```
Muestra una tabla comparativa de estrategias, modelos,
Hit@3, MRR, tiempo de ingesta y costo.

## Recursos adicionales
Ejecutar en el SQL Editor de Supabase
```markdown
create extension if not exists vector;

create table if not exists politicas_bench (
  id bigserial primary key,
  archivo text,
  estrategia text,          -- 'articulo' | 'renglones' | 'palabras'
  capitulo text,
  articulo text,
  content text,
  emb_minilm vector(384),   -- all-MiniLM-L6-v2
  emb_bge vector(1024)      -- BAAI/bge-m3
);

create or replace function buscar_minilm(
  query_embedding vector(384), estrategia_f text, match_count int)
returns table (id bigint, content text, articulo text, similarity float)
language sql stable as $$
  select id, content, articulo, 1 - (emb_minilm <=> query_embedding) as similarity
  from politicas_bench
  where estrategia = estrategia_f
  order by emb_minilm <=> query_embedding
  limit match_count;
$$;

create or replace function buscar_bge(
  query_embedding vector(1024), estrategia_f text, match_count int)
returns table (id bigint, content text, articulo text, similarity float)
language sql stable as $$
  select id, content, articulo, 1 - (emb_bge <=> query_embedding) as similarity
  from politicas_bench
  where estrategia = estrategia_f
  order by emb_bge <=> query_embedding
  limit match_count;
$$;
```