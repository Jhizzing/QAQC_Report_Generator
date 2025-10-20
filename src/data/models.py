"""
Data models for QAQC analysis.

Defines the core data structures used throughout the QAQC analysis system.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SampleType(Enum):
    """Enumeration of sample types."""
    UNKNOWN = "Unknown"
    STANDARD = "Standard"
    BLANK = "Blank"
    DUPLICATE = "Duplicate"
    CHECK = "Check"
    FIELD = "Field"
    CRM = "CRM"


class AnalysisStatus(Enum):
    """Enumeration of analysis status."""
    PENDING = "Pending"
    PASS = "Pass"
    WARNING = "Warning"
    FAIL = "Fail"
    ERROR = "Error"


@dataclass
class Sample:
    """Core sample data structure."""
    sample_id: str
    hole_id: Optional[str] = None
    from_depth: Optional[float] = None
    to_depth: Optional[float] = None
    sample_type: SampleType = SampleType.UNKNOWN
    result: Optional[float] = None
    lab: Optional[str] = None
    method: Optional[str] = None
    batch_id: Optional[str] = None
    analyte: Optional[str] = None
    units: Optional[str] = None
    qualifier: Optional[str] = None
    detection_limit: Optional[float] = None
    date_analyzed: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization processing."""
        if isinstance(self.sample_type, str):
            try:
                self.sample_type = SampleType(self.sample_type)
            except ValueError:
                self.sample_type = SampleType.UNKNOWN


@dataclass
class Standard(Sample):
    """Standard (CRM) sample with certified values."""
    crm_id: Optional[str] = None
    certified_value: Optional[float] = None
    certified_sd: Optional[float] = None
    lot_number: Optional[str] = None
    z_score: Optional[float] = None
    bias: Optional[float] = None
    bias_percent: Optional[float] = None
    status: AnalysisStatus = AnalysisStatus.PENDING

    def calculate_z_score(self) -> Optional[float]:
        """Calculate Z-score for the standard."""
        if self.certified_value is None or self.certified_sd is None or self.result is None:
            return None

        if self.certified_sd == 0:
            return None

        self.z_score = (self.result - self.certified_value) / self.certified_sd
        return self.z_score

    def calculate_bias(self) -> Optional[float]:
        """Calculate bias for the standard."""
        if self.certified_value is None or self.result is None:
            return None

        if self.certified_value == 0:
            return None

        self.bias = self.result - self.certified_value
        self.bias_percent = (self.bias / self.certified_value) * 100
        return self.bias


@dataclass
class Blank(Sample):
    """Blank sample for contamination assessment."""
    threshold: Optional[float] = None
    threshold_multiplier: float = 3.0
    status: AnalysisStatus = AnalysisStatus.PENDING
    is_carry_over: bool = False

    def check_contamination(self) -> bool:
        """Check if blank exceeds contamination threshold."""
        if self.result is None or self.detection_limit is None:
            return False

        if self.threshold is None:
            self.threshold = self.detection_limit * self.threshold_multiplier

        return self.result > self.threshold


@dataclass
class Duplicate(Sample):
    """Duplicate sample for precision assessment."""
    primary_id: Optional[str] = None
    duplicate_id: Optional[str] = None
    primary_result: Optional[float] = None
    duplicate_result: Optional[float] = None
    mean_result: Optional[float] = None
    absolute_difference: Optional[float] = None
    relative_percent_difference: Optional[float] = None
    correlation: Optional[float] = None
    nugget_ratio: Optional[float] = None
    status: AnalysisStatus = AnalysisStatus.PENDING

    def calculate_precision_metrics(self) -> Dict[str, float]:
        """Calculate precision metrics for duplicate pair."""
        if self.primary_result is None or self.duplicate_result is None:
            return {}

        # Mean result
        self.mean_result = (self.primary_result + self.duplicate_result) / 2

        # Absolute difference
        self.absolute_difference = abs(self.primary_result - self.duplicate_result)

        # Relative Percent Difference (RPD)
        if self.mean_result != 0:
            self.relative_percent_difference = (self.absolute_difference / self.mean_result) * 100
        else:
            self.relative_percent_difference = None

        return {
            "mean_result": self.mean_result,
            "absolute_difference": self.absolute_difference,
            "relative_percent_difference": self.relative_percent_difference
        }


@dataclass
class Batch:
    """Batch of samples for analysis."""
    batch_id: str
    lab: Optional[str] = None
    date_analyzed: Optional[datetime] = None
    method: Optional[str] = None
    analyte: Optional[str] = None
    samples: List[Sample] = field(default_factory=list)
    standards: List[Standard] = field(default_factory=list)
    blanks: List[Blank] = field(default_factory=list)
    duplicates: List[Duplicate] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_sample(self, sample: Sample):
        """Add a sample to the batch and categorize it."""
        self.samples.append(sample)

        if isinstance(sample, Standard):
            self.standards.append(sample)
        elif isinstance(sample, Blank):
            self.blanks.append(sample)
        elif isinstance(sample, Duplicate):
            self.duplicates.append(sample)

    def get_sample_count(self) -> int:
        """Get total number of samples in batch."""
        return len(self.samples)

    def get_standards_count(self) -> int:
        """Get number of standards in batch."""
        return len(self.standards)

    def get_blanks_count(self) -> int:
        """Get number of blanks in batch."""
        return len(self.blanks)

    def get_duplicates_count(self) -> int:
        """Get number of duplicates in batch."""
        return len(self.duplicates)


@dataclass
class QAQCDataset:
    """Complete QAQC dataset containing all samples and batches."""
    project_name: str
    created_date: datetime = field(default_factory=datetime.now)
    batches: List[Batch] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_batch(self, batch: Batch):
        """Add a batch to the dataset."""
        self.batches.append(batch)

    def get_all_samples(self) -> List[Sample]:
        """Get all samples from all batches."""
        all_samples = []
        for batch in self.batches:
            all_samples.extend(batch.samples)
        return all_samples

    def get_all_standards(self) -> List[Standard]:
        """Get all standards from all batches."""
        all_standards = []
        for batch in self.batches:
            all_standards.extend(batch.standards)
        return all_standards

    def get_all_blanks(self) -> List[Blank]:
        """Get all blanks from all batches."""
        all_blanks = []
        for batch in self.batches:
            all_blanks.extend(batch.blanks)
        return all_blanks

    def get_all_duplicates(self) -> List[Duplicate]:
        """Get all duplicates from all batches."""
        all_duplicates = []
        for batch in self.batches:
            all_duplicates.extend(batch.duplicates)
        return all_duplicates
