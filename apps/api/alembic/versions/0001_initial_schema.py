"""initial_schema

Revision ID: 0001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("gstin", sa.String(15), nullable=True),
        sa.Column("pan", sa.String(10), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("state", sa.String(100), nullable=True),
        sa.Column("pin_code", sa.String(10), nullable=True),
        sa.Column("contact_name", sa.String(200), nullable=True),
        sa.Column("contact_email", sa.String(320), nullable=False),
        sa.Column("contact_phone", sa.String(20), nullable=True),
        sa.Column("subscription_tier", sa.String(20), nullable=True),
        sa.Column("subscription_valid_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("razorpay_subscription_id", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "leads",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("company_name", sa.String(200), nullable=True),
        sa.Column("sector", sa.String(50), nullable=True),
        sa.Column("annual_export_tonnes", sa.Numeric(15, 2), nullable=True),
        sa.Column("estimated_cbam_cost", sa.Numeric(18, 2), nullable=True),
        sa.Column("utm_source", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "emission_factors",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("fuel_type", sa.String(50), nullable=False),
        sa.Column("ncv_gj_per_tonne", sa.Numeric(10, 4), nullable=True),
        sa.Column("ef_tco2_per_gj", sa.Numeric(10, 6), nullable=True),
        sa.Column("source", sa.String(100), nullable=True),
        sa.Column("valid_from", sa.Date(), nullable=True),
        sa.Column("valid_until", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "cea_grid_factors",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("grid_region", sa.String(50), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("ef_tco2_per_mwh", sa.Numeric(10, 6), nullable=False),
        sa.Column("source", sa.String(50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "eu_default_values",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("cn_code", sa.String(20), nullable=False),
        sa.Column("product_name", sa.Text(), nullable=False),
        sa.Column("default_value_tco2_per_tonne", sa.Numeric(10, 6), nullable=False),
        sa.Column("valid_from", sa.Date(), nullable=True),
        sa.Column("source", sa.String(50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "app_config",
        sa.Column("key", sa.String(100), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("key"),
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=True),
        sa.Column("role", sa.String(20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "installations",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("sector", sa.String(50), nullable=False),
        sa.Column("production_route", sa.String(100), nullable=False),
        sa.Column("state", sa.String(100), nullable=False),
        sa.Column("grid_region", sa.String(50), nullable=False),
        sa.Column("has_captive_power", sa.Boolean(), nullable=True),
        sa.Column("captive_power_type", sa.String(50), nullable=True),
        sa.Column("annual_capacity_tonnes", sa.Numeric(15, 2), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "products",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("installation_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("cn_code", sa.String(20), nullable=False),
        sa.Column("hs_code", sa.String(20), nullable=False),
        sa.Column("product_name", sa.Text(), nullable=False),
        sa.Column("production_route_detail", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["installation_id"], ["installations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "activity_data",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("installation_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("reporting_period_start", sa.Date(), nullable=False),
        sa.Column("reporting_period_end", sa.Date(), nullable=False),
        sa.Column("data_type", sa.String(50), nullable=False),
        sa.Column("fuel_type", sa.String(50), nullable=True),
        sa.Column("quantity", sa.Numeric(15, 4), nullable=False),
        sa.Column("unit", sa.String(20), nullable=False),
        sa.Column("source", sa.String(200), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["installation_id"], ["installations.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "emission_results",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("installation_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("reporting_period_start", sa.Date(), nullable=False),
        sa.Column("reporting_period_end", sa.Date(), nullable=False),
        sa.Column("scope1_direct", sa.Numeric(15, 6), nullable=True),
        sa.Column("scope2_indirect", sa.Numeric(15, 6), nullable=True),
        sa.Column("total_embedded", sa.Numeric(15, 6), nullable=True),
        sa.Column("production_volume", sa.Numeric(15, 4), nullable=True),
        sa.Column("specific_embedded", sa.Numeric(15, 6), nullable=True),
        sa.Column("eu_default_value", sa.Numeric(15, 6), nullable=True),
        sa.Column("savings_vs_default", sa.Numeric(15, 6), nullable=True),
        sa.Column("eu_ets_price_used", sa.Numeric(10, 2), nullable=True),
        sa.Column("eur_to_inr_rate", sa.Numeric(10, 4), nullable=True),
        sa.Column("cbam_cost_actual", sa.Numeric(18, 2), nullable=True),
        sa.Column("cbam_cost_default", sa.Numeric(18, 2), nullable=True),
        sa.Column("calculation_version", sa.String(20), nullable=True),
        sa.Column("input_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["installation_id"], ["installations.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "reports",
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("installation_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("report_type", sa.String(50), nullable=True),
        sa.Column("reporting_year", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(20), nullable=True),
        sa.Column("file_url", sa.Text(), nullable=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["installation_id"], ["installations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("reports")
    op.drop_table("emission_results")
    op.drop_table("activity_data")
    op.drop_table("products")
    op.drop_table("installations")
    op.drop_table("users")
    op.drop_table("app_config")
    op.drop_table("eu_default_values")
    op.drop_table("cea_grid_factors")
    op.drop_table("emission_factors")
    op.drop_table("leads")
    op.drop_table("companies")
