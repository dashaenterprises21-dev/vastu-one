"""
Package Score — Package-wise scoring & recommendations
"""

class PackageScore:
    """Package-based scoring"""

    def __init__(self):
        self.package_features = {
            "bronze": {"weight": 0.4, "features": ["auo", "marma", "basic_remedies"]},
            "silver": {"weight": 0.6, "features": ["astro", "disha_bal", "auo", "marma"]},
            "gold": {"weight": 0.8, "features": ["astro", "numerology", "disha_bal", "auo", "marma", "occult"]},
            "platinum": {"weight": 1.0, "features": ["all"]}
        }

    def calculate(self, package: str, base_score: float) -> dict:
        """Calculate package-specific score"""
        package = package.lower()
        if package not in self.package_features:
            return {"error": f"Invalid package: {package}"}

        info = self.package_features[package]
        adjusted = round(base_score * info["weight"] / 0.5, 2)  # normalized
        adjusted = min(100, adjusted)

        return {
            "package": package,
            "base_score": base_score,
            "package_score": adjusted,
            "weight": info["weight"],
            "features": info["features"],
            "grade": self._grade(adjusted),
            "recommended_for": self._recommend(base_score)
        }

    def _grade(self, score: float) -> str:
        if score >= 85: return "A+ (Excellent)"
        if score >= 70: return "A (Good)"
        if score >= 55: return "B (Average)"
        if score >= 40: return "C (Below Average)"
        return "D (Poor)"

    def _recommend(self, base_score: float) -> str:
        if base_score >= 80: return "Bronze sufficient"
        if base_score >= 65: return "Silver recommended"
        if base_score >= 50: return "Gold recommended"
        return "Platinum recommended"


if __name__ == "__main__":
    import json
    scorer = PackageScore()
    base = 74.33
    for pkg in ["bronze", "silver", "gold", "platinum"]:
        result = scorer.calculate(pkg, base)
        print(f"\n{pkg.upper()}:")
        print(json.dumps(result, indent=2))
    print("\n✅ Package Score working!")
