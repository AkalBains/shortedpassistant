from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from io import BytesIO
import matplotlib.pyplot as plt


def create_powerpoint(trait_data, radar_imgs, report_text):
    # Create a new PowerPoint presentation
    ppt = Presentation()

    # ----------------------
    # Slide 1: Title Slide
    # ----------------------
    title_slide_layout = ppt.slide_layouts[0]  # Title Slide
    slide = ppt.slides.add_slide(title_slide_layout)
    slide.shapes.title.text = "Leadership Report"
    slide.placeholders[1].text = "Generated using AI and assessment data"

    # ----------------------
    # Slide 2: Trait Data Table
    # ----------------------
    slide = ppt.slides.add_slide(ppt.slide_layouts[5])  # Blank layout
    title_shape = slide.shapes.title
    if title_shape:
        title_shape.text = "Trait Scores"

    rows, cols = trait_data.shape
    table = slide.shapes.add_table(rows + 1, cols, Inches(0.5), Inches(1.5), Inches(9), Inches(4)).table

    # Set column headers
    for col_index, column_name in enumerate(trait_data.columns):
        table.cell(0, col_index).text = str(column_name)

    # Fill table data
    for row_index, row in trait_data.iterrows():
        for col_index, value in enumerate(row):
            table.cell(row_index + 1, col_index).text = str(value)

    # ----------------------
    # Slide 3: Radar Charts
    # ----------------------
    for radar_img in radar_imgs:
        slide = ppt.slides.add_slide(ppt.slide_layouts[5])  # Blank layout
        left = Inches(1)
        top = Inches(1)
        slide.shapes.add_picture(radar_img, left, top, height=Inches(5))

    # ----------------------
    # Slide 4: AI-Generated Report
    # ----------------------
    slide = ppt.slides.add_slide(ppt.slide_layouts[1])  # Title and Content
    slide.shapes.title.text = "AI-Generated Leadership Summary"
    text_box = slide.placeholders[1]
    text_box.text = report_text

    # ----------------------
    # Save presentation to a BytesIO stream
    # ----------------------
    ppt_stream = BytesIO()
    ppt.save(ppt_stream)
    ppt_stream.seek(0)
    return ppt_stream
