# QAQC Pro - React UI

A modern, web-based interface for the QAQC Report Generator, built with React, TypeScript, and Vite.

## 🚀 Getting Started

### Prerequisites
- **Node.js**: v18 or higher
- **npm**: v9 or higher (usually bundled with Node.js)
- **Python 3.11+** (for backend API, optional)

### Installation

Navigate to the `react_ui` directory and install dependencies:

```bash
cd react_ui
npm install
```

### Development Server

Start the development server with Hot Module Replacement (HMR):

```bash
npm run dev
```

The app will be available at `http://localhost:5173` (or the next available port).

### Building for Production

To create a production build:

```bash
npm run build
```

The build artifacts will be output to the `dist` directory.

## 🏗 Project Structure

```
react_ui/
├── api/                  # FastAPI backend server
│   ├── main.py           # API endpoints
│   └── requirements.txt  # Python dependencies
├── src/
│   ├── api/              # API client for backend integration
│   ├── components/       # Reusable UI components
│   │   ├── common/       # Generic atoms/molecules (DataGrid, FileUpload)
│   │   └── layout/       # App shell (Sidebar, Header, MainLayout)
│   ├── features/         # Domain-specific modules
│   │   ├── analysis/     # QAQC engines (Standards, Blanks, Duplicates)
│   │   ├── import/       # File upload & mapping workflow
│   │   ├── projects/     # Project management & onboarding
│   │   ├── report/       # Report generation workflow
│   │   └── templates/    # JORC template editor
│   ├── stores/           # Global state management (Zustand)
│   ├── data/             # Mock data generators & CRM database
│   ├── utils/            # Helpers (file processing, export, project files)
│   ├── App.tsx           # Main application router/coordinator
│   └── main.tsx          # Entry point
├── public/               # Static assets
├── test_project.qaqc     # Sample project file for testing
└── package.json          # Dependencies & scripts
```

## 🛠 Tech Stack

- **Framework**: [React 19](https://react.dev/)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **State Management**: [Zustand](https://github.com/pmndrs/zustand)
- **Data Grid**: [AG Grid](https://www.ag-grid.com/)
- **Charts**: [Recharts](https://recharts.org/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (optional)

## 🧪 Current Features

1.  **Project Management**: Create, save, and load analysis sessions with `.qaqc` project files.
2.  **Data Import**: Drag-and-drop Excel/CSV support with client-side parsing.
3.  **Smart Mapping**: Heuristic auto-detection of Sample ID, Type, and Element columns.
4.  **Configuration Wizards**:
    *   **Data Category**: Gold, pXRF/Multi-element, or PhotonAssay presets.
    *   **Methodology**: Interactive wizard for assay methods & duplicate strategies.
    *   **QAQC Rules**: Configurable tolerances for Standards, Blanks, and Duplicates.
5.  **Analysis Dashboard**:
    *   **Standards**: Control charts with configurable CRMs.
    *   **Blanks**: Contamination monitoring.
    *   **Duplicates**: RPD/HARD precision scatter plots.
6.  **Export**: Client-side generation of DOCX reports, Excel data, and CSV statistics.
7.  **Project Persistence**: Save and load complete project state to `.qaqc` files.

## 💾 Project Files (.qaqc)

The application supports saving and loading project files in `.qaqc` format (JSON-based):

**Save Project:**
- Click "Save Project" button in the header
- Downloads a `.qaqc` file with all project state

**Open Project:**
- Click "Open Project File" on entry screen or header
- Select a `.qaqc` file to restore complete project state

**What's saved:**
- Project metadata (name, deposit, commodity)
- Imported data (headers + rows)
- Configuration (methodology, QAQC rules)
- Analysis results (standards, blanks, duplicates)
- Current workflow position

A test file is included: `test_project.qaqc`

## 🔄 Backend Integration

The React UI can connect to the Python FastAPI backend for server-side analysis.

### Running with Backend (Full Stack)

**Terminal 1 - Start the API Server:**
```bash
cd react_ui
pip install -r api/requirements.txt  # First time only
python3 -m uvicorn api.main:app --reload --port 8000
```

**Terminal 2 - Start the React UI:**
```bash
cd react_ui
npm run dev
```

**Access:**
- React UI: http://localhost:5173
- API Docs: http://localhost:8000/docs
- API Health: http://localhost:8000/health

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/projects` | POST | Create new analysis project |
| `/api/upload` | POST | Upload CSV/Excel file |
| `/api/preview/{file_id}` | GET | Preview uploaded data |
| `/api/crms` | GET | List available CRMs |
| `/api/analyze` | POST | Run QAQC analysis |
| `/api/export/excel` | POST | Generate Excel report |
| `/api/export/pdf` | POST | Generate PDF report |

### Standalone Mode

The application also works in standalone mode using client-side analysis engines (no backend required). This is useful for quick analyses without server setup.
