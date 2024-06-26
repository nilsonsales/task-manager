import streamlit as st
import logging
import pandas as pd
import services

from datetime import datetime


logger = logging.getLogger()

PRIORITY_OPTIONS = ['Low', 'Medium', 'High']


def main():
    initialize_session_state()

    # if st.secrets.get('ENV') == 'dev':
    #     # Automatically authenticate the user for development purposes
    #     authenticate('user', 'pass')
    #     st.session_state.user["authenticated"] = True
    #     st.session_state.user["username"] = 'user'

    # If not authenticated, show the login screen
    if not st.session_state.user["authenticated"]:
        st.title("Login")
        username = st.text_input("Username", key="username", type="default", value="").strip()
        password = st.text_input("Password", key="password", type="password", value="").strip()

        if st.button("Login"):
            if username and password and authenticate(username, password):
                st.success("Login successful!")
                st.session_state.user["authenticated"] = True
                st.session_state.user["username"] = username
                # Re-run the app
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.write("Don't have an account? ")
        if st.button("Create Account") or st.session_state.display_registration_page:
            # Redirect to the registration page or form
            display_registration_page()
    else:
        selected_tab = st.sidebar.radio('Navigation', ('Home', 'Add Task', 'Tasks Details'))

        if selected_tab == 'Home':
            display_home()
        elif selected_tab == 'Add Task':
            display_add_task()
        elif selected_tab == 'Tasks Details':
            display_tasks_details()


def initialize_session_state():
    if "user" not in st.session_state:
        st.session_state.user = {"authenticated": False, "username": None}
    if 'task_state' not in st.session_state:
        st.session_state.task_state = {}
    if 'display_registration_page' not in st.session_state:
        st.session_state.display_registration_page = False
    if 'display_edit' not in st.session_state:
        st.session_state.display_edit = False


def authenticate(username, password):
    # Authenticate the user
    return services.task_manager.authenticate_user(username, password)


def display_registration_page():
    st.title("Registration")
    st.session_state.display_registration_page = True

    username = st.text_input("Username", key="reg_username", type="default", value="").strip()
    password = st.text_input("Password", key="reg_password", type="password", value="").strip()
    confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", value="").strip()

    if st.button("Register"):
        if not username or not password:
            st.error("Please enter a username and password")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif services.task_manager.user_exists(username):
            st.error("Username already exists")
        else:
            # Add your code here to handle the registration logic
            services.db_conn.add_user(username, password)
            # and display a success message
            st.success("Registration successful!")


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

    st.markdown(" ")  # This adds a horizontal line to create space

    with st.expander("➕ Add Task"):
        display_add_task()


def display_tasks_in_home(tasks, subheader, color):
    if not tasks.empty:
        st.markdown(f'<h3 style="font-size: 1.5em; color: {color}; opacity: 0.8">{subheader}</h3>',
                    unsafe_allow_html=True)
        for _, task in tasks.iterrows():
            display_task_in_home(task)


def display_task_in_home(task):
    task_name = task['task_name']
    task_id = task['id']
    task_description = task['task_description']
    due_date = task['due_date']

    # Print if the task is overdue
    if not task['is_completed'] and due_date < datetime.now().date():
        logging.debug(f'Due date {due_date} is lower than current date {datetime.now().date()}')

        text_above = f"⚠️ overdue on {due_date.day}/{due_date.month}"
        box_html = f"""
        <div style="position:relative;">
            <div style="background-color: rgba(255, 0, 0, 0.1); padding:2px 6px; border-radius:3px; width:max-content;">
                <p style="margin:0; font-size: 12.5px;">{text_above}</p>
            </div>
        </div>
        """
        # Display the box and the text below
        st.markdown(box_html, unsafe_allow_html=True)

    # Use the task ID as the key for the session state variable
    if task_id not in st.session_state.task_state:
        st.session_state.task_state[task_id] = task['is_completed']

    separator = ': ' if task_name and task_description else ''
    is_completed = st.checkbox(f'{task_name}{separator}{task_description}',
                               value=st.session_state.task_state[task_id],
                               key=task_id)

    if is_completed != st.session_state.task_state[task_id]:
        st.session_state.task_state[task_id] = is_completed  # Update the session state
        if is_completed:
            services.task_manager.update_task(task_id, {'is_completed': True})
        else:
            services.task_manager.update_task(task_id, {'is_completed': False})
        st.rerun()


def display_add_task():
    """Displays a form for adding a new task."""
    st.title('Add new task')

    task_name = st.text_input('Task name')
    task_description = st.text_area('Task description')
    due_date = st.date_input('Due date')
    priority = st.selectbox('Priority', PRIORITY_OPTIONS)
    is_completed = st.checkbox('Is completed')

    # Submit button
    if st.button('Submit'):
        # Process the form data
        process_form_data(task_name, task_description, due_date, priority, is_completed)
        st.rerun()


def process_form_data(task_name, task_description, due_date, priority, is_completed):
    """Processes the form data and inserts it into the database."""
    st.write('Task name:', task_name)
    st.write('Task description:', task_description)
    st.write('Due date:', due_date)
    st.write('Priority:', priority)
    st.write('Is completed:', is_completed)

    data = {
        'task_name': task_name,
        'task_description': task_description,
        'due_date': due_date,
        'priority': PRIORITY_OPTIONS.index(priority),
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
    if st.button("Edit Task"):
        st.session_state.display_edit = True
    if st.session_state.display_edit and selected_task_id:
        task_to_edit = services.task_manager.get_task_by_id(selected_task_id)
        if not task_to_edit.empty:
            st.subheader("Edit Task Details")

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
                    'priority': PRIORITY_OPTIONS.index(updated_priority)
                }
                services.task_manager.update_task(selected_task_id, updated_task)
                st.success("Task updated successfully!")
                st.session_state.display_edit = False
        else:
            st.warning("Task not found. Please enter a valid Task ID.")


if __name__ == "__main__":
    main()

