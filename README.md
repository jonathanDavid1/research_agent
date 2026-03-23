# 🔬 AI Research Planner & Executor Agent
### Powered by Gemini 2.5 Flash & Google Search Grounding

Este proyecto implementa un agente de investigación autónomo de tres fases que utiliza la **Gemini Interactions API** para realizar búsquedas técnicas en tiempo real, sintetizar hallazgos y generar reportes ejecutivos. A diferencia de los sistemas lineales, este flujo gestiona el estado de la conversación de forma persistente y encadena tareas de búsqueda profunda.

## 🚀 Arquitectura del Sistema

El agente opera bajo un flujo de trabajo de **encadenamiento de interacciones** (interaction chaining):

1.  **Phase 1: Strategic Planning**
    * Utiliza `gemini-2.5-flash` para desglosar objetivos complejos en tareas atómicas.
    * Implementa **Google Search Grounding** para validar la relevancia de las tareas con datos actuales.
2.  **Phase 2: Deep Research Execution**
    * Ejecución de tareas en segundo plano (`background=True`).
    * Navegación y extracción de fuentes web para recopilar evidencia técnica detallada.
3.  **Phase 3: Executive Synthesis**
    * Refinamiento de datos crudos en un reporte estructurado (Summary, Findings, Recommendations, Risks).
    * Gestión de contexto mediante `previous_interaction_id` para mantener la coherencia semántica entre fases.

## 🛠️ Stack Técnico

* **Engine:** Google Gemini 2.5 Flash (Optimizado para baja latencia y alta ventana de contexto).
* **Interface:** Streamlit (Dashboard reactivo para monitoreo de tareas y visualización de resultados).
* **Infrastructure:** Entorno contenedorizado con Docker para despliegue consistente en Linux/WSL.
* **SDK:** `google-genai` para la orquestación de interacciones de IA.

## 🐳 Despliegue con Docker

Para mantener el entorno aislado y garantizar la portabilidad entre diferentes distribuciones de Linux o entornos WSL, el proyecto utiliza una arquitectura de contenedores.

**Construcción de la imagen:**
```bash
docker build -t research-agent .
