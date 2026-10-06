"""
VASTU ONE - Behen ka Course Auto-Seed Script
==============================================
Creates Advance Astro Vastu course with 30 modules + 200 lessons.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from database.base import AsyncSessionLocal
from database.models import Course, CourseSection, Lesson, User
from sqlalchemy import select


# ==========================================
# COURSE DATA â€” 30 Modules with Lessons
# ==========================================
COURSE_DATA = {
    "title": "Advance Astro Vastu",
    "slug": "advance-astro-vastu",
    "description": "Complete 30-module professional course on Astro Vastu integration. Learn 16 directions, 45 energy fields, 12 houses, dasha, AutoCAD, and practical case studies.",
    "language": "hi",
    "duration_weeks": 16,
    "price_inr": 15000,
    "is_published": True,
    "modules": [
        {"title": "Module 1: Vastu Shastra Foundation", "lessons": [
            "Introduction to Vastu Shastra",
            "History & Fundamental Concepts",
            "Importance in Residential & Commercial",
            "Basic Principles of Vastu",
            "Vastu & Space Planning",
            "Vastu Purusha Concept",
            "Vastu Purusha Mandala",
            "Understanding Brahmasthan",
            "Positive & Negative Spatial Factors",
            "Basic Vastu Assessment Process",
        ]},
        {"title": "Module 2: Entrance Directions", "lessons": [
            "Importance of Main Entrance",
            "Understanding Entrance Direction",
            "8 Main Directions",
            "16 Directions Explained",
            "Entrance Placement & Direction",
            "Direction-wise Entrance Analysis",
            "Entrance and Energy Flow",
            "Basic Entrance Defects",
            "Entrance-related Remedies",
            "Practical Entrance Case Examples",
        ]},
        {"title": "Module 3: 16 Directions Detailed Study", "lessons": [
            "North â€” Meaning & Significance",
            "North-East â€” Meaning & Significance",
            "East â€” Meaning & Significance",
            "South-East â€” Meaning & Significance",
            "South â€” Meaning & Significance",
            "South-West â€” Meaning & Significance",
            "West â€” Meaning & Significance",
            "North-West â€” Meaning & Significance",
            "Understanding Sub-Directions",
            "Direction-wise Element Association",
            "Direction-wise Functional Planning",
            "Practical Direction Analysis",
        ]},
        {"title": "Module 4: 45 Energy Fields", "lessons": [
            "Introduction to 45 Energy Fields",
            "Understanding Energy Zones",
            "45 Energy Fields â€” Basic Identification",
            "Direction-wise Energy Field Understanding",
            "Energy Field Activation Concepts",
            "Energy Field Imbalance",
            "Practical Application of Energy Fields",
            "Energy Field Analysis in Floor Plans",
            "Case Study Based Understanding",
        ]},
        {"title": "Module 5: Five Elements (Pancha Bhuta)", "lessons": [
            "Introduction to Five Elements",
            "Earth Element",
            "Water Element",
            "Fire Element",
            "Air Element",
            "Space Element",
            "Characteristics of Five Elements",
            "Direction & Element Relationship",
            "Elemental Balance",
            "Elemental Imbalance",
            "Identifying Element-related Issues",
            "Practical Five Element Analysis",
            "Element-based Remedies",
        ]},
        {"title": "Module 6: Cut & Extended Directions", "lessons": [
            "What is a Cut?",
            "What is an Extension?",
            "Identifying Directional Cuts",
            "Identifying Directional Extensions",
            "Impact of Cuts & Extensions",
            "Direction-wise Analysis",
            "Plot Shape & Vastu",
            "Irregular Plot Understanding",
            "Remedies for Directional Cuts",
            "Remedies for Directional Extensions",
            "Case Study Examples",
        ]},
        {"title": "Module 7: Vastu Purusha & Mandala", "lessons": [
            "Vastu Purusha â€” Introduction",
            "Vastu Purusha Mandala",
            "Understanding the Grid",
            "Centre & Brahmasthan",
            "Zone-wise Understanding",
            "Practical Application in Floor Plans",
            "Residential Application",
            "Commercial Application",
            "Common Planning Mistakes",
        ]},
        {"title": "Module 8: Residential Vastu", "lessons": [
            "Plot Selection Basics",
            "Plot Shape & Slope",
            "Main Entrance",
            "Living Room Placement",
            "Master Bedroom",
            "Children's Bedroom",
            "Guest Bedroom",
            "Kitchen Placement",
            "Pooja / Prayer Space",
            "Toilet & Bathroom Placement",
            "Staircase Placement",
            "Study Area",
            "Dining Area",
            "Balcony & Open Spaces",
            "Windows & Ventilation",
            "Water Tank",
            "Underground Water Tank",
            "Septic Tank",
            "Parking Area",
            "Garden / Green Area",
        ]},
        {"title": "Module 9: Commercial Vastu", "lessons": [
            "Office Vastu Basics",
            "Shop Vastu",
            "Showroom Vastu",
            "Clinic Vastu",
            "Restaurant Vastu",
            "Factory / Industrial Space",
            "Reception Area",
            "Owner / Decision Maker Seating",
            "Staff Seating",
            "Cash Counter",
            "Workstation Planning",
            "Meeting Room",
            "Store Room",
            "Entrance Analysis",
            "Toilet & Utility Areas",
            "Commercial Floor Plan Analysis",
        ]},
        {"title": "Module 10: Room-wise Advanced Vastu", "lessons": [
            "Main Entrance Analysis",
            "Bedroom Analysis",
            "Master Bedroom Analysis",
            "Children's Room Analysis",
            "Kitchen Analysis",
            "Toilet Analysis",
            "Bathroom Analysis",
            "Pooja Room Analysis",
            "Living Room Analysis",
            "Dining Area Analysis",
            "Study Room Analysis",
            "Office Room Analysis",
            "Staircase Analysis",
            "Parking Analysis",
            "Balcony & Terrace Analysis",
            "Storage Areas",
        ]},
        {"title": "Module 11: Vastu Defects & Analysis", "lessons": [
            "Common Vastu Defects",
            "Directional Defects",
            "Entrance-related Defects",
            "Element-related Defects",
            "Room Placement Defects",
            "Centre / Brahmasthan Issues",
            "Cut & Extension Defects",
            "Plot-related Issues",
            "Floor Plan Defects",
            "Identifying Major & Minor Issues",
            "Priority-based Analysis",
            "Practical Defect Identification",
        ]},
        {"title": "Module 12: Vastu Remedies", "lessons": [
            "Introduction to Remedies",
            "Principle of Vastu Remedies",
            "Direction-wise Remedies",
            "Element-based Remedies",
            "Entrance Remedies",
            "Bedroom Remedies",
            "Kitchen Remedies",
            "Toilet Remedies",
            "Brahmasthan Remedies",
            "Cut & Extension Remedies",
            "Colour-based Remedies",
            "Placement-based Remedies",
            "Practical & Non-Structural Remedies",
            "Remedy Selection",
            "Explaining to Clients",
            "Ethical Approach",
        ]},
        {"title": "Module 13: Astrology Basics for Astro Vastu", "lessons": [
            "Introduction to Astrology",
            "Horoscope Basics",
            "Understanding Lagna",
            "12 Houses â€” Introduction",
            "12 Rashis",
            "Rashis & Their Lords",
            "Planets â€” Basic Significance",
            "Direction of Rashis",
            "Planet & Direction Relationship",
            "House & Direction Connection",
            "Basic Horoscope Reading",
            "Understanding Planetary Influence",
            "Astrology & Vastu Integration",
        ]},
        {"title": "Module 14: 12 Houses Detailed Study", "lessons": [
            "1st House â€” Self & Personality",
            "2nd House â€” Family & Wealth",
            "3rd House â€” Communication",
            "4th House â€” Home & Property",
            "5th House â€” Education",
            "6th House â€” Service & Challenges",
            "7th House â€” Partnership & Marriage",
            "8th House â€” Transformation",
            "9th House â€” Fortune & Learning",
            "10th House â€” Career",
            "11th House â€” Gains & Networks",
            "12th House â€” Expenses & Isolation",
            "House-wise Practical Interpretation",
            "Property-related Houses",
            "Career-related Houses",
            "Wealth-related Houses",
        ]},
        {"title": "Module 15: 12 Rashis & Lords", "lessons": [
            "12 Rashis Introduction",
            "Rashi Characteristics",
            "Rashi Lords",
            "Element of Each Rashi",
            "Direction of Rashis",
            "Rashi & Planet Relationship",
            "Rashi-based Interpretation",
            "Practical Horoscope Examples",
            "Application in Astro Vastu",
        ]},
        {"title": "Module 16: Planets & Directions", "lessons": [
            "Sun â€” Basic Significance",
            "Moon â€” Basic Significance",
            "Mars â€” Basic Significance",
            "Mercury â€” Basic Significance",
            "Jupiter â€” Basic Significance",
            "Venus â€” Basic Significance",
            "Saturn â€” Basic Significance",
            "Rahu â€” Basic Significance",
            "Ketu â€” Basic Significance",
            "Planetary Directions",
            "Planetary Energy & Space",
            "Astro Vastu Application",
        ]},
        {"title": "Module 17: Dasha / Timeline", "lessons": [
            "What is Dasha?",
            "Understanding Mahadasha",
            "Understanding Antardasha",
            "Dasha Timeline",
            "Planetary Period Analysis",
            "Dasha & Life Events",
            "Property-related Timeline",
            "Career-related Timeline",
            "Basic Astro Vastu Application",
            "Practical Chart Examples",
        ]},
        {"title": "Module 18: Horoscope + Vastu Integration", "lessons": [
            "Why Combine Astrology & Vastu?",
            "Horoscope-based Vastu Approach",
            "Directional Analysis through Horoscope",
            "House & Direction Correlation",
            "Planetary Influence & Space",
            "Property-related Analysis",
            "Career & Workplace Analysis",
            "Family & Residential Analysis",
            "Identifying Priority Areas",
            "Practical Astro Vastu Method",
            "Client Case Interpretation",
        ]},
        {"title": "Module 19: Advanced Vastu Analysis", "lessons": [
            "Complete Floor Plan Reading",
            "Direction Mapping",
            "Zone Analysis",
            "Energy Field Analysis",
            "Five Element Analysis",
            "Entrance Analysis",
            "Room Placement Analysis",
            "Cut & Extension Analysis",
            "Defect Identification",
            "Remedy Planning",
            "Client Requirement Analysis",
            "Final Report Preparation",
        ]},
        {"title": "Module 20: Vastu Consultancy Process", "lessons": [
            "How to Take Client Details",
            "Client Requirement Understanding",
            "Required Documents & Floor Plans",
            "Direction Identification",
            "Measurement Basics",
            "Floor Plan Study",
            "Vastu Defect Identification",
            "Priority-wise Recommendations",
            "Remedy Selection",
            "Client Communication",
            "Consultation Presentation",
            "Follow-up Process",
            "Professional Etiquette",
        ]},
        {"title": "Module 21: Practical Floor Plan Training", "lessons": [
            "How to Read a Floor Plan",
            "North Direction Identification",
            "16-Direction Mapping",
            "Zone Identification",
            "Room Placement Analysis",
            "Entrance Analysis",
            "Kitchen Analysis",
            "Bedroom Analysis",
            "Toilet Analysis",
            "Staircase Analysis",
            "Brahmasthan Analysis",
            "Cut & Extension Identification",
            "Five Element Analysis",
            "Final Floor Plan Assessment",
        ]},
        {"title": "Module 22: Case Studies", "lessons": [
            "Residential Case Study",
            "Flat / Apartment Case Study",
            "Independent House Case Study",
            "Commercial Case Study",
            "Office Case Study",
            "Shop / Showroom Case Study",
            "Plot Case Study",
            "Defect Identification",
            "Astro Vastu Case Study",
            "Remedy Planning",
            "Before & After Analysis",
            "Client-style Discussions",
        ]},
        {"title": "Module 23: AutoCAD Vastu Practical", "lessons": [
            "Introduction to AutoCAD",
            "AutoCAD Interface",
            "Basic Drawing Commands",
            "Line & Polyline",
            "Rectangle & Circle",
            "Modify Commands",
            "Trim & Extend",
            "Offset",
            "Move & Copy",
            "Rotate & Mirror",
            "Dimensioning",
            "Layers",
            "Text & Annotation",
            "Creating Basic Floor Plans",
            "North Direction Marking",
            "16-Direction Grid Preparation",
            "Vastu Zone Marking",
            "Final Vastu Floor Plan",
            "Basic Printing / Plotting",
        ]},
        {"title": "Module 24: Vastu Consultation Workflow", "lessons": [
            "Client Enquiry Handling",
            "Initial Discussion",
            "Required Information Collection",
            "Birth Details Collection",
            "Property Details Collection",
            "Floor Plan Collection",
            "Direction & Measurement Requirements",
            "Vastu Analysis Workflow",
            "Astrology Analysis Workflow",
            "Combining Both Analyses",
            "Identifying Main Concerns",
            "Preparing Recommendations",
            "Preparing Remedy Plan",
            "Explaining Findings Professionally",
            "Preparing Client Presentation",
            "Consultation Follow-up",
        ]},
        {"title": "Module 25: Advanced Practical Training", "lessons": [
            "Live Floor Plan Analysis",
            "Direction Identification Practice",
            "16-Direction Practice",
            "45 Energy Field Practice",
            "Five Element Practice",
            "Cut & Extension Practice",
            "Entrance Analysis Practice",
            "Room-wise Analysis Practice",
            "Defect Identification Practice",
            "Remedy Selection Practice",
            "Astrology Chart Practice",
            "Astro Vastu Integration Practice",
            "Client Communication Practice",
        ]},
        {"title": "Module 26: Professional Case Study Work", "lessons": [
            "Case Study 1 â€” Residential",
            "Case Study 2 â€” Apartment",
            "Case Study 3 â€” Commercial",
            "Case Study 4 â€” Office",
            "Case Study 5 â€” Astro Vastu",
            "Case Study Documentation",
            "Floor Plan Marking",
            "Problem Identification",
            "Analysis",
            "Recommendations",
            "Remedy Planning",
            "Final Consultation Format",
        ]},
        {"title": "Module 27: Vastu Report Preparation", "lessons": [
            "Basic Report Format",
            "Property Details",
            "Direction & Floor Plan",
            "Zone-wise Observations",
            "Major Vastu Points",
            "Room-wise Recommendations",
            "Defect Summary",
            "Remedy Summary",
            "Priority-wise Recommendations",
            "Client-friendly Presentation",
            "Professional Documentation",
        ]},
        {"title": "Module 28: Advance Astro Vastu Final Integration", "lessons": [
            "Vastu + Astrology Fundamentals",
            "Direction + Rashi Connection",
            "House + Direction Connection",
            "Planet + Direction Connection",
            "Five Elements + Directions",
            "45 Energy Fields + Floor Plan",
            "Cut & Extension + Remedies",
            "Horoscope + Property Analysis",
            "Dasha / Timeline + Consultation",
            "Complete Astro Vastu Case Analysis",
            "Practical Client Consultation",
        ]},
        {"title": "Module 29: Course Practicals & Assignments", "lessons": [
            "Direction Identification Assignment",
            "16 Directions Assignment",
            "Five Elements Assignment",
            "45 Energy Fields Assignment",
            "Cut & Extension Assignment",
            "Entrance Analysis Assignment",
            "Residential Floor Plan Assignment",
            "Commercial Floor Plan Assignment",
            "Horoscope Basics Assignment",
            "Astro Vastu Integration Assignment",
            "AutoCAD Floor Plan Assignment",
            "Complete Case Study Assignment",
        ]},
        {"title": "Module 30: Professional Outcome & Certification", "lessons": [
            "Understanding Vastu from Basic to Advanced",
            "Analysing 16 Directions",
            "Understanding 45 Energy Fields",
            "Applying Five Element Concepts",
            "Identifying Cuts & Extensions",
            "Analysing Residential & Commercial",
            "Basic Astrology for Astro Vastu",
            "Reading 12 Houses & 12 Rashis",
            "Understanding Dasha / Timeline",
            "Integrating Astrology with Vastu",
            "Analysing Floor Plans",
            "Identifying Vastu Defects",
            "Suggesting Appropriate Remedies",
            "Using AutoCAD for Vastu",
            "Preparing Professional Reports",
            "Conducting Practical Case Studies",
            "Handling Client Consultations",
            "Professional Certification",
        ]},
    ],
}


# ==========================================
# MAIN SEED FUNCTION
# ==========================================
async def seed_course():
    async with AsyncSessionLocal() as db:
        # Get instructor (first consultant)
        result = await db.execute(
            select(User).where(User.role == "CONSULTANT").limit(1)
        )
        instructor = result.scalar_one_or_none()
        if not instructor:
            print("âŒ No consultant found. Create one first.")
            return
        
        print(f"âœ… Instructor: {instructor.full_name}")
        
        # Check if course exists
        existing = await db.execute(
            select(Course).where(Course.slug == COURSE_DATA["slug"])
        )
        course = existing.scalar_one_or_none()
        
        if course:
            print(f"â„¹ï¸  Course exists: {course.id}")
        else:
            course = Course(
                tenant_id=instructor.tenant_id,
                instructor_id=instructor.id,
                title=COURSE_DATA["title"],
                slug=COURSE_DATA["slug"],
                description=COURSE_DATA["description"],
                language=COURSE_DATA["language"],
                duration_weeks=COURSE_DATA["duration_weeks"],
                price_inr=COURSE_DATA["price_inr"],
                is_published=COURSE_DATA["is_published"],
            )
            db.add(course)
            await db.flush()
            print(f"âœ… Course created: {course.id}")
        
        # Create modules + lessons
        total_modules = 0
        total_lessons = 0
        
        for m_idx, module_data in enumerate(COURSE_DATA["modules"]):
            # Check if module exists
            existing_mod = await db.execute(
                select(CourseSection).where(
                    CourseSection.course_id == course.id,
                    CourseSection.order_index == m_idx,
                )
            )
            section = existing_mod.scalar_one_or_none()
            
            if not section:
                section = CourseSection(
                    course_id=course.id,
                    title=module_data["title"],
                    description=f"Module {m_idx + 1} of 30",
                    order_index=m_idx,
                )
                db.add(section)
                await db.flush()
                total_modules += 1
                print(f"\nðŸ“š [{m_idx + 1}/30] {module_data['title']}")
            else:
                print(f"\nðŸ“š [{m_idx + 1}/30] {module_data['title']} (exists)")
            
            # Create lessons
            for l_idx, lesson_title in enumerate(module_data["lessons"]):
                existing_lesson = await db.execute(
                    select(Lesson).where(
                        Lesson.section_id == section.id,
                        Lesson.order_index == l_idx,
                    )
                )
                if existing_lesson.scalar_one_or_none():
                    continue
                
                lesson = Lesson(
                    section_id=section.id,
                    module_id=None,
                    title=lesson_title,
                    content_type="video",
                    content_url="https://www.youtube.com/watch?v=PLACEHOLDER",
                    text_content=f"{lesson_title} â€” Full lesson content coming soon.",
                    duration_minutes=20 + (l_idx % 3) * 5,  # 20-30 min
                    order_index=l_idx,
                    is_preview=(m_idx == 0 and l_idx < 2),  # First 2 lessons of Module 1 free
                )
                db.add(lesson)
                total_lessons += 1
        
        await db.commit()
        
        print(f"\n" + "=" * 60)
        print(f"ðŸŽ‰ COURSE SEEDED SUCCESSFULLY")
        print(f"=" * 60)
        print(f"  Course:        {course.title}")
        print(f"  Course ID:     {course.id}")
        print(f"  Slug:          {course.slug}")
        print(f"  Modules:       {total_modules} new + {30 - total_modules} existing = 30")
        print(f"  Lessons:       {total_lessons} new")
        print(f"  Price:         Rs {course.price_inr}")
        print(f"  Published:     {course.is_published}")
        print(f"  Language:      {course.language}")
        print(f"\nðŸŒ Course URL:")
        print(f"  http://localhost:8000/lms/course-detail.html?course_id={course.id}")


if __name__ == "__main__":
    asyncio.run(seed_course())