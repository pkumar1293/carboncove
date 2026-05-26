"""SQLAlchemy ORM models for CarbonCove."""
from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import (
    Boolean, Column, Date, DateTime, ForeignKey, Integer,
    Numeric, String, Text, UniqueConstraint, func
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


def new_uuid():
    return str(uuid.uuid4())


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=False), primary_key=True, default=new_uuid)
    name = Column(Text, nullable=False)
    gstin = Column(String(15))
    pan = Column(String(10))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    pin_code = Column(String(10))
    contact_name = Column(String(200))
    contact_email = Column(String(320), nullable=False)
    contact_phone = Column(String(20))
    subscription_tier = Column(String(20), default="free")
    subscription_valid_until = Column(DateTime(timezone=True))
    razorpay_subscription_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    users = relationship("User", back_populates="company")
    installations = relationship("Installation", back_populates="company")
    reports = relationship("Report", back_populates="company")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), primary_key=True)  # matches Supabase auth.users.id
    company_id = Column(UUID(as_uuid=False), ForeignKey("companies.id"), nullable=False)
    full_name = Column(String(200))
    role = Column(String(20), default="member")  # owner|admin|member|viewer
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="users")


class Installation(Base):
    __tablename__ = "installations"

    id = Column(UUID(as_uuid=False), primary_key=True, default=new_uuid)
    company_id = Column(UUID(as_uuid=False), ForeignKey("companies.id"), nullable=False)
    name = Column(Text, nullable=False)
    sector = Column(String(50), nullable=False)
    production_route = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    grid_region = Column(String(50), nullable=False)
    has_captive_power = Column(Boolean, default=False)
    captive_power_type = Column(String(50))
    annual_capacity_tonnes = Column(Numeric(15, 2))
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="installations")
    products = relationship("Product", back_populates="installation")
    activity_data = relationship("ActivityData", back_populates="installation")
    emission_results = relationship("EmissionResult", back_populates="installation")


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=False), primary_key=True, default=new_uuid)
    installation_id = Column(UUID(as_uuid=False), ForeignKey("installations.id"), nullable=False)
    cn_code = Column(String(20), nullable=False)
    hs_code = Column(String(20), nullable=False)
    product_name = Column(Text, nullable=False)
    production_route_detail = Column(JSONB)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    installation = relationship("Installation", back_populates="products")


class ActivityData(Base):
    __tablename__ = "activity_data"

    id = Column(UUID(as_uuid=False), primary_key=True, default=new_uuid)
    installation_id = Column(UUID(as_uuid=False), ForeignKey("installations.id"), nullable=False)
    product_id = Column(UUID(as_uuid=False), ForeignKey("products.id"))
    reporting_period_start = Column(Date, nullable=False)
    reporting_period_end = Column(Date, nullable=False)
    data_type = Column(String(50), nullable=False)  # fuel|electricity|production
    fuel_type = Column(String(50))
    quantity = Column(Numeric(15, 4), nullable=False)
    unit = Column(String(20), nullable=False)
    source = Column(String(200))
    notes = Column(Text)
    created_by = Column(UUID(as_uuid=False), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    installation = relationship("Installation", back_populates="activity_data")
    product = relationship("Product")


class EmissionResult(Base):
    __tablename__ = "emission_results"

    id = Column(UUID(as_uuid=False), primary_key=True, default=new_uuid)
    installation_id = Column(UUID(as_uuid=False), ForeignKey("installations.id"), nullable=False)
    product_id = Column(UUID(as_uuid=False), ForeignKey("products.id"))
    reporting_period_start = Column(Date, nullable=False)
    reporting_period_end = Column(Date, nullable=False)
    scope1_direct = Column(Numeric(15, 6))
    scope2_indirect = Column(Numeric(15, 6))
    total_embedded = Column(Numeric(15, 6))
    production_volume = Column(Numeric(15, 4))
    specific_embedded = Column(Numeric(15, 6))
    eu_default_value = Column(Numeric(15, 6))
    savings_vs_default = Column(Numeric(15, 6))
    eu_ets_price_used = Column(Numeric(10, 2))
    eur_to_inr_rate = Column(Numeric(10, 4))
    cbam_cost_actual = Column(Numeric(18, 2))
    cbam_cost_default = Column(Numeric(18, 2))
    calculation_version = Column(String(20), default="1.0")
    input_data = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    installation = relationship("Installation", back_populates="emission_results")
    product = relationship("Product")


class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=False), primary_key=True, default=new_uuid)
    company_id = Column(UUID(as_uuid=False), ForeignKey("companies.id"))
    installation_id = Column(UUID(as_uuid=False), ForeignKey("installations.id"))
    report_type = Column(String(50))
    reporting_year = Column(Integer)
    status = Column(String(20), default="draft")  # draft|generating|ready|error
    file_url = Column(Text)
    generated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="reports")


class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = (UniqueConstraint("email"),)

    id = Column(UUID(as_uuid=False), primary_key=True, default=new_uuid)
    email = Column(String(320), nullable=False, unique=True)
    company_name = Column(String(200))
    sector = Column(String(50))
    annual_export_tonnes = Column(Numeric(15, 2))
    estimated_cbam_cost = Column(Numeric(18, 2))
    utm_source = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EmissionFactor(Base):
    __tablename__ = "emission_factors"

    id = Column(UUID(as_uuid=False), primary_key=True, default=new_uuid)
    fuel_type = Column(String(50), nullable=False)
    ncv_gj_per_tonne = Column(Numeric(10, 4))
    ef_tco2_per_gj = Column(Numeric(10, 6))
    source = Column(String(100))
    valid_from = Column(Date)
    valid_until = Column(Date)


class CeaGridFactor(Base):
    __tablename__ = "cea_grid_factors"

    id = Column(UUID(as_uuid=False), primary_key=True, default=new_uuid)
    grid_region = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    ef_tco2_per_mwh = Column(Numeric(10, 6), nullable=False)
    source = Column(String(50), default="CEA")


class EuDefaultValue(Base):
    __tablename__ = "eu_default_values"

    id = Column(UUID(as_uuid=False), primary_key=True, default=new_uuid)
    cn_code = Column(String(20), nullable=False)
    product_name = Column(Text, nullable=False)
    default_value_tco2_per_tonne = Column(Numeric(10, 6), nullable=False)
    valid_from = Column(Date)
    source = Column(String(50), default="EU_2023_1773")


class AppConfig(Base):
    """Dynamic configuration — overrides hardcoded defaults. Admin-editable."""
    __tablename__ = "app_config"

    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=False)
    description = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
