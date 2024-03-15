### Инструкции по настройке конфигурационных файлов:

1.  config.json - шаблон config_demo.json (в директории CheckMoodle). Настройка IDE, использующихся в GUI для проверки.
    Хотя бы один параметр должен быть определён.

    -   `vscode`: Путь к исполняемому файлу Visual Studio Code. Например: `"C:/Path_to_VSCode/vscode.exe"`
    -   `pascal`: Путь к исполняемому файлу Pascal. Например: `"C:/Path_to_Pascal/pascal.exe"`
    - 	`vsversion`":  Мажорная версия Visual Studio установленная в системе. Например для Visual Studio 2022 это `"17"`,
3.  credentials.json - шаблон credentials_demo.json (в директории MoodleAssistant).
    Настройка локального хранилища и доступа к moodle.

    -   `download_folder`: Путь к папке, в которую браузер скачивает файлы. Например: `"C:/Users/your_username/Downloads"`
    -   `username`: Имя пользователя для входа в Moodle. Например: `"your_moodle_username"`
    -   `password`: Пароль для входа в Moodle. Например: `"your_moodle_password"`
    -   `check_moodle`: Путь к исполняемому файлу CheckMoodle (После сборки лежит в репозитории). Например: `"D:/Path_to_your_project/AllTheMoodleMMCS/CheckMoodle/bin/Release/CheckMoodle.exe"`
5.  cs211b.json - шаблон cs211b_demo.json (в директории MoodleAssistant). Имя может быть любое. Конфиги для разных курсов.

    -   `course`: Ссылка на курс в Moodle. Например: `"https://your_moodle_link/course/view.php?id=XXX"`
    -   `data_folder`: Путь к папке с данными. Например: `"D:/Path_to_data_folder"`
    -   `l`: Язык программирования (например, "cc" для C++).
    -   `fexts`: Расширения файлов, которые следует учитывать. Например: `["*.cpp", "*.h"]`
    -   `IDE`: Используемая среда разработки (например, "vs" для Visual Studio).
    -   `groups`: Группы студентов и их расписание.
        -   Название группы (например, `"Name_of_the_group (Instructor's_name)"`):
            -   `group`: ID группы. Этот идентификатор следует получить с сайта. (TODO: Заполните это поле)
            -   `hb`: Час начала занятия. Например: `"XX"`
            -   `mb`: Минута начала занятия. Например: `"XX"`
            -   `he`: Час окончания занятия. Например: `"XX"`
            -   `me`: Минута окончания занятия. Например: `"XX"`

После того как вы настроите конфигурационные файлы, убедитесь, что все пути и учетные данные указаны верно. Это обеспечит корректную работу программы.
Вот пример файла `cs211b_demo.json` с двумя группами:



```json
{
	"course": "https://your_moodle_link/course/view.php?id=XXX",
	"data_folder": "D:/Path_to_data_folder",
	"l": "cc",
	"fexts": ["*.cpp", "*.h"],
	"IDE": "vs",
	"groups": {
		"Group_1 (Instructor's_name_1)": {
			"group": "ID_1",
			"hb": "XX",
			"mb": "XX",
			"he": "XX",
			"me": "XX"
		},
		"Group_2 (Instructor's_name_2)": {
			"group": "ID_2",
			"hb": "XX",
			"mb": "XX",
			"he": "XX",
			"me": "XX"
		}
	}
}
```

В этом примере:

-   `"Group_1 (Instructor's_name_1)"` и `"Group_2 (Instructor's_name_2)"` - это названия групп.
-   `"ID_1"` и `"ID_2"` - это идентификаторы групп, которые следует получить с сайта. (TODO: Заполните это поле)
-   `"XX"` - это временные значения, которые следует заменить на реальные значения времени начала и окончания занятий.

Вы можете адаптировать этот пример под свои нужды, заполнив все необходимые поля. Если у вас есть дополнительные вопросы или замечания, дайте знать!
