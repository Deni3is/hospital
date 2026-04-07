# Hospital Registry

Небольшой Django-проект для ведения таблиц пациентов и устройств.

1) У меня стоит anaconda, но в принципе можно и просто через локальный python. Задания развернуть докер не было, поэтому не стал ничего лишнего придумывать 

2)Для запуска
Открой терминал в папке проекта и выполни:

```powershell
conda create -n hospital python=3.12 -y
conda activate hospital
pip install -r requirements.txt
python manage.py migrate
python manage.py create_demo_user
python manage.py runserver
```

После этого проект будет доступен по адресу:
`http://127.0.0.1:8000/`

3)Вход
Если запускалась команда `create_demo_user`, можно войти так (если нет то запустите, создаст нового пользователя для теста):
- логин: `doctor`
- пароль: `StrongPassword123`

если хочется просто проверить, что всё в порядке, можно запустить тесты:

```powershell
python manage.py test
```
