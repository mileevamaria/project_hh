# [Сайт с вакансиями из hh.ru для профессий в сфере IT](https://pythonist-vacancies.herokuapp.com)


## Stack
- **Back-end**: flask, wtforms, sqlalchemy, migrations, blueprints
- **Front-end**: bootstrap
- **Database**: mysql
- **Parser**: scrapy
- **ML & statistics**: tensorflow, sklearn, pandas, numpy, nltk 



## Run web-application
- [Demo database](https://github.com/mileevamaria/demo_database/tree/master/project_hh)
- [Instructions](#instructions)

На сайте можно посмотреть вакансии, отфильтровать их по [ключевым навыкам](#skills-and-professional-areas) и профессиональным сферам, а также добавить вакансию в избранное. Вакансии на профессиональные сферы размечает [модель](https://colab.research.google.com/drive/1BsP6crvOYPihdtJ_rIx7KEms7z6nm0UE), которая также удаляет нерелеватные вакансии, выдаваемые hh по запросу "python".

![](https://github.com/mileevamaria/project_hh/blob/master/img/homepage.png)

Зарегистрированный юзер может выбрать свои навыки в кабинете, сразу посмотреть подходящие ему вакансии и добавить вакансию в избранное

![](https://github.com/mileevamaria/project_hh/blob/master/img/profile.png)

![](https://github.com/mileevamaria/project_hh/blob/master/img/relevant_vacancies.png)

![](https://github.com/mileevamaria/project_hh/blob/master/img/favourites.png)



## Instructions

1. Cклонируйте репозиторий:
```bash 
git clone https://github.com/mileevamaria/project_hh.git
```
2. Установите все пакеты из **requirements.txt**:
```bash 
pip install -r requirements.txt
```
3. В файле **config.py** в настройках базы данных `SQLALCHEMY_DATABASE_URI` запишите ссылку на вашу БД, например:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:your_password@localhost:3306/name_of_bd'
```
4. Установите все миграции для создания таблиц в БД:
```bash 
flask db upgrade
```
5. Заимпортируйте [данные](https://github.com/mileevamaria/demo_database/tree/master/project_hh) вакансий и навыков.

6. Сделайте файл запуска исполняемым:
```bash 
chmod +x run.sh
```
7. Запустите сайт:
```bash 
./run.sh
```



## Skills and professional areas

**Специализации:**
- Bigdata
- Development
- DevOps
- QA
- Systemadministration
- Teaching
- Teamlead

**Языки программирования:**
- Python
- Java
- PHP
- Pascal
- Ruby
- ABAP
- JavaScript
- C++
- SQL
- Delphi
- TypeScript
- .NET
- Kotlin
- Scala

**Базы данных:**
- MySQL
- PostgreSQL
- Redis
- Cassandra
- Prometheus
- InfluxDB
- MongoDB
- MariaDB
- CouchDB
- ClickHouse

**Фреймворки:**
- Django
- Flask
- AIOHTTP
- Falcon
- Spark

**Веб-протоколы:**
- TCP/IP
- TCP
- WebSocket

**Поисковые системы:**
- Elasticsearch
- Solr
- Sphinx

**Веб-серверы:**
- Tornado
- Apache
- Nginx

**Брокеры сообщений:**
- RabbitMQ
- Kafka
- Amazon SQS

**Операционные системы:**
- Windows
- Linux
- Debian

**Контроль версий:**
- Git
- Bitbucket
- Github
- Mercurial

**Виртуализация:**
- Docker
- VMware

**Автоматизация:**
- PowerShell
- Ansible
- Jenkins
- TeamCity

**ORM:**
- Sqlalchemy
- Mongoengine
- Hibernate

**Системы управление проектами:**
- Redmine
- Confluence
 
**Методы управления проектами:**
- Scrum
- Kanban
- Agile
 
**Системы мониторинга:**
- Zabbix
