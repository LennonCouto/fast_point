from http import HTTPStatus

import factory
import factory.fuzzy
import pytest

from fast_point.models_todos import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'todolist', 'description': 'Already', 'state': 'todo'},
    )

    assert response.json() == {
        'id': 1,
        'title': 'todolist',
        'description': 'Already',
        'state': 'todo',
    }


@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(session, client, user, token):
    # arrange
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    # act
    response = client.get(
        '/todos/', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):
    # arrange
    expected_todos = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    # act
    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_title_should_return_5_todos(
    session, client, user, token
):
    # arrange
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    )

    session.add_all(TodoFactory.create_batch(5, user_id=user.id))

    await session.commit()

    # act
    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_description_should_return_5_todos(
    session, client, user, token
):
    # arrange
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, description='description')
    )

    await session.commit()

    # act
    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_state_should_return_5_todos(
    session, client, user, token
):
    # arrange
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id, state='done'))

    await session.commit()

    # act
    response = client.get(
        '/todos/?state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


@pytest.mark.asyncio
async def test_delete_todo_error(client, token):
    response = client.delete(
        '/todos/10', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'


@pytest.mark.asyncio
async def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/10', json={}, headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}
