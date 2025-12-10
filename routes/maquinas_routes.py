# routes/maquinas_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from supabase_client import supabase
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from datetime import datetime, date, timedelta

maquinas_bp = Blueprint("maquinas", __name__, url_prefix="/maquinas")

# NOTA: no uso helpers aquí para evitar incompatibilidades de firma.
# Haré el cálculo de estado localmente con reglas simples.

# ===========================
# LISTAR MÁQUINAS (INDEX)
# ===========================
@maquinas_bp.route("/")
def index():
    # Traer máquinas
    maquinas = supabase.table("maquinas").select("*").order("id", desc=False).execute().data or []

    # Traer todas las piezas_instaladas
    piezas_inst = supabase.table("piezas_instaladas").select("*").execute().data or []

    # Mapear piezas_instaladas por maquina
    piezas_por_maquina = {}
    for inst in piezas_inst:
        piezas_por_maquina.setdefault(inst["maquina_id"], []).append(inst)

    # Traer stock (view)
    stock = supabase.table("stock").select("*").order("nombre", desc=False).execute().data or []

    maquinas_final = []
    for m in maquinas:
        lista_inst = piezas_por_maquina.get(m["id"], [])

        piezas_info = []
        for inst in lista_inst:
            # Obtener datos de la pieza (nombre, vida_dias) desde tabla piezas
            pieza = supabase.table("piezas").select("nombre, vida_dias").eq("id", inst.get("pieza_id")).single().execute().data or {}
            nombre_pieza = pieza.get("nombre", "Pieza desconocida")
            vida_dias = inst.get("vida_dias") or pieza.get("vida_dias") or 0

            # calcular dias_restantes desde fecha_caducidad (si existe) o desde fecha_instalacion+vida
            dias_restantes = None
            estado_color = "secondary"
            estado_texto = "Sin datos"
            fecha_cad = inst.get("fecha_caducidad")
            try:
                if fecha_cad:
                    # fecha_cad puede venir como 'YYYY-MM-DD' string
                    if isinstance(fecha_cad, str):
                        fc = datetime.fromisoformat(fecha_cad).date()
                    elif isinstance(fecha_cad, datetime):
                        fc = fecha_cad.date()
                    else:
                        fc = fecha_cad
                    hoy = date.today()
                    dias_restantes = (fc - hoy).days

                    # Reglas simples:
                    if dias_restantes < 0:
                        estado_color = "dark"  # rota / vencida
                        estado_texto = "Vencida"
                    elif dias_restantes <= 15:
                        estado_color = "danger"
                        estado_texto = "Crítica"
                    elif dias_restantes <= 30:
                        estado_color = "warning"
                        estado_texto = "Advertencia"
                    else:
                        estado_color = "success"
                        estado_texto = "Óptima"
                else:
                    # si no hay fecha_caducidad, se intenta calcular desde fecha_instalacion
                    fecha_inst = inst.get("fecha_instalacion")
                    if fecha_inst and vida_dias:
                        if isinstance(fecha_inst, str):
                            fi = datetime.fromisoformat(fecha_inst).date()
                        elif isinstance(fecha_inst, datetime):
                            fi = fecha_inst.date()
                        else:
                            fi = fecha_inst
                        fc = fi + timedelta(days=int(vida_dias))
                        hoy = date.today()
                        dias_restantes = (fc - hoy).days
                        if dias_restantes < 0:
                            estado_color = "dark"
                            estado_texto = "Vencida"
                        elif dias_restantes <= 15:
                            estado_color = "danger"
                            estado_texto = "Crítica"
                        elif dias_restantes <= 30:
                            estado_color = "warning"
                            estado_texto = "Advertencia"
                        else:
                            estado_color = "success"
                            estado_texto = "Óptima"
            except Exception:
                dias_restantes = None
                estado_color = "secondary"
                estado_texto = "Sin datos"

            piezas_info.append({
                "pieza_id": inst.get("pieza_id"),
                "nombre": nombre_pieza,
                "fecha_instalacion": inst.get("fecha_instalacion"),
                "vida_dias": vida_dias,
                "fecha_caducidad": inst.get("fecha_caducidad"),
                "dias_restantes": dias_restantes,
                "estado_color": estado_color,
                "estado_texto": estado_texto,
                "rota": inst.get("rota", False),
                "notas": inst.get("notas", "")
            })

        # calcular estado general de la maquina: prioridad dark > danger > warning > success
        colores = [p.get("estado_color") for p in piezas_info]
        if "dark" in colores:
            estado_texto = "Pieza vencida/rota"
            estado_color = "dark"
        elif "danger" in colores:
            estado_texto = "Crítica"
            estado_color = "danger"
        elif "warning" in colores:
            estado_texto = "Advertencia"
            estado_color = "warning"
        elif "success" in colores and colores:
            estado_texto = "Óptima"
            estado_color = "success"
        else:
            estado_texto = "Sin piezas"
            estado_color = "secondary"

        m["estado"] = estado_texto
        m["estado_color"] = estado_color
        m["piezas"] = piezas_info

        maquinas_final.append(m)

    return render_template("maquinas/index.html", maquinas=maquinas_final, stock=stock)


# ==========================================================
# INSTALAR PIEZA (POST desde modal en index)
# ==========================================================
@maquinas_bp.route("/instalar", methods=["POST"])
def instalar():
    try:
        maquina_id = int(request.form.get("maquina_id"))
        pieza_id = int(request.form.get("pieza_id"))
        vida_dias = int(request.form.get("vida_dias") or 0)
    except Exception:
        flash("Datos inválidos para instalar pieza", "danger")
        return redirect(url_for("maquinas.index"))

    fecha_inst = date.today()
    fecha_cad = fecha_inst + timedelta(days=vida_dias)

    supabase.table("piezas_instaladas").insert({
        "maquina_id": maquina_id,
        "pieza_id": pieza_id,
        "fecha_instalacion": fecha_inst.isoformat(),
        "vida_dias": vida_dias,
        "fecha_caducidad": fecha_cad.isoformat(),
        "rota": False,
        "notas": ""
    }).execute()

    flash("Pieza instalada correctamente", "success")
    return redirect(url_for("maquinas.index"))


# ==========================================================
# CREAR - EDITAR - ELIMINAR - PDF (sin areas)
# ==========================================================
@maquinas_bp.route("/crear", methods=["GET","POST"])
def crear_maquina():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        nro_serie = request.form.get("nro_serie")
        descripcion = request.form.get("descripcion") or ""

        supabase.table("maquinas").insert({
            "nombre": nombre,
            "marca": marca,
            "modelo": modelo,
            "nro_serie": nro_serie,
            "descripcion": descripcion
        }).execute()

        flash("Máquina creada", "success")
        return redirect(url_for("maquinas.index"))

    return render_template("maquinas/form.html", maquina=None)


@maquinas_bp.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        nro_serie = request.form.get("nro_serie")
        descripcion = request.form.get("descripcion") or ""

        supabase.table("maquinas").update({
            "nombre": nombre,
            "marca": marca,
            "modelo": modelo,
            "nro_serie": nro_serie,
            "descripcion": descripcion
        }).eq("id", id).execute()

        flash("Máquina actualizada", "success")
        return redirect(url_for("maquinas.index"))

    maquina = supabase.table("maquinas").select("*").eq("id", id).single().execute().data
    if not maquina:
        flash("Máquina no encontrada", "warning")
        return redirect(url_for("maquinas.index"))
    return render_template("maquinas/form.html", maquina=maquina)


@maquinas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    supabase.table("maquinas").delete().eq("id", id).execute()
    flash("Máquina eliminada", "info")
    return redirect(url_for("maquinas.index"))


# ==========================================================
# PDF
# ==========================================================
@maquinas_bp.route("/pdf_reporte")
def pdf_reporte():
    try:
        response = supabase.table("maquinas").select("*").execute()
        maquinas = response.data
    except Exception:
        maquinas = []

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 750, "Reporte de Máquinas")
    p.setFont("Helvetica", 10)
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    p.drawString(50, 730, f"Generado el: {fecha_hora}")

    y = 700
    p.setFont("Helvetica", 10)

    if not maquinas:
        p.drawString(50, y, "ATENCIÓN: No hay datos de máquinas para mostrar.")
    else:
        for m in maquinas:
            descripcion = (m.get("descripcion") or "").replace("\n", " ")
            linea = f"ID: {m.get('id','')} | Nombre: {m.get('nombre','')} | Desc: {descripcion}"
            if len(linea) > 120:
                linea = linea[:117] + "..."
            p.drawString(50, y, linea)
            y -= 20
            if y < 60:
                p.showPage()
                p.setFont("Helvetica-Bold", 16)
                p.drawString(200, 750, "Reporte de Máquinas")
                p.setFont("Helvetica", 10)
                p.drawString(50, 730, f"Generado el: {fecha_hora}")
                y = 700

    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="reporte_maquinas.pdf", mimetype="application/pdf")
