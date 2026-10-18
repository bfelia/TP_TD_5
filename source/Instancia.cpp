#include "Instancia.h"
#include <cmath>
#include <fstream>
#include <stdexcept>

// constructor por defecto arrancando todo en cero
Instancia::Instancia() : _n(0), _d(0), _k(0) {}

// constructor que de una te abre el archivo y lo carga
Instancia::Instancia(const std::string& ruta) : _n(0), _d(0), _k(0) {
    cargar(ruta);
}

// lee la instancia desde el archivo de texto
void Instancia::cargar(const std::string& ruta) {
    std::ifstream archivo(ruta);
    if (!archivo.is_open()) {
        throw std::runtime_error("No se pudo abrir el archivo de entrada: " + ruta);
    }

    archivo >> _n;
    archivo >> _d;
    archivo >> _k;

    // armamos la matriz y guardamos las d features de cada uno de los n pulsos
    _features.assign(_n, std::vector<double>(_d, 0.0));
    for (int i = 0; i < _n; ++i) {
        for (int j = 0; j < _d; ++j) {
            archivo >> _features[i][j];
        }
    }
}

// devuelve la cantidad total de pulsos n
int Instancia::n() const {
    return _n;
}

// devuelve la dimension d de los vectores de features
int Instancia::d() const {
    return _d;
}

// devuelve la cantidad k de pulsos requeridos en la solucion
int Instancia::k() const {
    return _k;
}

const std::vector<double>& Instancia::feature(int i) const {
    return _features[i - 1];
}

// calcula el costo de transicion de pasar del pulso i al pulso j
double Instancia::costo(int i, int j) const {
    // si son consecutivos no hay corte, el costo es cero
    if (j == i + 1) {
        return 0.0;
    }
    // si no son consecutivos calculamos la distancia euclidea
    double suma = 0.0;
    for (int t = 0; t < _d; t++) {
        double diff = _features[i][t] - _features[j - 1][t]; // pulso (i+1) contra pulso j
        suma += diff * diff;
    }
    return std::sqrt(suma);
}