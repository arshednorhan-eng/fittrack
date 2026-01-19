# FitTrack – Gym Management System (Backend)

FitTrack הוא פרויקט Backend לניהול חדר כושר, שפותח במסגרת מטלת סיום בקורס  
**תכנות מתקדם בפייתון**.

המערכת מאפשרת ניהול מתאמנים, מנויים, חוגים, תוכניות אימון ו־Check-in,  
וממומשת באמצעות Flask, SQLAlchemy ו־Pydantic,  
תוך הפרדה מלאה לשכבות.

---

## ארכיטקטורת הפרויקט

הפרויקט בנוי בארכיטקטורה שכבתית:

- **Models** (`fittrack/models`)  
  מודלי SQLAlchemy והגדרת קשרים בין טבלאות

- **Services** (`fittrack/services`)  
  לוגיקה עסקית וחוקי מערכת

- **Routes** (`fittrack/routes`)  
  REST API Endpoints באמצעות Flask Blueprints

- **Schemas** (`fittrack/schemas`)  
  ולידציות באמצעות Pydantic

- **Exceptions** (`fittrack/exceptions.py`)  
  חריגות מותאמות ומיפוי לשגיאות HTTP

---

## טכנולוגיות

- Python 3.10+
- Flask
- SQLAlchemy (ORM)
- Pydantic
- MySQL (בסביבת פיתוח מקומית)

---

## הוראות הפעלה (Step-by-Step)

יש להריץ את הפקודות הבאות **מתיקיית הפרויקט הראשית**
(התיקייה שמכילה את `fittrack/` ו־`requirements.txt`):

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt

cd fittrack
python app.py

```
**חשוב:** יש להריץ את `python app.py` מתוך תיקיית `fittrack` כדי שהייבואים `from fittrack.xxx` יעבדו נכון. 
--- 


בעת ההרצה הראשונה בסיס הנתונים נוצר אוטומט  
באמצעות SQLAlchemy לפי המודלים המוגדרים בפרויקט.

אם ההרצה הצליחה, תופיע הודעה דומה ל:
Running on http://127.0.0.1:5000

## Database Configuration

The project uses MySQL by default.

To configure the database:
1. Copy `fittrack/db.ini.example` to `fittrack/db.ini`
2. Update the credentials inside `db.ini`
3. Run the application


## שימוש במערכת

המערכת פועלת כ־REST API.

כתובת בסיס:
http://127.0.0.1:5000

ניתן לבדוק את ה־Endpoints באמצעות:
- Postman
- curl
- דפדפן (ל־GET requests)