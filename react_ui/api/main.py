"""
QAQC Analysis API Server

FastAPI backend that connects the React UI to the Python QAQC analysis engine.
Provides endpoints for data import, analysis execution, and report generation.
"""

import sys
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import tempfile
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
import pandas as pd

# Add project root and src directory to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from data import DataImporter
from data.crm_manager import CRMManager
from analysis import StandardsAnalyzer, BlanksAnalyzer, DuplicatesAnalyzer
from visualization import PlotGenerator
from reporting import ExcelReporter, PDFReporter

# Initialize FastAPI app
app = FastAPI(
    title="QAQC Analysis API",
    description="Backend API for QAQC Report Generator",
    version="2.0.0"
)

# Configure CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
data_importer = DataImporter()
crm_manager = CRMManager()
standards_analyzer = StandardsAnalyzer()
blanks_analyzer = BlanksAnalyzer()
duplicates_analyzer = DuplicatesAnalyzer()
plot_generator = PlotGenerator()
excel_reporter = ExcelReporter()
pdf_reporter = PDFReporter()

# Temporary storage for uploaded files and analysis results
temp_storage: Dict[str, Any] = {}

# ============== Pydantic Models ==============

class ColumnMapping(BaseModel):
    sample_id: str = "sample_id"
    sample_type: str = "sample_type"
    result: str = "result"
    batch_id: Optional[str] = None
    elements: Dict[str, str] = Field(default_factory=dict)


class MethodologyConfig(BaseModel):
    assay_method: str = "fire_assay"
    duplicate_strategy: str = "field_duplicate"
    insertion_rate: float = 5.0


class QAQCRulesConfig(BaseModel):
    standards_tolerance: float = 2.0  # Standard deviations
    blanks_threshold: float = 0.01
    duplicates_rpd_limit: float = 10.0
    duplicates_hard_limit: float = 15.0


class AnalysisRequest(BaseModel):
    file_id: str
    column_mapping: ColumnMapping
    methodology: MethodologyConfig
    qaqc_rules: QAQCRulesConfig


class ProjectCreate(BaseModel):
    name: str
    deposit: str
    commodity: str = "Gold"


class CRMSearchParams(BaseModel):
    element: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None


# ============== Health Check ==============

@app.get("/")
async def root():
    return {"status": "ok", "message": "QAQC Analysis API v2.0.0"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "data_importer": "ready",
            "crm_manager": "ready",
            "analyzers": "ready",
            "reporters": "ready"
        }
    }


# ============== Project Management ==============

@app.post("/api/projects")
async def create_project(project: ProjectCreate):
    """Create a new analysis project/session"""
    project_id = f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    temp_storage[project_id] = {
        "id": project_id,
        "name": project.name,
        "deposit": project.deposit,
        "commodity": project.commodity,
        "created_at": datetime.now().isoformat(),
        "files": [],
        "analysis_results": None
    }
    
    return {"project_id": project_id, **temp_storage[project_id]}


@app.get("/api/projects")
async def list_projects():
    """List all active projects"""
    projects = [
        {"id": k, "name": v.get("name"), "created_at": v.get("created_at")}
        for k, v in temp_storage.items()
        if k.startswith("proj_")
    ]
    return {"projects": projects}


@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """Get project details"""
    if project_id not in temp_storage:
        raise HTTPException(status_code=404, detail="Project not found")
    return temp_storage[project_id]


# ============== Data Import ==============

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a data file (CSV or Excel)"""
    # Generate file ID
    file_id = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Save to temp directory
    temp_dir = Path(tempfile.gettempdir()) / "qaqc_uploads"
    temp_dir.mkdir(exist_ok=True)
    
    file_path = temp_dir / f"{file_id}_{file.filename}"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Read and preview the file
        df = data_importer.read_table(file_path)
        
        # Store metadata
        temp_storage[file_id] = {
            "id": file_id,
            "filename": file.filename,
            "path": str(file_path),
            "row_count": len(df),
            "columns": list(df.columns),
            "uploaded_at": datetime.now().isoformat()
        }
        
        # Auto-detect column mapping
        suggestions = data_importer.suggest_mapping(list(df.columns))
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "row_count": len(df),
            "columns": list(df.columns),
            "mapping_suggestions": {
                k: {"column": v[0], "confidence": v[1]} 
                for k, v in suggestions.items() if v[0]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process file: {str(e)}")


@app.get("/api/preview/{file_id}")
async def preview_file(file_id: str, offset: int = 0, limit: int = 50):
    """Get paginated preview of uploaded data"""
    if file_id not in temp_storage:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_info = temp_storage[file_id]
    df = data_importer.read_table(file_info["path"])
    
    # Get slice of data
    preview_df = df.iloc[offset:offset + limit]
    
    return {
        "file_id": file_id,
        "total_rows": len(df),
        "offset": offset,
        "limit": limit,
        "columns": list(df.columns),
        "data": preview_df.fillna("").to_dict(orient="records")
    }


# ============== CRM Database ==============

@app.get("/api/crms")
async def list_crms(element: Optional[str] = None, search: Optional[str] = None):
    """List available CRMs with optional filtering"""
    try:
        if search:
            crms = crm_manager.search_crms(search)
        else:
            crms = crm_manager.get_all_crms()
        
        if element:
            crms = [c for c in crms if element.lower() in str(c.get("elements", [])).lower()]
        
        return {"crms": crms, "total": len(crms)}
    except Exception as e:
        return {"crms": [], "total": 0, "error": str(e)}


@app.get("/api/crms/{crm_name}")
async def get_crm(crm_name: str):
    """Get detailed CRM information"""
    crm_info = crm_manager.get_crm_info(crm_name)
    if not crm_info:
        raise HTTPException(status_code=404, detail="CRM not found")
    return crm_info


# ============== Analysis Execution ==============

@app.post("/api/analyze")
async def run_analysis(request: AnalysisRequest):
    """Run QAQC analysis on uploaded data"""
    if request.file_id not in temp_storage:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_info = temp_storage[request.file_id]
    
    try:
        # Load data
        df = data_importer.read_table(file_info["path"])
        
        # Apply column mapping
        mapping = {
            request.column_mapping.sample_id: "sample_id",
            request.column_mapping.sample_type: "sample_type",
            request.column_mapping.result: "result"
        }
        df = data_importer.apply_mapping(df, mapping)
        
        # Ensure numeric result column
        df["result"] = pd.to_numeric(df["result"], errors="coerce")
        
        results = {
            "analysis_id": f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "file_id": request.file_id,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_samples": len(df),
                "total_standards": 0,
                "total_blanks": 0,
                "total_duplicates": 0,
                "overall_pass_rate": 0.0
            },
            "standards": {"statistics": [], "data_points": [], "flagged_batches": []},
            "blanks": {"statistics": [], "flagged_blanks": []},
            "duplicates": {"statistics": [], "pairs": [], "flagged_pairs": []}
        }
        
        # Standards Analysis
        standards_df = df[df["sample_type"].str.upper() == "STANDARD"].copy()
        if len(standards_df) > 0:
            results["summary"]["total_standards"] = len(standards_df)
            standards_data = {
                "measured": standards_df["result"].tolist(),
                "certified": 1.0,  # Default, should come from CRM selection
                "uncertainty": 0.05
            }
            standards_results = standards_analyzer.analyze_standards(standards_data)
            results["standards"] = {
                "statistics": [{
                    "element": "Au",
                    "mean": standards_results.get("mean", 0),
                    "sd": standards_results.get("std_dev", 0),
                    "rsd": standards_results.get("rsd", 0),
                    "pass_rate": 100 if standards_results.get("overall_acceptable", False) else 50,
                    "count": len(standards_df)
                }],
                "data_points": [
                    {"sequence": i, "value": v, "status": "PASS" if abs(v - 1.0) < 0.1 else "FAIL"}
                    for i, v in enumerate(standards_df["result"].tolist())
                ],
                "flagged_batches": []
            }
        
        # Blanks Analysis
        blanks_df = df[df["sample_type"].str.upper() == "BLANK"].copy()
        if len(blanks_df) > 0:
            results["summary"]["total_blanks"] = len(blanks_df)
            blanks_data = {
                "blanks": blanks_df["result"].tolist(),
                "previous_samples": []
            }
            blanks_results = blanks_analyzer.analyze_blanks(blanks_data)
            results["blanks"] = {
                "statistics": [{
                    "element": "Au",
                    "max": blanks_results.get("max_value", 0),
                    "mean": blanks_results.get("mean", 0),
                    "median": blanks_results.get("median", 0),
                    "contamination_rate": blanks_results.get("contamination_rate", 0),
                    "count": len(blanks_df)
                }],
                "flagged_blanks": []
            }
        
        # Duplicates Analysis
        # Find duplicate pairs based on sample_id
        if "sample_id" in df.columns:
            dup_counts = df["sample_id"].value_counts()
            dup_ids = dup_counts[dup_counts == 2].index.tolist()
            
            if dup_ids:
                pairs = []
                for sample_id in dup_ids[:50]:  # Limit to 50 pairs
                    pair_df = df[df["sample_id"] == sample_id]
                    if len(pair_df) == 2:
                        values = pair_df["result"].tolist()
                        original, duplicate = values[0], values[1]
                        mean_val = (original + duplicate) / 2
                        rpd = abs(original - duplicate) / mean_val * 100 if mean_val > 0 else 0
                        pairs.append({
                            "sample_id": sample_id,
                            "original": original,
                            "duplicate": duplicate,
                            "rpd": rpd
                        })
                
                results["summary"]["total_duplicates"] = len(pairs)
                
                if pairs:
                    duplicates_data = {"duplicates": [[p["original"], p["duplicate"]] for p in pairs]}
                    dup_results = duplicates_analyzer.analyze_duplicates(duplicates_data)
                    
                    mean_rpd = sum(p["rpd"] for p in pairs) / len(pairs)
                    within_target = sum(1 for p in pairs if p["rpd"] <= request.qaqc_rules.duplicates_rpd_limit) / len(pairs) * 100
                    
                    results["duplicates"] = {
                        "statistics": [{
                            "element": "Au",
                            "mean_rpd": mean_rpd,
                            "mean_hard": dup_results.get("mean_absolute_diff", 0),
                            "within_target": within_target,
                            "count": len(pairs)
                        }],
                        "pairs": pairs,
                        "flagged_pairs": [p for p in pairs if p["rpd"] > request.qaqc_rules.duplicates_rpd_limit]
                    }
        
        # Calculate overall pass rate
        total_qc = results["summary"]["total_standards"] + results["summary"]["total_blanks"] + results["summary"]["total_duplicates"]
        if total_qc > 0:
            # Simplified pass rate calculation
            pass_count = (
                (results["summary"]["total_standards"] * results["standards"]["statistics"][0]["pass_rate"] / 100 if results["standards"]["statistics"] else 0) +
                (results["summary"]["total_blanks"] * (100 - results["blanks"]["statistics"][0]["contamination_rate"]) / 100 if results["blanks"]["statistics"] else 0) +
                (results["summary"]["total_duplicates"] * results["duplicates"]["statistics"][0]["within_target"] / 100 if results["duplicates"]["statistics"] else 0)
            )
            results["summary"]["overall_pass_rate"] = pass_count / total_qc * 100 if total_qc > 0 else 0
        
        # Store results
        temp_storage[results["analysis_id"]] = results
        temp_storage[request.file_id]["analysis_id"] = results["analysis_id"]
        
        return results
        
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}\n{traceback.format_exc()}")


@app.get("/api/results/{analysis_id}")
async def get_results(analysis_id: str):
    """Get analysis results"""
    if analysis_id not in temp_storage:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return temp_storage[analysis_id]


# ============== Export ==============

@app.post("/api/export/excel")
async def export_excel(analysis_id: str, background_tasks: BackgroundTasks):
    """Generate and download Excel report"""
    if analysis_id not in temp_storage:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    results = temp_storage[analysis_id]
    
    # Generate report
    output_dir = Path(tempfile.gettempdir()) / "qaqc_exports"
    output_dir.mkdir(exist_ok=True)
    
    filename = output_dir / f"qaqc_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    try:
        # Convert to format expected by ExcelReporter
        report_data = {
            "total_samples": results["summary"]["total_samples"],
            "analysis_date": results["timestamp"],
            "standards": results.get("standards", {}),
            "blanks": results.get("blanks", {}),
            "duplicates": results.get("duplicates", {})
        }
        
        excel_reporter.generate_excel_report(report_data, filename=str(filename))
        
        return FileResponse(
            path=str(filename),
            filename=filename.name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate Excel report: {str(e)}")


@app.post("/api/export/pdf")
async def export_pdf(analysis_id: str):
    """Generate and download PDF report"""
    if analysis_id not in temp_storage:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    results = temp_storage[analysis_id]
    
    output_dir = Path(tempfile.gettempdir()) / "qaqc_exports"
    output_dir.mkdir(exist_ok=True)
    
    filename = output_dir / f"qaqc_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    try:
        report_data = {
            "total_samples": results["summary"]["total_samples"],
            "analysis_date": results["timestamp"],
            "standards": results.get("standards", {}),
            "blanks": results.get("blanks", {}),
            "duplicates": results.get("duplicates", {})
        }
        
        pdf_reporter.generate_pdf_report(report_data, plots={}, filename=str(filename))
        
        return FileResponse(
            path=str(filename),
            filename=filename.name,
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF report: {str(e)}")


# ============== Run Server ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

