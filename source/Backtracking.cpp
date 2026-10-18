#include "Backtracking.h"
#include <limits>

// funcion recursiva de backtracking con podas por optimalidad y factibilidad
void generar(const Instancia& instancia, int pulso, int ultimoIncluido,
            std::vector<int>& seleccion, double costoParcial,
            double& mejorCosto, std::vector<int>& mejorSeleccion){
    int n = instancia.n();
    int k = instancia.k();
    // poda por optimalidad: si lo acumulado ya iguala o supera al mejor costo, retornamos de una
    if(costoParcial >= mejorCosto){
        return;
    }

    // caso base: llegamos al final de todos los pulsos
    if(pulso > n){
        // si logramos meter exactamente k pulsos, guardamos esta solucion como la mejor
        if (static_cast<int>(seleccion.size()) == k){
            mejorCosto = costoParcial;
            mejorSeleccion = seleccion;
        }
        return;
    }

    // poda por factibilidad: calculamos cuantos faltan meter y cuantos pulsos quedan disponibles
    int faltan = k - static_cast<int>(seleccion.size());
    int restantes = n - pulso + 1;
    // si ya metimos de mas o si los que quedan no alcanzan para llegar a k, descartamos la rama
    if (faltan < 0 || faltan > restantes){
        return;
    }

    // el primer pulso y el ultimo tienen que estar si o si
    bool obligatorio = (pulso == 1 || pulso == n);

    // rama 1: probamos no incluir el pulso actual si no es obligatorio
    if(!obligatorio){
        generar(instancia, pulso + 1, ultimoIncluido, seleccion, costoParcial, mejorCosto, mejorSeleccion);
    }

    // calculamos el costo de empalme entre el ultimo pulso que metimos y el actual
    double costoExtra = (ultimoIncluido == -1) ? 0.0 : instancia.costo(ultimoIncluido, pulso);
    seleccion.push_back(pulso);

    // rama 2: exploramos metiendo el pulso actual y sumando el costo correspondiente
    generar(instancia, pulso + 1, pulso, seleccion, costoParcial + costoExtra, mejorCosto, mejorSeleccion);

    // desarmamos la seleccion para volver al estado anterior
    seleccion.pop_back();
}

Solucion Backtracking::resolver(const Instancia& instancia) {
    std::vector<int> seleccion;
    double mejorCosto = std::numeric_limits<double>::infinity();
    std::vector<int> mejorSeleccion;

    // arrancamos a buscar desde el pulso 1 sin ningun pulso previo elegido y costo acumulado cero
    generar(instancia, 1, -1, seleccion, 0.0, mejorCosto, mejorSeleccion);

    // armamos la solucion final con los pulsos de la mejor combinacion encontrada
    Solucion solucion;
    for (int idx : mejorSeleccion) {
        solucion.agregar(idx);
    }
    return solucion;
}
