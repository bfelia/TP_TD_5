#include "FuerzaBruta.h"
#include <limits>

// funcion recursiva que explora todas las combinaciones posibles probando incluir o no cada pulso
void generar(const Instancia& instancia, int pulso, std::vector<int>& seleccion,
            double& mejorCosto, std::vector<int>& mejorSeleccion) {
                int n = instancia.n();
                int k = instancia.k();

                // caso base: ya tomamos una decision para cada uno de los n pulsos
                if(pulso > n){
                    // si metimos exactamente k pulsos, es una solucion candidata valida
                    if(static_cast<int>(seleccion.size()) == k){
                        double costo = 0;
                        // calculamos el costo total sumando la distancia de cada transicion
                        for(size_t t = 0; t+1 < seleccion.size(); t++){
                            costo += instancia.costo(seleccion[t], seleccion[t+1]);
                        }
                        // si encontramos un costo menor, actualizamos la mejor solucion que vimos
                        if(costo < mejorCosto){
                            mejorCosto = costo;
                            mejorSeleccion = seleccion;
                        }
                    }
                    return;
                }

                // el primero y el ultimo son obligatorios por enunciado, no se pueden saltear
                bool obligatorio = (pulso ==1 || pulso ==n);

                // rama 1: si no es obligatorio, exploramos la posibilidad de no incluirlo
                if(!obligatorio){
                    generar(instancia,pulso+1,seleccion,mejorCosto,mejorSeleccion);
                }

                // rama 2: incluimos el pulso actual en la seleccion
                seleccion.push_back(pulso);
                generar(instancia,pulso + 1, seleccion, mejorCosto, mejorSeleccion);
                // desarmamos la decision para volver a dejar el vector como estaba
                seleccion.pop_back();

            }

// resuelve el problema por fuerza bruta recorriendo el espacio de busqueda completo
Solucion FuerzaBruta::resolver(const Instancia& instancia) {
    Solucion solucion;
    std::vector<int> seleccion;
    double mejorCosto = std::numeric_limits<double>::infinity();
    std::vector<int> mejorSeleccion;

    // arrancamos la recursion desde el pulso 1 con la seleccion vacia
    generar(instancia,1,seleccion,mejorCosto,mejorSeleccion);

    // pasamos los pulsos de la mejor combinacion encontrada a la solucion
    for(int i: mejorSeleccion){
        solucion.agregar(i);
    }
    return solucion;
}
