# DYNAFOLD HUB — Plan Estratégico Maestro

> **PARA CLAUDE EN FUTURAS SESIONES**: Este documento es tu briefing completo. Léelo enteramente antes de tomar cualquier acción. Contiene toda la historia del proyecto, las decisiones tomadas, el plan actual, y las instrucciones específicas para trabajar conmigo (Sergio León, fundador).

**Fecha de creación**: 2026-05-24
**Última actualización**: 2026-05-24
**Versión**: 1.0
**Idioma**: Español (con términos técnicos en inglés)
**Estado**: Plan aprobado, ejecución pendiente

---

## 📑 ÍNDICE

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Historia del Proyecto](#2-historia-del-proyecto)
3. [Por qué pivotamos a DYNAFOLD Hub](#3-por-qué-pivotamos)
4. [Visión y Estrategia](#4-visión-y-estrategia)
5. [Arquitectura del Producto](#5-arquitectura-del-producto)
6. [Stack Tecnológico](#6-stack-tecnológico)
7. [Plan Fase 1 — MVP (4 semanas)](#7-plan-fase-1-mvp)
8. [Roadmap Fases 2-3 (meses 2-12)](#8-roadmap)
9. [Estructura del Repositorio](#9-estructura-del-repositorio)
10. [Workflow de Desarrollo](#10-workflow-de-desarrollo)
11. [Decisiones Clave Documentadas](#11-decisiones-clave)
12. [Assets Existentes a Reusar](#12-assets-existentes)
13. [Decisiones de Infraestructura](#13-infraestructura)
14. [Métricas de Éxito](#14-métricas-de-éxito)
15. [Modelos a Integrar (catálogo)](#15-modelos-a-integrar)
16. [Recursos y Enlaces](#16-recursos)
17. [Instrucciones Específicas para Claude](#17-instrucciones-para-claude)

---

## 1. RESUMEN EJECUTIVO

### Lo que somos
**DYNAFOLD Hub** es una plataforma open source + SaaS que da acceso unificado a TODOS los modelos open source de AI para drug discovery (AlphaFold 3, Chai-1/2, Boltz-2, OpenFold3, Protenix, RFdiffusion, ProteinMPNN, ESM3, etc.), los compara automáticamente, y construye workflows pre-configurados para tareas comunes en descubrimiento de fármacos.

### El problema que resolvemos
Existen 30+ modelos SOTA open source en bio AI, pero:
- Cada uno tiene su propio repositorio, dependencias, formatos de input/output
- Setear UN modelo toma 2-4 semanas a un investigador
- No hay forma sistemática de comparar modelos o usar varios en consenso
- Los workflows complejos (ej: diseño de anticuerpos completo) requieren código custom
- Las biotechs pequeñas no pueden permitirse esta complejidad técnica

### La oportunidad
Cuando hay proliferación de modelos competitivos, la capa de orquestación captura más valor que los modelos:
- **HuggingFace** (NLP) → $4.5B valoración
- **LangChain** (LLM apps) → $1.1B
- **Replicate** (AI models APIs) → $350M
- **DYNAFOLD Hub** (bio AI) → oportunidad equivalente, todavía SIN OCUPAR

### Tamaño del mercado
- TAM: $500M-$2B/año (drug discovery software market)
- SAM: ~5,000-15,000 empresas globalmente
- SOM realista año 3: 1-5% = $5-50M ARR

### Modelo de negocio
- **Tier gratuito**: 10 calls/día, modelos básicos (capta usuarios)
- **Pro ($99/mes)**: 1000 calls/día, workflows premium
- **Team ($499/mes)**: 10000 calls/día, MD validation
- **Enterprise (custom)**: Deployments privados, modelos custom, soporte dedicado

### Proyección financiera (sin BS)
| Año | Usuarios | ARR | Etapa |
|-----|----------|-----|-------|
| 1 | 10K free + 50-100 paying | $200-300K | Bootstrap |
| 2 | 50K + 500 paying | $1-2M | Seed |
| 3 | 200K + 2000 paying | $5-15M | Series A |
| Exit | — | — | $50M-$500M en 4-6 años |

---

## 2. HISTORIA DEL PROYECTO

### Origen
Sergio León (CEO) fundó DYNAFOLD inicialmente con la hipótesis:
> "Simulaciones MD de 50ns con un Dynamic Confidence Score (DCS) superan a AutoDock Vina (docking estático) en >15% AUC para predecir actividad biológica"

### Validación realizada (mayo 2026)
- **Target estudiado**: SARS-CoV-2 Mpro (proteína 6LU7)
- **Dataset**: COVID Moonshot, 25 compuestos × 3 réplicas = 75 simulaciones
- **Pipeline construido**: GROMACS + AutoDock Vina + CHARMM36m + ACPYPE + MM-GBSA
- **Coste total**: ~$240 USD en GPU (Verda RTX 6000 Ada)
- **Tiempo total**: ~3 semanas

### Resultados (negative result)
| Método | AUC | Resultado |
|--------|-----|-----------|
| Vina (baseline) | **0.7436** | Decente |
| DCS original | 0.4679 | -37% vs Vina ❌ |
| MM-GBSA (gold standard) | 0.5577 | -25% vs Vina ❌ |
| ML con 34 features (LOOCV) | 0.7500 | +0.9% NO significativo ❌ |

**Veredicto científico**: POST-MORTEM. Para SARS-CoV-2 Mpro, MD-based scoring NO supera al docking estático. Las métricas dinámicas que diseñamos premiaban "estabilidad en bolsillo" cuando los inhibidores reales son más dinámicos.

### Lecciones aprendidas
1. **Pipeline técnico funciona** (reproducibilidad σ=0.01)
2. **Mpro NO es el target correcto** para demostrar valor de MD
3. **Métricas hand-crafted son arbitrarias** sin calibración data-driven
4. **N=25 es demasiado pequeño** para ML serio
5. **El paradigma MD está siendo superado** por foundation models (AlphaFold 3, Chai)

---

## 3. POR QUÉ PIVOTAMOS

### El cambio de paradigma
**Mayo 2024**: DeepMind lanza AlphaFold 3 — predice complejos proteína-ligando directamente.
**Sept 2024**: Chai-1 (open source) iguala AF3 en PoseBusters benchmark.
**Junio 2025**: Chai-2 logra de novo antibody design con 16-20% hit rate.

**Implicación**: el enfoque MD-only que intentábamos ya estaba siendo obsoletado mientras lo construíamos.

### Lo que NOS PASÓ vs lo que está pasando en el mercado
- Nosotros: 3 semanas construyendo pipeline MD para 1 target
- Chai Discovery: $1.3B valoración haciendo foundation models
- AlphaFold 3: hace en SEGUNDOS lo nuestro tarda 4 HORAS

### Insight clave de Sergio (24-may-2026)
Tras investigar el ecosistema, identificó que hay 30+ modelos open source (Chai-1, Chai-2, Boltz-1/2, OpenFold3, Protenix, RFdiffusion, ProteinMPNN, ESM3, etc.), pero:
- No hay plataforma que los unifique
- No hay forma sencilla de compararlos
- No hay workflows estándar para drug discovery completo

### La nueva tesis
> "No construyamos otro modelo. Construyamos la PLATAFORMA que orquesta todos los modelos open source de bio AI. Como HuggingFace pero para drug discovery."

---

## 4. VISIÓN Y ESTRATEGIA

### Visión a 5 años
**Ser la infraestructura por defecto para acceso, comparación y orquestación de modelos AI de drug discovery, usado por >100K investigadores y >1000 empresas biotech.**

### Misión
Democratizar el acceso a modelos SOTA de bio AI eliminando la complejidad técnica que actualmente limita su adopción a labs con grandes equipos de computational biology.

### Valores
1. **Open source first**: el código core es abierto, construimos comunidad
2. **Model-agnostic**: no favorecemos a ningún model maker, somos neutrales
3. **Honestidad científica**: publicamos negative results, no exageramos capacidades
4. **Pragmatismo**: priorizamos lo que resuelve problemas reales, no lo que es "sexy"

### Estrategia de mercado

#### Fase de adopción (años 1-2)
- Captar académicos y biotechs pequeñas con tier gratuito
- Construir comunidad open source en GitHub
- Generar contenido técnico de alta calidad
- Conseguir 1-2 design partners enterprise para validar

#### Fase de crecimiento (años 2-4)
- Monetizar con tier Pro/Team
- Lanzar marketplace de workflows
- Partnerships con cloud providers (NVIDIA, Google Cloud)
- Considerar funding (Seed Round ~$1-2M)

#### Fase de escala (años 4-6)
- Enterprise contracts con Big Pharma
- Posibilidad de adquisición ($50M-$500M)
- O continuación independiente con $5-20M ARR

### Competidores y posicionamiento

| Competidor | Su enfoque | Por qué NO nos amenaza |
|------------|------------|------------------------|
| Schrödinger | Suite enterprise legacy | Caro ($50-200K/año), lento, no es model-agnostic |
| HuggingFace | NLP-first, alguna bio | No tiene profundidad bio-específica |
| Chai/Atomwise/Recursion | Construyen sus modelos | Cada uno vende SU modelo; nosotros vendemos TODOS |
| BioNeMo (NVIDIA) | Enterprise infrastructure | Solo enterprise + caro; nosotros SMB + free tier |
| DIY (scripts custom) | Cada investigador | Pierden 4-8h por análisis; nuestra plataforma 5 min |

**Posicionamiento único**:
> "La única plataforma open source que da acceso unificado a TODOS los modelos AI de drug discovery, los compara automáticamente, y construye workflows verticales completos."

---

## 5. ARQUITECTURA DEL PRODUCTO

### Componentes del sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    DYNAFOLD HUB Platform                     │
├─────────────────────────────────────────────────────────────┤
│  Web UI (Streamlit/Gradio)  │  API (FastAPI)                │
├─────────────────────────────────────────────────────────────┤
│              Orchestration Layer (Python)                    │
│  ┌──────────────┬──────────────┬──────────────┐             │
│  │ Smart Router │ Consensus    │ Workflow     │             │
│  │              │ Engine       │ Engine       │             │
│  └──────────────┴──────────────┴──────────────┘             │
├─────────────────────────────────────────────────────────────┤
│                    Model Adapters                            │
│  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐         │
│  │ AF3  │Chai-1│Chai-2│Boltz │RFdiff│ESM3  │ MD   │         │
│  │ API  │local │local │local │local │API   │GROMACS│        │
│  └──────┴──────┴──────┴──────┴──────┴──────┴──────┘         │
├─────────────────────────────────────────────────────────────┤
│  Validation Layer  │  Experiment Designer  │  Visualization │
├─────────────────────────────────────────────────────────────┤
│           Storage (PostgreSQL + S3-compatible)                │
└─────────────────────────────────────────────────────────────┘
```

### Las 5 capas explicadas

**1. Model Adapters**: wrappers Python que normalizan input/output de cada modelo a formato unificado.

**2. Orchestration Layer**:
- **Smart Router**: dado un task, recomienda qué modelo(s) usar
- **Consensus Engine**: corre N modelos, agrega resultados, flagea desacuerdos
- **Workflow Engine**: ejecuta pipelines pre-construidos (drag&drop)

**3. Validation Layer**:
- Análisis de incertidumbre (plDDT, PAE, RMSD intermodelo)
- Recomendaciones experimentales (qué mutar, qué medir)
- MD validation opcional (nuestro pipeline GROMACS existente)

**4. Web UI + API**:
- UI para usuarios no-técnicos (Streamlit)
- API para developers (FastAPI)
- Ambas comparten el mismo backend

**5. Storage**:
- PostgreSQL para metadata, usuarios, billing
- S3-compatible para outputs (estructuras, trayectorias)

### Producto MVP vs producto completo

**MVP (4 semanas)**:
- Web UI con tabs para 3 tareas: structure prediction, docking, antibody design
- Integración con 5 modelos: AF3 (vía API), Chai-1, Boltz-2, ProteinMPNN, Chai-2
- Comparison view side-by-side
- Hosting en HuggingFace Spaces (gratis)

**Producto completo (12 meses)**:
- Todos los componentes de la arquitectura
- 15+ modelos integrados
- 10+ workflows pre-construidos
- API SaaS con billing
- Hosting en cloud con GPU

---

## 6. STACK TECNOLÓGICO

### Lenguaje principal
**Python 3.11+** — estándar de la industria bio AI, todos los modelos open source son Python.

### Frameworks

| Capa | Tecnología | Razón |
|------|-----------|-------|
| Web UI MVP | **Streamlit** | Rápido para prototipar, gratuito, fácil deploy |
| Web UI v2 | Gradio o Next.js | Cuando crezcamos, según necesidades |
| API | **FastAPI** | Rápido, type-safe, OpenAPI nativo |
| Async tasks | **Celery + Redis** | Para tareas largas (predicciones) |
| Database | **PostgreSQL** | Estándar, free, escalable |
| Storage | **S3-compatible (R2/B2)** | Barato, escalable |
| Auth | **GitHub OAuth + Clerk** | Quick start, escalable |

### Bibliotecas científicas

| Propósito | Biblioteca | Razón |
|-----------|-----------|-------|
| Estructuras moleculares | **Biotite** | Más moderna que BioPython |
| Parsing CIF/PDB | **gemmi** | Rápido, mantenido por PDB |
| 3D viz web | **py3Dmol** | PyMOL en navegador |
| 3D viz desktop | **NGLView / Mol*** | Alternativas |
| ML auxiliar | **scikit-learn, PyTorch** | Estándar |
| MD (opcional) | **GROMACS, MDAnalysis** | Ya lo tenemos del proyecto previo |

### Models específicos (cómo integramos cada uno)

| Modelo | Cómo lo integramos | Licencia | Comentarios |
|--------|---------------------|----------|-------------|
| AlphaFold 3 | API (AlphaFold Server) | Free academic, paid commercial | Wrapper REST |
| Chai-1 | Local inference (pip install chai_lab) | Apache 2.0 | GPU recomendado |
| Chai-2 | Local inference | Apache 2.0 | GPU obligatorio |
| Boltz-2 | Local inference (pip install boltz) | MIT | GPU recomendado |
| OpenFold3 | Local inference | Apache 2.0 | A integrar cuando madure |
| Protenix | Local inference | Apache 2.0 | A integrar cuando madure |
| RFdiffusion | Docker container | BSD-3 | Necesita GPU |
| ProteinMPNN | Local inference | MIT | Liviano, corre en CPU |
| LigandMPNN | Local inference | MIT | Variante de ProteinMPNN |
| ESM3 | API (EvolutionaryScale) | Mix | Wrapper REST |
| BindCraft | Pipeline open source | MIT | A integrar Fase 2 |
| IgFold | Local | BSD-3 | Para anticuerpos |
| AntiFold | Local | MIT | Para anticuerpos |
| DiffDock-L | Local | MIT | Para docking |
| NeuralPLexer3 | Eval (open?) | Verificar | A confirmar acceso |
| Evo 2 | Local/API | Apache 2.0 | Para genómica |

### Infrastructure & DevOps

| Componente | Solución | Coste |
|------------|----------|-------|
| Repo público | **GitHub** | Gratis |
| CI/CD | **GitHub Actions** | Gratis hasta 2000 min/mes |
| Hosting MVP | **HuggingFace Spaces** | Gratis (con límites) |
| Hosting v2 | **Render / Railway** | $7-25/mes |
| GPU on-demand | **Modal / RunPod** | Pay-per-use (~$1-3/h) |
| Domain | **Namecheap** | $12/año |
| Analytics | **Plausible** | $9/mes (privacy-friendly) |
| Email | **Resend** | Gratis hasta 3K/mes |
| Error tracking | **Sentry** | Gratis tier |

### Coste mensual estimado (Fase 1)
- Hosting básico: $0-25
- Domain: $1/mes prorrateado
- Analytics: $9
- **Total**: ~$10-35/mes para empezar

---

## 7. PLAN FASE 1 — MVP (4 semanas)

### Objetivo del MVP
Demostrar el VALOR ÚNICO de DYNAFOLD Hub: ejecutar 1 input por 3+ modelos diferentes y ver outputs comparables side-by-side.

### Criterios de "MVP completo"
- [ ] Web app pública accesible 24/7
- [ ] Mínimo 3 modelos integrados (AF3 vía API + Chai-1 local + Boltz-2 local)
- [ ] 1 ejemplo completo funcionando (input → comparison → export)
- [ ] Documentación clara (README + tutorial)
- [ ] Repositorio GitHub público con licencia (MIT o Apache 2.0)
- [ ] Landing page con clear value proposition
- [ ] Métricas de uso instrumentadas (Plausible)

### Cronograma detallado por semana

#### SEMANA 1: Foundation & Architecture

**Día 1-2: Setup proyecto**
```bash
# Acciones concretas:
1. Crear repo en GitHub: dynafold-ai/dynafold-hub (público)
2. Definir licencia: MIT (más permisiva para adopción)
3. Setup Python venv + pyproject.toml
4. Definir estructura de carpetas (ver Sección 9)
5. Configurar pre-commit hooks (black, ruff, mypy)
6. Crear README inicial con vision
7. Configurar GitHub Actions básico (linting)
```

**Día 3-4: Architecture skeleton**
```bash
# Componentes a crear:
src/dynafold_hub/
├── adapters/          # Model wrappers
│   ├── base.py        # Abstract base class
│   ├── alphafold3.py  # AF3 API wrapper
│   ├── chai1.py       # Chai-1 wrapper
│   └── boltz2.py      # Boltz-2 wrapper
├── orchestration/
│   ├── router.py      # Smart routing logic
│   └── consensus.py   # Consensus engine
├── ui/
│   └── app.py         # Streamlit main
└── utils/
    ├── parsers.py     # CIF/PDB parsing
    └── viz.py         # py3Dmol helpers
```

**Día 5-7: First adapter (Chai-1)**
```bash
# Chai-1 es el primero porque:
# - Open source con buena documentación
# - pip installable: pip install chai_lab
# - Funciona en GPU (Modal) o CPU lento

# Tareas:
1. Implementar Chai1Adapter siguiendo BaseModelAdapter
2. Tests unitarios con secuencia mock
3. Probar end-to-end con 1 ejemplo real (e.g., 6LU7 + ligando)
4. Documentar uso en docs/adapters/chai1.md
```

**Entregable Semana 1**: Repo GitHub público + Chai-1 funcionando vía CLI Python

#### SEMANA 2: Multi-Model & UI Básica

**Día 8-10: Más adapters**
```bash
# Añadir:
1. AlphaFold3Adapter (vía AlphaFold Server API)
2. Boltz2Adapter (pip install boltz)
3. Tests unitarios para cada uno
4. Normalización de outputs a formato común (StructurePrediction class)
```

**Día 11-12: Consensus Engine**
```python
# Componente clave: ConsensusEngine
class ConsensusEngine:
    def run_all(self, input_data, models=['af3', 'chai1', 'boltz2']):
        results = {name: self.adapters[name].predict(input_data) for name in models}
        return self.compute_agreement(results)

    def compute_agreement(self, results):
        # Per-residue: RMSD between predicted positions
        # Returns: {'consensus_score': 0-1, 'divergent_regions': [...]}
```

**Día 13-14: Streamlit UI v0.1**
```python
# Single-page MVP:
- Sidebar: Input (sequence + ligand SMILES)
- Main: Tabs por modelo + tab "Consensus"
- Footer: Export buttons (PDB, JSON)
- Loading states con progress bars
```

**Entregable Semana 2**: Web app local que toma input, corre 3 modelos, muestra outputs side-by-side

#### SEMANA 3: Visualization & Polish

**Día 15-17: 3D Viewer integrado**
```python
# Con py3Dmol:
- Cada predicción muestra estructura 3D interactiva
- Color por confidence (plDDT)
- Vista "overlay" para ver consensus
- Highlight de regiones divergentes en rojo
```

**Día 18-19: Recomendaciones experimentales**
```python
# Lógica simple inicial:
def recommend_experiments(consensus_result):
    # Identifica regiones con baja confianza Y alta divergencia
    # Recomienda: mutagenesis dirigida, HDX-MS, SPR, etc.
    # Retorna lista de experimentos con coste/tiempo estimados
```

**Día 20-21: Ejemplos reales y documentación**
```bash
# Crear 3 ejemplos completos en examples/:
1. examples/01_kinase_inhibitor/    (EGFR + Gefitinib)
2. examples/02_protease_drug/       (Mpro + N3 inhibitor) ← podemos reusar 6LU7
3. examples/03_antibody_design/     (PD-L1 + Pembrolizumab)

# Cada ejemplo:
- input.json: datos de entrada
- run.py: cómo correrlo
- expected_output/: resultados esperados
- README.md: explicación
```

**Entregable Semana 3**: UI pulida, 3 ejemplos completos, documentación inicial

#### SEMANA 4: Deploy & Launch

**Día 22-23: Deploy HuggingFace Spaces**
```bash
# HuggingFace Spaces es ideal porque:
# - Gratis para apps open source
# - Audiencia integrada (1M+ devs)
# - SSL automático, dominio incluido
# - Soporta Streamlit nativamente

# Pasos:
1. Crear Space en huggingface.co/spaces/dynafold/hub
2. Configurar app.py compatible con Spaces
3. Push código vía git remote
4. Verificar funcionamiento público
```

**Día 24-25: Landing page**
```bash
# En GitHub Pages o Vercel (gratis):
- Hero section con clear value prop
- 30-second video demo
- "Try it now" → link a Spaces
- 3 ejemplos showcase
- GitHub stars badge
- CTA: "Star on GitHub" + "Try Demo"
```

**Día 26-27: Documentation polish**
```bash
# Crear docs/ con:
- docs/quickstart.md       (5 min tutorial)
- docs/concepts.md         (qué es consensus, etc.)
- docs/adapters/           (cómo añadir nuevos modelos)
- docs/workflows/          (futuros pipelines)
- docs/api.md              (API reference, aunque MVP no la tiene aún)
```

**Día 28-30: LAUNCH**
```bash
# Coordinación de lanzamiento:

DÍA 28 (preparación):
- Twitter thread escrito y schedulado
- LinkedIn post escrito
- Hacker News post draft
- Product Hunt page setup

DÍA 29 (lanzamiento):
- 9:00 PT: Publish HuggingFace Space (peak HF traffic)
- 9:30 PT: Twitter thread + tag @chai_discovery, @demishassabis, @rasmus_lindh
- 10:00 PT: LinkedIn post
- 11:00 PT: Hacker News "Show HN: DYNAFOLD Hub..."
- 12:00 PT: Product Hunt launch
- Throughout: respond to every comment within 1h

DÍA 30 (follow-up):
- Email a 20 biotechs pre-identificadas con personalized message
- Reddit r/bioinformatics post
- ResearchGate update
```

**Entregable Semana 4**: Producto LIVE, lanzado, primeras métricas reales

### Métricas de éxito Semana 4
- 50+ GitHub stars
- 500+ HuggingFace Spaces visits
- 100+ predictions ejecutadas
- 5+ conversaciones con potential customers
- 1+ press mention o tweet de cuenta influyente

---

## 8. ROADMAP FASES 2-3

### FASE 2: Workflows + API (Meses 2-4)

**Mes 2: Más modelos + workflows básicos**
- Integrar 5 modelos más: OpenFold3, Protenix, ProteinMPNN, RFdiffusion, ESM3
- Crear 3 workflows: "Antibody Design", "Kinase Discovery", "Allosteric Site"
- Lanzar API REST (FastAPI) con auth básica

**Mes 3: Tier de pago**
- Implementar billing (Stripe)
- Lanzar Pro tier ($99/mes)
- Migrar de HuggingFace Spaces a Render/Railway (más control)
- Primeros clientes pagando (target: 5-10)

**Mes 4: Pulir + marketing**
- Case studies de primeros usuarios
- Blog posts técnicos (DEV.to, Medium)
- Webinar gratuito sobre "Cómo usar AF3 + Chai-1 juntos"
- Aplicar a YC W27 o IndieBio (opcional)

### FASE 3: Platform & Marketplace (Meses 5-12)

**Mes 5-6: GPU cloud + escalabilidad**
- Partnership con Modal o RunPod para GPU on-demand
- Tier Team ($499/mes) con procesamiento más rápido
- Async task queue (Celery + Redis)
- Target: 50 paying customers

**Mes 7-9: Workflow Marketplace**
- Plataforma para que comunidad suba workflows
- Revenue share con creators (70/30)
- Sello "DYNAFOLD verified" para workflows de calidad
- Target: 100 workflows en marketplace

**Mes 10-12: Enterprise + Funding**
- Lanzar tier Enterprise (custom pricing, $5K-50K/mes)
- 1-3 enterprise contracts firmados
- Considerar levantar Seed Round ($1-3M)
- Target: $1M ARR

### Hitos clave a 12 meses

| Mes | Hito | Métrica |
|-----|------|---------|
| 1 | MVP lanzado | 500 visitas, 50 stars |
| 3 | API + pricing | 10 paying, $1K MRR |
| 6 | Workflows + Pro tier | 100 paying, $10K MRR |
| 9 | Marketplace launch | 50 workflows, $25K MRR |
| 12 | Enterprise + Seed | 200 paying + 3 enterprise, $80K MRR ($1M ARR) |

---

## 9. ESTRUCTURA DEL REPOSITORIO

```
dynafold-hub/
├── CLAUDE.md                       # Este documento (estrategia + briefing)
├── README.md                       # Publico-facing (English)
├── LICENSE                         # MIT
├── pyproject.toml                  # Dependencies + metadata
├── .gitignore
├── .env.example                    # Template para env vars
├── docker-compose.yml              # Para desarrollo local
│
├── docs/                           # Documentación pública
│   ├── quickstart.md
│   ├── concepts.md
│   ├── architecture.md
│   ├── adapters/                   # Cómo añadir nuevos modelos
│   ├── workflows/                  # Workflows disponibles
│   └── api.md                      # API reference
│
├── src/dynafold_hub/               # Código principal
│   ├── __init__.py
│   ├── adapters/                   # Model wrappers
│   │   ├── base.py                 # BaseModelAdapter (ABC)
│   │   ├── alphafold3.py
│   │   ├── chai1.py
│   │   ├── chai2.py
│   │   ├── boltz2.py
│   │   ├── openfold3.py
│   │   ├── protenix.py
│   │   ├── rfdiffusion.py
│   │   ├── proteinmpnn.py
│   │   ├── ligandmpnn.py
│   │   ├── esm3.py
│   │   ├── igfold.py
│   │   ├── antifold.py
│   │   └── md_gromacs.py           # Para validation Fase 2
│   │
│   ├── orchestration/
│   │   ├── router.py               # Smart Router
│   │   ├── consensus.py            # Consensus Engine
│   │   ├── workflows.py            # Workflow definitions
│   │   └── validation.py           # Experimental recommendations
│   │
│   ├── ui/
│   │   ├── app.py                  # Streamlit main
│   │   ├── pages/                  # Multi-page Streamlit
│   │   │   ├── 1_structure.py
│   │   │   ├── 2_docking.py
│   │   │   ├── 3_design.py
│   │   │   └── 4_antibody.py
│   │   └── components/             # Reusable UI components
│   │
│   ├── api/                        # FastAPI (Fase 2)
│   │   ├── main.py
│   │   ├── routers/
│   │   └── auth.py
│   │
│   ├── utils/
│   │   ├── parsers.py              # CIF/PDB/FASTA parsing
│   │   ├── viz.py                  # py3Dmol helpers
│   │   ├── caching.py              # Result caching
│   │   └── benchmarks.py           # Comparison metrics
│   │
│   └── data/                       # Static data
│       ├── pockets.json            # Known binding pockets
│       └── reference_structures/
│
├── tests/                          # Tests
│   ├── unit/
│   │   ├── adapters/
│   │   └── orchestration/
│   ├── integration/
│   └── fixtures/                   # Test data
│
├── examples/                       # Ejemplos completos
│   ├── 01_kinase_inhibitor/
│   ├── 02_protease_drug/
│   └── 03_antibody_design/
│
├── scripts/                        # Scripts útiles
│   ├── benchmark_all_models.py
│   ├── update_model_versions.py
│   └── generate_examples.py
│
└── .github/
    ├── workflows/
    │   ├── ci.yml                  # Linting + tests
    │   ├── docs.yml                # Build docs
    │   └── release.yml             # PyPI release
    └── ISSUE_TEMPLATE/
```

---

## 10. WORKFLOW DE DESARROLLO

### Convenciones de código

```python
# Style: PEP 8 + black formatter
# Type hints: obligatorios en funciones públicas
# Docstrings: Google style
# Tests: pytest, mínimo 70% coverage

# Ejemplo de función bien escrita:
def predict_structure(
    sequence: str,
    model: str = "chai1",
    n_recycles: int = 3,
) -> StructurePrediction:
    """Predict 3D structure of a protein sequence.

    Args:
        sequence: Single-letter amino acid sequence.
        model: Model adapter to use ('af3', 'chai1', 'boltz2').
        n_recycles: Number of recycling iterations.

    Returns:
        StructurePrediction object with coordinates and confidence.

    Raises:
        ModelNotAvailableError: If model adapter not found.
    """
    ...
```

### Git workflow

```bash
# Branch naming:
# - feature/add-boltz2-adapter
# - fix/parsing-bug-cif
# - docs/add-quickstart
# - refactor/consolidate-adapters

# Commit messages (conventional commits):
# feat: add Boltz-2 adapter
# fix: handle empty CIF files in parser
# docs: add quickstart tutorial
# refactor: extract common adapter logic to base class

# PR workflow:
# 1. Create branch from main
# 2. Make changes + tests
# 3. PR with description + screenshots if UI change
# 4. CI must pass (linting + tests)
# 5. Self-merge to main (solo developer initially)
```

### Testing strategy

```python
# Unit tests: cada adapter, cada utility
# Integration tests: workflows completos
# E2E tests: UI básicos con Playwright (Fase 2)

# Ejemplo de test:
def test_chai1_adapter_basic_prediction():
    adapter = Chai1Adapter()
    seq = "MGKSTRYS..."  # Sample sequence
    result = adapter.predict_structure(seq)
    assert result.n_residues == len(seq)
    assert result.confidence_score > 0
```

### Documentación

- **Inline**: docstrings en cada función pública
- **API docs**: auto-generadas con mkdocs + mkdocstrings
- **Tutorials**: en docs/ como Markdown
- **Notebooks**: en examples/ como Jupyter
- **Architecture**: diagrams en docs/architecture.md (Mermaid)

### Deployment workflow

```bash
# Development local:
poetry install
poetry run streamlit run src/dynafold_hub/ui/app.py

# Staging (HuggingFace Spaces):
git push huggingface main

# Production (Render, Fase 2):
git push origin main  # Auto-deploys vía GitHub Actions
```

---

## 11. DECISIONES CLAVE DOCUMENTADAS

> **Importante para Claude**: Este es el "single source of truth" de decisiones tomadas. Antes de proponer cambios estratégicos, lee esta sección.

### Decisión 001: Pivot de DCS/MD-scoring a Orchestration Platform
**Fecha**: 2026-05-24
**Decisor**: Sergio + Claude
**Contexto**: Tras Phase 1 validation, DCS+MD scoring underperformed Vina (AUC 0.47 vs 0.74). MM-GBSA tampoco mejoró (0.56). Hace falta pivot.
**Decisión**: Abandonar la dirección "MD-based scoring better than docking" y pivotar a "orchestration layer para modelos AI de drug discovery".
**Razón**: Hay 30+ modelos open source SOTA (AF3, Chai, Boltz, etc.) y NADIE los unifica. Es la oportunidad HuggingFace-style.
**Status**: ✅ Aprobada y vigente

### Decisión 002: Open source first, MIT license
**Fecha**: 2026-05-24
**Decisor**: Sergio + Claude
**Razón**: Para construir comunidad y adopción rápida. MIT es la más permisiva, facilita uso comercial por usuarios (lo que beneficia el ecosistema).
**Status**: ✅ Aprobada

### Decisión 003: Python como único lenguaje en MVP
**Fecha**: 2026-05-24
**Razón**: Todos los modelos bio AI son Python. Evita complejidad multi-lang.
**Trade-off**: La UI podría ser más rápida con TypeScript/Next.js, pero MVP no lo necesita.
**Status**: ✅ Aprobada

### Decisión 004: Streamlit para MVP, evaluar Gradio/Next.js después
**Fecha**: 2026-05-24
**Razón**: Streamlit es más rápido para prototipar UIs científicas. Gradio es alternativa válida si necesitamos integración HuggingFace más profunda.
**Status**: ✅ Aprobada para MVP

### Decisión 005: HuggingFace Spaces para hosting MVP
**Fecha**: 2026-05-24
**Razón**: Gratis, audiencia integrada (1M+ devs), SSL, fácil deploy.
**Alternativa considerada**: Render/Railway, pero coste >$0 y menor audiencia.
**Status**: ✅ Aprobada para MVP

### Decisión 006: Destruir instancia Verda (no más infraestructura GPU pre-pagada)
**Fecha**: 2026-05-24
**Razón**: $42 restantes en cuenta. Costo idle $21/día. No tenemos uso justificado de GPU dedicada. Cuando necesitemos GPU (para Chai-1/Boltz-2 inference) usaremos GPU on-demand (Modal, RunPod).
**Status**: ⏳ Pendiente acción del usuario en panel Verda

### Decisión 007: NO reusar pipeline GROMACS como producto principal
**Fecha**: 2026-05-24
**Razón**: MD-scoring no es nuestro diferenciador. Mantener como "MD Validation Module" opcional en Fase 2.
**Reuso**: Los scripts de GROMACS pueden integrarse como un adapter más (`md_gromacs.py`) para validation de regiones inciertas.
**Status**: ✅ Aprobada

### Decisión 008: Modelos prioritarios para MVP
**Fecha**: 2026-05-24
**Modelos en MVP (semana 4)**:
1. AlphaFold 3 (API)
2. Chai-1 (local)
3. Boltz-2 (local)
**Modelos en Fase 2 (mes 2-3)**:
4. OpenFold3
5. Protenix
6. ProteinMPNN
7. RFdiffusion
8. Chai-2 (anticuerpos)
9. ESM3 (embeddings)
**Razón**: Los 3 del MVP cubren el caso de uso más común (structure prediction). Después expandimos.
**Status**: ✅ Aprobada

### Decisión 009: Modelo de precios inicial
**Fecha**: 2026-05-24
**Free**: 10 calls/día, modelos básicos
**Pro**: $99/mes — 1000 calls/día
**Team**: $499/mes — 10000 calls/día + workflows premium + MD validation
**Enterprise**: Custom
**Razón**: Inspirado en HuggingFace + Replicate. Free tier robusto para captar usuarios.
**Status**: ✅ Aprobada para Fase 2

### Decisión 010: Nombre del proyecto
**Fecha**: 2026-05-24
**Nombre**: DYNAFOLD Hub
**Razón**: Mantiene el branding original (DYNAFOLD) pero el sufijo "Hub" comunica la nueva propuesta (orquestación, no modelo único).
**Alternativas consideradas**: BioStack, ModelMesh Bio, FoldOps
**Status**: ✅ Aprobada (tentativa, podemos rebrandear si feedback negativo)

### Cómo añadir nuevas decisiones
Cuando tomemos una decisión nueva, añadir a esta sección con formato:
```
### Decisión NNN: [Título corto]
**Fecha**: YYYY-MM-DD
**Decisor**: [Sergio | Claude | Conjunta]
**Contexto**: [Por qué surgió la pregunta]
**Decisión**: [Qué decidimos]
**Razón**: [Por qué]
**Alternativas consideradas**: [Otras opciones]
**Status**: [⏳ Pendiente | ✅ Aprobada | ❌ Revertida | 🔄 En revisión]
```

---

## 12. ASSETS EXISTENTES A REUSAR

### Del proyecto DYNAFOLD validation (Mpro)

#### ✅ A REUSAR

| Asset | Ubicación local | Reuso en DYNAFOLD Hub |
|-------|-----------------|----------------------|
| Pipeline GROMACS | `dynafold_outputs/scripts/` | Adapter `md_gromacs.py` para MD Validation Module (Fase 2) |
| Scripts análisis DCS/MM-GBSA | `dynafold_outputs/scripts/` | Referencia + módulo de validación opcional |
| Decision log methodology | `dynafold_outputs/logs/decisions.log` | Aplicar misma metodología en este proyecto |
| Selección estratificada con seed | `dynafold_outputs/scripts/01b_stratified_selection.py` | Plantilla para futuras validaciones |
| 75 trayectorias × 50ns Mpro | (en servidor, no descargado) | **Dataset de ejemplo** para "MD validation" feature |
| HIDDEN labels Mpro (ya rotas) | `dynafold_outputs/data/HIDDEN_true_labels.csv` | Caso de estudio para "cuándo MD NO añade valor" |
| 6LU7 + 50 compuestos preparados | `dynafold_outputs/data/` | Example data para tutorial "antiviral discovery" |

#### ❌ A NO REUSAR

| Asset | Razón |
|-------|-------|
| Algoritmo DCS (5 métricas + pesos) | Demostrado que no funciona para Mpro, métricas conceptualmente invertidas |
| Pipeline `production_25x3.sh` | Específico para Mpro, no generalizable |
| Análisis AUC para Mpro | Resultado negativo conocido, no relevante para Hub |
| Servidor Verda | Destruir, usar GPU on-demand cuando necesite |

#### 💡 OPORTUNIDAD: Publicar negative result

Los datos de Mpro tienen valor científico real como negative result. Considerar:
- Escribir preprint en bioRxiv: "MD-based scoring underperforms docking for SARS-CoV-2 Mpro"
- Publicar pipeline como "DYNAFOLD MD Validation Toolkit" en GitHub
- Citar en marketing de DYNAFOLD Hub como prueba de honestidad científica

### Del briefing original (Navas_Bio_Century)

Los archivos 01-06 del proyecto original tienen información que puede inspirar pero NO definir el nuevo proyecto:
- Idioma español: mantener
- Comunicación honesta: mantener
- Pre-commit thresholds: mantener metodología
- Decisión log: extender al nuevo proyecto

---

## 13. DECISIONES DE INFRAESTRUCTURA

### Infraestructura actual (legacy DYNAFOLD validation)

| Recurso | Estado | Acción |
|---------|--------|--------|
| Servidor Verda (95.133.252.87) | Activo, ~$21/día idle | **DESTRUIR** desde panel Verda |
| Saldo Verda | $42 USD | Mantener en cuenta para futuro |
| Datos en servidor | 200GB | Lo crítico ya descargado a Mac |

### Infraestructura nueva (DYNAFOLD Hub)

#### Desarrollo (local)
```bash
# Stack local:
- Mac (desarrollo principal)
- Docker Desktop (opcional, para Postgres/Redis local)
- Python 3.11+ con poetry
- VSCode/PyCharm + extensiones Python

# No requiere GPU para desarrollo de UI/API
# GPU solo necesaria para correr Chai-1/Boltz-2 localmente
# Alternativa GPU: Google Colab gratis para tests
```

#### Staging (MVP)
```bash
# HuggingFace Spaces (gratis)
- URL: huggingface.co/spaces/dynafold/hub
- Recursos: CPU básico (suficiente para AF3 API + UI)
- Para modelos GPU: integrar con Inference Endpoints HF ($) o Modal ($)
```

#### Production (post-MVP)
```bash
# Cuando tengamos primeros paying customers:
- Render (web app + API): $25/mes inicial
- Railway o Modal (GPU on-demand): pay-per-use
- Cloudflare R2 (storage): $0-15/mes
- Supabase (Postgres managed): free tier inicial
- Plausible (analytics): $9/mes
- Sentry (errors): free tier
```

### Estimación de costes operativos

| Fase | Coste mensual | Razón |
|------|---------------|-------|
| Desarrollo (mes 1) | $0-10 | Solo dominio prorrateado |
| MVP launch (mes 1-2) | $10-50 | HF Spaces + dominio + analytics |
| Primeros clientes (mes 3-6) | $50-200 | Render + Modal pay-per-use |
| Scaling (mes 6-12) | $500-2000 | GPU on-demand + storage |
| Post-funding | $5K-20K | Equipo + infra enterprise |

---

## 14. MÉTRICAS DE ÉXITO

### Métricas por fase

#### Fase 1: Validación (mes 1)
| Métrica | Target | Acción si NO se cumple |
|---------|--------|------------------------|
| GitHub stars | 50+ | Mejorar README, más outreach |
| HF Spaces visits | 500+ | Mejor demo, más canales |
| Predictions ejecutadas | 100+ | Hay que simplificar UX |
| Conversaciones con biotechs | 5+ | Más outreach proactivo |
| Press/tweet de cuenta influyente | 1+ | Pitch a journalists |

#### Fase 2: Monetización (mes 2-4)
| Métrica | Target |
|---------|--------|
| GitHub stars | 500+ |
| Free users activos | 1000+ |
| Pro tier subscribers | 10+ ($1K MRR) |
| Workflows usados | 500+ runs |

#### Fase 3: Escala (mes 5-12)
| Métrica | Target |
|---------|--------|
| GitHub stars | 5000+ |
| Free users | 10000+ |
| Pro subscribers | 200+ |
| Enterprise contracts | 1-3 |
| ARR | $200K-1M |

### KPIs operativos (semanales)

Tracking en dashboard simple:
- Weekly Active Users (WAU)
- Predictions/week
- Average time-to-first-prediction
- Error rate (%)
- NPS de usuarios pagos
- GitHub commits/week (proxy de health del proyecto)

---

## 15. MODELOS A INTEGRAR (CATÁLOGO COMPLETO)

### Predicción de estructura proteína-ligando

| Modelo | Repositorio | Licencia | Prioridad MVP | Notas |
|--------|-------------|----------|---------------|-------|
| AlphaFold 3 | DeepMind (server) | Free academic, paid commercial | **P1** | API access |
| Chai-1 | github.com/chaidiscovery/chai-lab | Apache 2.0 | **P1** | pip install chai_lab |
| Boltz-2 | github.com/jwohlwend/boltz | MIT | **P1** | pip install boltz |
| OpenFold3 | aqlaboratory/openfold | Apache 2.0 | P2 | Reproducción AF3 |
| Protenix | bytedance/Protenix | Apache 2.0 | P2 | ByteDance |
| HelixFold3 | PaddlePaddle/PaddleHelix | Mixed | P3 | Restricciones comerciales |
| RoseTTAFold AA | RosettaCommons/RFAA | BSD-3 | P3 | Académico |
| NeuralPLexer3 | iambic-therapeutics | Verificar | P3 | Confirmar acceso |

### Diseño generativo de proteínas

| Modelo | Repositorio | Licencia | Prioridad | Notas |
|--------|-------------|----------|-----------|-------|
| RFdiffusion | RosettaCommons/RFdiffusion | BSD-3 | **P2** | Diseño de novo |
| RFdiffusionAA | RosettaCommons | BSD-3 | P2 | Versión all-atom |
| ProteinMPNN | dauparas/ProteinMPNN | MIT | **P2** | Diseño de secuencias |
| LigandMPNN | dauparas/LigandMPNN | MIT | P2 | Con ligandos |
| BindCraft | martinpacesa/BindCraft | MIT | P3 | Pipeline binders |
| ESM3 | EvolutionaryScale/esm | Mixed | P3 | API access |

### Anticuerpos

| Modelo | Repositorio | Licencia | Prioridad | Notas |
|--------|-------------|----------|-----------|-------|
| Chai-2 | github.com/chaidiscovery/chai-lab | Apache 2.0 | **P2** | De novo antibody design |
| IgFold | Graylab/IgFold | BSD-3 | P2 | Predicción estructura |
| ImmuneBuilder | oxpig/ImmuneBuilder | BSD-3 | P3 | Multi-tipo (Ab, TCR) |
| AntiFold | DeepAntibodyDesign | MIT | P3 | Diseño inverso |
| IgDiff | (académico) | Verificar | P3 | Difusión para Ab |

### Docking y afinidad

| Modelo | Repositorio | Licencia | Prioridad | Notas |
|--------|-------------|----------|-----------|-------|
| DiffDock-L | gcorso/DiffDock | MIT | P2 | Docking por difusión |
| SigmaDock | (Universidad) | Verificar | P3 | Fragment-based |
| AutoDock Vina | ccsb-scripps/AutoDock-Vina | Apache 2.0 | P2 | Baseline obligatorio |

### Genómica / Foundation models

| Modelo | Repositorio | Licencia | Prioridad | Notas |
|--------|-------------|----------|-----------|-------|
| ESM3 | EvolutionaryScale/esm | Mixed | P3 | API + open weights subset |
| Evo 2 | ArcInstitute | Apache 2.0 | P3 | Genómico |
| BioNeMo | NVIDIA | Comercial | P4 | Enterprise only |

### Leyenda
- **P1**: Crítico para MVP semana 4
- **P2**: Importante para Fase 2 (mes 2-4)
- **P3**: Nice-to-have, Fase 3
- **P4**: Solo si demanda enterprise lo justifica

---

## 16. RECURSOS Y ENLACES

### Documentación oficial de modelos
- [AlphaFold 3 Server](https://alphafoldserver.com)
- [Chai Discovery Documentation](https://www.chaidiscovery.com/)
- [Boltz GitHub](https://github.com/jwohlwend/boltz)
- [OpenFold](https://github.com/aqlaboratory/openfold)
- [Protenix](https://github.com/bytedance/Protenix)
- [RFdiffusion](https://github.com/RosettaCommons/RFdiffusion)
- [ProteinMPNN](https://github.com/dauparas/ProteinMPNN)
- [ESM3](https://github.com/evolutionaryscale/esm)

### Comunidades
- r/bioinformatics (Reddit)
- BioStars (Q&A)
- HuggingFace Bio Discord
- AlphaFold Discord
- Comp Bio Slack workspaces

### Inspiración (empresas comparables)
- [HuggingFace](https://huggingface.co) — modelo de negocio reference
- [Replicate](https://replicate.com) — API platform reference
- [LangChain](https://langchain.com) — orchestration reference
- [Modal](https://modal.com) — GPU infra inspiration
- [Chai Discovery](https://www.chaidiscovery.com) — competidor de modelos (no de plataforma)

### Datasets útiles
- [PDB (Protein Data Bank)](https://www.rcsb.org)
- [ChEMBL](https://www.ebi.ac.uk/chembl/)
- [BindingDB](https://www.bindingdb.org)
- [SAbDab (anticuerpos)](http://opig.stats.ox.ac.uk/webapps/newsabdab/)
- [PDBbind](http://www.pdbbind.org.cn)

### Benchmarks de referencia
- PoseBusters (protein-ligand)
- CASP15/CASP16 (structure prediction)
- Sabdab benchmarks (antibodies)
- PDBbind v2020 (affinity)

### Papers fundamentales para leer
- "Highly accurate protein structure prediction with AlphaFold" (Jumper et al., 2021)
- "Accurate structure prediction of biomolecular interactions with AlphaFold 3" (Abramson et al., 2024)
- "Chai-1: Decoding the molecular interactions of life" (Chai team, 2024)
- "De novo design of protein structure and function with RFdiffusion" (Watson et al., 2023)
- "Robust deep learning-based protein sequence design using ProteinMPNN" (Dauparas et al., 2022)

---

## 17. INSTRUCCIONES ESPECÍFICAS PARA CLAUDE

### Cómo iniciar una nueva sesión

Cuando empieces una nueva sesión con este proyecto:

1. **Lee este documento completo** antes de cualquier acción
2. **Verifica el estado actual** del repositorio:
   ```bash
   ls ~/Desktop/git/Navas_Bio_Century/dynafold_hub/
   git -C ~/Desktop/git/Navas_Bio_Century/dynafold_hub status  # cuando exista
   ```
3. **Pregunta a Sergio** qué quiere hacer en esta sesión (no asumas)
4. **Revisa la sección "Decisiones Clave"** para no contradecir lo decidido

### Comunicación con Sergio (estilo de respuesta)

**SÍ hacer**:
- Español como idioma principal
- Términos técnicos en inglés cuando aplique (más claros)
- Tablas comparativas cuando hay opciones
- Análisis honesto, sin endulzar
- Decir "no sé" cuando no sé
- Predicciones con probabilidades estimadas
- Explicar trade-offs explícitamente

**NO hacer**:
- Inventar datos o capacidades
- Sobrevender opciones
- Esconder problemas o riesgos
- Asumir decisiones sin confirmar
- Cambiar dirección estratégica sin discutir

### Cuándo pedir confirmación

**Pedir confirmación SIEMPRE para**:
- Gastos monetarios (cualquier $)
- Decisiones estratégicas (pivot, target market, pricing)
- Lanzamientos públicos (publicar repo, tweet, etc.)
- Cambios al CLAUDE.md (este documento)
- Borrar/destruir cualquier recurso

**Proceder sin confirmar para**:
- Refactoring de código menor
- Añadir tests
- Fix de bugs evidentes
- Actualizar documentación menor
- Commits routine

### Estilo de código

- Python 3.11+ con type hints
- Black formatter
- Ruff para linting
- Docstrings Google style
- Tests con pytest, target 70%+ coverage

### Workflow recomendado por sesión

```
1. Sesión empieza
   ├─ Leer CLAUDE.md
   ├─ Verificar estado git
   └─ Preguntar: "¿Qué quieres hacer hoy?"

2. Sergio define objetivo

3. Claude propone plan
   ├─ Pasos concretos
   ├─ Tiempo estimado
   └─ Cualquier coste/riesgo

4. Sergio aprueba

5. Claude ejecuta
   ├─ Commits pequeños y descriptivos
   ├─ Tests cuando aplique
   └─ Reporta progreso

6. Sesión termina
   ├─ Update este CLAUDE.md si hay decisiones nuevas
   ├─ Commit final
   └─ Resumen de sesión + próximos pasos
```

### Estado del proyecto al inicio (2026-05-24)

| Item | Estado |
|------|--------|
| Plan estratégico | ✅ Este documento |
| Repositorio GitHub | ⏳ Por crear |
| Estructura local | ✅ Carpetas creadas |
| Dominio dynafold.io | ⏳ Por comprar |
| HuggingFace account | ⏳ Por verificar |
| Servidor Verda | ⏳ Por destruir (acción de Sergio) |
| Saldo Verda | $42 (preservar) |
| Código MVP | 0% (empezar desde cero) |
| Outreach a clientes | 0 conversaciones |

### Próxima sesión (cuando se retome)

**Cosas a hacer en orden**:

1. Sergio confirma que destruyó instancia Verda
2. Sergio confirma que tiene cuenta GitHub configurada
3. Crear repositorio público `dynafold-ai/dynafold-hub` (o similar)
4. Setup inicial:
   ```bash
   cd ~/Desktop/git/Navas_Bio_Century/dynafold_hub
   git init
   poetry init --no-interaction
   # Configurar pyproject.toml
   # Crear estructura inicial
   git add . && git commit -m "Initial commit: project scaffold"
   gh repo create dynafold-ai/dynafold-hub --public --source=.
   git push -u origin main
   ```
5. Implementar `BaseModelAdapter` (ABC)
6. Implementar primer adapter: `Chai1Adapter`
7. Tests básicos
8. Commit + push

### Cuando algo se complica

Si algo no va según plan o Sergio cambia de opinión:
1. **No te resistas** — su negocio, sus decisiones
2. **Pregunta el por qué** para entender mejor
3. **Documenta el cambio** en sección "Decisiones Clave"
4. **Actualiza el roadmap** si afecta plan
5. **Procede** con la nueva dirección

### Si encuentras información que contradice este plan

Por ejemplo: "salió un nuevo modelo X que cambia todo" o "Chai lanzó plataforma similar".
1. **Reporta el hallazgo** con fuentes
2. **Analiza impacto** en nuestra estrategia
3. **Propone ajustes** específicos
4. **Espera decisión** de Sergio
5. **No actúes unilateralmente**

---

## 📌 NOTAS FINALES

### Filosofía del proyecto
- **Lean**: empezar minimal, iterar basado en feedback real
- **Honesto**: si algo no funciona, decirlo (lección de Mpro)
- **Open**: maximizar transparencia, código abierto, decisiones documentadas
- **Pragmático**: priorizar lo que mueve la aguja, no lo que es "cool"

### Lo que NO somos
- ❌ NO somos un model maker (no construimos AlphaFold 4)
- ❌ NO competimos con Chai/Atomwise (los integramos)
- ❌ NO somos un wet-lab (no hacemos experimentos)
- ❌ NO somos un CRO (no ofrecemos servicios manuales)

### Lo que SÍ somos
- ✅ Una plataforma de orquestación
- ✅ Una capa de software encima de modelos AI
- ✅ Un puente entre investigadores y modelos SOTA
- ✅ Una empresa que captura valor por convenience + workflows

### Versión y evolución de este documento

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-05-24 | Documento inicial completo |

**Para Claude**: añade nueva fila cada vez que actualices este documento sustancialmente.

---

**FIN DEL DOCUMENTO MAESTRO**

Última verificación: 2026-05-24 por Claude + Sergio León
Próxima revisión sugerida: tras completar Semana 1 de Fase 1
