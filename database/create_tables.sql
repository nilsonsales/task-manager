CREATE DATABASE task_manager;

CREATE SCHEMA task_manager;

-- Create table tasks
CREATE TABLE tasks_manager.tasks (
	id BIGSERIAL PRIMARY KEY,
    task_name VARCHAR(255),
    task_description TEXT,
    due_date DATE,
    priority INTEGER,
    username VARCHAR(255),
    is_completed BOOLEAN,
    created_at TIMESTAMP WITH time ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH time ZONE DEFAULT NULL
);

-- Create table users
CREATE EXTENSION pgcrypto;

CREATE TABLE task_manager.users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
  	password TEXT NOT NULL
);