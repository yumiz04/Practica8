# Practica8

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