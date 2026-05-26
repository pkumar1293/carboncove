"""Async PDF generation tasks."""
from worker import celery_app
from services.pdf_generator import generate_cbam_report
import os


@celery_app.task(bind=True, max_retries=3)
def generate_report_task(self, result_id: str, company_info: dict, installation_info: dict):
    """Generate CBAM PDF report asynchronously."""
    try:
        pdf_bytes = generate_cbam_report(result_id, company_info, installation_info)
        upload_dir = os.environ.get("UPLOAD_DIR", "/var/www/carboncove/uploads/reports")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"cbam_report_{result_id}.pdf")
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)
        return {"status": "success", "file_path": file_path, "result_id": result_id}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
