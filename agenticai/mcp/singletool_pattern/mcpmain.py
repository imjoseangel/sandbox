import json
from typing import List, Literal, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from faker import Faker


# 1. Define Input Schema
class UserBatchRequest(BaseModel):
    locale: str = Field(
        ...,
        description="The Faker locale code (e.g., 'it_IT', 'ja_JP', 'en_US', 'es_ES')",
    )
    count: int = Field(..., description="Number of users to generate for this locale")
    include_address: bool = Field(
        False, description="Whether to include full address details"
    )
    include_company: bool = Field(
        False, description="Whether to include company/job details"
    )
    seed: Optional[int] = Field(
        None, description="Optional seed for reproducible data generation"
    )


# 2. Initialize FastMCP
mcp = FastMCP("Synthetic-User-Factory")


# 3. Define the Composite Tool
@mcp.tool()
def manage_synthetic_users(
    operations: List[Literal["generate", "validate", "preview", "count"]],
    batches: List[UserBatchRequest],
) -> str:
    """
    Composite tool for managing synthetic user data generation using Python Faker.
    Executes multiple operations in a SINGLE call to minimize LLM iterations:
    - 'validate': Checks if the requested locales are supported
    - 'count': Returns total number of users that would be generated
    - 'preview': Shows a sample output without full generation
    - 'generate': Creates synthetic user data for multiple locales

    Example: operations=["validate", "count", "generate"] will execute all three
    in sequence and return combined results in a single response.

    This design reduces agent iterations from 3-4 calls to just 1 call.
    """

    results = {}

    # Execute operations in the order provided
    for operation in operations:
        if operation == "count":
            # Return total count across all batches
            total = sum(b.count for b in batches)
            results["count"] = {
                "total_users": total,
                "breakdown": [{"locale": b.locale, "count": b.count} for b in batches],
            }

        elif operation == "validate":
            # Validate all locales before generation
            validation_results = []
            for batch in batches:
                try:
                    Faker(batch.locale)
                    validation_results.append(
                        {"locale": batch.locale, "valid": True, "count": batch.count}
                    )
                except Exception as e:
                    validation_results.append(
                        {"locale": batch.locale, "valid": False, "error": str(e)}
                    )

            results["validate"] = {
                "results": validation_results,
                "all_valid": all(r["valid"] for r in validation_results),
            }

        elif operation == "preview":
            # Generate only 1 sample per batch to show structure
            preview_results = {}
            for batch in batches:
                try:
                    fake = Faker(batch.locale)
                    if batch.seed is not None:
                        Faker.seed(batch.seed)

                    user = {
                        "name": fake.name(),
                        "email": fake.email(),
                        "country": fake.current_country(),
                    }
                    if batch.include_address:
                        user["address"] = fake.address().replace("\n", ", ")
                        user["phone"] = fake.phone_number()
                    if batch.include_company:
                        user["company"] = fake.company()
                        user["job"] = fake.job()

                    preview_results[batch.locale] = user
                except Exception as e:
                    preview_results[batch.locale] = {"error": str(e)}

            results["preview"] = {"samples": preview_results}

        elif operation == "generate":
            # Full generation
            generation_data: dict[str, list | dict] = {}

            for batch in batches:
                try:
                    fake = Faker(batch.locale)
                    if batch.seed is not None:
                        Faker.seed(batch.seed)
                except Exception as e:
                    generation_data[batch.locale] = {
                        "error": f"Invalid Locale: {str(e)}"
                    }
                    continue

                batch_data = []
                for _ in range(batch.count):
                    user = {
                        "name": fake.name(),
                        "email": fake.email(),
                        "country": fake.current_country(),
                    }
                    if batch.include_address:
                        user["address"] = fake.address().replace("\n", ", ")
                        user["phone"] = fake.phone_number()
                    if batch.include_company:
                        user["company"] = fake.company()
                        user["job"] = fake.job()

                    batch_data.append(user)

                generation_data[batch.locale] = batch_data

            results["generate"] = {
                "data": generation_data,
                "total_generated": sum(
                    len(v) for v in generation_data.values() if isinstance(v, list)
                ),
            }

    # Return combined results for all operations
    return json.dumps(
        {
            "operations_executed": operations,
            "results": results,
        },
        indent=2,
        ensure_ascii=False,
    )


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
