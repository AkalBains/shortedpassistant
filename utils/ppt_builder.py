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
    radar_chart_2_path=None
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

    # === Page 6: Insert radar charts ===
    slide6 = prs.slides[5]
    if radar_chart_1_path and os.path.exists(radar_chart_1_path):
        slide6.shapes.add_picture(radar_chart_1_path, Inches(0.5), Inches(2.2), height=Inches(4.5))
    if radar_chart_2_path and os.path.exists(radar_chart_2_path):
        slide6.shapes.add_picture(radar_chart_2_path, Inches(5.3), Inches(2.2), height=Inches(4.5))

    prs.save(output_path)
    return output_path
