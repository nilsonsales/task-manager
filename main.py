import streamlit as st
import logging
import pandas as pd
import services

from streamlit import session_state as state
from datetime import datetime


logger = logging.getLogger()

PRIORITY_NUMBER = {
    'Low': 1,
    'Medium': 2,
    'High': 3
}


def main():
    # Check if the user is authenticated
    if "user" not in st.session_state:
        st.session_state.user = {"authenticated": False, "username": None}

    # If not authenticated, show the login screen
    if not st.session_state.user["authenticated"]:
        st.title("Login")
        username = st.text_input("Username", key="username", type="default", value="").strip()
        password = st.text_input("Password", key="password", type="password", value="").strip()

        if st.button("Login"):
            if authenticate(username, password):
                st.success("Login successful!")
                st.session_state.user["authenticated"] = True
                st.session_state.user["username"] = username
                st.rerun()
            else:
                st.error("Invalid username or password")
    else:
        # User is authenticated, display the main content
        selected_tab = st.sidebar.radio('Navigation', ('Home', 'Add Task', 'Tasks Details'))

        if selected_tab == 'Home':
            display_home()
        elif selected_tab == 'Add Task':
            display_add_task()
        elif selected_tab == 'Tasks Details':
            display_tasks_details()


def authenticate(username, password):
    # Authenticate the user
    return services.task_manager.authenticate_user(username, password)


def display_home():
    """Displays the home page of the Simple Task Manager app."""
    st.title('Simple Task Manager')

    # Selectbox for filtering tasks
    filter_options = ['In Progress', 'Completed', 'All']
    filter_selection = st.selectbox('Filter Tasks', filter_options)

    # Filter tasks based on selection
    if filter_selection == 'In Progress':
        filtered_tasks = services.task_manager.list_in_progress_tasks()
    elif filter_selection == 'Completed':
        filtered_tasks = services.task_manager.list_completed_tasks()
    elif filter_selection == 'All':
        filtered_tasks = services.task_manager.list_all_tasks()

    high_priority_tasks = filtered_tasks[filtered_tasks['priority'] == 3]
    display_tasks_in_home(high_priority_tasks, "# High Priority", "#FF5555")

    medium_priority_tasks = filtered_tasks[filtered_tasks['priority'] == 2]
    display_tasks_in_home(medium_priority_tasks, "# Medium Priority", "orange")

    low_priority_tasks = filtered_tasks[filtered_tasks['priority'] == 1]
    display_tasks_in_home(low_priority_tasks, "# Low Priority", "green")


def display_tasks_in_home(tasks, subheader, color):
    if not tasks.empty:
        st.markdown(f'<h3 style="font-size: 1.5em; color: {color}; opacity: 0.8">{subheader}</h3>', unsafe_allow_html=True)
        for _, task in tasks.iterrows():
            display_task_in_home(task)


def display_task_in_home(task):
    task_name = task['task_name']
    task_id = task['id']
    task_description = task['task_description']
    due_date = task['due_date']

    # Print if the task is overdue
    if due_date < datetime.now().date():
        st.markdown('**The task below is overdue!**')

    # Use the task ID as the key for the session state variable
    if task_id not in state:
        state[task_id] = task['is_completed']

    is_completed = st.checkbox(f'{task_name}: {task_description}', value=task['is_completed'])

    if is_completed != state[task_id]:
        state[task_id] = is_completed  # Update the session state
        if is_completed:
            services.task_manager.update_task(task_id, {'is_completed': True})
        else:
            services.task_manager.update_task(task_id, {'is_completed': False})
        st.rerun()


def display_add_task():
    """Displays a form for adding a new task."""
    st.title('Add new task')

    # Text input fields
    task_name = st.text_input('Task name')
    task_description = st.text_area('Task description')

    # Date input field
    due_date = st.date_input('Due date')

    # Selectbox for priority
    priority_options = ['Low', 'Medium', 'High']
    priority = st.selectbox('Priority', priority_options)

    # Checkbox for completion status
    is_completed = st.checkbox('Is completed')

    # Submit button
    if st.button('Submit'):
        # Process the form data
        process_form_data(task_name, task_description, due_date, priority, is_completed)


def process_form_data(task_name, task_description, due_date, priority, is_completed):
    """Processes the form data and inserts it into the database."""
    st.write('Task name:', task_name)
    st.write('Task description:', task_description)
    st.write('Due date:', due_date)
    st.write('Priority:', priority)
    priority = PRIORITY_NUMBER[priority]
    st.write('Is completed:', is_completed)

    data = {
        'task_name': task_name,
        'task_description': task_description,
        'due_date': due_date,
        'priority': priority,
        'is_completed': is_completed
    }

    services.task_manager.insert_task(data)


def display_tasks_details():
    """Displays a list of tasks and their details."""
    st.title('Tasks Details')
    # Selectbox for filtering tasks
    filter_options = ['All', 'Completed', 'In Progress']
    filter_selection = st.selectbox('Filter Tasks', filter_options)

    # Filter tasks based on selection
    if filter_selection == 'All':
        filtered_tasks = services.task_manager.list_all_tasks()
    elif filter_selection == 'Completed':
        filtered_tasks = services.task_manager.list_completed_tasks()
    elif filter_selection == 'In Progress':
        filtered_tasks = services.task_manager.list_in_progress_tasks()

    # Remove time from dates columns:
    filtered_tasks['created_at'] = pd.to_datetime(filtered_tasks['created_at']).dt.date
    filtered_tasks['due_date'] = pd.to_datetime(filtered_tasks['due_date']).dt.date
    filtered_tasks['updated_at'] = pd.to_datetime(filtered_tasks['updated_at']).dt.date

    # Display tasks in a dataframe
    df = pd.DataFrame(filtered_tasks).sort_values(by='id', ascending=False)
    st.dataframe(df, hide_index=True)


if __name__ == "__main__":
    main()