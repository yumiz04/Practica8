"""Banco de pruebas: línea base + 3 chunkings x 2 modelos."""
from buscar import buscar, crear_buscar, MODELOS
from chunking import ESTRATEGIAS, evaluar

# Las evidencias deben aparecer literalmente en politicas_empresa.txt.
# Las de abajo vienen del ejemplo del PDF: verifícalas contra tu archivo.
GOLDEN = [
    {"pregunta": "¿Cuántos días de vacaciones me tocan después de 3 años?",
     "evidencia": "Cada año adicional suma 2 días"},                      
    {"pregunta": "¿Cuándo me pagan el aguinaldo?",
     "evidencia": "a más tardar el 20 de diciembre"},                     
    {"pregunta": "¿Puedo trabajar desde mi casa?",
     "evidencia": "trabajar desde casa hasta 2 días por semana"},        
    {"pregunta": "Se murió mi tío, ¿me dan permiso?",
     "evidencia": "fallecimiento del cónyuge, padres, hijos o hermanos"}, 
    {"pregunta": "¿Cuál es el código de vestimenta?",
     "evidencia": None},                                                  
    {"pregunta": "¿Cuántos minutos tengo para llegar tarde?",
     "evidencia": PENDIENTE},
    {"pregunta": "Falleció un familiar, ¿Qué puedo hacer?",
     "evidencia": "fallecimiento del cónyuge, padres, hijos o hermanos"}, 
    {"pregunta": "Llegué tarde varias veces, ¿qué pasa?",
     "evidencia": "Tres retardos en un mismo mes"},                       
    {"pregunta": "¿Cuando se realiza el depósito de la gratificación anual de fin de año?",
     "evidencia": "a más tardar el 20 de diciembre"},                     
    {"pregunta": "En caso del fallecimiento de un familiar, ¿cuántos días de permiso con goce tengo?",
     "evidencia": "fallecimiento del cónyuge, padres, hijos o hermanos"}, 
    {"pregunta": "¿Tengo la posibilidad de trabajar a distancia desde mi hogar?",
     "evidencia": "trabajar desde casa hasta 2 días por semana"},         
    {"pregunta": "Si acumulo retrasos de forma constante, ¿cuáles son las consecuencias?",
     "evidencia": "Tres retardos en un mismo mes"},                       
    {"pregunta": "¿Cómo se retribuye económicamente si presto mis servicios durante un día festivo?",
     "evidencia": "tres veces su salario diario"},                        
    {"pregunta": "¿Es factible monetizar los días de vacaciones en lugar de disfrutarlos físicamente?",
     "evidencia": "No se pueden vender ni cambiar por dinero"},          
    {"pregunta": "¿Cuál es el código de vestimenta para asistir de forma presencial a las oficinas?",
     "evidencia": None},                                                  
    {"pregunta": "¿Cuál es el margen de tolerancia permitido al llegar al corporativo?",
     "evidencia": PENDIENTE},
    {"pregunta": "Si muere un pariente cercano, ¿cuál es el procedimiento y plazo para notificarlo?",
     "evidencia": PENDIENTE},
    {"pregunta": "¿Cuántos días libres con goce de salario corresponden por contraer nupcias?",
     "evidencia": PENDIENTE},
    {"pregunta": "¿Cuál es el monto mensual que otorga la empresa para cubrir gastos en esquema remoto?",
     "evidencia": PENDIENTE},
    {"pregunta": "¿Existe alguna restricción sobre el uso de smartphones durante las horas laborales?",
     "evidencia": PENDIENTE},
]


def similitud_top1(b, preguntas):
    return [b(p, 1)[0]["similarity"] for p in preguntas]


def main():
    con_resp = [g["pregunta"] for g in GOLDEN if g["evidencia"]]
    sin_resp = [g["pregunta"] for g in GOLDEN if not g["evidencia"]]

    base = evaluar(GOLDEN, buscar, k=3)
    print(f"LÍNEA BASE  Hit@3={base['hit@k']:.2f}  MRR={base['mrr']:.2f}\n")

    print(f"{'estrategia':10s} {'modelo':7s} {'Hit@3':>6s} {'MRR':>6s} "
          f"{'sim min (con resp.)':>20s} {'sim max (sin resp.)':>20s}")
    for estrategia in ESTRATEGIAS:
        for clave in MODELOS:
            b = crear_buscar(estrategia, clave)
            m = evaluar(GOLDEN, b, k=3)
            s_con = similitud_top1(b, con_resp)
            s_sin = similitud_top1(b, sin_resp) if sin_resp else [float("nan")]
            print(f"{estrategia:10s} {clave:7s} {m['hit@k']:6.2f} {m['mrr']:6.2f} "
                  f"{min(s_con):20.3f} {max(s_sin):20.3f}")


if __name__ == "__main__":
    main()
