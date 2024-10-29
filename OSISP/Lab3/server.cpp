#include <bits/stdc++.h>
#include <windows.h>

using namespace std;

#define PIPE_NAME R"(\\.\pipe\LogPipe)"

bool running = true;
mutex log_mutex;
ofstream logfile;

string CurrentTimestamp()
{
    time_t now = time(nullptr);
    tm localTime;
    localtime_s(&localTime, &now);
    char buffer[64];
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &localTime);
    return buffer;
}

void HandleClient(HANDLE hPipe)
{
    char buffer[1024];
    DWORD bytesRead;

    while (true)
    {
        BOOL success = ReadFile(hPipe, buffer, sizeof(buffer) - 1, &bytesRead, NULL);
        if (!success || bytesRead == 0)
        {
            break;
        }
        buffer[bytesRead] = '\0';

        string timestamp = CurrentTimestamp();

        {
            lock_guard<mutex> lock(log_mutex);
            logfile << "[" << timestamp << "] " << buffer << endl;
            logfile.flush();
        }
        cout << "Получено сообщение: " << buffer << endl;
    }

    CloseHandle(hPipe);
}

int main()
{
    logfile.open("server.log", ios::out);
    if (!logfile.is_open())
    {
        cerr << "Ошибка при открытии файла журнала." << endl;
        return 1;
    }

    HANDLE hPipe;
    vector<thread> client_threads;

    cout << "Сервер ожидает подключения клиентов..." << endl;

    while (running)
    {
        hPipe = CreateNamedPipeA(
            PIPE_NAME,
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
            PIPE_UNLIMITED_INSTANCES,
            1024, 1024,
            0,
            NULL);

        if (hPipe == INVALID_HANDLE_VALUE)
        {
            cerr << "Ошибка при создании именованного канала: " << GetLastError() << endl;
            return 1;
        }

        BOOL connected = ConnectNamedPipe(hPipe, NULL) ? TRUE : (GetLastError() == ERROR_PIPE_CONNECTED);
        if (connected)
        {
            client_threads.emplace_back(HandleClient, hPipe);
        }
        else
        {
            CloseHandle(hPipe);
        }
    }

    for (auto &t : client_threads)
    {
        if (t.joinable())
        {
            t.join();
        }
    }

    logfile.close();
    return 0;
}
