# QAQC Pro - React UI

A modern, web-based interface for the QAQC Report Generator, built with React, TypeScript, and Vite.

## 🚀 Getting Started

### Prerequisites
- **Node.js**: v18 or higher
- **npm**: v9 or higher (usually bundled with Node.js)

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
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── common/       # Generic atoms/molecules (DataGrid, FileUpload)
│   │   └── layout/       # App shell (Sidebar, Header, MainLayout)
│   ├── features/         # Domain-specific modules
│   │   ├── analysis/     # QAQC engines (Standards, Blanks, Duplicates)
│   │   ├── import/       # File upload & mapping workflow
│   │   └── projects/     # Project management & onboarding
│   ├── stores/           # Global state management (Zustand)
│   ├── data/             # Mock data generators & CRM database
│   ├── utils/            # Helpers (file processing, export logic)
│   ├── App.tsx           # Main application router/coordinator
│   └── main.tsx          # Entry point
├── public/               # Static assets
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

## 🧪 Current Features

1.  **Project Management**: Create/resume analysis sessions with persistent metadata.
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
6.  **Export**: Client-side generation of PDF reports, Excel data, and CSV statistics.

## 🔄 Backend Integration (Upcoming)

Currently, the application runs in "standalone" mode using client-side analysis engines. Future updates will integrate with the Python backend for:
- Advanced statistical models
- Database persistence
- PDF generation using the Python reporting engine
