# EcoApp 🌱
***
EcoApp е Django уеб приложение за организиране на еко‑инициативи, управление на събития, локации, участници и роли. Проектът включва интерактивни карти, филтриране, сортиране и пълна many‑to‑many логика.

---

## Преглед

EcoApp предоставя:

- Създаване и управление на събития
- Регистрация на участници
- Разпределяне на роли за участници
- Управление на локации с поддръжка на карта
- Admin панел за операции с данни

> Текущо обновление: добавена е map визуализация за локации, а `Location` съдържа **2 допълнителни полета** за координати.

---

## Технологии

- **Backend:** Django
- **Database:** SQLite (dev) / PostgreSQL (препоръчително за production)
- **Frontend:** Django Templates + static assets
- **Deployment:** Gunicorn (+ по избор Nginx reverse proxy)
- **Containerization:** Docker + Docker Compose
    Python 3.12+
    Django 5
    PostgreSQL
    Bootstrap 5
    HTML + Django Templates
---

🚀 Функционалности

    При старт на проекта, ролите се създават автоматично чрез сигнал (post_migrate) и включват: "организатор", "доброволец", "спонсор".

    При старт на проекта се създават две групи потребители — "Администратори" и "Модератори" и се задават съответните права за модели и операции.

    Регистрираните потребители с различни роли (администратор, модератор, обикновен потребител) имат различни права за достъп и управление на данните.

✔ Управление на събития (Event)

    Създаване, редактиране, изтриване - от модератор

    Детайлен изглед

    Филтриране по локация, област, дата от/до

    Сортиране по дата (възходящо/низходящо)

    Автоматично деактивиране на бутони за минали събития

✔ Управление на локации (Location)

    CRUD операции, според потребител

    Детайлен изглед

    Използване на локации в събития

    Област

✔ Управление на участници (Participant)
    
    CRUD операции, според потребител

    Регистриран потребител се регистрира за доброволец, като посочва град (ако липсва, може да добави).
 
        Детайлен изглед
    
        Списък със събития, в които участва даден участник

✔ Many‑to‑Many връзка: Participant ↔ Event ↔ Role

    Добавяне на участник към събитие с роля

    Ролите имат име и описание

    Списък с роли се показва в UI

    Малък бутон с иконка за премахване на участник от събитие

    Премахването е възможно само за бъдещи събития и за участници с роля различна от "организатор" и според потребител

    Организаторът се определя от модератор

✔ Навигация и UI

    Bootstrap 5 дизайн

    Navbar + footer (partials)

    Base template с наследяване

    Home страница

✔ Custom 404 страница

    Активирана чрез handler404

    Стилен Bootstrap дизайн

✔ Custom 403 страница

    Активирана чрез handler403

    Стилен Bootstrap дизайн


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
├── accounts/                    # User authentication and registration app
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
├── media/                       # Uploaded media files (e.g. event photos)
├── events/                      # Events management application
│   ├── __init__.py
│   ├── models.py                # Event, Location, and Role models
│   ├── views.py                 # Event-related views
│   ├── urls.py                  # Events URL patterns
│   ├── admin.py                 # Admin interface for events
│   ├── apps.py                  # App configuration
│   ├── tests.py                 # Unit tests
│   ├── migrations/              # Database migration files
│   └── __pycache__/
│
├── cities/                      # Cities management application
├── participants/                # Participants management application
│   ├── __init__.py
│   ├── models.py                # Participant and ParticipantEventRole models
│   ├── views.py                 # Participant-related views
│   ├── urls.py                  # Participants URL patterns
│   ├── admin.py                 # Admin interface for participants
│   ├── apps.py                  # App configuration
│   ├── tests.py                 # Unit tests
│   ├── migrations/              # Database migration files
│   └── __pycache__/
│
└── static/                      # static files (CSS, JS, images)
│   └── images                   # Image assets
│        └── hero-road.jpg       # Hero image for home page
│
└── staticfiles/                 # static files (admin, vendor, images)
└── templates/                   # HTML templates
│   ├── accounts/                # registration and authentication templates
│   ├── cities/                  # city-related templates (list, detail, forms)
│   ├── registration/            # registration templates (event registration form, participant registration form)
│   ├── core/                    # home page and core templates
│   ├── events/                  # event-related templates (list, detail, forms)
│   ├── partials/                # navbar, footer, and other reusable components
│   ├── participants/            # participant-related templates (list, detail, forms)
    └── base.html                # Base template for all pages
```
***
### 🗄️ Модели

EcoApp използва шест основни модела и клиенстски потребителски модел, организирани в две приложения — events и participants. Те покриват всички изисквания за работа със свързани данни, включително many‑to‑many връзка с допълнителни полета.


### AppUser
Потребителски модел, наследяващ AbstractBaseUser. Използва email като USERNAME_FIELD.

### Cities
Модел за градове, с избор на област от предварително дефиниран списък.

### Location
Представлява физическо място, на което се провеждат събития. Съдържа име, адрес, описание и географски координати, използвани за визуализация върху интерактивна карта.

**Полета:**
- name — име на локацията
- address — адрес
- district — област (избор от предварително дефиниран списък)
- description — допълнителна информация
- latitude — географска ширина
- longitude — географска дължина
- user — връзка към потребител (кой е добавил локацията)
---

### Event
Описва екологично събитие — дата, място, описание и връзка към участниците.

**Полета:**
- title — заглавие
- date — дата на провеждане
- location — връзка към Location
- description — описание
- created_at — автоматично генерирана дата на създаване
- report — текстово поле за отчет след събитието (по избор)

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
- contact_email — имейл за контакт
- first_name — собствено име
- last_name — фамилия
- city — град
- car_registration_number — регистрационен номер на автомобил (по избор)
- phone — телефон
- profile_picture — снимка (по избор)
- appended_at — дата на регистрация
- user — връзка към потребител (по избор, ако участникът има акаунт в системата)
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

#### Локална разработка

### Изисквания

- Python 3.10+
- Django 6
- pip
- virtualenv (препоръчително)
- PostgreSQL (препоръчително за production)
- Docker + Docker Compose (по избор)
requirements.txt съдържа всички необходими зависимости.


### Настройка

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
```

Създай `.env` и задай стойности (виж [Променливи на средата](#променливи-на-средата)).

Изпълни миграции и стартирай сървъра:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Приложението е достъпно на: `http://127.0.0.1:8000/`

---

## Деплоймънт

Препоръки за production:

1. Задай `DEBUG=False`
2. Конфигурирай `ALLOWED_HOSTS`
3. Използвай PostgreSQL
4. Изпълни `collectstatic`
5. Стартирай с Gunicorn
6. Добави Nginx отпред (TLS, static/media)

Примерна команда за Gunicorn:

```bash
gunicorn ecoapp.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

---

## Docker деплоймънт

### 1) Build и run с Docker Compose

```bash
docker compose up --build -d
```

### 2) Миграции в контейнера

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

### 3) Събиране на static файлове

```bash
docker compose exec web python manage.py collectstatic --noinput
```

### 4) Проверка на логове

```bash
docker compose logs -f web
```

### 5) Спиране на контейнерите

```bash
docker compose down
```

---

## Променливи на средата

Създай `.env` файл (не commit-вай secrets):

```env
DEBUG=False
SECRET_KEY=replace-with-strong-secret
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=ecoapp.settings

# PostgreSQL (препоръчително за production)
DB_NAME=ecoapp
DB_USER=ecoapp_user
DB_PASSWORD=change_me
DB_HOST=db
DB_PORT=5432
```

---

## Често използвани команди

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py test
python manage.py collectstatic --noinput
```

---

## Отстраняване на проблеми

- **Картата не се показва:** провери дали `latitude` и `longitude` имат стойности и дали map JS assets се зареждат.
- **Липсват static файлове в production:** изпълни `collectstatic` и провери static volume/path.
- **Грешка при връзка с база в Docker:** провери `DB_HOST`, `DB_PORT` и service името в `docker-compose.yml`.
- **400 Bad Request (host header):** обнови `ALLOWED_HOSTS`.

---

## Проектът е публикуван и достъпен на http://13.61.221.228

## 📝 Лицензи

Този проект е с образователна цел и не е лицензиран за комерсиална употреба.

## 👥 Контакти

**Автор**: Диана Ситева
           Разработен от Диана Ситева като част от учебен проект по Django и с помощта на ИИ - Microsoft Copilot и GitHub Copilot.
**Email**: dianasiteva@gmail.com


---


