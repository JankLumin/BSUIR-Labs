1. Users (Пользователи)
   Id: serial (PK)
   Name: varchar(255) NOT NULL
   Email: varchar(255) NOT NULL, UNIQUE
   Password: varchar(255) NOT NULL

   Один ко многим:

   - Tasks;
   - TaskComments;
   - Logs;
   - Notifications.

   Один к одному:

   - UserProfiles.

   Один ко многим:

   - UserRoles.

2. Roles (Роли)
   Id: serial (PK)
   Role_Name: varchar(100) NOT NULL UNIQUE

   Один ко многим:

   - UserRoles.

3. UserProfiles (Профили пользователей)
   User_Id: integer (FK на Users), UNIQUE
   Phone: varchar(20)
   Address: varchar(255)
   Date_Of_Birth: date
   Profile_Picture: varchar(255)

   Один к одному:

   - Users.

4. Tasks (Задачи)
   Id: serial (PK)
   Title: varchar(255) NOT NULL
   Description: text NOT NULL
   Status: varchar(50) NOT NULL
   Creation_Date: timestamp NOT NULL
   Completion_Date: timestamp
   Project_Id: integer (FK на Project)
   Executor_Id: integer (FK на User)

   Многие к одному:

   - Projects.

   Один ко многим:

   - TaskComments.

   Многие к одному:

   - Users.

   Один к одному:

   - Deadlines.

5. TaskComments (Комментарий к задачам)
   Id: serial (PK)
   Text: text NOT NULL
   Creation_Date: timestamp NOT NULL
   Task_Id: integer (FK на Task)
   Author_Id: integer (FK на Users)

   Многие к одному:

   - Tasks;
   - Users.

6. Projects (Проекты)
   Id: serial (PK)
   Title: varchar(255) NOT NULL
   Description: text NOT NULL
   Start_Date: date NOT NULL
   End_Date: date

   Один ко многим:

   - Tasks;
   - ProjectResources;
   - Deadlines.

7. ProjectResources (Ресурсы проектов)
   Id: serial (PK)
   Description: text NOT NULL
   Type: varchar(50) NOT NULL
   Project_Id: integer (FK на Project)

   Многие к одному:

   - Projects.

8. Logs (Журналы действий)
   Id: serial (PK)
   Action: text NOT NULL
   Date: timestamp NOT NULL
   User_Id: integer (FK на Users)

   Многие к одному:

   - Users.

9. Notifications (Уведомления)
   Id: serial (PK)
   Message: text NOT NULL
   Read: boolean NOT NULL DEFAULT false
   Date: timestamp NOT NULL
   User_Id: integer (FK на Users)
   Project_Id: integer (FK на Project)

   Многие к одному:

   - Users;
   - Projects.

10. Deadlines (Сроки выполнения)
    Id: serial (PK)
    Due_Date: timestamp NOT NULL
    Type: varchar(50) NOT NULL
    Task_Id: integer (FK на Task), UNIQUE
    Project_Id: integer (FK на Project)

    Один к одному:

    - Tasks.

    Многие к одному:

    - Projects.

11. UserRoles (Роли пользователей)
    User_Id: integer (FK на Users), UNIQUE
    Role_Id: integer (FK на Role), UNIQUE
    Project_Id: integer (FK на Project)
    Один пользователь — одна роль в проекте.
