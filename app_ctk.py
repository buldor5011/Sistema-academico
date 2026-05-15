"""
app_ctk.py – Interfaz gráfica del Sistema Académico construida con CustomTkinter.

Flujo de uso:
    1. Ingresar el número de documento y presionar "Buscar Estudiante".
    2. Si el estudiante existe, se habilitan los campos del formulario.
    3. Completar materia, notas y asistencia, luego presionar "Calcular".
    4. Presionar "Ingresar Datos Nuevos" para reiniciar el formulario.
"""

import customtkinter as ctk
from logica import buscar_estudiante, ASIGNATURAS, validar_nota, validar_asistencia, calcular_estado


def buscar():
    """Busca al estudiante por documento y habilita el formulario si es encontrado.

    Lee el documento ingresado en entry_doc y consulta la base de datos mediante
    buscar_estudiante(). Si el estudiante existe, muestra su nombre en entry_nombre
    y activa los campos de captura de datos llamando a _habilitar_formulario(True).
    Si no existe, muestra un mensaje de error y mantiene el formulario deshabilitado.
    """
    doc = entry_doc.get().strip()
    nombre = buscar_estudiante(doc)
    if not nombre:
        lbl_resultado.configure(text="Estudiante no encontrado", text_color="red")
        _habilitar_formulario(False)
        return
    entry_nombre.configure(state="normal")
    entry_nombre.delete(0, "end")
    entry_nombre.insert(0, nombre)
    entry_nombre.configure(state="disabled")
    lbl_resultado.configure(text="Estudiante encontrado. Complete los datos.", text_color="green")
    _habilitar_formulario(True)


def _habilitar_formulario(habilitar):
    """Habilita o deshabilita todos los campos del formulario de notas.

    Cambia el estado interactivo de combo_materia, n1, n2, n3, entry_asis y
    btn_calcular según el valor de habilitar. Cuando se deshabilita, también
    oculta btn_nuevo del layout usando pack_forget().

    Args:
        habilitar (bool): True para activar los campos, False para desactivarlos.
    """
    estado = "normal" if habilitar else "disabled"
    combo_materia.configure(state=estado)
    n1.configure(state=estado)
    n2.configure(state=estado)
    n3.configure(state=estado)
    entry_asis.configure(state=estado)
    btn_calcular.configure(state=estado)
    if not habilitar:
        btn_nuevo.pack_forget()


def calcular():
    """Valida los datos del formulario y calcula el estado académico del estudiante.

    Convierte los valores de n1, n2, n3 y entry_asis a float y los valida con
    validar_nota() y validar_asistencia(). Si los rangos son correctos, llama a
    calcular_estado() y muestra el promedio y el veredicto en lbl_resultado.
    Al finalizar con éxito, hace visible btn_nuevo en el layout.
    Si algún campo no es numérico o está vacío, muestra un mensaje de error genérico.
    """
    try:
        notas = [float(n1.get()), float(n2.get()), float(n3.get())]
        asis = float(entry_asis.get())
        if not all(validar_nota(n) for n in notas) or not validar_asistencia(asis):
            lbl_resultado.configure(text="Datos inválidos (0-5 notas, 0-100 asistencia)", text_color="orange")
            return
        prom, msg, color = calcular_estado(notas, asis)
        lbl_resultado.configure(text=f"Promedio: {prom:.2f} - {msg}", text_color=color)
        btn_nuevo.pack(pady=10)
    except:
        lbl_resultado.configure(text="Complete todos los campos", text_color="orange")


def limpiar():
    """Reinicia todos los campos del formulario a su estado inicial vacío.

    Borra el documento, el nombre, las tres notas, el porcentaje de asistencia
    y el mensaje de resultado. Restablece el ComboBox a la primera asignatura
    y deshabilita el formulario llamando a _habilitar_formulario(False),
    lo que también retira btn_nuevo del layout.
    """
    entry_doc.delete(0, "end")
    entry_nombre.configure(state="normal")
    entry_nombre.delete(0, "end")
    entry_nombre.configure(state="disabled")
    n1.delete(0, "end")
    n2.delete(0, "end")
    n3.delete(0, "end")
    entry_asis.delete(0, "end")
    combo_materia.set(ASIGNATURAS[0])
    lbl_resultado.configure(text="")
    _habilitar_formulario(False)


# ---------------------------------------------------------------------------
# Configuración de la ventana principal
# ---------------------------------------------------------------------------
app = ctk.CTk()
app.title("Sistema Académico - CustomTkinter")
app.geometry("400x620")

# --- Sección: búsqueda de estudiante ---
ctk.CTkLabel(app, text="Documento:").pack(pady=5)
entry_doc = ctk.CTkEntry(app)
entry_doc.pack()

ctk.CTkButton(app, text="Buscar Estudiante", command=buscar).pack(pady=8)

ctk.CTkLabel(app, text="Nombre Estudiante:").pack(pady=5)
entry_nombre = ctk.CTkEntry(app, state="disabled")
entry_nombre.pack()

# --- Sección: datos académicos (inicia deshabilitada) ---
ctk.CTkLabel(app, text="Materia:").pack(pady=5)
combo_materia = ctk.CTkComboBox(app, values=ASIGNATURAS, state="disabled")
combo_materia.pack()

ctk.CTkLabel(app, text="Notas (1, 2 y 3):").pack(pady=5)
frame_notas = ctk.CTkFrame(app, fg_color="transparent")
frame_notas.pack()
n1 = ctk.CTkEntry(frame_notas, width=50, state="disabled")
n2 = ctk.CTkEntry(frame_notas, width=50, state="disabled")
n3 = ctk.CTkEntry(frame_notas, width=50, state="disabled")
n1.pack(side="left", padx=5); n2.pack(side="left", padx=5); n3.pack(side="left", padx=5)

ctk.CTkLabel(app, text="Asistencia (%):").pack(pady=5)
entry_asis = ctk.CTkEntry(app, state="disabled")
entry_asis.pack()

# --- Sección: acciones y resultado ---
btn_calcular = ctk.CTkButton(app, text="Calcular", command=calcular, state="disabled")
btn_calcular.pack(pady=15)

lbl_resultado = ctk.CTkLabel(app, text="", font=("Arial", 14, "bold"), wraplength=360)
lbl_resultado.pack()

# btn_nuevo se añade al layout dinámicamente desde calcular() y se retira desde _habilitar_formulario()
btn_nuevo = ctk.CTkButton(app, text="Ingresar Datos Nuevos", command=limpiar, fg_color="gray")

app.mainloop()
