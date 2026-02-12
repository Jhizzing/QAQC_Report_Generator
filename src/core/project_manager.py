"""
Project Manager Module

Handles the persistence of project state (save/load) for LogiQore Reporter.
"""
import json
import gzip
import base64
import io
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import pandas as pd

class ProjectManager:
    """
    Manages project state persistence.
    
    Uses a compressed JSON format to store:
    - Project metadata
    - Configuration
    - Analysis results
    - Raw data (serialized)
    """
    
    VERSION = "1.0.0"
    
    def __init__(self):
        pass
        
    def save_project(self, state: Dict[str, Any], filepath: str) -> None:
        """
        Save project state to a file.
        
        Args:
            state: Dictionary containing application state
            filepath: Path to save the project file
        """
        project_data = {
            "meta": {
                "version": self.VERSION,
                "created_at": datetime.now().isoformat(),
                "app_name": "LogiQore Reporter"
            },
            "config": state.get("config", {}),
            "results": state.get("results"),
            "data": self._serialize_data(state.get("data"))
        }
        
        # Save as compressed JSON
        with gzip.open(filepath, 'wt', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2)
            
    def load_project(self, filepath: str) -> Dict[str, Any]:
        """
        Load project state from a file.
        
        Args:
            filepath: Path to the project file
            
        Returns:
            Dictionary containing application state
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Project file not found: {filepath}")
            
        try:
            with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                project_data = json.load(f)
                
            # Validate version (basic check)
            version = project_data.get("meta", {}).get("version")
            if not version:
                raise ValueError("Invalid project file: missing version")
                
            return {
                "config": project_data.get("config", {}),
                "results": project_data.get("results"),
                "data": self._deserialize_data(project_data.get("data"))
            }
            
        except (gzip.BadGzipFile, json.JSONDecodeError):
            raise ValueError("Invalid project file format")
            
    def _serialize_data(self, data_info: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Serialize data info dictionary, converting DataFrame to JSON/base64."""
        if not data_info:
            return None
            
        serialized = data_info.copy()
        
        # Handle DataFrame
        if 'dataframe' in serialized:
            df = serialized['dataframe']
            if isinstance(df, pd.DataFrame):
                # Convert to JSON string
                serialized['dataframe'] = df.to_json(orient='split', date_format='iso')
                
        # Handle 'data' key if present (sometimes used as alias)
        if 'data' in serialized:
            df = serialized['data']
            if isinstance(df, pd.DataFrame):
                serialized['data'] = df.to_json(orient='split', date_format='iso')
                
        return serialized
        
    def _deserialize_data(self, data_info: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Deserialize data info dictionary, converting JSON back to DataFrame."""
        if not data_info:
            return None
            
        deserialized = data_info.copy()
        
        # Handle DataFrame
        if 'dataframe' in deserialized and isinstance(deserialized['dataframe'], str):
            try:
                deserialized['dataframe'] = pd.read_json(
                    io.StringIO(deserialized['dataframe']), 
                    orient='split'
                )
            except ValueError:
                # Fallback for older formats or errors
                pass
                
        # Handle 'data' key
        if 'data' in deserialized and isinstance(deserialized['data'], str):
            try:
                deserialized['data'] = pd.read_json(
                    io.StringIO(deserialized['data']), 
                    orient='split'
                )
            except ValueError:
                pass
                
        return deserialized
