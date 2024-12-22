import strawberry
from typing import List, Optional
from app.graphql.resolvers import get_tasks
from app.graphql.types import TaskType

@strawberry.type
class Query:
    @strawberry.field
    async def tasks(
        self,
        sort_by: Optional[str] = None,
        priority: Optional[int] = None,
        order: Optional[str] = "asc",
        status: Optional[str] = None,
        info: strawberry.types.Info = None,
    ) -> List[TaskType]:
        """
        Fetch tasks from resolver with optional filtering and sorting.
        """
        return await get_tasks(
            info, sort_by=sort_by, priority=priority, order=order, status=status
        )
