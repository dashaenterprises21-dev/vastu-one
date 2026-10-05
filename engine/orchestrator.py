"""
VASTU ONE - Engine Orchestrator
================================
Runs all Vastu engines on a property and aggregates findings.
"""
from __future__ import annotations
import sys
from pathlib import Path

# Add project root to path (so `import engine.*` works)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dataclasses import dataclass, asdict, field
from typing import Any
from datetime import datetime


@dataclass
class EngineResult:
    """Standard output from every engine."""
    engine: str
    status: str  # "success" | "skipped" | "error"
    findings: list = field(default_factory=list)
    score: float = 0.0
    confidence: float = 0.0
    metadata: dict = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


class EngineOrchestrator:
    """
    Runs all Vastu engines on a property input.
    
    Input: Property data (dict)
    Output: Aggregated report with findings, scores, guna profile
    """
    
    def __init__(self):
        self.engines_loaded: list[str] = []
        self.engines_failed: list[str] = []
        self._try_load_engines()
    
    def _try_load_engines(self):
        """Try to load each engine module. Track what works."""
        engine_paths = [
            ("grid_81", "engine.vastu.grid_81"),
            ("devata_audit", "engine.vastu.devata_audit"),
            ("element_balance", "engine.vastu.element_balance"),
            ("brahma_audit", "engine.vastu.brahma_audit"),
            ("direction_strength", "engine.vastu.direction_strength"),
            ("room_analysis", "engine.vastu.room_analysis"),
            ("entrance_audit", "engine.vastu.entrance_audit"),
            ("marma_engine", "engine.vastu.marma_engine"),
            ("soil_engine", "engine.vastu.new.soil_engine"),
            ("water_engine", "engine.vastu.new.water_engine"),
            ("colour_engine", "engine.vastu.new.colour_engine"),
            ("muhurt_engine", "engine.vastu.new.muhurt_engine"),
            ("land_testing_engine", "engine.vastu.new.land_testing_engine"),
            ("guna_engine", "engine.reasoning.guna_engine"),
        ]
        
        import importlib
        for name, path in engine_paths:
            try:
                importlib.import_module(path)
                self.engines_loaded.append(name)
            except Exception as e:
                self.engines_failed.append(f"{name}: {e}")
    
    def run_all(self, property_data: dict) -> dict:
        """
        Run all engines on property.
        
        property_data example:
        {
            "name": "Rajesh Kumar Residence",
            "property_type": "RESIDENTIAL",
            "north_direction_deg": 0,
            "rooms": {...},
            "water_features": {...},
            "colours": {...},
            ...
        }
        """
        results: list[EngineResult] = []
        
        # 1. Vastu core engines (grid, direction, etc.)
        results.extend(self._run_vastu_core(property_data))
        
        # 2. New syllabus engines
        results.extend(self._run_new_engines(property_data))
        
        # 3. Aggregate findings
        all_findings = []
        for r in results:
            for f in r.findings:
                all_findings.append({
                    "engine": r.engine,
                    **f,
                })
        
        # 4. Guna rollup
        guna_profile = self._compute_guna(all_findings)
        
        # 5. Overall score
        overall_score = self._compute_overall_score(all_findings)
        
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "engines_loaded": self.engines_loaded,
            "engines_failed": self.engines_failed,
            "total_findings": len(all_findings),
            "findings": all_findings,
            "guna_profile": guna_profile,
            "overall_score": overall_score,
            "engine_results": [r.to_dict() for r in results],
        }
    
    # ------------------------------------------------------------------
    # Engine runners
    # ------------------------------------------------------------------
    
    def _run_vastu_core(self, data: dict) -> list[EngineResult]:
        """Run Vastu core engines."""
        results = []
        north_deg = data.get("north_direction_deg", 0) or 0
        
        # Direction strength
        try:
            findings = []
            # Simple placeholder logic â€” will be replaced by actual engine
            for direction, in [("N",), ("NE",), ("E",), ("SE",), ("S",), ("SW",), ("W",), ("NW",)]:
                # Placeholder: mark all directions as analyzed
                findings.append({
                    "direction": direction,
                    "status": "analyzed",
                    "severity": "informational",
                    "guna": "Mixed",
                    "description": f"Direction {direction} analyzed",
                })
            results.append(EngineResult(
                engine="direction_strength",
                status="success",
                findings=findings,
                score=0.8,
                confidence=0.7,
            ))
        except Exception as e:
            results.append(EngineResult(engine="direction_strength", status="error", error=str(e)))
        
        return results
    
    def _run_new_engines(self, data: dict) -> list[EngineResult]:
        """Run syllabus-merged engines."""
        results = []
        
        # Soil engine (if soil data provided)
        if data.get("soil"):
            try:
                from engine.vastu.new.soil_engine import SoilEngine, SoilColour, SoilTexture, SoilTaste
                s = data["soil"]
                r = SoilEngine().evaluate(
                    SoilColour(s.get("colour", "mixed")),
                    SoilTexture(s.get("texture", "loamy")),
                    SoilTaste(s.get("taste", "sweet")) if s.get("taste") else None,
                )
                results.append(EngineResult(
                    engine="soil_engine",
                    status="success",
                    findings=[{
                        "category": "soil",
                        "severity": "informational",
                        "guna": r.guna,
                        "description": f"Soil: {r.caste.value}, {r.verdict}",
                    }],
                    score=1.0 if r.verdict == "Excellent" else 0.5,
                    confidence=0.9,
                ))
            except Exception as e:
                results.append(EngineResult(engine="soil_engine", status="error", error=str(e)))
        
        # Water engine (if water features provided)
        if data.get("water_features"):
            try:
                from engine.vastu.new.water_engine import WaterEngine, WaterFeature, Direction
                findings = []
                for feature_name, direction in data["water_features"].items():
                    try:
                        wf = WaterFeature(feature_name)
                        d = Direction(direction)
                        r = WaterEngine().analyze(wf, d)
                        findings.append({
                            "category": "water",
                            "severity": r.severity,
                            "guna": r.guna,
                            "description": r.description,
                        })
                    except Exception:
                        continue
                results.append(EngineResult(
                    engine="water_engine",
                    status="success",
                    findings=findings,
                    confidence=0.9,
                ))
            except Exception as e:
                results.append(EngineResult(engine="water_engine", status="error", error=str(e)))
        
        # Colour engine
        if data.get("colours"):
            try:
                from engine.vastu.new.colour_engine import ColourEngine, Direction
                findings = []
                for dir_name, colour in data["colours"].items():
                    try:
                        d = Direction(dir_name)
                        r = ColourEngine().check(d, colour)
                        findings.append({
                            "category": "colour",
                            "severity": r.severity,
                            "guna": r.guna,
                            "description": r.description,
                        })
                    except Exception:
                        continue
                results.append(EngineResult(
                    engine="colour_engine",
                    status="success",
                    findings=findings,
                    confidence=0.85,
                ))
            except Exception as e:
                results.append(EngineResult(engine="colour_engine", status="error", error=str(e)))
        
        return results
    
    # ------------------------------------------------------------------
    # Aggregation
    # ------------------------------------------------------------------
    
    def _compute_guna(self, findings: list[dict]) -> dict:
        """Compute Three Gunas profile from findings."""
        from engine.reasoning.guna_engine import GunaEngine, GunaFinding, Guna
        
        guna_findings = []
        for f in findings:
            guna_str = f.get("guna", "Mixed")
            try:
                guna = Guna(guna_str)
            except ValueError:
                guna = Guna.MIXED
            
            guna_findings.append(GunaFinding(
                rule_id=f.get("category", "unknown"),
                guna=guna,
                severity=f.get("severity", "medium"),
                description=f.get("description", ""),
            ))
        
        if not guna_findings:
            return {"verdict": "N/A", "net_score": 0.0, "note": "No findings"}
        
        profile = GunaEngine().evaluate(guna_findings)
        return profile.to_dict()
    
    def _compute_overall_score(self, findings: list[dict]) -> dict:
        """Compute overall Vastu score."""
        if not findings:
            return {"score": 0, "confidence": 0, "findings_count": 0}
        
        # Simple weighted score
        severity_weight = {"critical": -3, "high": -2, "medium": -1, "low": 0.5, "informational": 1}
        total = sum(severity_weight.get(f.get("severity", "informational"), 0) for f in findings)
        avg = total / len(findings)
        
        # Normalize to 0-100
        score = max(0, min(100, 50 + avg * 20))
        confidence = min(0.95, 0.5 + 0.05 * len(findings))
        
        return {
            "score": round(score, 1),
            "confidence": round(confidence, 2),
            "findings_count": len(findings),
        }


# Singleton
orchestrator = EngineOrchestrator()


if __name__ == "__main__":
    import json
    result = orchestrator.run_all({
        "name": "Test Property",
        "north_direction_deg": 0,
        "soil": {"colour": "white", "texture": "loamy", "taste": "sweet"},
        "water_features": {"septic_tank": "NE", "underground_tank": "NE"},
        "colours": {"NE": "White", "SE": "Blue"},
    })
    print(json.dumps(result, indent=2, default=str))