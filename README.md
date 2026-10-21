# Simulador del Algoritmo del Banquero 🏦

Este proyecto es una implementación en **Python** del **Algoritmo del Banquero**, diseñado para la gestión y evitación de interbloqueos (*deadlocks*) en la asignatura de **Sistemas Operativos**.

## 🧠 ¿Qué es el Algoritmo del Banquero?
Propuesto por Edsger Dijkstra, es un algoritmo de control de concurrencia y evitación de interbloqueos que simula la asignación de recursos de un "banco" a los procesos "clientes". El algoritmo evalúa constantemente si otorgar recursos a un proceso deja al sistema en un **estado seguro** (donde existe al menos una secuencia en la que todos los procesos pueden terminar) o en un **estado inseguro** (con riesgo de bloqueo mutuo).

## 🚀 Características del Simulador
El script incluye un menú interactivo con las siguientes opciones:
1. **Escenario Exitoso (Estado Seguro):** Carga un caso de prueba clásico para demostrar cómo el algoritmo calcula la matriz de necesidad (`Need = Max - Allocation`) y encuentra una secuencia segura.
2. **Escenario de Solicitud en Vivo (Petición Insegura):** Simula una petición de recursos de un proceso en ejecución y evalúa si se debe aprobar o denegar (aplicando *rollback* si pone en riesgo al sistema).
3. **Modo Manual:** Permite ingresar tu propia cantidad de procesos, recursos, matrices máximas, de asignación y recursos disponibles para evaluar cualquier ejercicio de clase.

## ⚙️ Requisitos
* Python 3.x instalado en tu sistema.

## 🕹️ ¿Cómo ejecutarlo?
Clona este repositorio o descarga los archivos, abre tu terminal en la carpeta del proyecto y ejecuta el siguiente comando:

```bash
python algoritmo_banquero_simulado.py