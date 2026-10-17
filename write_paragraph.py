from pathlib import Path

code = '''"""
VASTU ONE - Deep Paragraph Explanation Engine
Generates Maha Guru level paragraph explanations for every prediction
"""

from typing import Dict, List, Any


def generate_dasha_paragraph(planet: str, level: str, start: str, end: str) -> str:
    """Generate detailed paragraph for Dasha"""
    
    dasha_details = {
        "Sun": {
            "nature": "Surya (Sun) is the Atmakaraka of the zodiac  the soul of the nation, the king, the father figure. It represents authority, government, leadership, and the vital force that animates all life.",
            "positive": "During Surya Dasha, the nation experiences strong leadership, government stability, and recognition on the world stage. The ruling class becomes more assertive, and national pride swells.",
            "negative": "The shadow side brings ego clashes, government scandals, and health issues for leaders. The nation may face challenges from within the ruling establishment.",
            "historical": "When India entered Surya periods historically, we saw strong central leadership  the Emergency era, the rise of coalition politics, and major constitutional changes all occurred under Surya's influence.",
        },
        "Moon": {
            "nature": "Chandra (Moon) is the Manas  the mind of the nation, the public consciousness, the emotional body of the people. It governs water, agriculture, public welfare, and the collective psyche.",
            "positive": "During Chandra Dasha, the public becomes more engaged, emotional issues dominate the discourse, and there is a focus on welfare, water resources, and food security. The nation becomes more receptive and nurturing.",
            "negative": "The shadow side brings mental stress, public unrest, water-related disasters (floods, tsunamis), and emotional volatility in the masses. The government may face public backlash.",
            "historical": "India's major flood disasters, farmer movements, and public health crises have often coincided with Chandra periods. The 1977 post-Emergency election and 2011 anti-corruption movement both occurred under strong Chandra influence.",
        },
        "Mars": {
            "nature": "Mangal (Mars) is the commander-in-chief of the cosmic army  the planet of war, courage, land, and bloodshed. It represents military power, defense, aggression, and the will to fight.",
            "positive": "During Mangal Dasha, the nation's military strength is enhanced, borders are secured, and enemies are defeated. There is courage, initiative, and decisive action.",
            "negative": "The shadow side brings war, border conflicts, terrorism, accidents, and bloodshed. The nation may face military challenges or internal violence.",
            "historical": "Every major war India has fought  1962, 1965, 1971, 1999  occurred during significant Mangal periods. The 2001 Parliament attack, 2008 Mumbai attacks, and 2019 Pulwama-Balakot episode all had strong Mars signatures.",
        },
        "Mercury": {
            "nature": "Budh (Mercury) is the messenger of the gods  the planet of communication, trade, diplomacy, intelligence, and analysis. It represents commerce, media, education, and the analytical mind of the nation.",
            "positive": "During Budh Dasha, trade flourishes, diplomatic relations improve, communication networks expand, and education gets a boost. The nation becomes more articulate and business-savvy.",
            "negative": "The shadow side brings trade disputes, communication breakdowns, diplomatic failures, and economic policy errors. The nation may face intelligence failures or media controversies.",
            "historical": "India's economic liberalization (1991), the IT boom (2000s), and major trade agreements have all occurred under strong Budh periods. The 2016 demonetization and GST rollout also had Mercury signatures.",
        },
        "Jupiter": {
            "nature": "Guru (Jupiter) is the teacher of the gods  the planet of wisdom, dharma, prosperity, and spiritual growth. It represents religion, law, education, expansion, and divine grace.",
            "positive": "During Guru Dasha, the nation experiences spiritual awakening, economic prosperity, educational reforms, and dharmic governance. There is expansion, growth, and divine protection.",
            "negative": "The shadow side brings over-optimism, religious conflicts, legal challenges, and misguided expansion. The nation may face challenges from religious orthodoxy or legal overreach.",
            "historical": "India's major spiritual movements, the Green Revolution, and the economic reforms of the 1990s all occurred under Guru's influence. The Ram Mandir movement, and various religious consolidations, also happened during Guru periods.",
        },
        "Venus": {
            "nature": "Shukra (Venus) is the preceptor of the demons  the planet of luxury, arts, relationships, and material pleasures. It represents diplomacy, entertainment, beauty, and the finer aspects of civilization.",
            "positive": "During Shukra Dasha, the nation experiences cultural renaissance, artistic achievements, diplomatic breakthroughs, and economic prosperity. There is beauty, harmony, and material comfort.",
            "negative": "The shadow side brings excess indulgence, relationship breakdowns, diplomatic failures, and moral decay. The nation may face scandals or cultural conflicts.",
            "historical": "India's film industry boom, cultural exports (yoga, ayurveda), and major diplomatic initiatives have often occurred under Shukra periods. The 1991 economic crisis ended with Venusian reforms, and the 2010s cultural nationalism also had Shukra signatures.",
        },
        "Saturn": {
            "nature": "Shani (Saturn) is the judge of the gods  the planet of discipline, delays, karma, and structural change. It represents labor, law, aging, and the karmic ledger of the nation.",
            "positive": "During Shani Dasha, the nation experiences structural reforms, discipline, and karmic justice. There is hard work, perseverance, and eventual reward after delays.",
            "negative": "The shadow side brings delays, obstacles, chronic problems, poverty, and karmic retribution. The nation may face prolonged crises or systemic failures.",
            "historical": "India's major economic crises (1991, 2013), the Emergency (1975-77), and various periods of social unrest have occurred under Shani's influence. The COVID-19 pandemic and subsequent economic contraction also had strong Saturn signatures.",
        },
        "Rahu": {
            "nature": "Rahu is the serpent of illusion  the planet of sudden change, foreign influence, technology, and unconventional paths. It represents obsession, ambition, and the shadow side of progress.",
            "positive": "During Rahu Dasha, the nation experiences technological breakthroughs, foreign investments, and sudden expansions. There is innovation, ambition, and rapid transformation.",
            "negative": "The shadow side brings deception, foreign conspiracies, technological disasters, and sudden reversals. The nation may face scandals, cyber attacks, or foreign interference.",
            "historical": "India's IT revolution (1990s), economic liberalization, and major foreign policy shifts have occurred under Rahu's influence. The 2G scam, coal scam, and various foreign interference episodes also had Rahu signatures.",
        },
        "Ketu": {
            "nature": "Ketu is the flag of the ancestors  the planet of spirituality, isolation, sudden events, and moksha. It represents detachment, occult knowledge, and the karmic residue of past actions.",
            "positive": "During Ketu Dasha, the nation experiences spiritual awakening, sudden insights, and liberation from old patterns. There is detachment, wisdom, and karmic resolution.",
            "negative": "The shadow side brings isolation, sudden losses, confusion, and spiritual crisis. The nation may face unexpected events or loss of direction.",
            "historical": "India's spiritual renaissance, the rise of new religious movements, and various periods of national introspection have occurred under Ketu's influence. The 1984 anti-Sikh riots, 1992 Babri demolition, and 2002 Gujarat riots all had Ketu signatures.",
        },
    }
    
    details = dasha_details.get(planet, {
        "nature": f"{planet} is a significant planetary influence.",
        "positive": "Positive effects may manifest.",
        "negative": "Negative effects may manifest.",
        "historical": "Historical patterns may correlate.",
    })
    
    paragraph = f"""
{level}: {planet} ({details['nature']})

This period began on {start} and will continue until {end}. During this time, the nation will experience the full spectrum of {planet}'s influence  both its luminous and shadow aspects.

{details['positive']}

However, the shadow side cannot be ignored. {details['negative']}

{details['historical']}

Classical Reference: BPHS Ch. 46 describes the effects of {planet} in detail. The Vimshottari Dasha system, revealed by Parashara Muni, is the most precise timing tool in Vedic astrology.
"""
    return paragraph.strip()


def generate_yoga_paragraph(yoga_name: str, effect: str, strength: str, ref: str) -> str:
    """Generate detailed paragraph for Yoga"""
    return f"""
{yoga_name} ({strength})

This yoga is formed by a specific combination of planetary energies in the national chart. {effect}

In the context of a nation, this yoga influences the collective destiny  its government, economy, military, and social fabric. The strength of this yoga determines how powerfully it will manifest. A "Strong" yoga will have obvious, undeniable effects, while a "Moderate" yoga will be felt more subtly.

Classical Reference: {ref}
"""


def generate_transit_paragraph(planet: str, rashi: str, house: int, bindu: int, verdict: str) -> str:
    """Generate detailed paragraph for Transit"""
    return f"""
{planet} transiting {rashi} (House {house})  Bindu Score: {bindu}/8

{planet} is currently moving through {rashi}, which falls in the {house}th house from the national ascendant. The {house}th house governs {get_house_meaning(house)}. With a bindu score of {bindu}/8, this transit is classified as {verdict}.

The bindu score is derived from the Ashtakavarga system, a sophisticated point-based method where each planet contributes points to different signs. A higher score indicates greater strength and more favorable results. A lower score indicates weakness and potential challenges.

When {planet} transits this position, it activates the significations of the {house}th house. The effects will be felt in the areas of {get_house_meaning(house)}. The {verdict.lower()} verdict suggests that the nation should {get_verdict_action(verdict)}.

Classical Reference: BPHS Ch. 45 describes the transit effects of {planet} in detail. Varahamihira's Brihat Samhita also provides specific rules for planetary transits.
"""


def get_house_meaning(house: int) -> str:
    meanings = {
        1: "country, leadership, national identity",
        2: "wealth, economy, currency, banking",
        3: "communication, neighbors, borders, media",
        4: "land, earthquakes, natural disasters, public welfare",
        5: "education, youth, creativity, political succession",
        6: "enemies, war, disease, military, health",
        7: "partnerships, alliances, war, international relations",
        8: "death, transformations, sudden events, crisis",
        9: "dharma, religion, foreign relations, higher learning",
        10: "government, politics, leadership, authority",
        11: "gains, alliances, economy, income",
        12: "losses, foreign, spiritual, espionage",
    }
    return meanings.get(house, "general matters")


def get_verdict_action(verdict: str) -> str:
    if "Excellent" in verdict or "Favorable" in verdict:
        return "take bold initiatives, expand, and capitalize on opportunities"
    elif "Challenging" in verdict:
        return "exercise caution, strengthen defenses, and avoid risky ventures"
    else:
        return "maintain balance, neither too aggressive nor too passive"


def generate_planet_paragraph(planet: str, data: Dict) -> str:
    """Generate detailed paragraph for a planet's position"""
    return f"""
{planet} in {data.get('rashi', '')} ({data.get('degree', 0)})  House {data.get('house', '')}

{planet} occupies {data.get('rashi', '')} at {data.get('degree', 0)} degrees, placing it in the {data.get('house', '')}th house from the national ascendant. Its dignity is {data.get('dignity', 'Neutral')}, and its nakshatra is {data.get('nakshatra', {}).get('name', '') if isinstance(data.get('nakshatra'), dict) else data.get('nakshatra', '')}.

The 1st house represents the nation's identity and leadership. 2nd house governs wealth and economy. 3rd house represents communication and neighbors. 4th house rules land and natural disasters. 5th house governs education and youth. 6th house rules war and enemies. 7th house represents partnerships and alliances. 8th house rules death and transformation. 9th house governs dharma and foreign relations. 10th house rules government and politics. 11th house represents gains and alliances. 12th house rules losses and foreign affairs.

With {planet} in the {data.get('house', '')}th house, the nation's destiny in these areas will be strongly influenced by this planetary placement. The nakshatra adds another layer  {data.get('nakshatra', {}).get('name', '') if isinstance(data.get('nakshatra'), dict) else ''}  which gives specific qualities to this placement.

Classical Reference: BPHS Ch. 36 describes the effects of {planet} in each house.
"""


def get_full_explanation_report(country: str = "India") -> Dict:
    """Generate full explanation report with paragraphs"""
    from engine.astro.master_prediction_engine import get_master_prediction
    
    data = get_master_prediction(country)
    
    paragraphs = []
    
    # Dasha paragraphs
    dasha = data.get("complete_dasha", {}).get("levels", {})
    for level_name, level in dasha.items():
        if level.get("planet"):
            para = generate_dasha_paragraph(
                level["planet"],
                level_name.title(),
                level.get("start_date", ""),
                level.get("end_date", ""),
            )
            paragraphs.append({
                "type": "Dasha",
                "title": f"{level_name.title()}: {level['planet']}",
                "paragraph": para,
            })
    
    # Yoga paragraphs
    for y in data.get("yogas_complete", {}).get("auspicious", []):
        para = generate_yoga_paragraph(y["name"], y["effect"], y["strength"], y.get("classical_ref", ""))
        paragraphs.append({
            "type": "Yoga",
            "title": y["name"],
            "paragraph": para,
        })
    
    # Transit paragraphs
    for t in data.get("transit_ashtakavarga", {}).get("transit_analysis", []):
        if t.get("verdict_type") == "negative":
            para = generate_transit_paragraph(t["planet"], t["rashi"], t["house"], t["bindu"], t["verdict"])
            paragraphs.append({
                "type": "Transit",
                "title": f"{t['planet']} in House {t['house']}",
                "paragraph": para,
            })
    
    # Planet paragraphs
    for planet, pdata in data.get("planetary_deep", {}).get("planets", {}).items():
        para = generate_planet_paragraph(planet, pdata)
        paragraphs.append({
            "type": "Planet",
            "title": planet,
            "paragraph": para,
        })
    
    return {
        "country": country,
        "total": len(paragraphs),
        "paragraphs": paragraphs,
    }


if __name__ == "__main__":
    result = get_full_explanation_report("India")
    
    print("=" * 70)
    print(f"DEEP PARAGRAPH EXPLANATIONS - {result['country']}")
    print("=" * 70)
    print(f"Total Paragraphs: {result['total']}")
    print()
    
    for p in result["paragraphs"][:5]:
        print(f"=== {p['type']}: {p['title']} ===")
        print(p["paragraph"])
        print()
        print("-" * 70)
        print()
'''

Path("engine/astro/deep_paragraph_engine.py").write_text(code, encoding="utf-8")
print("File written:", Path("engine/astro/deep_paragraph_engine.py").stat().st_size, "bytes")