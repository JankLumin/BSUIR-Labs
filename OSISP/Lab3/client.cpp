#include <bits/stdc++.h>
#include <windows.h>

#define ll long long

using namespace std;

#define PIPE_NAME R"(\\.\pipe\LogPipe)"

void ClientThread(ll source_id)
{
    HANDLE hPipe;
    DWORD bytesWritten;

    while (true)
    {
        hPipe = CreateFileA(
            PIPE_NAME,
            GENERIC_WRITE,
            0,
            NULL,
            OPEN_EXISTING,
            0,
            NULL);

        if (hPipe != INVALID_HANDLE_VALUE)
        {
            break;
        }

        if (GetLastError() != ERROR_PIPE_BUSY)
        {
            cerr << "Клиент " << source_id << ": Не удалось подключиться к серверу." << endl;
            return;
        }

        if (!WaitNamedPipeA(PIPE_NAME, 1000))
        {
            cerr << "Клиент " << source_id << ": Сервер не отвечает." << endl;
            return;
        }
    }

    for (ll i = 0; i < 5; ++i)
    {
        string message = "Источник " + to_string(source_id) + ": Сообщение " + to_string(i + 1);
        BOOL result = WriteFile(
            hPipe,
            message.c_str(),
            static_cast<DWORD>(message.size()),
            &bytesWritten,
            NULL);

        if (!result)
        {
            cerr << "Клиент " << source_id << ": Ошибка при отправке сообщения." << endl;
        }
        else
        {
            cout << "Клиент " << source_id << " отправил сообщение: " << message << endl;
        }

        this_thread::sleep_for(chrono::milliseconds(100));
    }

    CloseHandle(hPipe);
}

int main()
{
    ll num_clients;
    cout << "Введите количество клиентов: ";
    cin >> num_clients;

    vector<thread> threads;

    for (ll i = 0; i < num_clients; ++i)
    {
        threads.emplace_back(ClientThread, i + 1);
    }

    for (auto &t : threads)
    {
        t.join();
    }

    return 0;
}
