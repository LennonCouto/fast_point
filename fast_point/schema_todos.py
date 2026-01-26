from pydantic import BaseModel, Field

from fast_point.models_todos import TodoState
from fast_point.schemas import FilterPage


class TodoShema(BaseModel):
    title: str
    description: str
    state: TodoState = Field(default=TodoState.todo)


class TodoPublic(TodoShema):
    id: int


class FilterTodo(FilterPage):
    title: str | None = Field(default=None, min_length=3, max_length=20)
    description: str | None = None
    state: TodoState | None = None


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
