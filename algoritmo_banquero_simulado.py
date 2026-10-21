import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def calcular_necesidad(max_matriz, asignacion, n, m):
    """Calcula y retorna la matriz de necesidad (Max - Asignación)."""
    return [
        [max_matriz[i][j] - asignacion[i][j] for j in range(m)]
        for i in range(n)
    ]

def es_estado_seguro_con_trazas(procesos, disponible, max_matriz, asignacion, mostrar_pasos=True):
    """
    Verifica si el sistema está en un estado seguro e imprime el paso a paso
    de cómo toma la decisión.
    """
    n = len(procesos)
    m = len(disponible)
    necesidad = calcular_necesidad(max_matriz, asignacion, n, m)
    
    trabajo = list(disponible)
    terminado = [False] * n
    secuencia_segura = []
    
    if mostrar_pasos:
        print("\n--- INICIO DEL ALGORITMO DE SEGURIDAD ---")
        print(f"Recursos disponibles iniciales (Work): {trabajo}")
        print(f"Matriz de Necesidades (Need):\n{necesidad}\n")

    paso = 1
    while len(secuencia_segura) < n:
        encontrado = False
        if mostrar_pasos:
            print(f"--- Iteración {paso} ---")
            
        for i in range(n):
            if not terminado[i]:
                # Verificar si Need[i] <= Trabajo
                cabe = all(necesidad[i][j] <= trabajo[j] for j in range(m))
                
                if mostrar_pasos:
                    print(f"  > Evaluando {procesos[i]}: Su Need es {necesidad[i]} | Trabajo actual: {trabajo}")
                    print(f"    ¿Su necesidad cabe en los recursos disponibles? {'SÍ' if cabe else 'NO'}")
                
                if cabe:
                    # El proceso puede terminar y liberar recursos
                    if mostrar_pasos:
                        print(f"    [¡ÉXITO!] A {procesos[i]} le alcanza. Simulando su finalización...")
                        print(f"    Liberando recursos de {procesos[i]}: Asignados eran {asignacion[i]}")
                    
                    for j in range(m):
                        trabajo[j] += asignacion[i][j]
                        
                    terminado[i] = True
                    secuencia_segura.append(procesos[i])
                    encontrado = True
                    
                    if mostrar_pasos:
                        print(f"    Nuevo recurso disponible (Work) tras liberar a {procesos[i]}: {trabajo}\n")
                    break
        
        if not encontrado:
            if mostrar_pasos:
                print("  [ALERTA] En esta iteración ninguno de los procesos restantes pudo avanzar con los recursos disponibles.")
            break
        paso += 1

    if len(secuencia_segura) == n:
        if mostrar_pasos:
            print(f"-> ¡ESTADO SEGURO ENCONTRADO! Secuencia: {' -> '.join(secuencia_segura)}\n")
        return True, secuencia_segura
    else:
        if mostrar_pasos:
            print("-> ¡ESTADO INSEGURO! No hay una secuencia posible para que todos terminen.\n")
        return False, []

def simular_solicitud(procesos, disponible, max_matriz, asignacion, id_proceso, solicitud):
    """Simula una solicitud en tiempo de ejecución explicando el porqué de la decisión."""
    m = len(disponible)
    i = procesos.index(id_proceso)
    necesidad = calcular_necesidad(max_matriz, asignacion, len(procesos), m)
    
    print(f"\n==================================================")
    print(f"PETICIÓN EN VIVO: El proceso {id_proceso} solicita {solicitud}")
    print(f"==================================================")
    
    # Validación 1: Solicitud <= Necesidad
    print(f"Paso 1: Verificando si {id_proceso} pide más de lo que declaró como máximo (Need).")
    print(f"  - Necesidad actual de {id_proceso}: {necesidad[i]}")
    for j in range(m):
        if solicitud[j] > necesidad[i][j]:
            print(f"  [DENEGADO] Error: El proceso excede su demanda máxima declarada en el recurso tipo {j}.")
            return False
    print("  [APROBADO] La solicitud es menor o igual a lo que necesita.")

    # Validación 2: Solicitud <= Disponible
    print(f"\nPaso 2: Verificando si el banco tiene suficientes recursos en la caja fuerte.")
    print(f"  - Disponible actual: {disponible}")
    for j in range(m):
        if solicitud[j] > disponible[j]:
            print(f"  [ESPERA] El recurso tipo {j} no tiene suficientes unidades libres. {id_proceso} debe esperar.")
            return False
    print("  [APROBADO] Hay suficientes recursos disponibles para entregar ahora.")

    # Simulación temporal
    print(f"\nPaso 3: Simulando la entrega temporal de recursos a {id_proceso}...")
    for j in range(m):
        disponible[j] -= solicitud[j]
        asignacion[i][j] += solicitud[j]
    
    print(f"  - Nuevo Disponible temporal: {disponible}")
    print(f"  - Nueva Asignación temporal de {id_proceso}: {asignacion[i]}")

    # Validación 3: Prueba de seguridad
    print(f"\nPaso 4: Corriendo el Algoritmo de Seguridad para verificar si el estado resultante es seguro...")
    seguro, secuencia = es_estado_seguro_con_trazas(procesos, disponible, max_matriz, asignacion, mostrar_pasos=True)

    if seguro:
        print(f"-> DECISIÓN FINAL: ¡Solicitud APROBADA! El estado resultante es SEGURO.")
        print(f"   Secuencia segura resultante: {' -> '.join(secuencia)}")
        return True
    else:
        print(f"-> DECISIÓN FINAL: ¡Solicitud DENEGADA! Dejaría al sistema en un estado INSEGURO.")
        print(f"   Revirtiendo cambios (Rollback) a los valores originales...")
        for j in range(m):
            disponible[j] += solicitud[j]
            asignacion[i][j] -= solicitud[j]
        return False


# --- MENÚ INTERACTIVO EN CONSOLA ---
def menu():
    while True:
        print("\n==================================================")
        print("      SIMULADOR DEL ALGORITMO DEL BANQUERO        ")
        print("==================================================")
        print("1. Escenario Exitoso (Buen uso / Estado Seguro)")
        print("2. Escenario con Solicitud Insegura (Mala petición / Denegada)")
        print("3. Ingresar Datos Manualmente y Probar")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("--- CARGANDO ESCENARIO EXITOSO ---")
            procesos = ["P0", "P1", "P2", "P3", "P4"]
            disponible = [3, 3, 2]
            max_matriz = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
            asignacion = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
            
            print(f"Procesos: {procesos}")
            print(f"Disponibles: {disponible}")
            print(f"Máximos:\n{max_matriz}")
            print(f"Asignación:\n{asignacion}")
            
            es_estado_seguro_con_trazas(procesos, disponible, max_matriz, asignacion, mostrar_pasos=True)
            input("\nPresione ENTER para volver al menú...")
            
        elif opcion == "2":
            limpiar_pantalla()
            print("--- CARGANDO ESCENARIO DE SOLICITUD INSEGURA ---")
            procesos = ["P0", "P1", "P2", "P3", "P4"]
            disponible = [3, 3, 2]
            max_matriz = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
            asignacion = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
            
            # Hacemos una petición que arriesgaría el sistema si se da sin control
            simular_solicitud(procesos, disponible, max_matriz, asignacion, "P0", [1, 0, 2])
            input("\nPresione ENTER para volver al menú...")
            
        elif opcion == "3":
            limpiar_pantalla()
            print("--- MODO MANUAL ---")
            try:
                num_proc = int(input("Ingrese el número de procesos: "))
                num_rec = int(input("Ingrese el número de tipos de recursos: "))
                
                procesos = [f"P{i}" for i in range(num_proc)]
                
                print(f"\nIngrese los recursos disponibles separados por espacio (ej. 3 3 2):")
                disponible = list(map(int, input("Disponible: ").split()))
                
                print(f"\nIngrese la Matriz Máxima (fila por fila, valores separados por espacio):")
                max_matriz = []
                for i in range(num_proc):
                    fila = list(map(int, input(f"Max para P{i}: ").split()))
                    max_matriz.append(fila)
                    
                print(f"\nIngrese la Matriz de Asignación (fila por fila, valores separados por espacio):")
                asignacion = []
                for i in range(num_proc):
                    fila = list(map(int, input(f"Asignación para P{i}: ").split()))
                    asignacion.append(fila)
                
                print("\nEvaluando estado inicial con sus datos...")
                es_estado_seguro_con_trazas(procesos, disponible, max_matriz, asignacion, mostrar_pasos=True)
                
            except Exception as e:
                print(f"\n[ERROR] Ocurrió un error en los datos ingresados: {e}. Intente de nuevo.")
                
            input("\nPresione ENTER para volver al menú...")
            
        elif opcion == "4":
            print("\n¡Saliendo del simulador. Hasta luego!")
            break
        else:
            print("\nOpción no válida. Por favor elija entre 1 y 4.")

if __name__ == "__main__":
    menu()
