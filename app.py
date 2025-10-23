from flask import Flask, render_template, request
import math

# --- Tus funciones de redondeo ---
def redondear_alta(valor):
    # Evita resultados negativos raros y redondea hacia arriba
    return int(math.ceil(max(0, valor)))

def redondear_baja(valor):
    # Redondea hacia abajo al entero más cercano (no usada en la lógica actual, pero se mantiene)
    return int(math.floor(max(0, valor)))

def redondear_estandar(valor):
    # Redondea al entero más cercano (0.5 se redondea hacia arriba)
    return int(valor + 0.5)

# --- Inicializa la aplicación Flask ---
app = Flask(__name__)

# --- Lógica de cálculo adaptada a una función ---
def calcular_materiales(m2, material):
    if m2 <= 0:
        return "Error: Ingrese un valor de m² mayor que 0."

    # Fórmulas comunes
    ml_totales = m2 * 6.5
    piezas_material = redondear_alta(ml_totales / 2.2)  # ML / 2.2 y redondear arriba

    # Cálculos por material
    if material == "Deck":
        clip_inc = redondear_alta(m2 * 2)        # m2 * 2
        clip_fija = redondear_alta(m2 * 23)      # m2 * 23
        tornillos = redondear_alta(m2 * 25)      # m2 * 25
        # Piezas de rastrel: (m2 * 3.5 ML) / 3m por pieza
        rastrel = redondear_estandar((m2 * 3.5) / 3)

        texto = (
            f"Material: Deck\n"
            f"Superficie: {m2:.2f} m²\n"
            f"Metros lineales requeridos: {ml_totales:.2f} ML\n"
            f"Piezas de material (tablas): {piezas_material} pzas (ML/2.2 redondeo arriba)\n\n"
            f"Cotizar:\n"            
            f"- Deck: {piezas_material} pzas\n"
            f"- Clip Inc: {clip_inc} pzas\n"            
            f"- Clip Fija: {clip_fija} pzas\n"
            f"- Tornillos: {tornillos} pzas\n"
            f"- Rastrel: {rastrel} pzas\n"
        )

    elif material == "Monblack":  # Monblack
        clip_fija = redondear_alta(m2 * 20)      # m2 * 20
        tornillo_7504p = redondear_alta(m2 * 2)  # m2 * 2
        tornillo_7505a = redondear_alta(m2 * 9)  # m2 * 9
        # Piezas de rastrel: (m2 * 3 ML) / 3m por pieza
        rastrel = redondear_estandar((m2 * 3) / 3)

        texto = (
            f"Material: Monblack\n"
            f"Superficie: {m2:.2f} m²\n"
            f"Metros lineales requeridos: {ml_totales:.2f} ML\n"
            f"Piezas de material (tablas): {piezas_material} pzas (ML/2.2 redondeo arriba)\n\n"
            f"Cotizar (Fijaciones):\n"
            f"- Monblack: {piezas_material} pzas\n"
            f"- Clip Fija: {clip_fija} pzas\n"
            f"- Tornillo 7504p: {tornillo_7504p} pzas\n"
            f"- Tornillo 7505a: {tornillo_7505a} pzas\n"
            f"- Rastrel: {rastrel} pzas\n"
        )
    else:
        return "Error: Material no válido."

    return texto

# --- Rutas de la aplicación web ---
@app.route('/', methods=['GET', 'POST'])
def index():
    resultado_calculo = ""
    if request.method == 'POST':
        try:
            m2 = float(request.form['m2'])
            material = request.form['material']
            resultado_calculo = calcular_materiales(m2, material)
        except (ValueError, KeyError):
            resultado_calculo = "Error: Por favor, ingrese datos válidos."
    
    # El `render_template` busca el archivo 'index.html' en la carpeta 'templates'
    return render_template('index.html', resultado=resultado_calculo)

# --- Para ejecutar la aplicación localmente ---
if __name__ == '__main__':
    app.run(debug=True) # debug=True permite recarga automática y muestra errores