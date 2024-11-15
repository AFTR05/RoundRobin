import time
from collections import deque

class Proceso:
    def __init__(self, id, duracion):
        self.id = id                    # Identificador del proceso
        self.duracion = duracion        # Duración total que el proceso necesita
        self.tiempo_restante = duracion # Tiempo restante para que el proceso termine
        self.tiempo_espera = 0          # Tiempo de espera acumulado
        self.tiempo_inicio = None       # Tiempo de inicio de la ejecución
        self.tiempo_finalizacion = None # Tiempo en que el proceso termina

    def __str__(self):
        return (f"Proceso {self.id} | Duración: {self.duracion}s | "
                f"Restante: {self.tiempo_restante}s | Espera: {self.tiempo_espera}s")
    
def round_robin(procesos, quantum):
    """
    Implementación del algoritmo Round Robin para planificación de procesos.
    :param procesos: Lista de procesos a planificar
    :param quantum: Tiempo máximo que un proceso puede ejecutarse antes de ser interrumpido
    :return: Métricas de tiempo de espera y ejecución promedio
    """
    cola = deque(procesos)  # Cola para manejar los procesos
    tiempo_actual = 0       # Reloj del sistema

    print("Inicio de la planificación Round Robin\n")
    
    while cola:
        proceso = cola.popleft()  # Toma el siguiente proceso de la cola

        if proceso.tiempo_inicio is None:  # Si el proceso nunca ha sido ejecutado
            proceso.tiempo_inicio = tiempo_actual

        # Tiempo de ejecución es el mínimo entre el quantum y el tiempo restante del proceso
        tiempo_ejecucion = min(quantum, proceso.tiempo_restante)

        print(f"Ejecutando {proceso} durante {tiempo_ejecucion}s.")
        time.sleep(0.1)  # Simula el tiempo de ejecución (puedes ajustar o quitar esta línea)
        
        # Actualiza el tiempo restante y el reloj del sistema
        proceso.tiempo_restante -= tiempo_ejecucion
        tiempo_actual += tiempo_ejecucion

        # Actualiza el tiempo de espera para los otros procesos en la cola
        for p in cola:
            p.tiempo_espera += tiempo_ejecucion

        if proceso.tiempo_restante > 0:
            # Si el proceso no ha terminado, vuelve al final de la cola
            cola.append(proceso)
        else:
            # Si el proceso terminó, registra el tiempo de finalización
            proceso.tiempo_finalizacion = tiempo_actual
            print(f"{proceso} ha terminado. Tiempo de finalización: {proceso.tiempo_finalizacion}s.\n")

    # Cálculo de métricas
    tiempos_espera = [p.tiempo_espera for p in procesos]
    tiempos_ejecucion = [p.tiempo_finalizacion - p.tiempo_inicio for p in procesos]

    espera_promedio = sum(tiempos_espera) / len(procesos)
    ejecucion_promedio = sum(tiempos_ejecucion) / len(procesos)

    print("\nMétricas finales:")
    print(f"Tiempo de espera promedio: {espera_promedio:.2f}s")
    print(f"Tiempo de ejecución promedio: {ejecucion_promedio:.2f}s")

    return espera_promedio, ejecucion_promedio

# Ejemplo de uso
if __name__ == "__main__":
    # Crear algunos procesos con duraciones aleatorias
    procesos = [
        Proceso(id=1, duracion=10),
        Proceso(id=2, duracion=4),
        Proceso(id=3, duracion=6),
        Proceso(id=4, duracion=8)
    ]
    quantum = 3  # Define el quantum de tiempo

    # Imprimir la lista inicial de procesos
    print("Procesos iniciales:")
    for proceso in procesos:
        print(proceso)
    print("\n")

    # Ejecutar el planificador Round Robin
    round_robin(procesos, quantum)
