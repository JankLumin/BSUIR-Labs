#include <windows.h>
#include <Lmcons.h>
#include <bits/stdc++.h>

#define vs vector<string>

using namespace std;

string GetOSVersion()
{
    OSVERSIONINFOEX osvi;
    ZeroMemory(&osvi, sizeof(OSVERSIONINFOEX));
    osvi.dwOSVersionInfoSize = sizeof(OSVERSIONINFOEX);
    if (!GetVersionEx((OSVERSIONINFO *)&osvi))
    {
        return "Не удалось определить версию ОС.";
    }

    string version = "Версия ОС: " + to_string(osvi.dwMajorVersion) + "." +
                     to_string(osvi.dwMinorVersion) + " (Build " +
                     to_string(osvi.dwBuildNumber) + ")";
    return version;
}

string GetCPUInfo()
{
    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);

    string cpuInfo = "Архитектура процессора: ";
    switch (sysInfo.wProcessorArchitecture)
    {
    case PROCESSOR_ARCHITECTURE_AMD64:
        cpuInfo += "x64";
        break;
    case PROCESSOR_ARCHITECTURE_INTEL:
        cpuInfo += "x86";
        break;
    case PROCESSOR_ARCHITECTURE_ARM:
        cpuInfo += "ARM";
        break;
    case PROCESSOR_ARCHITECTURE_ARM64:
        cpuInfo += "ARM64";
        break;
    default:
        cpuInfo += "Неизвестная архитектура";
        break;
    }

    cpuInfo += "\nКоличество логических процессоров: " + to_string(sysInfo.dwNumberOfProcessors);
    return cpuInfo;
}

string GetProcessorModel()
{
    HKEY hKey;
    const char *subKey = "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0";
    const char *valueName = "ProcessorNameString";

    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, subKey, 0, KEY_READ, &hKey) != ERROR_SUCCESS)
    {
        return "Не удалось открыть реестр для получения модели процессора.";
    }

    char processorName[256];
    DWORD bufferSize = sizeof(processorName);
    DWORD type = 0;

    if (RegQueryValueExA(hKey, valueName, NULL, &type, (LPBYTE)processorName, &bufferSize) != ERROR_SUCCESS or type != REG_SZ)
    {
        RegCloseKey(hKey);
        return "Не удалось получить модель процессора из реестра.";
    }

    RegCloseKey(hKey);
    return string("Модель процессора: ") + processorName;
}

string GetMemoryInfo()
{
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(MEMORYSTATUSEX);
    if (!GlobalMemoryStatusEx(&memInfo))
    {
        return "Не удалось получить информацию об оперативной памяти.";
    }

    DWORDLONG totalPhys = memInfo.ullTotalPhys / (1024 * 1024);
    DWORDLONG availPhys = memInfo.ullAvailPhys / (1024 * 1024);
    string memoryInfo = "Общая физическая память: " + to_string(totalPhys) + " МБ\n" +
                        "Доступная физическая память: " + to_string(availPhys) + " МБ";
    return memoryInfo;
}

string GetSystemDirectoryPath()
{
    char systemDir[MAX_PATH];
    UINT len = GetSystemDirectoryA(systemDir, MAX_PATH);
    if (len == 0 or len > MAX_PATH)
    {
        return "Не удалось получить системный каталог.";
    }
    return string("Системный каталог: ") + systemDir;
}

string GetCurrentUser()
{
    char username[UNLEN + 1];
    DWORD username_len = UNLEN + 1;
    if (GetUserNameA(username, &username_len))
    {
        return string("Текущий пользователь: ") + username;
    }
    return "Не удалось получить имя текущего пользователя.";
}

string GetComputerNameFromRegistry()
{
    HKEY hKey;
    const char *subKey = "SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ComputerName";
    const char *valueName = "ComputerName";

    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, subKey, 0, KEY_READ, &hKey) != ERROR_SUCCESS)
    {
        return "Не удалось открыть реестр для получения имени компьютера.";
    }

    char computerName[256];
    DWORD bufferSize = sizeof(computerName);
    DWORD type = 0;

    if (RegQueryValueExA(hKey, valueName, NULL, &type, (LPBYTE)computerName, &bufferSize) != ERROR_SUCCESS or type != REG_SZ)
    {
        RegCloseKey(hKey);
        return "Не удалось получить имя компьютера из реестра.";
    }

    RegCloseKey(hKey);
    return string("Имя компьютера: ") + computerName;
}

int main()
{
    vs systemInfo;
    systemInfo.push_back(GetOSVersion());
    systemInfo.push_back(GetCPUInfo());
    systemInfo.push_back(GetProcessorModel());
    systemInfo.push_back(GetMemoryInfo());
    systemInfo.push_back(GetSystemDirectoryPath());
    systemInfo.push_back(GetCurrentUser());
    systemInfo.push_back(GetComputerNameFromRegistry());

    ofstream outFile("system_info.txt");
    if (!outFile.is_open())
    {
        cerr << "Не удалось открыть файл для записи.\n";
        return 1;
    }

    for (const auto &info : systemInfo)
    {
        cout << info << endl
             << endl;
        outFile << info << endl
                << endl;
    }

    outFile.close();
    cout << "Информация успешно записана в файл 'system_info.txt'.\n";
    return 0;
}
