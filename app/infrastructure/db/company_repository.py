from app.application.ports.ports import CompanyRepositoryPort
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from app.domain.post_analysis.company_model import Company

class SqlAlchemyCompanyRepository(CompanyRepositoryPort):
    def __init__(self, session_factory:Session):
        self.session_factory = session_factory

    def get_company_info(self, company_id: int) -> Optional[Company]:
        with self.session_factory() as session:  # session_factory가 callable일 때
            statement = select(Company).where(Company.id == company_id)
            company = session.execute(statement).first()
            
            if company is None:
                raise ValueError(f"Company not found: {company_id}")
            
            return dict(company._mapping)