"""Interview question templates for different industries"""

from typing import List, Dict
from pydantic import BaseModel


class Question(BaseModel):
    text: str
    type: str  # "open", "yes_no", "multiple_choice", "numeric"
    options: List[str] = []  # For multiple choice
    required: bool = True


class InterviewTemplate(BaseModel):
    name: str
    description: str
    industry: str
    questions: List[Question]
    duration_minutes: int = 5
    passing_score: int = 70


class InterviewTemplates:
    """Pre-built interview templates for different verticals"""

    GENERAL_SERVICE = InterviewTemplate(
        name="General Service",
        description="Retail, hospitality, admin, customer service roles",
        industry="general",
        duration_minutes=5,
        passing_score=70,
        questions=[
            Question(
                text="Can you tell me about your previous work experience?",
                type="open",
                required=True,
            ),
            Question(
                text="What is your availability? Are you available weekends or evenings?",
                type="open",
                required=True,
            ),
            Question(
                text="Do you have reliable transportation to get to work?",
                type="yes_no",
                required=True,
            ),
            Question(
                text="What are your salary expectations?",
                type="open",
                required=True,
            ),
            Question(
                text="When would you be able to start?",
                type="open",
                required=True,
            ),
        ],
    )

    SKILLED_TRADES = InterviewTemplate(
        name="Skilled Trades",
        description="HVAC, plumbing, construction, electrical",
        industry="trades",
        duration_minutes=7,
        passing_score=75,
        questions=[
            Question(
                text="How many years of experience do you have in this trade?",
                type="numeric",
                required=True,
            ),
            Question(
                text="Do you have any certifications or licenses? Please list them.",
                type="open",
                required=True,
            ),
            Question(
                text="Are you comfortable working outdoors in various weather conditions?",
                type="yes_no",
                required=True,
            ),
            Question(
                text="Do you have OSHA safety training or certifications?",
                type="yes_no",
                required=False,
            ),
            Question(
                text="What tools or equipment are you most experienced with?",
                type="open",
                required=True,
            ),
            Question(
                text="Are you willing to travel to different job sites?",
                type="yes_no",
                required=True,
            ),
        ],
    )

    HEALTHCARE = InterviewTemplate(
        name="Healthcare",
        description="Dental, medical, chiropractic offices",
        industry="healthcare",
        duration_minutes=6,
        passing_score=80,
        questions=[
            Question(
                text="What healthcare certifications or degrees do you hold?",
                type="open",
                required=True,
            ),
            Question(
                text="How many years have you worked in a healthcare setting?",
                type="numeric",
                required=True,
            ),
            Question(
                text="Are you comfortable working with patients of all ages?",
                type="yes_no",
                required=True,
            ),
            Question(
                text="Do you have experience with [specific software/procedures]?",
                type="open",
                required=False,
            ),
            Question(
                text="Are you up to date on required vaccinations and health screenings?",
                type="yes_no",
                required=True,
            ),
            Question(
                text="Why do you want to work in healthcare?",
                type="open",
                required=True,
            ),
        ],
    )

    STAFFING_AGENCY = InterviewTemplate(
        name="Staffing Agency",
        description="General staffing, temp work, flexible placements",
        industry="staffing",
        duration_minutes=5,
        passing_score=65,
        questions=[
            Question(
                text="What types of jobs are you interested in?",
                type="open",
                required=True,
            ),
            Question(
                text="What is your availability? Full-time, part-time, or flexible?",
                type="multiple_choice",
                options=["Full-time", "Part-time", "Flexible", "Weekend only"],
                required=True,
            ),
            Question(
                text="Are you willing to travel for work assignments?",
                type="yes_no",
                required=True,
            ),
            Question(
                text="Do you have reliable transportation?",
                type="yes_no",
                required=True,
            ),
            Question(
                text="When can you start working?",
                type="open",
                required=True,
            ),
            Question(
                text="Have you worked through a staffing agency before?",
                type="yes_no",
                required=False,
            ),
        ],
    )


# Template registry
TEMPLATES = {
    "general": InterviewTemplates.GENERAL_SERVICE,
    "retail": InterviewTemplates.GENERAL_SERVICE,
    "hospitality": InterviewTemplates.GENERAL_SERVICE,
    "admin": InterviewTemplates.GENERAL_SERVICE,
    "trades": InterviewTemplates.SKILLED_TRADES,
    "hvac": InterviewTemplates.SKILLED_TRADES,
    "plumbing": InterviewTemplates.SKILLED_TRADES,
    "construction": InterviewTemplates.SKILLED_TRADES,
    "electrical": InterviewTemplates.SKILLED_TRADES,
    "healthcare": InterviewTemplates.HEALTHCARE,
    "dental": InterviewTemplates.HEALTHCARE,
    "medical": InterviewTemplates.HEALTHCARE,
    "chiropractic": InterviewTemplates.HEALTHCARE,
    "staffing": InterviewTemplates.STAFFING_AGENCY,
    "recruitment": InterviewTemplates.STAFFING_AGENCY,
}


def get_template(template_name: str) -> InterviewTemplate:
    """Get interview template by name"""
    template = TEMPLATES.get(template_name.lower())
    if not template:
        # Default to general service template
        return InterviewTemplates.GENERAL_SERVICE
    return template


# Unique templates list
_UNIQUE_TEMPLATES = [
    InterviewTemplates.GENERAL_SERVICE,
    InterviewTemplates.SKILLED_TRADES,
    InterviewTemplates.HEALTHCARE,
    InterviewTemplates.STAFFING_AGENCY,
]

# Pre-computed cached template summaries for fast O(1) response
_CACHED_TEMPLATE_LIST: List[Dict] = [
    {
        "name": t.name,
        "description": t.description,
        "industry": t.industry,
        "duration_minutes": t.duration_minutes,
        "question_count": len(t.questions),
    }
    for t in _UNIQUE_TEMPLATES
]


def list_templates() -> List[Dict]:
    """List all available templates (O(1) cached lookup)"""
    return _CACHED_TEMPLATE_LIST.copy()
