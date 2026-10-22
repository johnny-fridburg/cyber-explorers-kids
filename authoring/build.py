import json,html,re,shutil
from visuals import visual_panel
from pathlib import Path
root=Path(__file__).resolve().parent.parent
out=root
modules=json.loads((root/'authoring/course.json').read_text())
refs={
'nist':('NIST CSF 2.0','https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20','Прочитай Abstract, затем открой документ и найди функции Govern, Identify, Protect, Detect, Respond, Recover. Сопоставь по одной мере со своей картой рисков.'),
'wireshark':('Wireshark User’s Guide','https://www.wireshark.org/docs/wsug_html/','В оглавлении открой User Interface и Display Filters. Сопоставь список пакетов, поля и байты; найди пример фильтра tcp. Для практики используй только собственный разрешённый трафик.'),
'ad':('Microsoft: AD DS overview','https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview','Рассмотри описание каталога и объектов. Объясни разницу между пользователем, группой и ресурсом своей схемы.'),
'powershell':('Microsoft: PowerShell 101','https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/00-introduction','Открой вводную главу и главы о командах и конвейере. На своей Windows-системе попробуй только команды чтения Get-Process и Get-Service.'),
'linux':('Ubuntu: командная строка','https://ubuntu.com/tutorials/command-line-for-beginners','Следуй ссылке New version available на обновлённое руководство. Найди упражнения с pwd, ls, каталогами и pipe; выполняй их в отдельной учебной папке.'),
'python':('Python Tutorial','https://docs.python.org/3/tutorial/','Найди Control Flow, Functions, Input and Output, Errors and Exceptions. Руководство предполагает знакомство с программированием; сначала разбери наши вводные уроки и скрипт.'),
'ai':('OWASP: GenAI Security','https://owasp.org/www-project-top-10-for-large-language-model-applications/','Открой ссылку на GenAI Security Project и найди риски инструкций внутри недоверенных данных. Составь критерии проверки ответа на учебном CSV.'),
'kali':('Kali: официальные инструкции','https://www.kali.org/docs/','В разделе Virtualization выбери платформу и архитектуру своего устройства. До установки прочитай требования и разницу сетевых режимов.'),
'metasploit':('Metasploit Documentation','https://docs.metasploit.com/','Открой Getting Started → Using Metasploit. Найди различие модулей и payloads. Инструментальная практика выполняется только в разрешённом изолированном стенде.'),
'portswigger':('PortSwigger Web Security Academy','https://portswigger.net/web-security','Выбери тему SQL injection или XSS, прочитай вводный текст и beginner/Apprentice-лабораторию. Внешние лаборатории требуют интернета и могут требовать аккаунт; границы заданы их авторами.'),
'owasp':('OWASP Web Security Testing Guide','https://owasp.org/www-project-web-security-testing-guide/','Открой версионный раздел v4.2: Information Gathering, Authentication Testing и Input Validation Testing. Сопоставь выбранный тест с причиной ошибки и исправлением.'),
'procmon':('Microsoft: Process Monitor','https://learn.microsoft.com/en-us/sysinternals/downloads/procmon','Изучи описание и иллюстрации интерфейса. Если установишь официальный инструмент на учебную Windows-машину, наблюдай только свой текстовый редактор и фильтруй по его процессу.'),
'autoruns':('Microsoft: Autoruns','https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns','Рассмотри видео и список мест автозапуска. Для первого опыта только читай записи; не отключай элементы системы наугад.'),
'splunk':('Splunk Search Tutorial — требуется проверка доступа','https://docs.splunk.com/Documentation/Splunk/latest/SearchTutorial/WelcometotheSearchTutorial','При подготовке страница вернула 403, содержимое не подтверждено. Если ссылка недоступна, открой официальный сайт документации Splunk и найди Search Tutorial. Не считай наш фильтр полноценным SPL.'),
'volatility':('Volatility 3 Documentation','https://volatility3.readthedocs.io/en/latest/','Найди Getting Started и плагины для процессов. Для работы нужен подходящий учебный дамп и символы. Сопоставь структуру результата с нашей готовой таблицей, не смешивай версии 2 и 3.'),
'ot':('NIST SP 800-82 Rev. 3: OT Security','https://csrc.nist.gov/pubs/sp/800/82/r3/final','Открой итоговый документ Rev. 3, найди схемы OT-архитектуры и сегментации. Объясни физическое последствие потери связи. Упоминание проекта Rev. 4 не означает, что это финальная замена.'),
}
def esc(s):return html.escape(str(s))
lessons=''
for i,m in enumerate(modules,1):
    body=''.join(f'<details class="lesson" open><summary>{i}.{j} {esc(title)}</summary><p>{esc(text)}</p><label class="done"><input type="checkbox" data-progress="m{i}l{j}"> Я объяснила эту тему своими словами</label></details>' for j,(title,text) in enumerate(m['lessons'],1))
    investigate=['Что изменится, если резервная копия хранится на том же диске? Нарисуй отказ одного диска и проверь, переживает ли его твоя защита.', 'Почему Wi-Fi может работать, а сайт — не открываться? Придумай три разные причины и по одной проверке, которая отличит их друг от друга.', 'Что произойдёт с правами после изменения членства в группе? Сравни две роли на одном ресурсе и запиши, какие действия должны остаться запрещёнными.', 'Чем право x для каталога отличается от x для файла? Создай модель двух путей и объясни, почему чтение списка имён не равно доступу к содержимому.', 'Как изменить счётчик, чтобы учитывать только события в пяти минутах? Начни с двух времён и проверки границы ровно пять минут; затем добавь третье событие.', 'Можно ли заставить ответ выглядеть убедительно, убрав ограничения? Перепиши учебный вывод двумя способами и отметь фразы, которые скрывают неопределённость.', 'Какая мера остановит следующий этап после начального доступа? Соедини цепочку действий с минимальными правами, сегментацией и журналом наблюдений.', 'Почему один и тот же текст должен обрабатываться по-разному в HTML и SQL? Нарисуй два интерпретатора и покажи, где данные могли стать инструкцией.', 'Как убедиться, что исправление не сломало обычную функцию? Придумай один нормальный, один граничный и один запрещённый сценарий; предскажи результаты.', 'Что произойдёт с числом сигналов, если снизить порог с трёх fail до двух? Сравни чувствительность и нагрузку на проверку, не предполагая автоматически лучшую защиту.', 'Может ли ошибка часового пояса изменить вывод расследования? Сдвинь один источник на три часа и покажи, какая предполагаемая последовательность перестанет совпадать.', 'Какой новый источник сильнее всего различит две гипотезы? Выбери один журнал и назови поле, которое поддержит или опровергнет твоё объяснение.', 'Что будет, если датчик сообщает старое значение? Раздели реальный уровень и показание, затем объясни, почему одного сетевого статуса недостаточно.'][i-1]
    q,opts,a,ex=m['quiz']
    quiz=f'<div class="investigation"><div class="eyebrow">ЕЩЁ ОДНО ОТКРЫТИЕ · ПО ЖЕЛАНИЮ</div><h3>Хочешь копнуть глубже?</h3><p>{esc(investigate)}</p><details><summary>Как подойти к исследованию</summary><ol><li>Сформулируй прогноз до опыта.</li><li>Измени один фактор.</li><li>Сравни наблюдение с прогнозом.</li><li>Назови то, что пока неизвестно.</li></ol></details><label>Моё открытие<textarea class="reflection" data-note="reflection{i}" rows="3" placeholder="Я ожидала… Я заметила… Теперь хочу проверить…"></textarea></label></div>'+f'<div class="quiz" data-answer="{a}"><h3>Проверь себя</h3><p>{esc(q)}</p>'+''.join(f'<label><input type="radio" name="quiz{i}" value="{j}"> {esc(t)}</label>' for j,t in enumerate(opts))+f'<button type="button" class="check">Проверить</button><p class="feedback" aria-live="polite" data-explanation="{esc(ex)}"></p></div>'
    links=''.join(f'<li><a href="{esc(refs[r][1])}" target="_blank" rel="noopener noreferrer">{esc(refs[r][0])} ↗</a><p>{esc(refs[r][2])}</p></li>' for r in m['refs'])
    lessons+=f'<section class="module" id="m{i}"><div class="eyebrow">МОДУЛЬ {i:02} · {m["hours"]} АКАДЕМИЧЕСКИХ ЧАСОВ В СИЛЛАБУСЕ</div><h2>{esc(m["title"])}</h2><p class="lead">{esc(m["goal"])}</p>{visual_panel(i)}{body}<div class="quest"><h3>Твоя самостоятельная проба</h3><p>{esc(m["quest"])}</p><details><summary>Подсказка</summary><p>Сначала выпиши входные данные и ожидаемый результат. Измени только одну переменную и сравни.</p></details><details><summary>Разбор и критерий успеха</summary><p>{esc(m["solution"])}</p></details></div>{quiz}<h3>Посмотри и попробуй дальше</h3><ul class="resources">{links}</ul><label class="done"><input type="checkbox" data-progress="m{i}practice"> Я выполнила самостоятельную пробу</label><p><a href="#m{i+1}" class="next">Следующий модуль →</a></p></section>' if i<13 else f'<section class="module" id="m{i}"><div class="eyebrow">МОДУЛЬ {i:02} · {m["hours"]} АКАДЕМИЧЕСКИХ ЧАСОВ В СИЛЛАБУСЕ</div><h2>{esc(m["title"])}</h2><p class="lead">{esc(m["goal"])}</p>{visual_panel(i)}{body}<div class="quest"><h3>Твоя самостоятельная проба</h3><p>{esc(m["quest"])}</p><details><summary>Разбор</summary><p>{esc(m["solution"])}</p></details></div>{quiz}<h3>Источники и практика</h3><ul class="resources">{links}</ul><label class="done"><input type="checkbox" data-progress="m{i}practice"> Я выполнила самостоятельную пробу</label><p><a href="#finish">Итоговая работа →</a></p></section>'
nav=''.join(f'<a href="#m{i}"><span>{i:02}</span>{esc(m["title"].split(":")[0])}</a>' for i,m in enumerate(modules,1))
# Preserve exact English topic wording from the supplied PDF in a compact coverage appendix.
syllabus=(root/'authoring/cyber-syllabus.txt').read_text()
eng=[]
for line in syllabus.splitlines():
    if re.search('[A-Za-z]',line) and not line.startswith('---'):
        eng.append(line)
coverage='<br>'.join(esc(l) for l in eng)
frame=(root/'authoring/frame.html').read_text()
frame=frame.replace('@@VISUAL_CSS@@',(root/'authoring/visual.css').read_text()).replace('@@VISUAL_LABS@@',(root/'authoring/visual-labs.html').read_text()).replace('@@VISUAL_JS@@',(root/'authoring/visual.js').read_text())
frame=frame.replace('@@NAV@@',nav).replace('@@LESSONS@@',lessons).replace('@@COVERAGE@@',coverage)
(out/'index.html').write_text(frame)
(out/'labs/events.csv').write_text('timestamp,host,source,user,action,result\n2026-01-10T09:00:00Z,portal,192.0.2.10,student,login,fail\n2026-01-10T09:01:00Z,portal,192.0.2.10,student,login,fail\n2026-01-10T09:02:00Z,portal,192.0.2.10,student,login,fail\n2026-01-10T09:03:00Z,portal,192.0.2.10,student,login,success\n2026-01-10T09:04:00Z,workstation,192.0.2.20,student,file_create,success\n2026-01-10T09:05:00Z,portal,192.0.2.11,teacher,login,success\n')
(out/'labs/process-tree.csv').write_text('pid,ppid,name,path,timestamp\n100,50,editor,C:/Lab/editor.exe,2026-01-10T09:03:30Z\n420,100,marker,C:/Lab/marker.exe,2026-01-10T09:04:00Z\n')
(out/'labs/timeline.csv').write_text('timestamp,artifact,event,certainty\n2026-01-10T09:03:00Z,events.csv row 5,login success,synthetic fact\n2026-01-10T09:04:00Z,events.csv row 6,file create,synthetic fact\n2026-01-10T09:04:00Z,process-tree.csv row 3,process with parent 100,synthetic fact\n')
(out/'labs/analyze_events.py').write_text('''"""Безопасный учебный анализ локального CSV; сеть не используется."""
import csv
from collections import Counter
from pathlib import Path

def count_failures(rows):
    return Counter(row["source"] for row in rows
                   if row.get("action") == "login" and row.get("result") == "fail")

if __name__ == "__main__":
    path = Path(__file__).with_name("events.csv")
    try:
        with path.open(encoding="utf-8", newline="") as file:
            counts = count_failures(csv.DictReader(file))
        for source, count in sorted(counts.items()):
            print(f"{source}: {count} failed logins")
        print("This count does NOT implement a time window or prove compromise.")
    except FileNotFoundError:
        raise SystemExit("Put events.csv next to this script.")
''')
(out/'labs/report-template-ru.md').write_text('''# Учебный отчёт

Все данные вымышленные. Вариант: офлайн-модель / разрешённая лаборатория.

## Цель и границы
Что проверяется, какие ресурсы разрешены, что нельзя делать.

## Среда и предпосылки
Версии, роли, входные данные и ожидаемое поведение.

## Факты
| Время UTC | Артефакт и строка | Наблюдение | Ограничение |
|---|---|---|---|

## Гипотезы
| Гипотеза | Поддерживает | Противоречит | Следующая проверка |
|---|---|---|---|

## Проверка
Вход → действия → ожидаемый результат → фактический результат.
Не выдавай условный вывод за результат реального инструмента.

## Риск и рекомендации
Последствия, предпосылки, меры и их проверка.

## Повторная проверка
Обычный сценарий, граничный сценарий и запрет.

## Восстановление и неизвестное
Как вернуть среду; какие выводы нельзя сделать.
''')
print('modules',len(modules),'lessons',sum(len(m['lessons']) for m in modules),'hours',sum(m['hours'] for m in modules),'html bytes',len(frame.encode()))
