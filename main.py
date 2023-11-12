import streamlit as st
import logging
import pandas as pd
import services

from streamlit import session_state as state
from datetime import datetime

logger = logging.getLogger()

PRIORITY_NUMBER = {
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3
}


def main():
    selected_tab = st.sidebar.radio('Navigation',
                                    ('Home', 'Add Task', 'Task Details'))

    if selected_tab == 'Home':
        display_home()
    elif selected_tab == 'Add Task':
        display_add_task()
    elif selected_tab == 'Task Details':
        display_tasks_details()


def display_home():
    st.title('Simple Task Manager')
    st.write("Here's a list of all your tasks in progress:")

    in_progress_tasks = services.task_manager.list_in_progress_tasks()

    high_priority_tasks = in_progress_tasks[in_progress_tasks['priority'] == 3]
    display_tasks_in_home(high_priority_tasks, "# High Priority", "#FF5555")

    medium_priority_tasks = in_progress_tasks[in_progress_tasks['priority'] == 2]
    display_tasks_in_home(medium_priority_tasks, "# Medium Priority", "orange")

    low_priority_tasks = in_progress_tasks[in_progress_tasks['priority'] == 1]
    display_tasks_in_home(low_priority_tasks, "# Low Priority", "green")

def display_tasks_in_home(tasks, subheader, color):
    if not tasks.empty:
        #st.subheader(subheader)
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
        if is_completed:
            st.markdown('~~This task is completed.~~')
            services.task_manager.update_task(task_id, {'is_completed': True})
        else:
            st.write('This task is in progress.')


def display_add_task():
    st.title('Add new task')

    # Text input fields
    task_name = st.text_input('Task Name')
    task_description = st.text_area('Task Description')

    # Date input field
    due_date = st.date_input('Due Date')

    # Selectbox for priority
    priority_options = ['LOW', 'MEDIUM', 'HIGH']
    priority = st.selectbox('Priority', priority_options)

    # Checkbox for completion status
    is_completed = st.checkbox('Is Completed')

    # Submit button
    if st.button('Submit'):
        # Process the form data
        process_form_data(task_name, task_description, due_date, priority, is_completed)


def process_form_data(task_name, task_description, due_date, priority, is_completed):
    # Process the form data here (e.g., save to a database, perform actions)
    st.write('Task name:', task_name)
    st.write('Task description:', task_description)
    st.write('Due date:', due_date)
    st.write('Priority:', priority)
    priority = PRIORITY_NUMBER[priority]
    st.write('Is completed:', is_completed)

    print(f"Task name: {task_name}")
    print(f"Task description: {task_description}")
    print(f"Due date: {due_date}")
    print(f"Priority: {priority}")
    print(f"Is completed: {is_completed}")

    services.task_manager.insert_task(task_name, task_description, due_date,
                                        priority, is_completed)


def display_tasks_details():
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