import streamlit as st
import logging
import pandas as pd
import services


logger = logging.getLogger()

PRIORITY_NUMBER = {
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3
}


def main():
    selected_tab = st.sidebar.radio('Navigation', ('Home', 'Add Task', 'Task Details'))

    if selected_tab == 'Home':
        display_home()
    elif selected_tab == 'Add Task':
        display_add_task()
    elif selected_tab == 'Task Details':
        display_tasks_details()



def display_home():
    st.title('Simple Task Manager')
    st.write('Welcome to the Task Manager homepage!')
    st.write('Here you can view your tasks and manage them.')

    tasks = [
        {'Task Name': 'Task 1', 'Task Description': 'Description 1', 'Due Date': '2022-01-01', 'Priority': 'LOW',
         'Is Completed': False},
        {'Task Name': 'Task 2', 'Task Description': 'Description 2', 'Due Date': '2022-01-02', 'Priority': 'MEDIUM',
         'Is Completed': True},
        {'Task Name': 'Task 3', 'Task Description': 'Description 3', 'Due Date': '2022-01-03', 'Priority': 'HIGH',
         'Is Completed': False}
    ]

    # Display tasks in a clean design
    in_progress_tasks = [task for task in tasks if not task['Is Completed']]
    for task in in_progress_tasks:
        task_name = task['Task Name']
        task_description = task['Task Description']
        is_completed = st.checkbox(f'{task_name} - {task_description}', value=task['Is Completed'])
        if is_completed:
            st.write('This task is completed.')
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
    st.write('Task Name:', task_name)
    st.write('Task Description:', task_description)
    st.write('Due Date:', due_date)
    st.write('Priority:', priority)
    priority = PRIORITY_NUMBER[priority]
    st.write('Is Completed:', is_completed)

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
    df = pd.DataFrame(filtered_tasks)
    st.dataframe(df, hide_index=True)


if __name__ == "__main__":
    main()