"""
VASTU ONE - AI-Powered Prediction Engine
Uses LLM to generate natural language predictions
"""

import os
from typing import Dict, Any

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

from engine.astro.predictions_engine import get_predictions


class AIPredictionEngine:
    """AI-powered prediction engine using LLM"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if HAS_OPENAI and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def generate_narrative(self, country: str) -> Dict[str, Any]:
        """Generate natural language narrative from predictions"""
        data = get_predictions(country)
        if "error" in data:
            return data
        
        # If no API key, return structured data
        if not self.client:
            return self._fallback_narrative(data)
        
        # Build prompt
        prompt = self._build_prompt(data)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional Vedic astrologer. Write clear, insightful predictions based on the astrological data provided."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7,
            )
            
            narrative = response.choices[0].message.content
            
            return {
                "country": country,
                "date": data["date"],
                "narrative": narrative,
                "data": data,
            }
        except Exception as e:
            print(f"AI error: {e}")
            return self._fallback_narrative(data)
    
    def _build_prompt(self, data: Dict) -> str:
        """Build prompt from prediction data"""
        dasha = data["dasha"]
        yogas = data["yogas"]
        shadbala = data["shadbala"]
        ashtaka = data["ashtakavarga"]
        varshphal = data["varshphal"]
        transit = data.get("transit", {})
        
        prompt = f"""
        Generate a detailed astrological prediction for {data['country']} based on the following data:
        
        CURRENT DASHA:
        - Mahadasha: {dasha['mahadasha']['lord']}
        - Antardasha: {dasha['antardasha']['lord']}
        - Pratyantardasha: {dasha['pratyantardasha']['lord']}
        - Age: {dasha['age_years']} years
        
        YOGAS DETECTED ({yogas['total_yogas']} total):
        """
        
        for y in yogas["auspicious"][:5]:
            prompt += f"- {y['name']}: {y['effect']}\n"
        
        for y in yogas["doshas"][:3]:
            prompt += f"- DOSHA {y['name']}: {y['effect']}\n"
        
        prompt += f"""
        
        SHADBALA (Planetary Strength):
        - Strongest: {shadbala['strongest']}
        - Weakest: {shadbala['weakest']}
        
        ASHTAKAVARGA:
        - Total: {ashtaka['total']} points
        - Strongest signs: {', '.join([s[0] for s in ashtaka['strongest']])}
        - Weakest signs: {', '.join([s[0] for s in ashtaka['weakest']])}
        
        VARSHPHAL {varshphal['year']}:
        - Muntha: {varshphal['muntha']['rashi']}
        - Year Lord: {varshphal['year_lord']['planet']}
        
        TRANSIT (Current Planetary Positions):
        """
        
        for t in transit.get("planets", [])[:9]:
            prompt += f"- {t['planet']} in {t['rashi']} (House {t['house']})\n"
        
        prompt += """
        
        Based on this data, write a comprehensive prediction covering:
        1. Overall theme for the year
        2. Economic outlook
        3. Political situation
        4. Natural disaster risks
        5. War/conflict possibilities
        6. Key opportunities
        7. Recommended actions
        
        Write in clear, accessible language. Be specific but not deterministic.
        """
        
        return prompt
    
    def _fallback_narrative(self, data: Dict) -> Dict:
        """Fallback when no API key — generate narrative from templates"""
        dasha = data["dasha"]
        yogas = data["yogas"]
        
        narrative = f"""
        # {data['country']} — Astrological Analysis
        Generated: {data['date']}
        
        ## Current Period
        
        {data['country']} is currently in **{dasha['mahadasha']['lord']} Mahadasha** 
        with **{dasha['antardasha']['lord']} Antardasha** and 
        **{dasha['pratyantardasha']['lord']} Pratyantardasha**.
        
        """
        
        # Add dasha meaning
        dasha_meanings = {
            "Sun": "This period emphasizes leadership, authority, and government focus.",
            "Moon": "This period brings public emotions, water-related issues, and mass movements.",
            "Mars": "This period indicates military action, conflict, and courage.",
            "Mercury": "This period favors diplomacy, communication, and trade.",
            "Jupiter": "This period brings growth, wisdom, prosperity, and spiritual development.",
            "Venus": "This period emphasizes luxury, arts, diplomacy, and relationships.",
            "Saturn": "This period brings discipline, delays, and structural change.",
            "Rahu": "This period indicates sudden change, transformation, and foreign influence.",
            "Ketu": "This period brings spirituality, isolation, and sudden events.",
        }
        
        maha = dasha['mahadasha']['lord']
        narrative += f"{dasha_meanings.get(maha, '')}\n\n"
        
        # Add yogas
        if yogas['auspicious']:
            narrative += "## Positive Indicators\n\n"
            for y in yogas['auspicious']:
                narrative += f"- **{y['name']}** ({y['strength']}): {y['effect']}\n"
            narrative += "\n"
        
        if yogas['doshas']:
            narrative += "## Challenges\n\n"
            for y in yogas['doshas']:
                narrative += f"- **{y['name']}** ({y['strength']}): {y['effect']}\n"
            narrative += "\n"
        
        # Add predictions
        narrative += "## Detailed Predictions\n\n"
        for p in data['predictions'][:20]:
            narrative += f"**{p['title']}**\n{p['prediction']}\n\n"
        
        return {
            "country": data["country"],
            "date": data["date"],
            "narrative": narrative,
            "data": data,
            "note": "This is a template-based narrative. Set OPENAI_API_KEY for AI-powered version.",
        }


def generate_ai_prediction(country: str = "India"):
    """Convenience function"""
    engine = AIPredictionEngine()
    return engine.generate_narrative(country)


if __name__ == "__main__":
    result = generate_ai_prediction("India")
    print("=== AI PREDICTION ===")
    print(result.get("narrative", "")[:2000])
