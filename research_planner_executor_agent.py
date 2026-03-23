import streamlit as st, time, re
from google import genai

def get_text(outputs): 
    return "\n".join(o.text for o in (outputs or []) if hasattr(o, 'text') and o.text) or ""

def parse_tasks(text):
    return [{"num": m.group(1), "text": m.group(2).strip().replace('\n', ' ')} 
            for m in re.finditer(r'^(\d+)[\.\)\-]\s*(.+?)(?=\n\d+[\.\)\-]|\n\n|\Z)', text, re.MULTILINE | re.DOTALL)]

def wait_for_completion(client, iid, timeout=300):
    progress, status, elapsed = st.progress(0), st.empty(), 0
    while elapsed < timeout:
        interaction = client.interactions.get(iid)
        if interaction.status != "in_progress": 
            progress.progress(100)
            return interaction
        elapsed += 3
        progress.progress(min(90, int(elapsed/timeout*100)))
        status.text(f"⏳ {elapsed}s...")
        time.sleep(3)
    return client.interactions.get(iid)

# Configuración de la página
st.set_page_config(page_title="Research Planner", page_icon="🔬", layout="wide")
st.title("🔬 AI Research Planner & Executor (Gemini 2.5 Flash Edition) ✨")

# Inicialización del estado de la sesión
for k in ["plan_id", "plan_text", "tasks", "research_id", "research_text", "synthesis_text", "infographic"]:
    if k not in st.session_state: st.session_state[k] = [] if k == "tasks" else None

with st.sidebar:
    api_key = st.text_input("🔑 Google API Key", type="password")
    if st.button("Reset"): 
        for k in ["plan_id", "plan_text", "tasks", "research_id", "research_text", "synthesis_text", "infographic"]:
            st.session_state[k] = [] if k == "tasks" else None
        st.rerun()
    st.markdown("""
    ### Optimización para Free Tier
    - **Modelo:** Gemini 2.5 Flash
    - **Grounding:** Google Search habilitado
    - **Costo:** $0 (Dentro de límites de Google AI Studio)
    """)

client = genai.Client(api_key=api_key) if api_key else None
if not client: 
    st.info("👆 Por favor, ingrese su API Key en el menú lateral para comenzar"); st.stop()

# Fase 1: Planificación
research_goal = st.text_area("📝 Objetivo de Investigación", placeholder="Ej: Investigar el mercado de energía solar en Colombia 2026")
if st.button("📋 Generar Plan", disabled=not research_goal, type="primary"):
    with st.spinner("Planificando con Gemini 2.5 Flash..."):
        try:
            # Cambio a gemini-2.5-flash
            i = client.interactions.create(
                model="gemini-2.5-flash", 
                input=f"Create a numbered research plan for: {research_goal}\n\nFormat: 1. [Task] - [Details]\n\nInclude 5-8 specific tasks.", 
                tools=[{"type": "google_search"}], 
                store=True
            )
            st.session_state.plan_id, st.session_state.plan_text, st.session_state.tasks = i.id, get_text(i.outputs), parse_tasks(get_text(i.outputs))
        except Exception as e: st.error(f"Error en Planificación: {e}")

# Fase 2: Selección e Investigación
if st.session_state.plan_text:
    st.divider(); st.subheader("🔍 Seleccionar Tareas e Investigar")
    selected = [f"{t['num']}. {t['text']}" for t in st.session_state.tasks if st.checkbox(f"**{t['num']}.** {t['text']}", True, key=f"t{t['num']}")]
    st.caption(f"✅ {len(selected)}/{len(st.session_state.tasks)} seleccionadas")
    
    if st.button("🚀 Iniciar Investigación Profunda", type="primary", disabled=not selected):
        with st.spinner("Investigando (esto puede tardar unos minutos)..."):
            try:
                # Usamos el modelo 2.5 Flash en lugar del agente Pro para asegurar gratuidad
                i = client.interactions.create(
                    model="gemini-2.5-flash", 
                    input=f"Research these tasks thoroughly with sources and real-time data:\n\n" + "\n\n".join(selected), 
                    previous_interaction_id=st.session_state.plan_id, 
                    tools=[{"type": "google_search"}],
                    background=True, 
                    store=True
                )
                i = wait_for_completion(client, i.id)
                st.session_state.research_id, st.session_state.research_text = i.id, get_text(i.outputs) or f"Status: {i.status}"
                st.rerun()
            except Exception as e: st.error(f"Error en Investigación: {e}")

if st.session_state.research_text:
    st.divider(); st.subheader("📄 Resultados de la Investigación"); st.markdown(st.session_state.research_text)

# Fase 3: Síntesis
if st.session_state.research_id:
    if st.button("📊 Generar Reporte Ejecutivo", type="primary"):
        with st.spinner("Sintetizando reporte final..."):
            try:
                # Cambio a gemini-2.5-flash para el reporte final
                i = client.interactions.create(
                    model="gemini-2.5-flash", 
                    input=f"Create a professional executive report with Summary, Findings, Recommendations, and Risks based on:\n\n{st.session_state.research_text}", 
                    previous_interaction_id=st.session_state.research_id, 
                    store=True
                )
                st.session_state.synthesis_text = get_text(i.outputs)
                st.rerun()
            except Exception as e: st.error(f"Error en Síntesis: {e}")

if st.session_state.synthesis_text:
    st.divider(); st.markdown("## 📊 Reporte Ejecutivo Final")
    st.markdown(st.session_state.synthesis_text)
    st.download_button("📥 Descargar Reporte (Markdown)", st.session_state.synthesis_text, "research_report.md", "text/markdown")

st.divider(); st.caption("Desarrollado con Gemini 2.5 Flash API")