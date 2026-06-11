# LangGraph Workflow Engine

Build, execute, and monitor AI agent workflows using LangGraph.

## Features

- **Visual Workflow Builder** — Drag-and-drop canvas for designing workflows
- **Multi-Agent Orchestration** — Coordinate multiple AI agents in complex workflows
- **LLM Integration** — Built-in support for OpenAI, Anthropic Claude, and local models
- **Conditional Routing** — Branching logic with dynamic edge routing
- **Human-in-the-Loop** — Approval gates and manual review steps
- **Memory & State** — Persistent state and checkpoint management
- **Monitoring** — Real-time execution tracking with Prometheus/Grafana
- **Docker/K8s** — Containerized deployment ready

## Quick Start

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Open http://localhost:8000/docs for API docs.

## Project Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph Workflow Engine                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────┐        ┌──────────────────────┐       │
│  │    Frontend (React)  │        │   Backend (FastAPI)  │       │
│  │  - Dashboard UI      │◄─────►│  - REST API (v1)     │       │
│  │  - Workflow Builder  │        │  - WebSocket Manager │       │
│  │  - Execution Monitor │        │  - Middleware Stack  │       │
│  └──────────────────────┘        └──────────────────────┘       │
│           │                                 │                     │
│           └─────────────┬───────────────────┘                    │
│                         │                                         │
│           ┌─────────────▼──────────────┐                        │
│           │  LangGraph Engine Core      │                        │
│           │  - Graph Builder            │                        │
│           │  - Node Executor            │                        │
│           │  - Edge Router              │                        │
│           │  - State Management         │                        │
│           └────────────┬────────────────┘                        │
│                        │                                          │
│        ┌───────────────┼───────────────┐                         │
│        │               │               │                         │
│    ┌───▼─────┐  ┌──────▼──────┐  ┌────▼────┐                   │
│    │ Nodes   │  │  Workflows  │  │ Edges   │                   │
│    │ Module  │  │  Module     │  │ Module  │                   │
│    └─────────┘  └─────────────┘  └─────────┘                   │
│        │               │               │                         │
│    ┌───▼─────────────┬─▼────────────┬─▼──────┐                │
│    │                 │              │         │                 │
│  ┌─▼────┐  ┌────────▼────┐  ┌─────▼──┐  ┌──▼──┐              │
│  │Agent │  │ Execution   │  │Memory  │  │LLM  │              │
│  │Nodes │  │ Service     │  │Module  │  │Fac. │              │
│  └──────┘  └─────────────┘  └────────┘  └─────┘              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Database Layer (SQLAlchemy)                    │  │
│  │  - Workflow Persistence  - Execution History            │  │
│  │  - Node State Storage    - Metrics Storage             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │    External Services & Infrastructure                    │  │
│  │  - LLM Providers (OpenAI, Claude, Local)                │  │
│  │  - Monitoring (Prometheus/Grafana)                      │  │
│  │  - Scheduling (APScheduler)                            │  │
│  │  - Authentication (JWT)                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Project Structure

```
langgraph_workflow_engine/
│
├── backend/                           # FastAPI Backend Application
│   ├── main.py                       # Application Entry Point
│   │
│   ├── api/                          # REST API Layer
│   │   ├── routes.py                 # Endpoint Definitions
│   │   ├── schemas.py                # Pydantic Request/Response Models
│   │   ├── auth.py                   # Authentication Logic
│   │   ├── dependencies.py           # FastAPI Dependency Injection
│   │   ├── metrics.py                # Metrics Endpoints
│   │   ├── middleware.py             # API Middleware
│   │   └── websocket_manager.py      # WebSocket Connection Management
│   │
│   ├── langgraph_engine/             # Core LangGraph Engine (121 Python Files)
│   │   │
│   │   ├── core/                     # Core Graph Execution
│   │   │   ├── graph_builder.py      # Build Workflow Graphs
│   │   │   ├── graph_compiler.py     # Compile Graphs to Executable
│   │   │   ├── node_executor.py      # Execute Individual Nodes
│   │   │   ├── edge_router.py        # Route Execution Between Nodes
│   │   │   └── state_management.py   # Manage Workflow State
│   │   │
│   │   ├── nodes/                    # Node Types & Implementations
│   │   │   ├── base_node.py          # Base Node Class
│   │   │   │
│   │   │   ├── agent_nodes/          # AI Agent Nodes
│   │   │   │   ├── agent_node.py     # Generic Agent Node
│   │   │   │   ├── planner_agent.py  # Planning Agent
│   │   │   │   ├── reasoning_agent.py # Reasoning Agent
│   │   │   │   └── tool_agent.py     # Tool-Using Agent
│   │   │   │
│   │   │   ├── processing_nodes/     # Data Processing Nodes
│   │   │   │   ├── llm_node.py       # LLM Call Node
│   │   │   │   ├── data_transformer.py # Transform Data
│   │   │   │   ├── text_processor.py # Process Text
│   │   │   │   ├── validator_node.py # Validate Data
│   │   │   │   └── custom_node.py    # Custom Processing
│   │   │   │
│   │   │   ├── decision_nodes/       # Control Flow Nodes
│   │   │   │   ├── conditional_node.py # If/Then Logic
│   │   │   │   ├── loop_node.py      # Looping Logic
│   │   │   │   ├── router_node.py    # Route Based on Condition
│   │   │   │   └── switch_node.py    # Multi-way Switch
│   │   │   │
│   │   │   ├── aggregation_nodes/    # Result Aggregation
│   │   │   │   ├── aggregate_node.py # Aggregate Results
│   │   │   │   ├── combine_node.py   # Combine Outputs
│   │   │   │   └── merge_node.py     # Merge Data
│   │   │   │
│   │   │   ├── input_nodes/          # Data Input Nodes
│   │   │   │   ├── api_input.py      # Receive API Input
│   │   │   │   ├── database_input.py # Read from Database
│   │   │   │   ├── file_input.py     # Read from Files
│   │   │   │   └── manual_input.py   # Manual/Approval Input
│   │   │   │
│   │   │   └── output_nodes/         # Data Output Nodes
│   │   │       ├── api_output.py     # Send API Response
│   │   │       ├── database_output.py # Store to Database
│   │   │       ├── file_output.py    # Write to Files
│   │   │       └── display_output.py # Display Results
│   │   │
│   │   ├── edges/                    # Edge Types & Routing
│   │   │   ├── base_edge.py          # Base Edge Class
│   │   │   ├── conditional_edge.py   # Conditional Routing
│   │   │   ├── dynamic_edge.py       # Dynamic/Runtime Routing
│   │   │   └── event_edge.py         # Event-Driven Routing
│   │   │
│   │   ├── workflows/                # Pre-built Workflow Templates
│   │   │   ├── custom_workflow.py    # Custom Workflow
│   │   │   ├── multi_agent_workflow.py # Multi-Agent Workflows
│   │   │   ├── parallel_workflow.py  # Parallel Execution
│   │   │   ├── decision_tree_workflow.py # Decision Trees
│   │   │   ├── data_pipeline_workflow.py # Data Pipelines
│   │   │   ├── document_workflow.py  # Document Processing
│   │   │   └── research_workflow.py  # Research Workflows
│   │   │
│   │   ├── execution/                # Execution & Scheduling
│   │   │   ├── executor.py           # Execute Workflows
│   │   │   ├── scheduler.py          # Schedule Executions
│   │   │   ├── error_handler.py      # Error Handling
│   │   │   ├── retry_logic.py        # Retry Mechanisms
│   │   │   └── timeout_manager.py    # Timeout Management
│   │   │
│   │   ├── memory/                   # State & Memory Management
│   │   │   ├── memory_manager.py     # Manage Workflow Memory
│   │   │   ├── state_persistence.py  # Persist State
│   │   │   ├── checkpoint.py         # Create Checkpoints
│   │   │   └── context_store.py      # Store Context Data
│   │   │
│   │   ├── tools/                    # Tool/Function Registry
│   │   │   ├── tool_registry.py      # Register Tools
│   │   │   ├── tool_executor.py      # Execute Tools
│   │   │   ├── built_in_tools.py     # Built-in Tools
│   │   │   └── custom_tools.py       # Custom Tools
│   │   │
│   │   └── supervision/              # Human-in-Loop
│   │       ├── human_in_loop.py      # Human Interaction
│   │       ├── approval_manager.py   # Approval Gates
│   │       └── review_node.py        # Review Node
│   │
│   ├── services/                     # Business Logic Services
│   │   ├── workflow_service.py       # Workflow CRUD & Management
│   │   ├── execution_service.py      # Execution Management
│   │   ├── orchestration_service.py  # Orchestrate Workflows
│   │   ├── state_service.py          # State Management
│   │   ├── memory_service.py         # Memory Operations
│   │   ├── tool_service.py           # Tool Management
│   │   ├── monitoring_service.py     # Monitoring & Metrics
│   │   └── logging_service.py        # Logging Operations
│   │
│   ├── llm/                          # LLM Providers & Configuration
│   │   ├── llm_factory.py            # LLM Factory Pattern
│   │   ├── llm_config.py             # LLM Configuration
│   │   ├── openai_llm.py             # OpenAI Integration
│   │   ├── claude_llm.py             # Anthropic Claude Integration
│   │   └── local_llm.py              # Local LLM Support
│   │
│   ├── models/                       # SQLAlchemy Database Models
│   │   ├── database.py               # Base Model & Session
│   │   ├── workflow.py               # Workflow Model
│   │   ├── node.py                   # Node Model
│   │   ├── edge.py                   # Edge Model
│   │   ├── execution.py              # Execution Model
│   │   ├── agent.py                  # Agent Model
│   │   └── tool.py                   # Tool Model
│   │
│   ├── db/                           # Database Layer
│   │   ├── session.py                # Database Session Management
│   │   └── repositories.py           # Data Access Objects
│   │
│   ├── middleware/                   # HTTP Middleware
│   │   ├── auth_middleware.py        # Authentication
│   │   ├── logging_middleware.py     # Request/Response Logging
│   │   ├── timing_middleware.py      # Performance Timing
│   │   └── error_handler.py          # Error Handling
│   │
│   └── utils/                        # Utility Functions
│       ├── logger.py                 # Logging Configuration
│       ├── exceptions.py             # Custom Exceptions
│       ├── validators.py             # Input Validation
│       ├── config.py                 # Configuration Loading
│       ├── constants.py              # Constants & Defaults
│       ├── helpers.py                # Helper Functions
│       ├── decorators.py             # Custom Decorators
│       └── graph_utils.py            # Graph Utilities
│
├── frontend/                         # React Frontend Application
│   ├── public/                       # Static Assets
│   │   ├── index.html               # HTML Entry Point
│   │   ├── manifest.json            # PWA Manifest
│   │   └── favicon.ico              # Site Icon
│   │
│   └── src/                          # React Source Code
│       ├── App.js                    # Main Application
│       ├── App.css                   # Global Styles
│       ├── index.js                  # Entry Point
│       │
│       ├── pages/                    # Page Components
│       │   ├── Dashboard.js          # Main Dashboard
│       │   ├── WorkflowBuilder.js    # Workflow Designer
│       │   ├── ExecutionMonitor.js   # Execution Monitor
│       │   ├── Settings.js           # Settings Page
│       │   └── Documentation.js      # Docs Page
│       │
│       ├── components/               # Reusable Components
│       │   ├── WorkflowCanvas.js     # Canvas Component
│       │   ├── NodePalette.js        # Node Types Panel
│       │   ├── ExecutionLog.js       # Execution Log Viewer
│       │   ├── MetricsPanel.js       # Metrics Display
│       │   └── ...                   # Other UI Components
│       │
│       ├── hooks/                    # Custom React Hooks
│       │   ├── useWorkflow.js        # Workflow Hook
│       │   ├── useExecution.js       # Execution Hook
│       │   └── useWebSocket.js       # WebSocket Hook
│       │
│       ├── services/                 # API Services
│       │   ├── api.js                # API Client
│       │   ├── workflowService.js    # Workflow API Calls
│       │   └── executionService.js   # Execution API Calls
│       │
│       └── store/                    # State Management
│           ├── actions.js            # Redux Actions
│           ├── reducers.js           # Redux Reducers
│           └── store.js              # Redux Store Config
│
├── config/                           # Application Configuration
│   ├── settings.py                  # Main Settings
│   ├── database_config.py           # Database Configuration
│   ├── llm_config.py                # LLM Configuration
│   ├── langraph_config.py           # LangGraph Configuration
│   └── logging_config.py            # Logging Configuration
│
├── tests/                            # Test Suite
│   ├── conftest.py                  # Pytest Configuration
│   │
│   ├── unit/                        # Unit Tests
│   │   ├── test_graph_builder.py    # Graph Builder Tests
│   │   ├── test_node_executor.py    # Node Executor Tests
│   │   ├── test_edge_router.py      # Edge Router Tests
│   │   ├── test_state_management.py # State Management Tests
│   │   ├── test_workflows.py        # Workflow Tests
│   │   ├── test_agents.py           # Agent Tests
│   │   ├── test_tools.py            # Tool Tests
│   │   └── test_error_handling.py   # Error Handling Tests
│   │
│   ├── integration/                 # Integration Tests
│   │   ├── test_workflow_execution.py # End-to-End Workflows
│   │   ├── test_multi_agent.py      # Multi-Agent Systems
│   │   ├── test_end_to_end.py       # Full System Tests
│   │   ├── test_tool_integration.py # Tool Integration
│   │   └── test_api_endpoints.py    # API Endpoint Tests
│   │
│   └── load/                        # Load Tests
│       └── test_performance.py      # Performance Tests
│
├── docs/                             # Documentation
│   ├── README.md                    # Docs Index
│   ├── QUICKSTART.md                # Quick Start Guide
│   ├── ARCHITECTURE.md              # Architecture Overview
│   ├── API_REFERENCE.md             # API Documentation
│   ├── WORKFLOW_GUIDE.md            # Workflow Creation Guide
│   ├── NODE_GUIDE.md                # Node Types Guide
│   ├── AGENT_GUIDE.md               # Agent Configuration Guide
│   ├── TOOL_GUIDE.md                # Tool Integration Guide
│   ├── LANGGRAPH_GUIDE.md           # LangGraph Concepts
│   ├── DEPLOYMENT.md                # Deployment Guide
│   ├── TROUBLESHOOTING.md           # Troubleshooting Guide
│   └── EXAMPLES.md                  # Code Examples
│
├── examples/                        # Example Workflows & Scripts
│   ├── basic/                       # Basic Examples
│   │   ├── simple_workflow.py       # Simple Linear Workflow
│   │   ├── branching_workflow.py    # Branching Example
│   │   └── looping_workflow.py      # Looping Example
│   │
│   ├── agents/                      # Agent Examples
│   │   ├── single_agent.py          # Single Agent
│   │   ├── multi_agent.py           # Multi-Agent System
│   │   ├── agent_with_tools.py      # Agent Using Tools
│   │   └── hierarchical_agents.py   # Hierarchical Agents
│   │
│   ├── advanced/                    # Advanced Examples
│   │   ├── parallel_processing.py   # Parallel Workflows
│   │   ├── decision_tree.py         # Decision Trees
│   │   ├── data_pipeline.py         # Data Pipelines
│   │   ├── document_processing.py   # Document Processing
│   │   └── research_workflow.py     # Research Workflows
│   │
│   └── real_world/                  # Real-World Use Cases
│       ├── customer_support.py      # Support Agent
│       ├── code_review.py           # Code Review Workflow
│       ├── content_generation.py    # Content Generation
│       └── data_analysis.py         # Data Analysis Workflow
│
├── scripts/                          # Utility Scripts
│   ├── init_db.py                   # Initialize Database
│   ├── seed_data.py                 # Seed Sample Data
│   ├── create_example_workflows.py  # Create Example Workflows
│   ├── import_workflows.py          # Import Workflows
│   ├── export_workflows.py          # Export Workflows
│   ├── test_workflow.py             # Test Workflow Script
│   └── benchmark.py                 # Benchmark Performance
│
├── kubernetes/                       # K8s Deployment
│   ├── deployment.yaml              # Deployment Config
│   ├── service.yaml                 # Service Config
│   ├── ingress.yaml                 # Ingress Config
│   ├── configmap.yaml               # ConfigMap
│   └── secret.yaml                  # Secrets
│
├── monitoring/                       # Monitoring & Observability
│   ├── prometheus.yml               # Prometheus Config
│   ├── alerts.yml                   # Alert Rules
│   │
│   └── grafana_dashboards/          # Grafana Dashboards
│       ├── workflow_metrics.json     # Workflow Metrics
│       ├── agent_performance.json    # Agent Performance
│       ├── execution_stats.json      # Execution Stats
│       └── system_health.json        # System Health
│
├── docker/                           # Docker Configurations
│   ├── Dockerfile.backend           # Backend Docker Image
│   ├── Dockerfile.frontend          # Frontend Docker Image
│   ├── docker-compose.yml           # Local Dev Stack
│   │
│   └── nginx/                       # Nginx Configuration
│       ├── nginx.conf               # Nginx Config
│       └── ssl/                     # SSL Certificates
│
├── data/                             # Data Files
│   ├── raw/                         # Raw Data
│   ├── processed/                   # Processed Data
│   └── datasets/                    # Sample Datasets
│       ├── workflow_examples.json   # Example Workflows
│       └── sample_data.csv          # Sample Data
│
├── alembic/                          # Database Migrations
│   ├── env.py                       # Migration Environment
│   ├── script.py.mako               # Migration Template
│   ├── alembic.ini                  # Alembic Config
│   └── versions/                    # Migration Scripts
│
├── .github/                          # GitHub Configuration
│   └── workflows/                   # CI/CD Workflows
│       ├── tests.yml                # Test Pipeline
│       ├── build.yml                # Build Pipeline
│       ├── deploy.yml               # Deploy Pipeline
│       ├── lint.yml                 # Linting Pipeline
│       └── security.yml             # Security Checks
│
├── docker-compose.yml                # Main Docker Compose
├── Dockerfile                        # Main Dockerfile
├── Dockerfile.dashboard              # Dashboard Dockerfile
├── setup.py                          # Python Package Setup
├── requirements.txt                  # Python Dependencies
├── CONTRIBUTING.md                   # Contributing Guide
└── README.md                         # This File
```

## Core Components

### 1. **LangGraph Engine Core** (`backend/langgraph_engine/core/`)
- **Graph Builder**: Constructs workflow graphs from node and edge definitions
- **Graph Compiler**: Compiles graphs into optimized execution plans
- **Node Executor**: Executes individual nodes with state management
- **Edge Router**: Routes execution between nodes based on conditions
- **State Management**: Manages workflow state throughout execution

### 2. **Nodes Module** (`backend/langgraph_engine/nodes/`)
- **Agent Nodes**: AI agents (planner, reasoner, tool-user)
- **Processing Nodes**: LLM calls, data transformation, validation
- **Decision Nodes**: Control flow (conditionals, loops, switches)
- **Aggregation Nodes**: Combine and merge results
- **Input/Output Nodes**: API, database, file, and manual inputs

### 3. **Workflows** (`backend/langgraph_engine/workflows/`)
Pre-built templates for common patterns:
- Multi-agent orchestration
- Parallel processing
- Decision trees
- Data pipelines
- Document processing

### 4. **Execution Engine** (`backend/langgraph_engine/execution/`)
- **Executor**: Main execution engine
- **Scheduler**: APScheduler-based task scheduling
- **Error Handler**: Exception handling and recovery
- **Retry Logic**: Automatic retries with backoff
- **Timeout Manager**: Execution timeout enforcement

### 5. **Memory System** (`backend/langgraph_engine/memory/`)
- **Memory Manager**: Workflow memory operations
- **State Persistence**: Persistent state storage
- **Checkpoints**: Create/restore execution checkpoints
- **Context Store**: Shared context between nodes

### 6. **LLM Integration** (`backend/llm/`)
- **LLM Factory**: Create LLM instances (OpenAI, Claude, Local)
- **OpenAI Integration**: GPT-3.5, GPT-4 support
- **Claude Integration**: Anthropic Claude support
- **Local LLM Support**: Run local models

### 7. **API Layer** (`backend/api/`)
- RESTful endpoints for workflows, executions, and monitoring
- WebSocket support for real-time updates
- Authentication and authorization
- Request validation and error handling

### 8. **Database Layer** (`backend/db/` & `backend/models/`)
- SQLAlchemy ORM models
- Workflow, execution, node, edge persistence
- State and checkpoint storage
- Migration management (Alembic)

### 9. **Services** (`backend/services/`)
Business logic layer:
- Workflow management
- Execution orchestration
- State operations
- Memory management
- Tool registry
- Monitoring and metrics

### 10. **Frontend** (`frontend/src/`)
React-based dashboard:
- Visual workflow builder
- Real-time execution monitoring
- Metrics and performance tracking
- Interactive node palette

## API Endpoints

- `GET /api/v1/health` — Health check
- `POST /api/v1/workflows` — Create workflow
- `GET /api/v1/workflows` — List workflows
- `GET /api/v1/workflows/{id}` — Get workflow
- `PUT /api/v1/workflows/{id}` — Update workflow
- `DELETE /api/v1/workflows/{id}` — Delete workflow
- `POST /api/v1/executions` — Create execution
- `GET /api/v1/executions` — List executions
- `GET /api/v1/executions/{id}` — Get execution
- `GET /api/v1/monitoring/summary` — Metrics summary
- `WS /ws/executions/{id}` — WebSocket for execution updates

## Key Features by Component

| Component | Features |
|-----------|----------|
| **Graph Engine** | Build, compile, execute workflows |
| **Nodes** | 15+ node types for diverse tasks |
| **Edges** | Conditional, dynamic, event-driven routing |
| **Workflows** | 6+ pre-built workflow templates |
| **Execution** | Scheduling, retries, timeouts, error handling |
| **Memory** | Persistent state, checkpoints, context |
| **LLM** | OpenAI, Claude, local model support |
| **Supervision** | Human-in-loop, approvals, reviews |
| **Tools** | Registry, execution, custom tools |
| **Monitoring** | Prometheus metrics, Grafana dashboards |
| **API** | RESTful endpoints, WebSocket support |
| **Auth** | JWT-based authentication |
| **Deployment** | Docker, Kubernetes, docker-compose |

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, LangGraph
- **Frontend**: React, Redux, Canvas API
- **Database**: PostgreSQL (SQLAlchemy compatible)
- **LLM**: OpenAI, Anthropic Claude, Local models
- **Monitoring**: Prometheus, Grafana
- **Scheduling**: APScheduler
- **Deployment**: Docker, Kubernetes
- **CI/CD**: GitHub Actions
- **Testing**: Pytest, coverage

## Development

```bash
# Install dependencies
pip install -r requirements.txt
npm install --prefix frontend

# Run database migrations
python scripts/init_db.py

# Start backend
uvicorn backend.main:app --reload

# Start frontend (in separate terminal)
cd frontend && npm start

# Run tests
pytest tests/ -v

# Run with docker-compose
docker-compose up
```

## Documentation

- [QUICKSTART.md](docs/QUICKSTART.md) - Get started quickly
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
- [WORKFLOW_GUIDE.md](docs/WORKFLOW_GUIDE.md) - Create workflows
- [API_REFERENCE.md](docs/API_REFERENCE.md) - API documentation
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deploy to production
