#include "ProgramacionDinamica.h"
#include <cmath>
#include <limits>
#include <vector>

// resuelve el problema usando programacion dinamica
Solucion ProgramacionDinamica::resolver(const Instancia& instancia) {
    int n = instancia.n();
    int k = instancia.k();

    const double INF = std::numeric_limits<double>::infinity();

    // dp[j][t]: guarda el costo minimo de meter t pulsos terminando en el pulso j
    std::vector<std::vector<double>> dp(n + 1, std::vector<double>(k + 1, INF));

    // caso base: meter solo el pulso 1 como unico elemento cuesta cero
    dp[1][1] = 0.0; 
    // recorremos t que es la cantidad de pulsos que llevamos metidos
    for (int t = 2; t <= k; t++) {
        // j es el pulso que termina la secuencia de t elementos
        for (int j = t; j <= n; j++) {        
            // i es el pulso previo que queremos empalmar con j
            for (int i = t - 1; i < j; i++) { 
                // si el estado anterior es inalcanzable, seguimos de largo
                if (dp[i][t - 1] == INF) continue;

                // costo de enganchar j viniendo desde i
                double candidato = dp[i][t - 1] + instancia.costo(i, j);
                // si este enganche es mas barato que lo que teniamos, actualizamos dp
                if (candidato < dp[j][t]) {
                    dp[j][t] = candidato;
                }
            }
        }
    }

    // reconstruimos la solucion optima directo desde la dp yendo para atras
    std::vector<int> seleccion;
    int j = n;
    seleccion.push_back(j);

    // para cada paso t buscamos que pulso previo i dio el optimo
    for (int t = k; t >= 2; t--) {
        for (int i = t - 1; i < j; i++) {
            if (dp[i][t - 1] == INF) continue;

            // si el costo coincide con la transicion, encontramos de donde vino
            if (dp[j][t] == dp[i][t - 1] + instancia.costo(i, j)) {
                j = i;
                seleccion.push_back(j);
                break;
            }
        }
    }

    // como fuimos para atras, invertimos la seleccion para que quede en orden y armamos la solucion
    Solucion solucion;
    for (auto it = seleccion.rbegin(); it != seleccion.rend(); ++it) {
        solucion.agregar(*it);
    }
    return solucion;
}