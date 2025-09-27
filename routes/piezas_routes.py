# routes/piezas_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from supabase_client import supabase

piezas_bp = Blueprint("piezas", __name__, url_prefix="/piezas")

@piezas_bp.route("/", methods=["GET"])
def index():
    res = supabase.table("piezas").select("*").order("id", desc=False).execute()
    piezas = res.data or []
    # enriquecer con fabricante y material
    for p in piezas:
        fab = supabase.table("fabricantes").select("nombre").eq("id", p.get("fabricante_id")).single().execute()
        mat = supabase.table("materiales").select("nombre").eq("id", p.get("material_id")).single().execute()
        p["fabricante"] = fab.data.get("nombre") if fab and fab.data else "N/A"
        p["material"] = mat.data.get("nombre") if mat and mat.data else "N/A"
    return render_template("piezas/index.html", piezas=piezas)

@piezas_bp.route("/crear", methods=["GET","POST"])
def crear():
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "fabricante_id": request.form.get("fabricante_id") or None,
            "material_id": request.form.get("material_id") or None,
            "vida_horas": request.form.get("vida_horas") or None,
            "imagen_url": request.form.get("imagen_url") or None
        }
        supabase.table("piezas").insert(data).execute()
        flash("Pieza creada", "success")
        return redirect(url_for("piezas.index"))
    fabricantes = supabase.table("fabricantes").select("*").order("nombre").execute().data or []
    materiales = supabase.table("materiales").select("*").order("nombre").execute().data or []
    return render_template("piezas/form.html", pieza=None, fabricantes=fabricantes, materiales=materiales)

@piezas_bp.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "fabricante_id": request.form.get("fabricante_id") or None,
            "material_id": request.form.get("material_id") or None,
            "vida_horas": request.form.get("vida_horas") or None,
            "imagen_url": request.form.get("imagen_url") or None
        }
        supabase.table("piezas").update(data).eq("id", id).execute()
        flash("Pieza actualizada", "success")
        return redirect(url_for("piezas.index"))
    pieza = supabase.table("piezas").select("*").eq("id", id).single().execute().data
    fabricantes = supabase.table("fabricantes").select("*").order("nombre").execute().data or []
    materiales = supabase.table("materiales").select("*").order("nombre").execute().data or []
    return render_template("piezas/form.html", pieza=pieza, fabricantes=fabricantes, materiales=materiales)

@piezas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    supabase.table("piezas").delete().eq("id", id).execute()
    flash("Pieza eliminada", "info")
    return redirect(url_for("piezas.index"))
