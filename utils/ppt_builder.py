from pptx import Presentation
from pptx.util import Inches
import os

def build_report_pptx(
    template_path,
    output_path,
    candidate_name,
    role_and_company,
    personal_profile,
    strengths,
    development_areas,
    future_considerations,
    radar_chart_1_path=None,
    radar_chart_2_path=None,
    bar_scores=None
):
    prs = Presentation(template_path)

    # === Page 1 ===
    slide1 = prs.slides[0]
    for shape in slide1.shapes:
        if shape.has_text_frame:
            text = shape.text
            if "Insert Candidate Name" in text:
                shape.text = text.replace("Insert Candidate Name", candidate_name)
            if "Insert Role and Company Name" in text:
                shape.text = text.replace("Insert Role and Company Name", role_and_company)

    # === Page 3 ===
    slide3 = prs.slides[2]
    for shape in slide3.shapes:
        if shape.has_text_frame:
            text = shape.text
            if "Insert Personal Profile here" in text:
                shape.text = personal_profile
            elif "Strength One" in text:
                shape.text = strengths[0]["title"]
            elif "Strength Two" in text:
                shape.text = strengths[1]["title"]
            elif "Strength Three" in text:
                shape.text = strengths[2]["title"]
            elif "Development Area One" in text:
                shape.text = development_areas[0]["title"]
            elif "Development Area Two" in text:
                shape.text = development_areas[1]["title"]
            elif "Development Area Three" in text:
                shape.text = development_areas[2]["title"]
            elif "Insert explanatory paragraph" in text:
                if "Strength" in text:
                    shape.text = strengths.pop(0)["paragraph"]
                else:
                    shape.text = development_areas.pop(0)["paragraph"]
            elif "Insert Future Considerations here" in text:
                shape.text = future_considerations

    # === Page 5: Adjust bar widths ===
    if bar_scores:
        slide5 = prs.slides[4]
        max_width = Inches(5.5)  # Full width for a score of 5

        for trait, score in bar_scores.items():
            for shape in slide5.shapes:
                if shape.has_text_frame and trait.lower() in shape.text.strip().lower():
                    # Find the nearest non-text shape (the bar) beneath the text box
                    label_top = shape.top
                    label_left = shape.left
                    for bar in slide5.shapes:
                        if not bar.has_text_frame and abs(bar.left - label_left) < Inches(0.1) and bar.top > label_top:
                            bar.width = max_width * (score / 5)
                            break  # Stop after first match

    # === Page 6: Insert radar charts ===
    slide6 = prs.slides[5]
    if radar_chart_1_path and os.path.exists(radar_chart_1_path):
        slide6.shapes.add_picture(radar_chart_1_path, Inches(0.5), Inches(2.2), height=Inches(4.5))
    if radar_chart_2_path and os.path.exists(radar_chart_2_path):
        slide6.shapes.add_picture(radar_chart_2_path, Inches(5.3), Inches(2.2), height=Inches(4.5))

    prs.save(output_path)
    return output_path
