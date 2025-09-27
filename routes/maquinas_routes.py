# routes/maquinas_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from supabase_client import supabase

maquinas_bp = Blueprint("maquinas", __name__, url_prefix="/maquinas")

@maquinas_bp.route("/", methods=["GET"])
def index():
    res = supabase.table("maquinas").select("*").order("id", desc=False).execute()
    maquinas = res.data or []
    return render_template("maquinas/index.html", maquinas=maquinas)

@maquinas_bp.route("/crear", methods=["GET","POST"])
def crear():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        nro_serie = request.form.get("nro_serie")
        area_id = request.form.get("area_id") or None
        supabase.table("maquinas").insert({
            "nombre": nombre, "marca": marca, "modelo": modelo,
            "nro_serie": nro_serie, "area_id": area_id
        }).execute()
        flash("Máquina creada", "success")
        return redirect(url_for("maquinas.index"))
    # GET -> formulario
    # opcional: cargar areas para select
    areas = (supabase.table("areas").select("*").order("nombre", desc=False).execute().data) or []
    return render_template("maquinas/form.html", maquina=None, areas=areas)

@maquinas_bp.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        nro_serie = request.form.get("nro_serie")
        area_id = request.form.get("area_id") or None
        supabase.table("maquinas").update({
            "nombre": nombre, "marca": marca, "modelo": modelo, "nro_serie": nro_serie, "area_id": area_id
        }).eq("id", id).execute()
        flash("Máquina actualizada", "success")
        return redirect(url_for("maquinas.index"))
    # GET -> obtener datos existentes
    r = supabase.table("maquinas").select("*").eq("id", id).single().execute()
    maquina = r.data
    areas = (supabase.table("areas").select("*").order("nombre", desc=False).execute().data) or []
    if not maquina:
        flash("Máquina no encontrada", "warning")
        return redirect(url_for("maquinas.index"))
    return render_template("maquinas/form.html", maquina=maquina, areas=areas)

@maquinas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    supabase.table("maquinas").delete().eq("id", id).execute()
    flash("Máquina eliminada", "info")
    return redirect(url_for("maquinas.index"))
