# ✅ To-Do Web Application

A sleek and modern to-do application built using **Python** with [NiceGUI](https://nicegui.io/) for the frontend and **Google Firebase Firestore** for real-time backend storage.

Perfect for productivity addicts who also enjoy good design. This app supports full CRUD, drag-and-drop priorities, filtering, and syncs it all with Firebase 🔥.

---

## 🚀 Features

- ✨ Beautiful UI with NiceGUI
- 🔥 Real-time sync with Firebase Firestore
- 📌 Priority tagging (High, Medium, Low)
- 🔍 Search and filter tasks
- ✅ Mark done, edit, delete tasks
- 🧹 Bulk actions: Mark all done, clear all
- 📊 Progress bar with completion tracking
- 🔄 Reorder tasks (move up/down)

## 🛠️ Tech Stack

- [NiceGUI](https://nicegui.io/) – Python-native frontend framework
- [Firebase Firestore](https://firebase.google.com/docs/firestore) – Realtime cloud NoSQL DB
- [Python 3.10+](https://www.python.org/) – Main language
- Firebase Admin SDK

---
## 📸 UI Preview
<img width="1085" height="901" alt="image" src="https://github.com/user-attachments/assets/d6c5bb74-c4e0-473f-85d5-7cb3fdcfa012" />

---
## 📁 Folder Structure
```pgsql
todo-app/
├── todo_app.py
├── to-do-app-<project>-firebase-adminsdk.json  # Your Firebase credentials
└── README.md
```

## 🔌 Setup Instructions

Follow these steps to run the project locally:

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/todo-app.git
cd todo-app
```
### 2. Install dependencies

```bash
pip install firebase-admin

```
### 3. Setup Firebase
- 1.Go to Firebase Console.
- 2.Create a new project (e.g., To-Do App).
- 3.Navigate to Project Settings > Service Accounts.
- 4.Click Generate new private key and download the .json file.
- 5.Move the downloaded JSON key to your project directory.

⚠️ Do NOT commit the JSON file to GitHub. It contains sensitive credentials.

### 4.Update Python Script
In your todo_app.py, update this line:
```python
cred = credentials.Certificate("path/to/your/firebase-adminsdk.json")
```
Replace the path with the actual filename

## 5. Run the App
```bash
python todo_app.py
```

---
## 📋 Core Functionalities
➕ Add Task
Enter task text and select priority.
Click Add Task button.
🔄 Edit Task
Click Edit, modify text or priority.
Press Enter or click Save.
✅ Complete Task
Check the box to mark as done.
🗑️ Delete Task
Click Delete button.
📊 Progress Bar
Dynamically updates based on completed tasks.
🔍 Filter & Search
Filter by All, Done, or Pending.
Live search input.
📦 Bulk Actions
Mark All Done
Clear All Tasks
--
## 💡 Future Enhancements (Optional Ideas)
✅ User authentication via Firebase Auth
🌐 Multi-user task sync
📱 PWA/mobile support
🕒 Due dates and reminders
