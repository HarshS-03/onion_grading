from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class AssessmentBase(BaseModel):
    lot_id: Optional[str] = None
    supplier_name: str
    supplier_phone: str
    state: str = "Maharashtra"
    variety: str = "nashik_red"
    grade: str = "Grade A"
    size_class: str = "Medium"
    moisture: float = 12.0
    sprouting: float = 0.0
    damage: float = 0.0
    doubles: float = 0.0
    inspector_name: Optional[str] = ""
    notes: Optional[str] = ""

class AssessmentCreate(AssessmentBase):
    pass

class AssessmentResponse(AssessmentBase):
    id: int
    computed_score: int
    quality_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
