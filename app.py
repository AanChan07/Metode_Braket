from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Fungsi untuk parsing input pengguna
def parse_function(user_input):
    user_input = user_input.replace("^", "**").replace(",", ".")
    return user_input

# Fungsi untuk evaluasi
def evaluate_function(func, x):
    try:
        return eval(func, {"x": x, "math": math, "e": math.e})  # Menambahkan euler sebagai math.e
    except Exception as e:
        raise ValueError(f"Error evaluating function: {e}")

# Validasi awal interval
def validate_bracket(func, a, b):
    f_a = evaluate_function(func, a)
    f_b = evaluate_function(func, b)
    if f_a * f_b > 0:
        raise ValueError(f"Tidak ada akar pada interval [{a}, {b}] karena f(xl) * f(xu) > 0. Inputkan kembali interval yang benar")
    return f_a, f_b

# Metode Bisection
def bisection_method(func, a, b, iterations):
    results = []
    for i in range(iterations):
        c = (a + b) / 2
        f_a = evaluate_function(func, a)
        f_b = evaluate_function(func, b)
        f_c = evaluate_function(func, c)
        f_prod = f_a * f_c

        results.append({
            "iteration": i + 1,
            "Xl": a,
            "Xu": b,
            "Xr": c,
            "F(Xl)": f_a,
            "F(Xu)": f_b,
            "F(Xr)": f_c,
            "F(Xl)*F(Xr)": f_prod,
            "Error": abs(b - a),
        })

        if f_c == 0:  # Akar ditemukan
            break

        if f_prod < 0:
            b = c
        else:
            a = c
    return results

# Metode Regula Falsi
def regula_falsi_method(func, a, b, iterations):
    results = []
    for i in range(iterations):
        f_a = evaluate_function(func, a)
        f_b = evaluate_function(func, b)
        # cek pembagian oleh 0
        if f_b - f_a == 0:
            raise ValueError ("Nilai f(xu) - f(xl) = 0. Inputkan kembali fungsi yang benar ")
        c = (a * f_b - b * f_a) / (f_b - f_a)
        f_c = evaluate_function(func, c)
        f_prod = f_a * f_c

        results.append({
            "iteration": i + 1,
            "Xl": a,
            "Xu": b,
            "Xr": c,
            "F(Xl)": f_a,
            "F(Xu)": f_b,
            "F(Xr)": f_c,
            "F(Xl)*F(Xr)": f_prod,
            "Error": abs(b - a),
        })

        if f_c == 0:  # Akar ditemukan
            break

        if f_prod < 0:
            b = c
        else:
            a = c
    return results

# Halaman utama
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

# Halaman hasil
@app.route("/result", methods=["POST"])
def result():
    user_function = request.form["function"]
    method = request.form["method"]
    a = float(request.form["a"])
    b = float(request.form["b"])
    iterations = int(request.form["iterations"])

    parsed_function = parse_function(user_function)

    try:
        f_a, f_b = validate_bracket(parsed_function, a, b)

        if method == "bisection":
            results = bisection_method(parsed_function, a, b, iterations)
        elif method == "regula_falsi":
            results = regula_falsi_method(parsed_function, a, b, iterations)
        else:
            raise ValueError("Metode tidak valid.")

    except ValueError as e:
        return render_template("result.html", error=str(e))

    return render_template("result.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
