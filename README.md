# 🪴 Root Record

A full-stack Django web application for tracking your personal plant collection and managing care schedules. Root Record lets plant owners log every watering, fertilizing, pruning, and repotting event — with photo support, filtering, and overdue task alerts.

---

## 📸 Features

### 🌿 Species Library
- Browse a curated reference list of plant species managed by the admin
- Each species includes scientific name, common name, light requirements, recommended watering interval, and care notes
- Detail page for each species with all relevant care info at a glance

### 🪴 My Plants
- Add and manage your personal plant collection
- Upload a photo for each plant
- Track nickname, location in your home, and species
- View all care tasks associated with a plant from its detail page
- Edit or delete plants (deletion cascades to all associated tasks and logs)

### ✔️ Care Tasks
- Create tasks for individual plants: **Water**, **Fertilize**, **Prune**, or **Repot**
- Set a due date for each task
- Tasks are automatically sorted: **Overdue → Upcoming → Completed**
- Visual status indicators:
  - 🚨 Overdue tasks highlighted in red
  - ✔️ Completed tasks marked clearly
  - ▪️ Active upcoming tasks
- Mark a task complete by logging it (see Care History)
- Edit or delete tasks at any time

### 📋 Care History
- Every completed task generates a care log with a timestamp
- Add notes and an optional photo to each log entry
- Logs are grouped by date for easy browsing
- Filter logs by:
  - **Plant** — see all care for a specific plant
  - **Task type** — filter by watering, fertilizing, etc.
  - **Species** — see care across all plants of the same species
- Edit log entries after the fact

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Framework | Django 4.2 |
| Database | SQLite (dev) |
| Image Handling | Pillow |
| Frontend | Django Templates, HTML, CSS |
| Static Files | Django staticfiles |
| Media Files | Django media file handling |

---

## 📁 Project Structure

```
rootrecord_project/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── rootrecord_project/          # Django project configuration
│   ├── settings.py              # App settings, DB config, media/static paths
│   ├── urls.py                  # Top-level URL routing
│   ├── wsgi.py
│   └── asgi.py
│
└── rootrecord/                  # Main application
    ├── models.py                # Data models
    ├── views.py                 # Class-based views
    ├── urls.py                  # App-level URL patterns
    ├── forms.py                 # ModelForms with custom widgets
    ├── admin.py                 # Admin site registrations
    ├── apps.py
    ├── tests.py
    ├── static/
    │   └── rootrecord.css       # App stylesheet
    └── templates/rootrecord/    # HTML templates
        ├── base.html
        ├── species_list.html
        ├── species_detail.html
        ├── plant_list.html
        ├── plant_detail.html
        ├── plant_form.html
        ├── plant_update.html
        ├── plant_delete.html
        ├── caretask_list.html
        ├── caretask_detail.html
        ├── caretask_form.html
        ├── caretask_update.html
        ├── caretask_delete.html
        ├── carelog_list.html
        ├── carelog_detail.html
        ├── carelog_form.html
        └── carelog_update.html
```

---

## 🗃️ Data Models

### `Species`
| Field | Type | Description |
|---|---|---|
| `name` | TextField | Scientific name |
| `common_name` | TextField | Common name |
| `notes` | TextField | General care notes |
| `water_interval` | IntegerField | Recommended days between watering |
| `light_req` | TextField | Light requirement (e.g. low, medium, bright) |

### `Plant`
| Field | Type | Description |
|---|---|---|
| `nickname` | TextField | User-given name |
| `species` | ForeignKey → Species | Plant species (cascades on delete) |
| `location` | TextField | Where in the home the plant lives |
| `image_file` | ImageField | Optional photo upload |
| `timestamp` | DateTimeField | Auto-set when plant is added |

### `CareTask`
| Field | Type | Description |
|---|---|---|
| `plant` | ForeignKey → Plant | Associated plant (cascades on delete) |
| `task` | TextField | Task type: water, fertilize, prune, repot |
| `due` | DateTimeField | When the task is due |
| `completed` | BooleanField | Whether the task has been logged |

### `CareLog`
| Field | Type | Description |
|---|---|---|
| `care_task` | ForeignKey → CareTask | The task this log completes (cascades on delete) |
| `notes` | TextField | Optional care notes |
| `image_file` | ImageField | Optional photo of the plant post-care |
| `timestamp` | DateTimeField | Auto-set when log is created |

---

## 🔗 URL Structure

| URL | View | Description |
|---|---|---|
| `/` | SpeciesListView | Home — species library |
| `/rootrecord/species/` | SpeciesListView | Species list |
| `/rootrecord/species/<pk>/` | SpeciesDetailView | Species detail |
| `/rootrecord/plants/` | PlantListView | All plants |
| `/rootrecord/plants/<pk>/` | PlantDetailView | Plant detail + tasks |
| `/rootrecord/plants/create/` | PlantCreateView | Add a plant |
| `/rootrecord/plants/<pk>/update/` | PlantUpdateView | Edit a plant |
| `/rootrecord/plants/<pk>/delete/` | PlantDeleteView | Delete a plant |
| `/rootrecord/tasks/` | CareTaskListView | All tasks |
| `/rootrecord/tasks/<pk>/` | CareTaskDetailView | Task detail + logs |
| `/rootrecord/plants/<pk>/tasks/create/` | CareTaskCreateView | Add a task to a plant |
| `/rootrecord/tasks/<pk>/update/` | CareTaskUpdateView | Edit a task |
| `/rootrecord/tasks/<pk>/delete/` | CareTaskDeleteView | Delete a task |
| `/rootrecord/logs/` | CareLogListView | Care history with filters |
| `/rootrecord/logs/<pk>/` | CareLogDetailView | Log detail |
| `/rootrecord/tasks/<pk>/logs/create/` | CareLogCreateView | Complete a task / create log |
| `/rootrecord/logs/<pk>/update/` | CareLogUpdateView | Edit a log |
| `/admin/` | Django Admin | Manage all data as superuser |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/rootrecord_project.git
cd rootrecord_project

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create an admin account
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/root_record** in your browser.

### Adding Species (Admin Only)

Species are managed through the Django admin panel — regular users can browse them but not create them, keeping the species library curated.

1. Go to **http://127.0.0.1:8000/admin/**
2. Log in with your superuser credentials
3. Click **Species → Add Species**
4. Fill in the name, common name, watering interval, light requirements, and any notes

Once species exist, anyone can add plants from the **My Plants** page.
