#!/usr/bin/env python3
"""
Genera gráficos de complejidad temporal a partir de output/numericos/experimento_n.csv.
Genera automáticamente:
  1. output/grafico_complejidad_n.svg (vectorial de alta definición, sin dependencias)
  2. output/grafico_complejidad_n.html (interactivo con Chart.js para abrir en cualquier navegador)
  3. output/grafico_complejidad_n.png (si matplotlib está instalado)
"""

import csv
import os
import sys

def cargar_datos(ruta_csv):
    if not os.path.exists(ruta_csv):
        print(f"Error: no existe {ruta_csv}. Correr primero el experimento.")
        sys.exit(1)
    
    datos = []
    with open(ruta_csv) as f:
        r = csv.DictReader(f)
        for row in r:
            datos.append({
                'algo': row['algoritmo'],
                'n': int(row['n']),
                'k': int(row['k']),
                'costo': float(row['costo']),
                'ms': float(row['ms'])
            })
    return datos

def generar_svg(datos, ruta_salida):
    fb = [d for d in datos if d['algo'] == 'fb']
    bt = [d for d in datos if d['algo'] == 'bt']
    pd = [d for d in datos if d['algo'] == 'pd']

    width, height = 1200, 620
    p1_x0, p1_x1, p1_y0, p1_y1 = 90, 540, 490, 110
    p2_x0, p2_x1, p2_y0, p2_y1 = 690, 1140, 490, 110

    def to_p1(n, ms, max_n=30, max_ms=5300):
        x = p1_x0 + (n - 8) / (max_n - 8) * (p1_x1 - p1_x0)
        y = p1_y0 - (ms / max_ms) * (p1_y0 - p1_y1)
        return x, y

    def to_p2(n, ms, max_n=500, max_ms=3000):
        x = p2_x0 + (n - 8) / (max_n - 8) * (p2_x1 - p2_x0)
        y = p2_y0 - (ms / max_ms) * (p2_y0 - p2_y1)
        return x, y

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background-color:#ffffff; font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">')

    # Encabezado
    svg.append('<rect width="100%" height="100%" fill="#ffffff"/>')
    svg.append('<text x="600" y="45" text-anchor="middle" font-size="22" font-weight="bold" fill="#0f172a">Comparativa Empírica de Complejidad Temporal según el Tamaño n</text>')
    svg.append('<text x="600" y="70" text-anchor="middle" font-size="13" fill="#64748b">Fuerza Bruta vs. Backtracking vs. Programación Dinámica (k = n/2) — UTDT TD V</text>')

    # Panel 1: n <= 30
    svg.append(f'<rect x="{p1_x0-15}" y="85" width="{p1_x1-p1_x0+30}" height="450" rx="8" fill="#f8fafc" stroke="#e2e8f0"/>')
    svg.append(f'<text x="{(p1_x0+p1_x1)/2}" y="105" text-anchor="middle" font-size="15" font-weight="600" fill="#0f172a">Panel A: Los 3 Algoritmos (n ≤ 30)</text>')
    svg.append(f'<text x="{(p1_x0+p1_x1)/2}" y="122" text-anchor="middle" font-size="11" fill="#64748b">Explosión Exponencial de Fuerza Bruta vs. BT y PD</text>')

    for ms_val in [0, 1000, 2000, 3000, 4000, 5000]:
        _, y = to_p1(8, ms_val)
        svg.append(f'<line x1="{p1_x0}" y1="{y}" x2="{p1_x1}" y2="{y}" stroke="#e2e8f0" stroke-width="1"/>')
        svg.append(f'<text x="{p1_x0-10}" y="{y+4}" text-anchor="end" font-size="11" fill="#64748b">{ms_val} ms</text>')

    for n_val in [8, 12, 16, 20, 24, 28, 30]:
        x, _ = to_p1(n_val, 0)
        svg.append(f'<line x1="{x}" y1="{p1_y0}" x2="{x}" y2="{p1_y1+25}" stroke="#e2e8f0" stroke-dasharray="3,3" stroke-width="1"/>')
        svg.append(f'<text x="{x}" y="{p1_y0+18}" text-anchor="middle" font-size="11" fill="#64748b">{n_val}</text>')

    svg.append(f'<text x="{(p1_x0+p1_x1)/2}" y="{p1_y0+40}" text-anchor="middle" font-size="12" font-weight="500" fill="#334155">Cantidad de pulsos (n)</text>')

    # Panel 2: n hasta 500
    svg.append(f'<rect x="{p2_x0-15}" y="85" width="{p2_x1-p2_x0+30}" height="450" rx="8" fill="#f8fafc" stroke="#e2e8f0"/>')
    svg.append(f'<text x="{(p2_x0+p2_x1)/2}" y="105" text-anchor="middle" font-size="15" font-weight="600" fill="#0f172a">Panel B: Gran Escala (n hasta 500)</text>')
    svg.append(f'<text x="{(p2_x0+p2_x1)/2}" y="122" text-anchor="middle" font-size="11" fill="#64748b">Crecimiento Cúbico O(n³) de PD vs. Backtracking</text>')

    for ms_val in [0, 500, 1000, 1500, 2000, 2500, 3000]:
        _, y = to_p2(8, ms_val)
        svg.append(f'<line x1="{p2_x0}" y1="{y}" x2="{p2_x1}" y2="{y}" stroke="#e2e8f0" stroke-width="1"/>')
        svg.append(f'<text x="{p2_x0-10}" y="{y+4}" text-anchor="end" font-size="11" fill="#64748b">{ms_val} ms</text>')

    for n_val in [8, 100, 200, 300, 400, 500]:
        x, _ = to_p2(n_val, 0)
        svg.append(f'<line x1="{x}" y1="{p2_y0}" x2="{x}" y2="{p2_y1+25}" stroke="#e2e8f0" stroke-dasharray="3,3" stroke-width="1"/>')
        svg.append(f'<text x="{x}" y="{p2_y0+18}" text-anchor="middle" font-size="11" fill="#64748b">{n_val}</text>')

    svg.append(f'<text x="{(p2_x0+p2_x1)/2}" y="{p2_y0+40}" text-anchor="middle" font-size="12" font-weight="500" fill="#334155">Cantidad de pulsos (n)</text>')

    # Curvas Panel 1
    fb_pts = [to_p1(d['n'], d['ms']) for d in fb]
    svg.append(f'<polyline fill="none" stroke="#ef4444" stroke-width="3.5" points="{" ".join([f"{x},{y}" for x, y in fb_pts])}"/>')
    for x, y in fb_pts:
        svg.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#ef4444" stroke="#ffffff" stroke-width="1.5"/>')

    bt_p1_pts = [to_p1(d['n'], d['ms']) for d in bt if d['n'] <= 30]
    svg.append(f'<polyline fill="none" stroke="#3b82f6" stroke-width="2.5" points="{" ".join([f"{x},{y}" for x, y in bt_p1_pts])}"/>')
    for x, y in bt_p1_pts:
        svg.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#3b82f6"/>')

    pd_p1_pts = [to_p1(d['n'], d['ms']) for d in pd if d['n'] <= 30]
    svg.append(f'<polyline fill="none" stroke="#10b981" stroke-width="2.5" points="{" ".join([f"{x},{y}" for x, y in pd_p1_pts])}"/>')
    for x, y in pd_p1_pts:
        svg.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#10b981"/>')

    x_fb30, y_fb30 = to_p1(30, fb[-1]['ms'])
    svg.append(f'<text x="{x_fb30-12}" y="{y_fb30-10}" text-anchor="end" font-size="11" font-weight="bold" fill="#ef4444">FB (n=30): 5.050 ms</text>')
    svg.append(f'<text x="{x_fb30-12}" y="{p1_y0-8}" text-anchor="end" font-size="10" font-weight="bold" fill="#3b82f6">BT: 0,08 ms / PD: 0,04 ms</text>')

    # Curvas Panel 2
    bt_p2_pts = [to_p2(d['n'], d['ms']) for d in bt]
    svg.append(f'<polyline fill="none" stroke="#3b82f6" stroke-width="3" points="{" ".join([f"{x},{y}" for x, y in bt_p2_pts])}"/>')
    for x, y in bt_p2_pts:
        svg.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#3b82f6" stroke="#ffffff" stroke-width="1.5"/>')

    pd_p2_pts = [to_p2(d['n'], d['ms']) for d in pd]
    svg.append(f'<polyline fill="none" stroke="#10b981" stroke-width="3" points="{" ".join([f"{x},{y}" for x, y in pd_p2_pts])}"/>')
    for x, y in pd_p2_pts:
        svg.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#10b981" stroke="#ffffff" stroke-width="1.5"/>')

    x_bt500, y_bt500 = to_p2(500, bt[-1]['ms'])
    svg.append(f'<text x="{x_bt500-12}" y="{y_bt500-10}" text-anchor="end" font-size="11" font-weight="bold" fill="#3b82f6">BT (n=500): 2.695 ms</text>')

    x_pd500, y_pd500 = to_p2(500, pd[-1]['ms'])
    svg.append(f'<text x="{x_pd500}" y="{y_pd500+22}" text-anchor="middle" font-size="11" font-weight="bold" fill="#10b981">PD (n=500): 103 ms</text>')

    # Leyenda
    leg_y = 575
    svg.append(f'<rect x="330" y="{leg_y-16}" width="540" height="38" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>')

    svg.append(f'<line x1="360" y1="{leg_y}" x2="395" y2="{leg_y}" stroke="#ef4444" stroke-width="3.5"/>')
    svg.append(f'<circle cx="377" cy="{leg_y}" r="4" fill="#ef4444"/>')
    svg.append(f'<text x="405" y="{leg_y+4}" font-size="12" font-weight="600" fill="#1e293b">Fuerza Bruta (FB)</text>')

    svg.append(f'<line x1="530" y1="{leg_y}" x2="565" y2="{leg_y}" stroke="#3b82f6" stroke-width="3"/>')
    svg.append(f'<circle cx="547" cy="{leg_y}" r="4" fill="#3b82f6"/>')
    svg.append(f'<text x="575" y="{leg_y+4}" font-size="12" font-weight="600" fill="#1e293b">Backtracking (BT)</text>')

    svg.append(f'<line x1="700" y1="{leg_y}" x2="735" y2="{leg_y}" stroke="#10b981" stroke-width="3"/>')
    svg.append(f'<circle cx="717" cy="{leg_y}" r="4" fill="#10b981"/>')
    svg.append(f'<text x="745" y="{leg_y+4}" font-size="12" font-weight="600" fill="#1e293b">Prog. Dinámica (PD)</text>')

    svg.append('</svg>')

    os.makedirs(os.path.dirname(ruta_salida) or '.', exist_ok=True)
    with open(ruta_salida, 'w') as f:
        f.write('\n'.join(svg))
    print(f"Gráfico vectorial generado: {ruta_salida}")

def generar_html(datos, ruta_salida):
    fb = [d for d in datos if d['algo'] == 'fb']
    bt = [d for d in datos if d['algo'] == 'bt']
    pd = [d for d in datos if d['algo'] == 'pd']

    labels_p1 = [d['n'] for d in fb]
    ms_fb_p1 = [round(d['ms'], 3) for d in fb]
    ms_bt_p1 = [round(next(b['ms'] for b in bt if b['n'] == d['n']), 4) for d in fb]
    ms_pd_p1 = [round(next(p['ms'] for p in pd if p['n'] == d['n']), 4) for d in fb]

    labels_p2 = [d['n'] for d in pd]
    ms_bt_p2 = [round(next(b['ms'] for b in bt if b['n'] == d['n']), 3) for d in pd]
    ms_pd_p2 = [round(d['ms'], 3) for d in pd]

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Comparativa de Complejidad Temporal - TD V UTDT</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f1f5f9; margin: 0; padding: 30px; color: #0f172a; }}
    .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 16px; padding: 32px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
    h1 {{ font-size: 26px; text-align: center; margin-bottom: 8px; color: #1e293b; }}
    p.sub {{ text-align: center; color: #64748b; margin-top: 0; margin-bottom: 30px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
    .card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; }}
    .card h2 {{ font-size: 17px; margin-top: 0; color: #334155; text-align: center; }}
    .card p {{ font-size: 12px; color: #64748b; text-align: center; margin-bottom: 16px; }}
  </style>
</head>
<body>
<div class="container">
  <h1>Comparativa Empírica de Complejidad Temporal según n</h1>
  <p class="sub">Fuerza Bruta vs. Backtracking vs. Programación Dinámica (k = n/2) — Trabajo Práctico 1 UTDT</p>
  
  <div class="grid">
    <div class="card">
      <h2>Panel A: Los 3 Algoritmos (n ≤ 30)</h2>
      <p>Explosión Exponencial de Fuerza Bruta frente a BT y PD</p>
      <canvas id="chart1" height="260"></canvas>
    </div>
    <div class="card">
      <h2>Panel B: Gran Escala (n hasta 500)</h2>
      <p>Crecimiento Cúbico O(n³) de Programación Dinámica vs. Backtracking</p>
      <canvas id="chart2" height="260"></canvas>
    </div>
  </div>
</div>

<script>
const ctx1 = document.getElementById('chart1').getContext('2d');
new Chart(ctx1, {{
  type: 'line',
  data: {{
    labels: {labels_p1},
    datasets: [
      {{ label: 'Fuerza Bruta (FB)', data: {ms_fb_p1}, borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.1)', borderWidth: 3, tension: 0.2 }},
      {{ label: 'Backtracking (BT)', data: {ms_bt_p1}, borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.1)', borderWidth: 2.5, tension: 0.2 }},
      {{ label: 'Prog. Dinámica (PD)', data: {ms_pd_p1}, borderColor: '#10b981', backgroundColor: 'rgba(16,185,129,0.1)', borderWidth: 2.5, tension: 0.2 }}
    ]
  }},
  options: {{
    responsive: true,
    scales: {{
      x: {{ title: {{ display: true, text: 'Pulsos (n)' }} }},
      y: {{ title: {{ display: true, text: 'Tiempo (ms)' }} }}
    }}
  }}
}});

const ctx2 = document.getElementById('chart2').getContext('2d');
new Chart(ctx2, {{
  type: 'line',
  data: {{
    labels: {labels_p2},
    datasets: [
      {{ label: 'Backtracking (BT)', data: {ms_bt_p2}, borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.1)', borderWidth: 2.5, tension: 0.2 }},
      {{ label: 'Prog. Dinámica (PD)', data: {ms_pd_p2}, borderColor: '#10b981', backgroundColor: 'rgba(16,185,129,0.1)', borderWidth: 2.5, tension: 0.2 }}
    ]
  }},
  options: {{
    responsive: true,
    scales: {{
      x: {{ title: {{ display: true, text: 'Pulsos (n)' }} }},
      y: {{ title: {{ display: true, text: 'Tiempo (ms)' }} }}
    }}
  }}
}});
</script>
</body>
</html>
"""
    with open(ruta_salida, 'w') as f:
        f.write(html)
    print(f"Visualizador interactivo generado: {ruta_salida}")

def main():
    csv_path = "output/numericos/experimento_n.csv"
    datos = cargar_datos(csv_path)
    
    # 1. SVG
    generar_svg(datos, "output/grafico_complejidad_n.svg")
    
    # 2. HTML interactivo
    generar_html(datos, "output/grafico_complejidad_n.html")

    # 3. PNG si matplotlib existe
    try:
        import matplotlib.pyplot as plt
        fb = [d for d in datos if d['algo'] == 'fb']
        bt = [d for d in datos if d['algo'] == 'bt']
        pd = [d for d in datos if d['algo'] == 'pd']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

        # Panel 1: n <= 30
        ax1.plot([d['n'] for d in fb], [d['ms'] for d in fb], 'o-', color='#ef4444', label='Fuerza Bruta (FB)', lw=2.5)
        ax1.plot([d['n'] for d in bt if d['n'] <= 30], [d['ms'] for d in bt if d['n'] <= 30], 's-', color='#3b82f6', label='Backtracking (BT)', lw=2)
        ax1.plot([d['n'] for d in pd if d['n'] <= 30], [d['ms'] for d in pd if d['n'] <= 30], '^-', color='#10b981', label='Prog. Dinámica (PD)', lw=2)
        ax1.set_title('Panel A: Los 3 Algoritmos ($n \le 30$)\nExplosión Exponencial de Fuerza Bruta', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Cantidad de pulsos ($n$)', fontsize=11)
        ax1.set_ylabel('Tiempo de ejecución (ms)', fontsize=11)
        ax1.grid(True, linestyle='--', alpha=0.6)
        ax1.legend()

        # Panel 2: n hasta 500
        ax2.plot([d['n'] for d in bt], [d['ms'] for d in bt], 's-', color='#3b82f6', label='Backtracking (BT)', lw=2)
        ax2.plot([d['n'] for d in pd], [d['ms'] for d in pd], '^-', color='#10b981', label='Prog. Dinámica (PD)', lw=2)
        ax2.set_title('Panel B: Gran Escala ($n$ hasta 500)\nCrecimiento Cúbico de PD vs. Backtracking', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Cantidad de pulsos ($n$)', fontsize=11)
        ax2.set_ylabel('Tiempo de ejecución (ms)', fontsize=11)
        ax2.grid(True, linestyle='--', alpha=0.6)
        ax2.legend()

        plt.tight_layout()
        plt.savefig("output/grafico_complejidad_n.png", dpi=300)
        print("Gráfico PNG generado: output/grafico_complejidad_n.png")
    except ImportError:
        pass

if __name__ == '__main__':
    main()
