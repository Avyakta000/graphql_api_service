import httpx
from typing import List, Optional
from app.graphql.types import TaskType
from fastapi import Request
import os
from dotenv import load_dotenv

# load env vairables
load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://localhost:5001") 

async def get_tasks(
    info,
    sort_by: Optional[str] = None,
    priority: Optional[int] = None,
    order: Optional[str] = "asc",
    status: Optional[str] = None,
) -> List[TaskType]:
    """
    Fetch tasks with optional filtering and sorting.
    """
    try:
        # Step 1: access the request from the context
        request: Request = info.context["request"]

        # Step 2: extract the JWT token from cookies
        jwt_token = request.cookies.get("jwt_auth")
        if not jwt_token:
            raise Exception("JWT token is missing in cookies")

        # Step 3: set up the cookies with the JWT token
        cookies = {"jwt_auth": jwt_token}

        # Step 4: fetch tasks from Express with the JWT cookie
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/api/tasks", cookies=cookies)
            response.raise_for_status()  # Raise error if not 200 OK
            user_tasks = response.json()
            print(f"All Tasks: {user_tasks}")

        # Step 5: apply filtering (if provided)
        if status:
            user_tasks = [task for task in user_tasks if task["status"] == status]
            print(f"Filtered Tasks (Status {status}): {user_tasks}")

        if priority:
            user_tasks = [task for task in user_tasks if task["priority"] == priority]
            print(f"Filtered Tasks (Status {priority}): {user_tasks}")

        # Step 6: sorting (if sort_by is provided)
        if sort_by:
            reverse = order == "desc"
            user_tasks = sorted(user_tasks, key=lambda x: x.get(sort_by), reverse=reverse)
            print(f"Sorted Tasks (Sort By {sort_by}, Order {order}): {user_tasks}")

        # Step 7: map to GraphQL TaskType and return
        return [TaskType(**task) for task in user_tasks]

    except httpx.HTTPStatusError as e:
        raise Exception(f"Failed to fetch tasks from the Express server. Error: {e.response.status_code}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
