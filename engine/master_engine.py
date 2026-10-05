"""
Master Engine — Sab engines ko jodkar complete report
"""
import os
import sys
from datetime import datetime

ENGINE_DIR = os.path.dirname(__file__)
sys.path.insert(0, ENGINE_DIR)

from astro_engine_v3_complete import AstroEngineV3Complete
from yogas_engine import YogasEngine
from doshas_engine import DoshasEngine
from predictions_engine import PredictionsEngine
from remedies_engine_v3 import RemediesEngineV3
from transit_engine import TransitEngine
from sadesati_engine import SadesatiEngine


class MasterEngine:
    def __init__(self):
        self.astro = AstroEngineV3Complete()
    
    def full_report(self, dob, tob="12:00", place="Unknown"):
        positions = self.astro.calculate_positions(dob, tob)
        lagna = self.astro.calculate_lagna(dob, tob, place)
        dasha = self.astro.vimshottari_dasha(dob, tob)
        
        yogas = YogasEngine(positions, lagna, self.astro.planets).detect_all()
        doshas = DoshasEngine(positions, lagna, self.astro.planets).detect_all()
        predictions = PredictionsEngine(positions, dasha).generate()
        remedies = RemediesEngineV3(positions).generate()
        transit = TransitEngine(self.astro, dob, tob).calculate()
        sadesati = SadesatiEngine(positions, self.astro.rashis).calculate()
        
        return {
            "basic": self.astro.basic_details(dob, tob, place),
            "lagna": lagna,
            "positions": positions,
            "bhava_chalit": self.astro.bhava_chalit(dob, tob, place),
            "shodashvarga": self.astro.shodashvarga(dob, tob),
            "dasha": dasha,
            "ashtakavarga": self.astro.ashtakavarga(dob, tob),
            "shadbala": self.astro.shadbala(dob, tob),
            "yogas": yogas,
            "doshas": doshas,
            "predictions": predictions,
            "remedies": remedies,
            "transit": transit,
            "sadesati": sadesati,
            "meta": {
                "generated_at": datetime.now().isoformat(),
                "engine_version": "3.0",
                "total_yogas": len(yogas),
                "total_doshas": len(doshas)
            }
        }


if __name__ == "__main__":
    engine = MasterEngine()
    report = engine.full_report("1990-05-04", "21:35", "Bhandara")
    print("Yogas:", len(report["yogas"]))
    print("Doshas:", len(report["doshas"]))
    print("Predictions:", len(report["predictions"]))
    print("SUCCESS: Master engine working!")
