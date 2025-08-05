from nicegui import ui
from functools import partial
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = cred = credentials.Certificate("path/to/your/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

tasks = []
current_filter = 'all'
search_query = ''
edit_index = None  # Track which task is being edited

# Firestore collection ref
tasks_ref = db.collection('tasks')

# --- Firestore integration functions ---

def load_tasks_from_firestore():
    global tasks
    tasks = []
    docs = tasks_ref.stream()
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id  # Track Firestore doc ID for update/delete
        tasks.append(data)

def save_task_to_firestore(task):
    data_to_save = {
        'text': task['text'],
        'done': task['done'],
        'priority': task['priority'],
    }
    if 'id' in task:
        tasks_ref.document(task['id']).set(data_to_save)
    else:
        doc_ref = tasks_ref.document()
        doc_ref.set(data_to_save)
        task['id'] = doc_ref.id  # Assign Firestore doc ID to local task

def delete_task_from_firestore(task):
    if 'id' in task:
        tasks_ref.document(task['id']).delete()

# --- Modified app logic to sync with Firestore ---

def add_task(text_input, priority_select):
    text = text_input.value.strip()
    priority = priority_select.value
    if text:
        new_task = {'text': text, 'done': False, 'priority': priority}
        save_task_to_firestore(new_task)
        tasks.append(new_task)
        text_input.value = ''
        ui.notify('📝 Task added successfully!', color='primary')
        refresh_tasks()
    else:
        ui.notify('Please enter a task', color='warning')

def toggle_task(index):
    tasks[index]['done'] = not tasks[index]['done']
    save_task_to_firestore(tasks[index])
    refresh_tasks()

def delete_task(index):
    task_to_delete = tasks.pop(index)
    delete_task_from_firestore(task_to_delete)
    ui.notify('🗑️ Task deleted', color='warning')
    refresh_tasks()

def edit_task(index, *_):
    global edit_index
    edit_index = index
    refresh_tasks()

def save_task(index, input_field, label, priority_select):
    global edit_index
    new_text = input_field.value.strip()
    if new_text:
        tasks[index]['text'] = new_text
        tasks[index]['priority'] = priority_select.value
        save_task_to_firestore(tasks[index])
    edit_index = None
    refresh_tasks()

def mark_all_done():
    for task in tasks:
        task['done'] = True
        save_task_to_firestore(task)
    ui.notify('✅ All tasks marked as done!', color='positive')
    refresh_tasks()

def clear_all():
    for task in tasks:
        delete_task_from_firestore(task)
    tasks.clear()
    ui.notify('🧹 All tasks cleared', color='negative')
    refresh_tasks()

def set_filter(value):
    global current_filter
    current_filter = value
    refresh_tasks()

def set_search(text):
    global search_query
    search_query = text.lower()
    refresh_tasks()

def move_task_up(index):
    if index > 0:
        tasks[index], tasks[index - 1] = tasks[index - 1], tasks[index]
        # Not syncing order to Firestore here for simplicity
        refresh_tasks()

def move_task_down(index):
    if index < len(tasks) - 1:
        tasks[index], tasks[index + 1] = tasks[index + 1], tasks[index]
        # Not syncing order to Firestore here for simplicity
        refresh_tasks()

def matches_filter(task):
    if current_filter == 'done' and not task['done']:
        return False
    if current_filter == 'pending' and task['done']:
        return False
    if search_query and search_query not in task['text'].lower():
        return False
    return True

def refresh_tasks():
    global edit_index
    task_container.clear()
    completed = sum(1 for t in tasks if t['done'])
    total = len(tasks)
    progress = completed / total if total else 0
    progress_bar.value = progress
    progress_label.text = f'{int(progress * 100)}% Completed'

    filtered_tasks = [(i, t) for i, t in enumerate(tasks) if matches_filter(t)]

    for i, task in filtered_tasks:
        with task_container:
            with ui.row().classes(
                'items-center justify-between bg-white rounded-lg p-4 shadow hover:shadow-lg '
                'transition-all duration-300 ease-in-out transform hover:scale-[1.02]'):
                with ui.row().classes('items-center gap-4'):
                    ui.checkbox(value=task['done'], on_change=partial(toggle_task, i))
                    if i == edit_index:
                        # Show inputs for editing
                        task_input = ui.input(value=task['text']).props('dense outlined').classes('w-60 text-black')
                        priority_select = ui.select(['High', 'Medium', 'Low'], value=task.get('priority', 'Medium')) \
                            .props('dense outlined').classes('w-32')
                        task_input.on('keydown.enter', partial(save_task, i, task_input, None, priority_select))
                        ui.button('Save', on_click=partial(save_task, i, task_input, None, priority_select)).props('color=green')
                    else:
                        # Show label normally
                        task_label = ui.label(task['text']).classes(
                            'text-lg text-black font-semibold transition-all duration-300 ease-in-out'
                        ).style(f'text-decoration: {"line-through" if task["done"] else "none"};')
                        priority_color = {'High': 'red', 'Medium': 'yellow', 'Low': 'green'}.get(task.get('priority', 'Medium'), 'gray')
                        ui.label(task.get('priority', 'Medium')).classes(
                            f'text-sm font-medium px-3 py-1 rounded-full bg-{priority_color}-200 text-{priority_color}-800 select-none'
                        )

                with ui.row().classes('gap-2'):
                    if i != edit_index:
                        ui.button('Edit', on_click=partial(edit_task, i)).props('outlined color=blue')
                    ui.button('Delete', on_click=partial(delete_task, i)).props('outlined color=red')
                    ui.button('⬆', on_click=partial(move_task_up, i)).props('outlined color=gray')
                    ui.button('⬇', on_click=partial(move_task_down, i)).props('outlined color=gray')

    if total > 0 and progress == 1:
        ui.notify('🎉 All tasks completed! You crushed it!', color='positive')

# --- UI Layout ---

with ui.column().classes('min-h-screen w-full flex justify-center items-center bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100 font-sans'):
    with ui.column().classes('w-full max-w-3xl p-6 bg-gray-100 rounded-lg shadow-xl flex flex-col justify-center items-center text-black'):

        ui.label('🗒️ To-Do App').classes('text-4xl font-extrabold mb-6 text-center text-gray-900 select-none')

        with ui.row().classes('gap-4 justify-center mb-4 w-full'):
            task_input = ui.input('Add a new task...').props('clearable outlined dense').classes('w-full text-gray-900 font-semibold placeholder-opacity-70')
            priority_select = ui.select(['High', 'Medium', 'Low'], value='Medium').props('dense outlined').classes('w-32')
            ui.button('Add Task', on_click=lambda: add_task(task_input, priority_select)).props('color=indigo')

        with ui.row().classes('gap-4 justify-between w-full mb-4'):
            with ui.row().classes('gap-3'):
                ui.button('All', on_click=lambda: set_filter('all')).props('color=primary' if current_filter == 'all' else '')
                ui.button('Done', on_click=lambda: set_filter('done')).props('color=primary' if current_filter == 'done' else '')
                ui.button('Pending', on_click=lambda: set_filter('pending')).props('color=primary' if current_filter == 'pending' else '')

            search_input = ui.input(placeholder='Search tasks...').props('outlined dense clearable').classes('w-64')
            search_input.on('input', lambda e=None: set_search(search_input.value))

        ui.separator().classes('my-4')

        # Progress Tracker
        progress_label = ui.label('0% Completed').classes('text-md font-semibold text-gray-800 mb-1')
        progress_bar = ui.linear_progress(value=0).classes('w-full h-3 rounded-full bg-gray-300 mb-4')

        task_container = ui.column().classes('mt-6 space-y-4 w-full')

        with ui.row().classes('gap-6 justify-center mt-6 w-full'):
            ui.button('Mark All Done', on_click=mark_all_done).props('color=green')
            ui.button('Clear All', on_click=clear_all).props('color=red')

# On app start: load tasks and refresh UI
load_tasks_from_firestore()
refresh_tasks()

ui.run()
