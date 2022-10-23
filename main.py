import requests
import datetime as dt
import time
import os


dict_user = requests.get('https://json.medrocket.ru/users').json()
dict_task = requests.get('https://json.medrocket.ru/todos').json()


def index():
    for user in dict_user:
        company = user['company']['name']
        time_now = dt.datetime.now().strftime('%d.%m.%Y %H:%M')
        content = f"Отчет для {company}.\n"
        content += f"{user['name']} <{user['email']}> {time_now} \n"
        tasks = 0
        complete_task = ''
        uncomplete_task = ''
        try:
            for task in dict_task:
                if len(task['title']) > 48:
                    task['title'] = task['title'][:48] + '...'
                if user['id'] == task['userId']:
                    tasks += 1
                    if task['completed']:
                        complete_task += task['title'] + '\n'
                    else:
                        uncomplete_task += task['title'] + '\n'
        except KeyError:
            comp = complete_task.count('\n')
            uncomp = uncomplete_task.count('\n')
            if tasks == 0:
                content += 'У пользователя нет задач'
            else:
                content += f'Всего задач: {tasks} \n \n'
                content += f'Завершенные задачи ({comp}): \n'
                content += complete_task + '\n'
                content += f'Оставшиеся задачи ({uncomp}): \n'
                content += uncomplete_task
                generate_report(user['username'], content)
    fail_task()


def fail_task():
    content = ''
    for task in dict_task:
        if 'userId' not in task:
            content += 'Некорректное задание под номером ' + str(task['id']) + '\n'
    generate_report('incorrect', content)


def generate_report(file_name, content):
    if os.path.exists(f'tasks/{file_name}.txt'):
        rename_file(file_name)
    if not os.path.isdir("tasks"):
        os.mkdir("tasks")
    file = open(f"tasks/{file_name}.txt", "x", encoding="UTF-8")
    file.write('\n' + content)
    file.close()


def rename_file(file_name):
    time_create = time.localtime(os.path.getmtime(f"tasks/{file_name}.txt"))
    time_title = time.strftime('%Y-%m-%dT%H.%M', time_create)
    return os.rename(f"tasks/{file_name}.txt", f"tasks/old_{file_name}_{time_title}.txt")


index()
