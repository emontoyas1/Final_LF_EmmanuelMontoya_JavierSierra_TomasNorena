# Interprete: ejecuta las reglas hasta llegar al punto fijo
from ast_nodes import And, Comparison, Fact


def evaluar_condicion(cond, variables, hechos):
    if isinstance(cond, And):
        izq = evaluar_condicion(cond.left, variables, hechos)
        der = evaluar_condicion(cond.right, variables, hechos)
        return izq and der
    elif isinstance(cond, Comparison):
        if cond.identifier not in variables:
            return False
        valor = variables[cond.identifier]
        if cond.operator == ">":
            return valor > cond.value
        elif cond.operator == "<":
            return valor < cond.value
        elif cond.operator == "=":
            return valor == cond.value
        return False
    elif isinstance(cond, Fact):
        return cond.identifier in hechos
    return False


# evalua todas las reglas una y otra vez hasta que ya no salgan hechos nuevos
def ejecutar(programa, variables, hechos_iniciales):
    hechos = set(hechos_iniciales)
    activados = set()
    while True:
        nuevos = []
        for regla in programa.rules:
            if evaluar_condicion(regla.condition, variables, hechos):
                accion = regla.action.identifier
                if accion not in hechos and accion not in nuevos:
                    nuevos.append(accion)
        if len(nuevos) == 0:
            break
        for h in nuevos:
            hechos.add(h)
            activados.add(h)
    return activados
