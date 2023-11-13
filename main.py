import streamlit as st
import logging
import pandas as pd
import services

from datetime import datetime


logger = logging.getLogger()

PRIORITY_OPTIONS = ['Low', 'Medium', 'High']


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
                # Re-run the app
                st.rerun()
            else:
                st.error("Invalid username or password")
    else:
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
    filter_options = ['In progress', 'Completed', 'All tasks']
    filter_selection = st.selectbox('', filter_options)

    # Filter tasks based on selection
    if filter_selection == 'In progress':
        filtered_tasks = services.task_manager.list_in_progress_tasks()
    elif filter_selection == 'Completed':
        filtered_tasks = services.task_manager.list_completed_tasks()
    elif filter_selection == 'All tasks':
        filtered_tasks = services.task_manager.list_all_tasks()

    high_priority_tasks = filtered_tasks[filtered_tasks['priority'] == 2]
    display_tasks_in_home(high_priority_tasks, "# High Priority", "#FF5555")

    medium_priority_tasks = filtered_tasks[filtered_tasks['priority'] == 1]
    display_tasks_in_home(medium_priority_tasks, "# Medium Priority", "orange")

    low_priority_tasks = filtered_tasks[filtered_tasks['priority'] == 0]
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
    if 'state' not in st.session_state:
        st.session_state.state = {}

    # Use the task ID as the key for the session state variable
    if task_id not in st.session_state.state:
        st.session_state.state[task_id] = task['is_completed']

    is_completed = st.checkbox(f'{task_name}: {task_description}', value=st.session_state.state[task_id], key=task_id)

    if is_completed != st.session_state.state[task_id]:
        st.session_state.state[task_id] = is_completed  # Update the session state
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
    priority = st.selectbox('Priority', PRIORITY_OPTIONS)

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
    priority = PRIORITY_OPTIONS.index(priority)
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

    # Button to edit a task
    edit_task()


def edit_task():
    # Add a form for editing tasks
    st.header("Edit Task")
    selected_task_id = st.text_input("Enter Task ID to Edit:")
    if st.button("Edit Task") and selected_task_id:
        task_to_edit = services.task_manager.get_task_by_id(selected_task_id)
        if not task_to_edit.empty:
            st.subheader("Edit Task Details")
            print(task_to_edit['task_name'])

            # Create form for editing task details
            updated_task_name = st.text_input("Task Name", value=task_to_edit['task_name'].item())
            updated_task_description = st.text_input("Task Description", value=task_to_edit['task_description'].item())
            updated_due_date = st.date_input("Due Date", value=pd.to_datetime(task_to_edit['due_date'].item()).date())
            updated_priority = st.selectbox("Priority", PRIORITY_OPTIONS, index=task_to_edit['priority'].item())

            # Button to update the task
            if st.button("Update Task"):
                # Update the task in the database
                updated_task = {
                    'task_name': updated_task_name,
                    'task_description': updated_task_description,
                    'due_date': updated_due_date,
                    'priority': updated_priority
                }
                services.task_manager.update_task(selected_task_id, updated_task)
                st.success("Task updated successfully!")
            else:
                st.warning("Please fill in the required information to update the task.")
        else:
            st.warning("Task not found. Please enter a valid Task ID.")


if __name__ == "__main__":
    main()