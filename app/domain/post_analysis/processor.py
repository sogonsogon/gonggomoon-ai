from typing import Any
from app.application.ports.ports import PostAnalyzerPort, PostRepositoryPort, CompanyRepositoryPort

class PostAnalysisProcessor:
    def __init__(self, post_analyzer: PostAnalyzerPort, company_repository: CompanyRepositoryPort, post_repository: PostRepositoryPort) -> None:
        self.post_analyzer = post_analyzer
        self.company_repository = company_repository
        self.post_repository = post_repository

    def process(self, post_id: int) -> dict[str, Any]:
        print(f"log : post ID : {post_id}")

        found_post = self.post_repository.get_post_info(post_id=post_id)
        print(f"found post : {found_post}")

        post = found_post.get("Post")
        if post is None:
            raise ValueError(f"Post not found in result: {found_post}")

        post_content = post.original_content
        company_id = post.company_id

        print(f"log : company ID : {company_id}")

        found_company = self.company_repository.get_company_info(company_id=company_id)
        company = found_company.get("Company")
        if company is None:
            raise ValueError(f"Company not found in result: {found_company}")

        company_name = company.name
        company_description = company.description

        return self.post_analyzer.analyze(
            company_name=company_name,
            company_description=company_description,
            post_content=post_content
        )