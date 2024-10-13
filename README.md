![kandinsky-download-1728781924725](https://github.com/user-attachments/assets/c6ab919f-66e3-4b5e-b0bb-edf1de4e5f9a)

# :robot: Chat-Bot to help Russian Railways employees

### Команда Мои-Закупки предствляет решение на кейс Разработка QnA чат-бота на основе базы знаний
[Ссылка на решение](http://176.109.110.144:3000/)


## :exploding_head: Проблематика

Ежегодно более 100 000 сотрудников ОАО "РЖД" сталкиваются с необходимостью ознакомиться с большим количеством документов по льготам, а специалисты по кадрам не всегда успевают объяснить все детали. Дополнительную сложность создают постоянные изменения нормативных актов и наличие 3500 филиалов с собственными правилами предоставления льгот.
## :hugs: Решение

Эффективным решением станет чат-бот для поддержки сотрудников, который позволит быстро находить ответы на вопросы по документам, адаптируясь к персональным данным каждого сотрудника и учитывая его уникальные потребности.

## :building_construction: Архитектра решения

Интеллектуальный чат-бот построен на RAG-pipeline, который включает в себя:
- Bi-encoder
- Cross-encoder
- LLM

### :hammer: Подготовка данных

Данные из исходного документа мы побили на части по пунктно. Пункт наболее полно выражает законченную единицу информации, в следствии чего был взять за основу

### :pencil2: Ввод пользователя

Происходит векторизация пользовательского запроса

### :mag_right: Поиск запроса по вектоной базе данных

Векторным поиском находим топ 15 релеваных документов

>[!Note]
>Причем векторный поиск происходит только по документам предприятия, к которому относиться сотрудник
>

### :bookmark_tabs: Фильтруем документы

LLM выполняет фильтрацию документов и выбирает k документов для генерации ответа

>[!Note]
>LLM использует подход, при котором она сама решает сколько релевантных документов брать 
>

### :bulb: Генерация ответа

На основании отфильтрованных документов, генерируем ответ
> [!Note]
> Но если с фильтрации пришло 0 документов, модель сразу ответит "Я не знаю". Поэтому у модели нет возможности
> придумывать свои ответ. Ответы всегда будут опираться на документы
>

### :haircut: Персонализация ответа

В следствии того, что ответ может быть большим длинным и не вся информация будет реливанта пользователю, на данном этапе мы на основании данных о пользователю вычленяем полезную лично ему информацию, тем самым освобождая от надобности изучать длинный пункты
> [!Note]
> На этом этапе мы скрываем информацию о каких-то льготах, которые ждут сотрудника через n лет и показываем информацию,
> которая будет для него актуальна в текущем году. Но при необходммости он может подробно ознакомиться с теми пунктами, на котором
> основывался ответ
>

### :floppy_disk: Запись в БЗ

Вопрос пользователя и ответ системы сохраняются в базу знаний для будующего масштабирования и улучшения системы

### :bricks: Композиция нагядно
![805909b7-deae-4918-9464-6502a8581b39](https://github.com/user-attachments/assets/edef0ea9-8aa3-4e58-8a86-2b272e5c6295)

# :rocket: Запуск
Решение упаковано и будет готов к работе через **2 строки**

**Для запуска нужны**
- docker
- docker compose
- make

**Запуск инференса LLM**
```
vllm serve --dtype half --max-model-len 16000 -tp 1 Vikhrmodels/Vikhr-Nemo-12B-Instruct-R-21-09-24 --api-key token-abc123
```

**Развертывание**
```
make up
```

# :computer: Стек технологий
[![My Skills](https://skillicons.dev/icons?i=python,vue,redis)](https://skillicons.dev) 

**БД**
- redis (хранилище информации о документах и запросов пользователей)
- chroma (векторное хранилище)

**Код**
- python
- langchain 🦜️🔗
- Vue

# :checkered_flag: Итог
**В конечном итоге мы предлагалем решение у которого**

:heavy_check_mark: Быстрый инференс (до 15 секнуд)

:heavy_check_mark: Точнось и полнота ответа 0.85

:heavy_check_mark: Персонализация

:heavy_check_mark: Защита от галлюцинаций

:heavy_check_mark: Простое обогащение новыми документами

:heavy_check_mark: Легкая интеграция

:heavy_check_mark: Интерфейс-песочница для тестирования фич

## made with ♥️ by Мои-Закупки for
![header-logo c7e8f395](https://github.com/user-attachments/assets/8a56ca15-e17a-4ab6-b864-017fce804610)


