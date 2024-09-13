1. App_User (Пользователь)
   Id: serial (PK)
   Name: varchar(255) NOT NULL
   Email: varchar(255) NOT NULL UNIQUE
   Password: varchar(255) NOT NULL
   Связи: Один ко многим с Task и TaskComment, Один к одному с UserProfile, Многие ко многим с Role через UserRole.

2. Role (Роль)
   Id: serial (PK)
   Role_Name: varchar(255) NOT NULL UNIQUE
   Связи: Многие ко многим с User через UserRole.

3. UserProfile (Профиль пользователя)
   User_Id: integer (FK на User)
   Phone: varchar(15)
   Address: varchar(255)
   Date_Of_Birth: date
   Profile_Picture: text
   Связи: Один к одному с User.

4. Task (Задача)
   Id: serial (PK)
   Title: varchar(255) NOT NULL
   Description: text NOT NULL
   Status: varchar(50) NOT NULL
   Creation_Date: timestamp NOT NULL
   Completion_Date: timestamp
   Priority: integer
   Project_Id: integer (FK на Project)
   Creator_Id: integer (FK на User)
   Executor_Id: integer (FK на User)
   Связи: Многие к одному с Project, один ко многим с TaskComment и Deadline, Многие к одному с User.

5. TaskComment (Комментарий к задаче)
   Id: serial (PK)
   Text: text NOT NULL
   Creation_Date: timestamp NOT NULL
   Task_Id: integer (FK на Task)
   Author_Id: integer (FK на User)
   Связи: Многие к одному с Task и User.

6. Project (Проект)
   Id: serial (PK)
   Title: varchar(255) NOT NULL
   Description: text NOT NULL
   Start_Date: date NOT NULL
   End_Date: date
   Связи: Один ко многим с Task, ProjectResource и Deadline.

7. ProjectResource (Ресурс проекта)
   Id: serial (PK)
   Description: text NOT NULL
   Type: varchar(50) NOT NULL
   Project_Id: integer (FK на Project)
   Связи: Многие к одному с Project.

8. Log (Журнал действий)
   Id: serial (PK)
   Action: text NOT NULL
   Date: timestamp NOT NULL
   User_Id: integer (FK на User)
   Связи: Многие к одному с User.

9. Notification (Уведомление)
   Id: serial (PK)
   Message: text NOT NULL
   Read: boolean NOT NULL DEFAULT false
   Date: timestamp NOT NULL
   User_Id: integer (FK на User)
   Связи: Многие к одному с User.

10. Deadline (Срок выполнения)
    Id: serial (PK)
    Due_Date: timestamp NOT NULL
    Type: varchar(50) NOT NULL
    Task_Id: integer (FK на Task)
    Project_Id: integer (FK на Project)
    Связи: Многие к одному с Task, Многие к одному с Project.

11. UserRole (Роли пользователя) - МТМ
    User_Id: integer (FK на User)
    Role_Id: integer (FK на Role)
    Связи: Реализует многие ко многим между User и Role.
