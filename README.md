# EcoApp 🌱
***
EcoApp е Django уеб приложение за организиране на еко‑инициативи, управление на събития, локации, участници и роли. Проектът включва интерактивни карти, филтриране, сортиране и пълна many‑to‑many логика.

🚀 Функционалности

✔ Управление на събития (Event)

    Създаване, редактиране, изтриване

    Детайлен изглед

    Филтриране по локация, дата от/до

    Сортиране по дата (възходящо/низходящо)

    Автоматично деактивиране на бутони за минали събития

✔ Управление на локации (Location)

    CRUD операции

    Детайлен изглед

    Използване на локации в събития

✔ Управление на участници (Participant)
    
    CRUD операции

✔ Many‑to‑Many връзка: Participant ↔ Event ↔ Role

    Добавяне на участник към събитие с роля

    Ролите имат име и описание

    Списък с роли се показва в UI

    Малък бутон с иконка за премахване на участник от събитие

    Премахването е възможно само за бъдещи събития

✔ Навигация и UI

    Bootstrap 5 дизайн

    Navbar + footer (partials)

    Base template с наследяване

    Home страница

✔ Custom 404 страница

    Активирана чрез handler404

    Стилен Bootstrap дизайн

🛠 Технологии

    Python 3.12+

    Django 5

    PostgreSQL

    Bootstrap 5

    HTML + Django Templates

📁 Структура на проекта

```
EcoApp/
├── manage.py                    # Django management command script
├── requirements.txt             # Python package dependencies
├── README.md                    # This file
│
├── EcoApp/                      # Main project configuration package
│   ├── __init__.py
│   ├── settings.py              # Django configuration settings
│   ├── urls.py                  # URL routing configuration
│   ├── asgi.py                  # ASGI application (for async support)
│   ├── wsgi.py                  # WSGI application (for production servers)
│   └── __pycache__/
│
├── core/                        # Core application (homepage & main site views)
│   ├── __init__.py
│   ├── models.py                # Core data models
│   ├── views.py                 # View logic for core pages
│   ├── urls.py                  # Core URL patterns
│   ├── admin.py                 # Admin interface registration
│   ├── apps.py                  # App configuration
│   ├── tests.py                 # Unit tests
│   ├── migrations/              # Database migration files
│   └── __pycache__/
│
├── events/                      # Events management application
│   ├── __init__.py
│   ├── models.py                # Event, Location, and Role models
│   ├── views.py                 # Event-related views
│   ├── urls.py                  # Events URL patterns
│   ├── admin.py                 # Admin interface for events
│   ├── apps.py                  # App configuration
│   ├── tests.py                 # Unit tests
│   ├── migrations/              # Database migration files
│   │   ├── __init__.py
│   │   ├── 0001_initial.py      # Initial migration
│   │   ├── 0002_location....py  # Added latitude and longitude to Location
│   │   └── __pycache__/
│   └── __pycache__/
│
├── participants/                # Participants management application
│   ├── __init__.py
│   ├── models.py                # Participant and ParticipantEventRole models
│   ├── views.py                 # Participant-related views
│   ├── urls.py                  # Participants URL patterns
│   ├── admin.py                 # Admin interface for participants
│   ├── apps.py                  # App configuration
│   ├── tests.py                 # Unit tests
│   ├── migrations/              # Database migration files
│   │   ├── __init__.py
│   │   ├── 0001_initial.py      # Initial migration
│   │   ├── 0002_information.py  # Added information field to ParticipantEventRole
│   │   └── __pycache__/
│   └── __pycache__/
│
└── static/                      # static files (CSS, JS, images)
│   └── images                   # Image assets
│        └── hero-road.jpg       # Hero image for home page
│
└── templates/                   # HTML templates
│   ├── core/                    # home page and core templates
│   ├── events/                  # event-related templates (list, detail, forms)
│   ├── partials/                # navbar, footer, and other reusable components
│   ├── participants/            # participant-related templates (list, detail, forms)
    └── base.html                # Base template for all pages
```
***
### 🗄️ Модели

EcoApp използва четири основни модела, организирани в две приложения — events и participants. Те покриват всички изисквания за работа със свързани данни, включително many‑to‑many връзка с допълнителни полета.

### Location
Представлява физическо място, на което се провеждат събития. Съдържа име, адрес, описание и географски координати, използвани за визуализация върху интерактивна карта.

**Полета:**
- name — име на локацията
- address — адрес
- description — допълнителна информация
- latitude — географска ширина
- longitude — географска дължина

---

### Event
Описва екологично събитие — дата, място, описание и връзка към участниците.

**Полета:**
- title — заглавие
- date — дата на провеждане
- location — връзка към Location
- description — описание
- created_at — автоматично генерирана дата на създаване

---

### Role
Определя ролята на участник в дадено събитие (напр. доброволец, организатор, спонсор).

**Полета:**
- name — име на ролята
- description — кратко описание

  Ролите са предварително дефинирани и се показват в UI при добавяне на участник към събитие. Те се управляват от админ панела, но не са обвързани с конкретно събитие, т.е. една роля може да се използва в множество събития. 
---

### Participant
Представлява човек, който участва в събития.

**Полета:**
- first_name — собствено име
- last_name — фамилия
- email — уникален имейл
- phone — телефон
- appended_at — дата на регистрация

---

### ParticipantEventRole
Междинен модел, реализиращ many‑to‑many връзката между Participant и Event, като добавя и Role.

**Полета:**
- participant — участник |
- event — събитие        | уникален троен ключ
- role — роля            |
- information — допълнителна информация (по избор)

**Ограничения:**
- unique_together - в дадено събитие участник може да има различни роли, като не може да се дублира роля.
  напр. участник може да е спонсор, но и да е доброволец, т.е. участва освен с пари, примерно, и с труда си.

***
### 🖥️ Интерфейс и навигация```
EcoApp използва Bootstrap 5 за стил и оформление. Навигацията е реализирана чрез navbar, който включва линкове към основните страници: Home, Events, Locations, Participants. Footer - година и цел на приложението. 



## 📝 Лицензи

Този проект е с образователна цел и не е лицензиран за комерсиална употреба.

## 👥 Контакти

**Автор**: Диана Ситева
           Разработен от Диана Ситева като част от учебен проект по Django и с помощта на ИИ - Microsoft Copilot и GitHub Copilot.
**Email**: dianasiteva@gmail.com


---


