from fastapi import FastAPI, APIRouter, Form, UploadFile, File, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from supabase import create_client, Client

from database import engine, SessionLocal, Base
from schemas import AssessmentResponse
from models import Assessment, OnionVariety, DefectSample
from utils import calculate_quality_metrics
from pdf_generator import generate_assessment_pdf
from fastapi.responses import Response

SUPABASE_API_URL = os.getenv("SUPABASE_API_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase_client: Optional[Client] = None
if SUPABASE_API_URL and SUPABASE_KEY:
    try:
        supabase_client = create_client(SUPABASE_API_URL, SUPABASE_KEY)
        print("Supabase client initialized successfully")
    except Exception as e:
        print("Could not initialize Supabase client:", e)
else:
    print("Warning: SUPABASE_API_URL or SUPABASE_KEY not found in env")
from schemas import AssessmentResponse
from models import Assessment, OnionVariety, DefectSample
from utils import calculate_quality_metrics
from pdf_generator import generate_assessment_pdf
from fastapi.responses import Response

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

DEFAULT_VARIETIES = [
    {
        "id": "nashik_red",
        "code": "nashik_red",
        "name": "Nashik Red",
        "type": "Rabi / Storage",
        "variety_type": "Rabi / Storage",
        "origin": "Nashik, Maharashtra",
        "img": "/varieties/nashik-red.jpg",
        "image_url": "/varieties/nashik-red.jpg",
        "characteristics": "High TSS, firm tight scales, deep purplish-red skin with excellent storage life.",
        "order": 1,
    },
    {
        "id": "bhima_super",
        "code": "bhima_super",
        "name": "Bhima Super",
        "type": "Kharif / High Yield",
        "variety_type": "Kharif / High Yield",
        "origin": "ICAR-DOGR, Rajgurunagar",
        "img": "/varieties/Bhima-Super-Red-Onion.jpg",
        "image_url": "/varieties/Bhima-Super-Red-Onion.jpg",
        "characteristics": "Vibrant red round bulbs, high yield, moderate pungency.",
        "order": 2,
    },
    {
        "id": "bellary_red",
        "code": "bellary_red",
        "name": "Bellary Red",
        "type": "Southern High Color",
        "variety_type": "Southern High Color",
        "origin": "Bellary, Karnataka",
        "img": "/varieties/bellary red.jpg",
        "image_url": "/varieties/bellary red.jpg",
        "characteristics": "Bright coppery red, slightly flattened round bulb, robust export caliber.",
        "order": 3,
    },
    {
        "id": "pune_fursungi",
        "code": "pune_fursungi",
        "name": "Pune Fursungi",
        "type": "Export / Rabi",
        "variety_type": "Export / Rabi",
        "origin": "Pune / Ahmednagar, MH",
        "img": "/varieties/puna-fursungi-onion.jpg",
        "image_url": "/varieties/puna-fursungi-onion.jpg",
        "characteristics": "Light copper red, thin neck, tight adherent skin with minimal sprouting.",
        "order": 4,
    },
    {
        "id": "bangalore_rose",
        "code": "bangalore_rose",
        "name": "Bangalore Rose (GI Tag)",
        "type": "Southern High Color",
        "variety_type": "Southern High Color",
        "origin": "Chikkaballapur / Bengaluru, Karnataka",
        "img": "/varieties/bangalore-rose-onion.jpg",
        "image_url": "/varieties/bangalore-rose-onion.jpg",
        "characteristics": "GI Tagged. Spherical flat-topped button bulbs, deep scarlet color, rich in anthocyanin.",
        "order": 5,
    },
    {
        "id": "agrifound_dark_red",
        "code": "agrifound_dark_red",
        "name": "Agrifound Dark Red",
        "type": "Rabi / Storage",
        "variety_type": "Rabi / Storage",
        "origin": "NHRDF, Nashik",
        "img": "/varieties/agrifound-red-organic-red-onion.jpeg",
        "image_url": "/varieties/agrifound-red-organic-red-onion.jpeg",
        "characteristics": "Dark purplish-red globular bulbs, 5–6 cm diameter, firm fleshy scales.",
        "order": 6,
    },
    {
        "id": "pusa_red",
        "code": "pusa_red",
        "name": "Pusa Red",
        "type": "Rabi / Storage",
        "variety_type": "Rabi / Storage",
        "origin": "IARI, New Delhi",
        "img": "/varieties/pusa-red-onion.jpg",
        "image_url": "/varieties/pusa-red-onion.jpg",
        "characteristics": "Bronze red, flat-globular, 13–14% TSS, less prone to bolting.",
        "order": 7,
    },
    {
        "id": "white_onion",
        "code": "white_onion",
        "name": "White Onion (Dehydration Grade)",
        "type": "Export / Rabi",
        "variety_type": "Export / Rabi",
        "origin": "Bhavnagar / Mahuva, Gujarat",
        "img": "/varieties/white-onion.webp",
        "image_url": "/varieties/white-onion.webp",
        "characteristics": "Chalky white, high dry matter (18–20% TSS), tailored for dehydration flakes and powder.",
        "order": 8,
    },
    {
        "id": "yellow_granex",
        "code": "yellow_granex",
        "name": "Yellow Granex",
        "type": "Export / Rabi",
        "variety_type": "Export / Rabi",
        "origin": "Subtropical / Winter Crop",
        "img": "/varieties/Yellow Granex.jpg",
        "image_url": "/varieties/Yellow Granex.jpg",
        "characteristics": "Semi-flat golden-yellow scales, sweet juicy flesh, mild pungency.",
        "order": 9,
    },
    {
        "id": "red_creole",
        "code": "red_creole",
        "name": "Red Creole",
        "type": "Rabi / Storage",
        "variety_type": "Rabi / Storage",
        "origin": "Warm Semi-Arid Tropics",
        "img": "/varieties/redcreoleonion.jpg",
        "image_url": "/varieties/redcreoleonion.jpg",
        "characteristics": "Deep bronze-red skin, flat thick bulbs, heavy pungency, long shelf life.",
        "order": 10,
    },
    {
        "id": "pusa_white_round",
        "code": "pusa_white_round",
        "name": "Pusa White Round",
        "type": "Export / Rabi",
        "variety_type": "Export / Rabi",
        "origin": "IARI, New Delhi",
        "img": "/varieties/Pusa White Round.jpg",
        "image_url": "/varieties/Pusa White Round.jpg",
        "characteristics": "Uniform globe shape, pure white wrapper scales, excellent dehydration yield.",
        "order": 11,
    },
    {
        "id": "pusa_madhavi",
        "code": "pusa_madhavi",
        "name": "Pusa Madhavi",
        "type": "Rabi / Storage",
        "variety_type": "Rabi / Storage",
        "origin": "IARI, New Delhi",
        "img": "/varieties/Pusa Madhavi.jpg",
        "image_url": "/varieties/Pusa Madhavi.jpg",
        "characteristics": "Light reddish-bronze outer skin, mild to medium storage potential.",
        "order": 12,
    },
    {
        "id": "arka_kalyan",
        "code": "arka_kalyan",
        "name": "Arka Kalyan",
        "type": "Kharif / High Yield",
        "variety_type": "Kharif / High Yield",
        "origin": "ICAR-IIHR, Bengaluru",
        "img": "/varieties/Arka Kalyan.jpg",
        "image_url": "/varieties/Arka Kalyan.jpg",
        "characteristics": "Pinkish-red globes, resistance to purple blotch disease, thick cured wrapper.",
        "order": 13,
    },
    {
        "id": "agrifound_light_red",
        "code": "agrifound_light_red",
        "name": "Agrifound Light Red",
        "type": "Rabi / Storage",
        "variety_type": "Rabi / Storage",
        "origin": "NHRDF, Nashik",
        "img": "/varieties/aflightred.jpg",
        "image_url": "/varieties/aflightred.jpg",
        "characteristics": "Light copper-red, tight bulb center, high export suitability to Southeast Asia.",
        "order": 14,
    },
]

DEFAULT_DEFECT_SAMPLES = [
    {
        "id": "sample_sprout",
        "sample_id": "sample_sprout",
        "title": "Sprouted Bulb Evidence",
        "tag": "[DEFECT: SPROUT (MODERATE)]",
        "classTag": "TAG: CLASS II",
        "class_tag": "TAG: CLASS II",
        "tagBg": "bg-rose-950/85 text-rose-200 border-rose-700",
        "badgeBg": "bg-amber-900/85 text-amber-200 border-amber-700",
        "img": "/samples/sprouted_sample.jpg",
        "image_url": "/samples/sprouted_sample.jpg",
        "description": "Fresh shoot emerging from neck. Moisture exposure during storage.",
        "order": 1,
    },
    {
        "id": "sample_grade_a",
        "sample_id": "sample_grade_a",
        "title": "Pristine Export Grade A",
        "tag": "[OK: EXPORT COMPLIANT]",
        "classTag": "TAG: GRADE A",
        "class_tag": "TAG: GRADE A",
        "tagBg": "bg-emerald-950/85 text-emerald-200 border-emerald-700",
        "badgeBg": "bg-teal-900/85 text-teal-200 border-teal-700",
        "img": "/samples/pristine_sample.jpg",
        "image_url": "/samples/pristine_sample.jpg",
        "description": "Dry intact wrapper scales, cured tight neck, firm solid flesh.",
        "order": 2,
    },
    {
        "id": "sample_doubles",
        "sample_id": "sample_doubles",
        "title": "Twin / Split Bulb Defect",
        "tag": "[DEFECT: DOUBLES (LIGHT)]",
        "classTag": "TAG: BORDERLINE",
        "class_tag": "TAG: BORDERLINE",
        "tagBg": "bg-amber-950/85 text-amber-200 border-amber-700",
        "badgeBg": "bg-stone-900/85 text-stone-200 border-stone-600",
        "img": "/samples/twin_sample.jpg",
        "image_url": "/samples/twin_sample.jpg",
        "description": "Secondary growing point splitting bulb into conjoined twin bulbs.",
        "order": 3,
    },
]

def seed_database_if_empty():
    db = SessionLocal()
    try:
        if db.query(OnionVariety).count() == 0:
            for item in DEFAULT_VARIETIES:
                variety = OnionVariety(
                    code=item["code"],
                    name=item["name"],
                    variety_type=item["variety_type"],
                    origin=item["origin"],
                    characteristics=item["characteristics"],
                    image_url=item["image_url"],
                    order=item["order"],
                )
                db.add(variety)
            db.commit()

        if db.query(DefectSample).count() == 0:
            for item in DEFAULT_DEFECT_SAMPLES:
                sample = DefectSample(
                    sample_id=item["sample_id"],
                    title=item["title"],
                    tag=item["tag"],
                    class_tag=item["class_tag"],
                    tag_bg=item["tagBg"],
                    badge_bg=item["badgeBg"],
                    image_url=item["image_url"],
                    description=item["description"],
                    order=item["order"],
                )
                db.add(sample)
            db.commit()
    except Exception as e:
        print(f"Database seed note: {e}")
        db.rollback()
    finally:
        db.close()

seed_database_if_empty()

app = FastAPI(title="Onion Grading API")

# Ensure media directory exists
os.makedirs("media", exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/health/")
def health_check():
    return {
        "status": "healthy",
        "service": "Onion Grading FastAPI Backend",
        "protocol": "APEDA-AGMARK-2026"
    }

@app.get("/api/meta/")
def get_metadata(db: Session = Depends(get_db)):
    db_varieties = db.query(OnionVariety).order_by(OnionVariety.order).all()
    if not db_varieties:
        varieties = DEFAULT_VARIETIES
    else:
        varieties = []
        for v in db_varieties:
            varieties.append({
                "id": v.code,
                "code": v.code,
                "name": v.name,
                "type": v.variety_type,
                "variety_type": v.variety_type,
                "origin": v.origin,
                "img": f"http://127.0.0.1:8000/media{v.image_url}" if str(v.image_url).startswith("/") else v.image_url,
                "image_url": f"http://127.0.0.1:8000/media{v.image_url}" if str(v.image_url).startswith("/") else v.image_url,
                "characteristics": v.characteristics,
                "order": v.order,
            })

    db_samples = db.query(DefectSample).order_by(DefectSample.order).all()
    if not db_samples:
        defect_samples = DEFAULT_DEFECT_SAMPLES
    else:
        defect_samples = []
        for s in db_samples:
            defect_samples.append({
                "id": s.sample_id,
                "sample_id": s.sample_id,
                "title": s.title,
                "tag": s.tag,
                "classTag": s.class_tag,
                "class_tag": s.class_tag,
                "tagBg": s.tag_bg,
                "badgeBg": s.badge_bg,
                "img": f"http://127.0.0.1:8000/media{s.image_url}" if str(s.image_url).startswith("/") else s.image_url,
                "image_url": f"http://127.0.0.1:8000/media{s.image_url}" if str(s.image_url).startswith("/") else s.image_url,
                "description": s.description,
                "order": s.order,
            })

    return {
        "states": [
            "Maharashtra", "Karnataka", "Madhya Pradesh", "Gujarat", "Rajasthan",
            "Bihar", "Andhra Pradesh", "Telangana", "Haryana", "Uttar Pradesh",
            "West Bengal", "Tamil Nadu", "Odisha", "Punjab"
        ],
        "grades": [
            {"id": "Grade A", "label": "Grade A", "badge": "Premium Export"},
            {"id": "Grade B", "label": "Grade B", "badge": "Domestic Standard"},
            {"id": "Grade C", "label": "Grade C", "badge": "Discount / Local"},
            {"id": "Reject", "label": "Reject / Culled", "badge": "Sub-standard"},
        ],
        "sizeClasses": [
            {"id": "Small", "label": "Small (S)", "range": "< 35 mm"},
            {"id": "Medium", "label": "Medium (M)", "range": "35-55 mm"},
            {"id": "Large", "label": "Large (L)", "range": "55-70 mm"},
            {"id": "Jumbo", "label": "Jumbo (XL)", "range": "> 70 mm"},
        ],
        "varieties": varieties,
        "defectSamples": defect_samples,
    }

@app.get("/api/varieties/")
def get_varieties(db: Session = Depends(get_db)):
    db_varieties = db.query(OnionVariety).order_by(OnionVariety.order).all()
    if not db_varieties:
        return DEFAULT_VARIETIES
    return [
        {
            "id": v.code,
            "code": v.code,
            "name": v.name,
            "type": v.variety_type,
            "variety_type": v.variety_type,
            "origin": v.origin,
            "img": f"http://127.0.0.1:8000/media{v.image_url}" if str(v.image_url).startswith("/") else v.image_url,
            "image_url": f"http://127.0.0.1:8000/media{v.image_url}" if str(v.image_url).startswith("/") else v.image_url,
            "characteristics": v.characteristics,
            "order": v.order,
        }
        for v in db_varieties
    ]

@app.get("/api/assessments/", response_model=List[AssessmentResponse])
def get_assessments(db: Session = Depends(get_db)):
    return db.query(Assessment).order_by(Assessment.id.desc()).all()

@app.post("/api/assessments/", response_model=AssessmentResponse)
async def create_assessment(
    request: Request,
    db: Session = Depends(get_db)
):
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        data = await request.json()
        supplier_name = data.get("supplierName") or data.get("supplier_name", "")
        supplier_phone = data.get("supplierPhone") or data.get("supplier_phone", "")
        state = data.get("state", "Maharashtra")
        variety = data.get("variety", "nashik_red")
        grade = data.get("grade", "Grade A")
        size_class = data.get("sizeClass") or data.get("size_class", "Medium")
        moisture = float(data.get("moisture", 12.0) or 12.0)
        sprouting = float(data.get("sprouting", 0.0) or 0.0)
        damage = float(data.get("damage", 0.0) or 0.0)
        doubles = float(data.get("doubles", 0.0) or 0.0)
        inspector_name = data.get("inspectorName") or data.get("inspector_name", "")
        notes = data.get("notes", "")
        images_files = []
    else:
        form = await request.form()
        supplier_name = form.get("supplier_name", "")
        supplier_phone = form.get("supplier_phone", "")
        state = form.get("state", "Maharashtra")
        variety = form.get("variety", "nashik_red")
        grade = form.get("grade", "Grade A")
        size_class = form.get("size_class", "Medium")
        moisture = float(form.get("moisture", 12.0) or 12.0)
        sprouting = float(form.get("sprouting", 0.0) or 0.0)
        damage = float(form.get("damage", 0.0) or 0.0)
        doubles = float(form.get("doubles", 0.0) or 0.0)
        inspector_name = form.get("inspector_name", "")
        notes = form.get("notes", "")
        images_files = form.getlist("uploaded_images")

    lot_id = f"IN-ONION-{uuid.uuid4().hex[:6].upper()}"
    score, status = calculate_quality_metrics(moisture, sprouting, damage, doubles)

    uploaded_urls = []
    if supabase_client and images_files:
        for idx, file_obj in enumerate(images_files):
            if idx >= 3:
                break
                
            content = await file_obj.read()
            if len(content) > 500 * 1024:
                continue
                
            file_ext = file_obj.filename.split(".")[-1] if "." in getattr(file_obj, 'filename', '') else "jpg"
            filename = f"assessments/{lot_id}_{idx}.{file_ext}"
            
            try:
                res = supabase_client.storage.from_("Onion Assessments").upload(
                    path=filename,
                    file=content,
                    file_options={"content-type": getattr(file_obj, 'content_type', 'image/jpeg')}
                )
                
                public_url = supabase_client.storage.from_("Onion Assessments").get_public_url(filename)
                uploaded_urls.append(public_url)
            except Exception as e:
                print(f"Failed to upload image {filename} to Supabase:", e)

    images_str = ",".join(uploaded_urls)

    db_assessment = Assessment(
        lot_id=lot_id,
        supplier_name=supplier_name,
        supplier_phone=supplier_phone,
        state=state,
        variety=variety,
        grade=grade,
        size_class=size_class,
        moisture=moisture,
        sprouting=sprouting,
        damage=damage,
        doubles=doubles,
        inspector_name=inspector_name,
        notes=notes,
        computed_score=score,
        quality_status=status,
        images=images_str
    )

    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)

    return db_assessment

@app.get("/api/assessments/stats/")
def get_stats(db: Session = Depends(get_db)):
    assessments = db.query(Assessment).all()
    
    total = len(assessments)
    if total == 0:
        return {"totalAssessments": 0, "averageScore": 0, "gradeBreakdown": {}}
        
    avg_score = sum(a.computed_score for a in assessments) / total
    
    return {
        "totalAssessments": total,
        "averageScore": round(avg_score, 1),
        "gradeBreakdown": {},
    }

@app.get("/api/assessments/{assessment_id}/pdf/")
def get_pdf(assessment_id: int, db: Session = Depends(get_db)):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    # Convert SQLAlchemy model to dict for pdf_generator
    assessment_dict = {c.name: getattr(assessment, c.name) for c in assessment.__table__.columns}
    
    pdf_bytes = generate_assessment_pdf(assessment_dict)
    filename = f"Certificate-{assessment.lot_id}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Filename": filename,
            "Access-Control-Expose-Headers": "Content-Disposition, X-Filename"
        }
    )
