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
    # Create a sidebar with tab buttons
    st.sidebar.title('Navigation')
    st.sidebar.button('Tasks List', key='list_tasks', type='primary')
    if  st.sidebar.button('Add Task', key='add_task'):
        add_task()
    else:
        list_tasks()


def add_task():
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

def list_tasks():
    # TODO: resgatar do banco de dados
    # Dummy data for task listing
    tasks = [
        {'Task Name': 'Task 1', 'Task Description': 'Description 1', 'Due Date': '2022-01-01', 'Priority': 'LOW',
         'Is Completed': False},
        {'Task Name': 'Task 2', 'Task Description': 'Description 2', 'Due Date': '2022-01-02', 'Priority': 'MEDIUM',
         'Is Completed': True},
        {'Task Name': 'Task 3', 'Task Description': 'Description 3', 'Due Date': '2022-01-03', 'Priority': 'HIGH',
         'Is Completed': False}
    ]

    # Selectbox for filtering tasks
    filter_options = ['All', 'Completed', 'In Progress']
    filter_selection = st.selectbox('Filter Tasks', filter_options)

    # Filter tasks based on selection
    if filter_selection == 'All':
        filtered_tasks = tasks
    elif filter_selection == 'Completed':
        filtered_tasks = [task for task in tasks if task['Is Completed']]
    elif filter_selection == 'In Progress':
        filtered_tasks = [task for task in tasks if not task['Is Completed']]

    # Display tasks in a dataframe
    df = pd.DataFrame(filtered_tasks)
    st.dataframe(df)


if __name__ == "__main__":
    main()