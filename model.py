from dataclasses import dataclass, field
from typing import List, Optional
import uuid

@dataclass
class FarmRecord:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    record_type: str = ""
    location: str = ""
    area_ha: Optional[float] = None
    primary_crop: str = ""
    notes: str = ""

# Simple in‑memory store; replace with MySQL/Supabase in production
records_db: List[FarmRecord] = []
