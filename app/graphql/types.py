from typing import Optional
import strawberry

@strawberry.type
class TaskType:
    id: str
    title: str
    startTime: str    
    endTime: str    
    priority: int
    status: str
    userId: str    
    createdAt: str
    updatedAt: str
    description: Optional[str]  # this is Optional if it can be None (to handle cannot provide null of TaskType.description)
