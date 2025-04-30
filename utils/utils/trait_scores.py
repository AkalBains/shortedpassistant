# utils/trait_scores.py

def calculate_report_scores(personal_ratings, capability_ratings):
    scale = {"Below": 1, "Developing": 2, "Hits": 3, "Good": 4, "Strong": 5}

    def avg(traits, source):
        values = [scale[source[trait]] for trait in traits]
        return round(sum(values) / len(values), 2)

    # === Page 5 bar chart metrics ===
    bar_scores = {
        "Purpose Energy": avg(["Mission", "Drive", "Agency"], personal_ratings),
        "Intellectual Energy": avg(["Judgment", "Incisiveness", "Curiosity"], personal_ratings),
        "Emotional Energy": avg(["Positivity", "Resilience", "Growth Mindset"], personal_ratings),
        "People Energy": avg(["Compelling Impact", "Connection", "Environmental Insight"], personal_ratings),

        "Performance Impact": avg(["Achieves Sustainable Impact", "Creates Focus", "Orchestrates Delivery"], capability_ratings),
        "Strategic Framing": avg(["Frames Complexity", "Identifies New Possibilities", "Generates Solutions"], capability_ratings),
        "Mobilisation": avg(["Inspires People", "Drives Culture", "Grows Self and Others"], capability_ratings),
        "Powerful Relationships": avg(["Aligns Stakeholders", "Models Collaboration", "Builds Teams"], capability_ratings),
    }

    # === Page 6 radar chart data ===
    radar_data = {
        "Personal Characteristics": {trait: scale[personal_ratings[trait]] for trait in personal_ratings},
        "Leadership Capabilities": {trait: scale[capability_ratings[trait]] for trait in capability_ratings}
    }

    return bar_scores, radar_data
