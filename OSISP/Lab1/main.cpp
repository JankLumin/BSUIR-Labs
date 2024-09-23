#include <bits/stdc++.h>
#include <windows.h>

#define ll long long
#define ld long double
#define vi vector<ll>
#define vd vector<ld>
#define vvi vector<vector<ll>>
#define vvd vector<vector<ld>>

using namespace std;
using namespace chrono;

CRITICAL_SECTION coutCS;

HANDLE hConsole;
const ll numThreads = 6;

ll threadPriorities[numThreads] = {
    THREAD_PRIORITY_TIME_CRITICAL,
    THREAD_PRIORITY_HIGHEST,
    THREAD_PRIORITY_NORMAL,
    THREAD_PRIORITY_BELOW_NORMAL,
    THREAD_PRIORITY_LOWEST,
    THREAD_PRIORITY_IDLE};

string priorityNames[numThreads] = {
    "TIME_CRITICAL",
    "HIGHEST",
    "NORMAL",
    "BELOW NORMAL",
    "LOWEST",
    "IDLE"};

WORD threadColors[numThreads] = {
    FOREGROUND_RED | FOREGROUND_BLUE | FOREGROUND_INTENSITY,
    FOREGROUND_RED | FOREGROUND_INTENSITY,
    FOREGROUND_GREEN | FOREGROUND_INTENSITY,
    FOREGROUND_BLUE | FOREGROUND_INTENSITY,
    FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY,
    FOREGROUND_GREEN};

void UpdateProgressBar(ll index, ll progress)
{
    EnterCriticalSection(&coutCS);

    SetConsoleTextAttribute(hConsole, threadColors[index]);

    COORD cursorPosition;
    cursorPosition.X = 0;
    cursorPosition.Y = (SHORT)(index);
    SetConsoleCursorPosition(hConsole, cursorPosition);

    string progressBar = "Поток " + to_string(index + 1) + " прогресс: [";
    ll barWidth = 50;
    ll pos = barWidth * progress / 100;
    for (ll i = 0; i < barWidth; ++i)
    {
        if (i < pos)
            progressBar += "=";
        else
            progressBar += " ";
    }
    progressBar += "] " + to_string(progress) + "%";

    cout << progressBar;

    SetConsoleTextAttribute(hConsole, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);

    LeaveCriticalSection(&coutCS);
}

void MultiplyMatrices(const vvd &A, const vvd &B, vvd &C, ll threadIndex)
{
    ll N = A.size();
    for (ll i = 0; i < N; ++i)
    {
        for (ll j = 0; j < N; ++j)
        {
            C[i][j] = 0;
            for (ll k = 0; k < N; ++k)
            {
                C[i][j] += A[i][k] * B[k][j];
            }
        }

        ll progress = (100 * (i + 1)) / N;
        if (progress > 100)
            progress = 100;
        UpdateProgressBar(threadIndex, progress);
    }
}

DWORD WINAPI ThreadFunction(LPVOID lpParam)
{
    ll threadIndex = *(ll *)lpParam;
    SetThreadPriority(GetCurrentThread(), threadPriorities[threadIndex]);

    auto startTime = high_resolution_clock::now();

    vvd A(500, vector<ld>(500, 1.0));
    vvd B(500, vector<ld>(500, 1.0));
    vvd C(500, vector<ld>(500, 0.0));

    MultiplyMatrices(A, B, C, threadIndex);

    auto endTime = high_resolution_clock::now();
    duration<ld> elapsed = endTime - startTime;

    EnterCriticalSection(&coutCS);

    SetConsoleTextAttribute(hConsole, threadColors[threadIndex]);

    COORD cursorPosition;
    cursorPosition.X = 0;
    cursorPosition.Y = (SHORT)(numThreads + threadIndex);
    SetConsoleCursorPosition(hConsole, cursorPosition);

    cout << "Поток " << threadIndex + 1 << " с приоритетом " << priorityNames[threadIndex]
         << " завершен за " << elapsed.count() << " секунд." << endl;

    SetConsoleTextAttribute(hConsole, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);

    LeaveCriticalSection(&coutCS);

    return 0;
}

int main()
{
    InitializeCriticalSection(&coutCS);
    hConsole = GetStdHandle(STD_OUTPUT_HANDLE);

    system("cls");

    HANDLE hThreads[numThreads];
    DWORD threadIDs[numThreads];
    ll threadIndices[numThreads];

    for (ll i = 0; i < numThreads; ++i)
    {
        threadIndices[i] = i;
        hThreads[i] = CreateThread(NULL, 0, ThreadFunction, &threadIndices[i], 0, &threadIDs[i]);
    }

    WaitForMultipleObjects(numThreads, hThreads, TRUE, INFINITE);

    for (ll i = 0; i < numThreads; ++i)
    {
        CloseHandle(hThreads[i]);
    }

    DeleteCriticalSection(&coutCS);

    COORD cursorPosition;
    cursorPosition.X = 0;
    cursorPosition.Y = (SHORT)(12);
    SetConsoleCursorPosition(hConsole, cursorPosition);
    cout << "Все потоки завершены." << endl;
    return 0;
}
