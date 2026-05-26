"""Async email sending tasks via Resend."""
import os
import httpx
from worker import celery_app

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")


@celery_app.task(bind=True, max_retries=3)
def send_lead_email(self, email: str, company_name: str, savings_inr: float):
    """Send lead capture confirmation email via Resend."""
    try:
        resp = httpx.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
            json={
                "from": "noreply@carboncove.in",
                "to": [email],
                "subject": "Your CBAM Exposure Report — CarbonCove",
                "html": (
                    f"<h2>Thank you, {company_name}!</h2>"
                    f"<p>Based on your inputs, you could save approximately "
                    f"<strong>₹{savings_inr:,.0f}</strong> by using actual emission data "
                    f"instead of EU defaults.</p>"
                    f"<p>Our team will reach out within 24 hours.</p>"
                    f"<p>— CarbonCove Team</p>"
                ),
            },
        )
        resp.raise_for_status()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=120)
