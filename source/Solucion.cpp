#include "Solucion.h"

#include <fstream>
#include <iomanip>
#include <iostream>

#include "Instancia.h"

Solucion::Solucion() {}

void Solucion::agregar(int pulso) {
    _indices.push_back(pulso);
}

// borra todos los pulsos que teniamos guardados
void Solucion::limpiar() {
    _indices.clear();
}

const std::vector<int>& Solucion::indices() const {
    return _indices;
}

// devuelve la cantidad de pulsos que metimos en la solucion
int Solucion::cantidad() const {
    return static_cast<int>(_indices.size());
}

// calcula el costo total sumando las transiciones entre pulsos consecutivos
double Solucion::costo(const Instancia& instancia) const {
    // si no hay al menos dos pulsos no hay transiciones
    if (_indices.size() < 2) {
        return 0.0;
    }
    double total = 0.0;
    // vamos sumando el costo de saltar de cada pulso al siguiente
    for (size_t t = 0; t + 1 < _indices.size(); ++t) {
        total += instancia.costo(_indices[t], _indices[t + 1]);
    }
    return total;
}

// chequea que la solucion cumpla todas las restricciones del problema
bool Solucion::esValida(const Instancia& instancia) const {
    // tiene que tener exactamente k pulsos
    if (static_cast<int>(_indices.size()) != instancia.k()) {
        return false;
    }
    // no puede estar vacia
    if (_indices.empty()) {
        return false;
    }
    // el primero tiene que ser el pulso 1 y el ultimo el pulso n
    if (_indices.front() != 1 || _indices.back() != instancia.n()) {
        return false;
    }
    // los pulsos tienen que estar en orden estrictamente creciente
    for (size_t t = 0; t + 1 < _indices.size(); ++t) {
        if (_indices[t] >= _indices[t + 1]) {
            return false;
        }
    }
    return true;
}

// imprime los pulsos elegidos y el costo total formateado
void Solucion::imprimir(const Instancia& instancia) const {
    std::cout << "Selección (" << _indices.size() << " pulsos): ";
    for (size_t i = 0; i < _indices.size(); ++i) {
        std::cout << _indices[i] << (i + 1 < _indices.size() ? " " : "");
    }
    std::cout << "\n";
    std::cout << "Costo total: " << std::fixed << std::setprecision(6) << costo(instancia) << "\n";
}

// guarda los indices de la solucion en un archivo de texto
void Solucion::guardar(const std::string& ruta) const {
    std::ofstream archivo(ruta);
    if (!archivo.is_open()) {
        std::cerr << "Error: No se pudo abrir el archivo para guardar: " << ruta << "\n";
        return;
    }
    for (size_t i = 0; i < _indices.size(); ++i) {
        archivo << _indices[i] << (i + 1 < _indices.size() ? " " : "");
    }
    archivo << "\n";
}