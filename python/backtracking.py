#!/usr/bin/env python3
import argparse
import math
import os
import sys
import time

# Aumentamos el límite de recursión para instancias grandes (n > 1000)
sys.setrecursionlimit(200000)

class Instancia:
    def __init__(self, ruta):
        with open(ruta, 'r') as file:
            lineas = file.read().splitlines()
            
        if not lineas:
            raise ValueError("El archivo está vacío.")
            
        # Extraer n, d, y k de la primera línea
        parametros = lineas[0].strip().split()
        self._n = int(parametros[0])
        self._d = int(parametros[1])
        self._k = int(parametros[2])
        
        # Inicializar la lista de pulsos con un dummy en el índice 0 para usar 1-indexación
        self._pulsos = [None]
        
        # Leer las siguientes n líneas con las características cromáticas
        for i in range(1, self._n + 1):
            caracteristicas = list(map(float, lineas[i].strip().split()))
            self._pulsos.append(caracteristicas)

    def n(self):
        return self._n

    def d(self):
        return self._d

    def k(self):
        return self._k

    def costo(self, i, j):
        if j == i + 1:
            return 0.0
        
        f_sig_i = self._pulsos[i + 1]
        f_j = self._pulsos[j]
        
        suma = sum((f_sig_i[l] - f_j[l]) ** 2 for l in range(self._d))
        return math.sqrt(suma)


def resolver_backtracking(instancia):
    n = instancia.n()
    k = instancia.k()
    mejor_costo = math.inf
    mejor_seleccion = []
    seleccion = []

    def generar(pulso, costo_parcial):
        nonlocal mejor_costo, mejor_seleccion

        # 1. Poda por optimalidad: si el costo acumulado ya supera o iguala la mejor solucion
        if costo_parcial >= mejor_costo:
            return

        # Caso base: recorrimos todos los pulsos
        if pulso > n:
            if len(seleccion) == k:
                mejor_costo = costo_parcial
                mejor_seleccion = list(seleccion)
            return

        # 2. Poda por factibilidad: verificar si aun podemos alcanzar exactamente k pulsos
        faltan = k - len(seleccion)
        restantes = n - pulso + 1
        if faltan < 0 or faltan > restantes:
            return

        obligatorio = (pulso == 1 or pulso == n)

        # Rama 1: No incluir el pulso actual (si no es obligatorio)
        if not obligatorio:
            generar(pulso + 1, costo_parcial)

        # Rama 2: Incluir el pulso actual
        costo_extra = 0.0 if not seleccion else instancia.costo(seleccion[-1], pulso)
        seleccion.append(pulso)
        generar(pulso + 1, costo_parcial + costo_extra)
        seleccion.pop()

    generar(1, 0.0)
    return mejor_seleccion, mejor_costo


def main():
    parser = argparse.ArgumentParser(description="Radio Edit - Backtracking")
    parser.add_argument("instancia_pos", nargs="?", default=None, help="Ruta al archivo de instancia")
    parser.add_argument("--instancia", default=None, help="Ruta al archivo de instancia")
    parser.add_argument("--salida", default=None, help="Ruta al archivo de salida con la seleccion de pulsos")
    parser.add_argument("--csv", default=None, help="Ruta al archivo CSV para registrar los tiempos")
    args = parser.parse_args()

    ruta_instancia = args.instancia or args.instancia_pos
    if not ruta_instancia:
        parser.error("Debe especificar la ruta de la instancia (posicional o con --instancia).")

    instancia = Instancia(ruta_instancia)
    print(f"Instancia cargada: n={instancia.n()} pulsos, d={instancia.d()} características, k={instancia.k()} a conservar")

    inicio = time.perf_counter()
    seleccion, costo = resolver_backtracking(instancia)
    fin = time.perf_counter()
    ms = (fin - inicio) * 1000.0

    print(f"Selección ({len(seleccion)} pulsos): {' '.join(map(str, seleccion))}")
    print(f"Costo total: {costo:.6f}")
    print(f"Tiempo: {ms:.2f} ms")

    if args.salida:
        os.makedirs(os.path.dirname(args.salida) or ".", exist_ok=True)
        with open(args.salida, "w") as f:
            f.write(" ".join(map(str, seleccion)) + "\n")
        print(f"Resultado guardado en {args.salida}")

    if args.csv:
        os.makedirs(os.path.dirname(args.csv) or ".", exist_ok=True)
        existe = os.path.isfile(args.csv)
        with open(args.csv, "a") as f:
            if not existe:
                f.write("algoritmo,n,d,k,costo,ms\n")
            f.write(f"bt_py,{instancia.n()},{instancia.d()},{instancia.k()},{costo:.10f},{ms:.3f}\n")
        print(f"Medición agregada a {args.csv}")


if __name__ == "__main__":
    main()