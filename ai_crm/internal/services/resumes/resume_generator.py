"""Resume document generator service (DOCX/PDF)."""

from datetime import date
import io

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

from ai_crm.pkg import context
from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.models.ai_crm import parsed_resume as parsed_resume_models
from ai_crm.pkg.models.exceptions import ai as ai_exceptions

logger = logger_lib.get_logger(__name__)


async def generate_docx_resume(
    context: context.AnyContext,
    parsed_resume: parsed_resume_models.ParsedResume,
) -> bytes:
    """Generate DOCX resume from parsed data.

    Args:
        context: Application context
        parsed_resume: Structured resume data

    Returns:
        DOCX file as bytes

    Raises:
        ResumeGenerationFailed: If generation fails
    """
    try:
        logger.info(f"Generating DOCX resume for: {parsed_resume.name}")

        doc = Document()
        _set_document_margins(doc)

        _add_header(doc, parsed_resume)
        _add_summary(doc, parsed_resume)
        _add_professional_experience(doc, parsed_resume)
        _add_education(doc, parsed_resume)
        _add_skills(doc, parsed_resume)
        _add_certifications(doc, parsed_resume)

        output = io.BytesIO()
        doc.save(output)
        output.seek(0)

        logger.info("Successfully generated DOCX resume")
        return output.getvalue()

    except Exception as e:
        logger.error(f"Resume generation failed: {e}")
        raise ai_exceptions.ResumeGenerationFailed from e


def _set_document_margins(doc: Document) -> None:
    """Set document margins."""
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)


def _add_header(
    doc: Document, resume: parsed_resume_models.ParsedResume
) -> None:
    """Add resume header with name and contact info."""
    name_para = doc.add_paragraph()
    name_run = name_para.add_run(resume.name.upper())
    name_run.font.size = Pt(24)
    name_run.font.bold = True
    name_run.font.color.rgb = RGBColor(0, 51, 102)
    name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if resume.position:
        position_para = doc.add_paragraph()
        position_run = position_para.add_run(resume.position)
        position_run.font.size = Pt(14)
        position_run.font.italic = True
        position_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    contact_info = []
    if resume.email:
        contact_info.append(f"Email: {resume.email}")
    if resume.phone:
        contact_info.append(f"Phone: {resume.phone}")
    if resume.linkedin:
        contact_info.append(f"LinkedIn: {resume.linkedin}")

    if contact_info:
        contact_para = doc.add_paragraph(" | ".join(contact_info))
        contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        contact_run = contact_para.runs[0]
        contact_run.font.size = Pt(10)

    doc.add_paragraph()


def _add_summary(
    doc: Document, resume: parsed_resume_models.ParsedResume
) -> None:
    """Add professional summary section."""
    if not resume.summary:
        return

    _add_section_header(doc, "PROFESSIONAL SUMMARY")
    summary_para = doc.add_paragraph(resume.summary)
    summary_para.paragraph_format.space_after = Pt(12)


def _add_professional_experience(
    doc: Document, resume: parsed_resume_models.ParsedResume
) -> None:
    """Add professional experience section."""
    if not resume.professional_experience:
        return

    _add_section_header(doc, "PROFESSIONAL EXPERIENCE")

    for exp in resume.professional_experience:
        company_para = doc.add_paragraph()
        company_run = company_para.add_run(exp.company_name)
        company_run.font.bold = True
        company_run.font.size = Pt(12)

        position_para = doc.add_paragraph()
        position_run = position_para.add_run(exp.position)
        position_run.font.italic = True
        position_run.font.size = Pt(11)

        date_range = _format_date_range(exp.hired_date, exp.fired_date)
        date_para = doc.add_paragraph(date_range)
        date_para.runs[0].font.size = Pt(10)
        date_para.runs[0].font.color.rgb = RGBColor(100, 100, 100)

        if exp.achievements:
            for achievement in exp.achievements:
                ach_para = doc.add_paragraph(achievement, style="List Bullet")
                ach_para.paragraph_format.left_indent = Inches(0.25)

        doc.add_paragraph()


def _add_education(
    doc: Document, resume: parsed_resume_models.ParsedResume
) -> None:
    """Add education section."""
    if not resume.education:
        return

    _add_section_header(doc, "EDUCATION")

    for edu in resume.education:
        institution_para = doc.add_paragraph()
        institution_run = institution_para.add_run(edu.institution)
        institution_run.font.bold = True
        institution_run.font.size = Pt(12)

        if edu.degree:
            degree_para = doc.add_paragraph(edu.degree)
            degree_para.runs[0].font.size = Pt(11)

        date_range = _format_date_range(edu.from_date, edu.to_date)
        date_para = doc.add_paragraph(date_range)
        date_para.runs[0].font.size = Pt(10)
        date_para.runs[0].font.color.rgb = RGBColor(100, 100, 100)

        if edu.description:
            desc_para = doc.add_paragraph(edu.description)
            desc_para.paragraph_format.left_indent = Inches(0.25)

        doc.add_paragraph()


def _add_skills(
    doc: Document, resume: parsed_resume_models.ParsedResume
) -> None:
    """Add skills section."""
    if not any(
        [
            resume.skills.tech_stack,
            resume.skills.languages,
            resume.skills.soft_skills,
        ]
    ):
        return

    _add_section_header(doc, "SKILLS")

    if resume.skills.tech_stack:
        tech_para = doc.add_paragraph()
        tech_para.add_run("Technical Skills: ").font.bold = True
        tech_para.add_run(resume.skills.tech_stack)

    if resume.skills.languages:
        lang_para = doc.add_paragraph()
        lang_para.add_run("Languages: ").font.bold = True
        lang_para.add_run(resume.skills.languages)

    if resume.skills.soft_skills:
        soft_para = doc.add_paragraph()
        soft_para.add_run("Soft Skills: ").font.bold = True
        soft_para.add_run(resume.skills.soft_skills)

    doc.add_paragraph()


def _add_certifications(
    doc: Document, resume: parsed_resume_models.ParsedResume
) -> None:
    """Add certifications section."""
    if not resume.certifications:
        return

    _add_section_header(doc, "CERTIFICATIONS & TRAINING")

    for cert in resume.certifications:
        cert_para = doc.add_paragraph()
        cert_run = cert_para.add_run(cert.name)
        cert_run.font.bold = True
        cert_run.font.size = Pt(11)

        if cert.date_obtained:
            date_str = cert.date_obtained.strftime("%B %Y")
            date_para = doc.add_paragraph(date_str)
            date_para.runs[0].font.size = Pt(10)
            date_para.runs[0].font.color.rgb = RGBColor(100, 100, 100)

        if cert.description:
            desc_para = doc.add_paragraph(cert.description)
            desc_para.paragraph_format.left_indent = Inches(0.25)

        doc.add_paragraph()


def _add_section_header(doc: Document, title: str) -> None:
    """Add section header with styling."""
    header_para = doc.add_paragraph()
    header_run = header_para.add_run(title)
    header_run.font.size = Pt(14)
    header_run.font.bold = True
    header_run.font.color.rgb = RGBColor(0, 51, 102)

    header_para.add_run().add_break()


def _format_date_range(from_date: date | None, to_date: date | None) -> str:
    """Format date range string."""
    if not from_date:
        return ""

    from_str = from_date.strftime("%B %Y")
    to_str = "Present" if to_date is None else to_date.strftime("%B %Y")

    return f"{from_str} - {to_str}"
