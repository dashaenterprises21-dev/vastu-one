import json
from engine.grid_81 import Grid81
from engine.devata_audit import DevataAudit
from engine.element_balance import ElementBalance
from engine.remedy_engine import RemedyEngine
from scoring.vastu_score import VastuScore


def run_demo():
    with open("data/devatas_45.json", "r", encoding="utf-8-sig") as f:
        devatas_json = json.load(f)

    with open("data/elements_5.json", "r", encoding="utf-8-sig") as f:
        elements_json = json.load(f)

    with open("data/shastra_rules.json", "r", encoding="utf-8-sig") as f:
        shastra_rules = json.load(f)

    grid = Grid81()
    grid.load_devatas(devatas_json)
    grid.map_devata_to_grid()

    audit = DevataAudit(grid, devatas_json, shastra_rules)
    balance = ElementBalance(elements_json)
    remedy = RemedyEngine(devatas_json, elements_json)
    scorer = VastuScore()

    plan = [
        {"row": 0, "col": 0, "object": "toilet"},
        {"row": 4, "col": 4, "object": "heavy"},
        {"row": 8, "col": 8, "object": "cash"},
        {"row": 2, "col": 2, "object": "water"},
    ]

    result = audit.audit_plan(plan)
    print("=== Devata Audit ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    balance.analyze_zone("NE", ["toilet", "water"])
    balance.analyze_zone("SW", ["cash"])
    print("\n=== Element Balance ===")
    print(json.dumps(balance.get_imbalance(), indent=2))

    print("\n=== Remedies ===")
    for issue in result["issues"]:
        r = remedy.remedy_for_devata(issue["devata"])
        print(json.dumps(r, indent=2, ensure_ascii=False))

    final = scorer.calculate(
        devata_score=result["devata_score"],
        element_balance_score=70,
        brahma_score=50,
        direction_score=80
    )
    print("\n=== Final Score ===")
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    run_demo()
