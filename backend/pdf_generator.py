import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

def generate_assessment_pdf(assessment: dict):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CertTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor('#781a28'), alignment=1)
    subtitle_style = ParagraphStyle('CertSubtitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=colors.HexColor('#57534e'), alignment=1)
    
    story = []
    story.append(Paragraph("ONION GRADING & DEFECT INSPECTION CERTIFICATE", title_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#781a28'), spaceAfter=14))
    
    data = [
        ["Lot Identifier", assessment.get('lot_id', 'N/A')],
        ["Supplier", assessment.get('supplier_name', 'N/A')],
        ["Grade", assessment.get('grade', 'N/A')],
        ["Score", f"{assessment.get('computed_score', 0)} / 100"],
        ["Status", assessment.get('quality_status', 'N/A')],
        ["Inspection Date", assessment.get('created_at', datetime.now().isoformat())]
    ]
    
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f4')),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
