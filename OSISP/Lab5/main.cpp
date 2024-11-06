#include <bits/stdc++.h>
#include <winsock2.h>
#include <iphlpapi.h>
#include <ws2tcpip.h>
#include <icmpapi.h>
#pragma comment(lib, "Ws2_32.lib")
#pragma comment(lib, "Iphlpapi.lib")
#pragma comment(lib, "Icmp.lib")

#define PACKET_SIZE 32
#define MAX_HOPS 30
#define TIMEOUT_SEC 1000

#define ll long long

using namespace std;
using namespace chrono;

bool isValidTTL(const string &ttl_str)
{
    try
    {
        size_t pos = 0;
        ll ttl_value = stoi(ttl_str, &pos);
        if (pos != ttl_str.size())
        {
            return false;
        }
        return (ttl_value >= 1 and ttl_value <= 255);
    }
    catch (const invalid_argument &e)
    {
        return false;
    }
}

void printHelp(const char *programName)
{
    cerr << "Usage: " << programName << " [-f first_ttl] [-m max_ttl] <destination_host>" << endl;
    cerr << "Options:" << endl;
    cerr << "  -f, --first-ttl=VALUE  Start from the first_ttl hop (instead from 1)" << endl;
    cerr << "  -m, --max-ttl=VALUE    Set the max number of hops (max TTL to be reached). Default is 30" << endl;
    ;
    cerr << "  -h, --help             Read this help and exit" << endl;
}

bool parseCommandLine(ll argc, char *argv[], ll &first_ttl, ll &max_ttl, string &destination_host)
{
    for (ll i = 1; i < argc; ++i)
    {
        if (strcmp(argv[i], "-f") == 0 and i + 1 < argc)
        {
            if (!isValidTTL(argv[i + 1]))
            {
                cerr << "First hop value must be in the range 1-255." << endl;
                return false;
            }
            first_ttl = stoi(argv[++i]);
        }
        else if (strcmp(argv[i], "-m") == 0 and i + 1 < argc)
        {
            if (!isValidTTL(argv[i + 1]))
            {
                cerr << "Max TTL value must be in the range 1-255." << endl;
                return false;
            }
            max_ttl = stoi(argv[++i]);
        }
        else if (strcmp(argv[i], "-h") == 0 or strcmp(argv[i], "--help") == 0)
        {
            printHelp(argv[0]);
            return false;
        }
        else
        {
            destination_host = argv[i];
        }
    }

    if (destination_host.empty())
    {
        cerr << "Missing destination_host." << endl;
        printHelp(argv[0]);
        return false;
    }

    if (max_ttl < first_ttl)
    {
        cerr << "Max TTL value must be greater than or equal to first TTL value." << endl;
        return false;
    }

    return true;
}

bool resolveHostname(const string &hostname, struct sockaddr_in &address)
{
    struct addrinfo hints = {0};
    struct addrinfo *result = nullptr;

    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_RAW;
    hints.ai_protocol = IPPROTO_ICMP;

    if (getaddrinfo(hostname.c_str(), nullptr, &hints, &result) != 0)
    {
        cerr << "Error resolving destination host." << endl;
        return false;
    }

    address = *reinterpret_cast<struct sockaddr_in *>(result->ai_addr);
    freeaddrinfo(result);
    return true;
}

void traceRoute(const struct sockaddr_in &addr, ll first_ttl, ll max_ttl)
{
    HANDLE icmpHandle = IcmpCreateFile();
    if (icmpHandle == INVALID_HANDLE_VALUE)
    {
        cerr << "Unable to open ICMP handle: " << GetLastError() << endl;
        return;
    }

    char sendData[PACKET_SIZE] = {0};
    DWORD replySize = sizeof(ICMP_ECHO_REPLY) + PACKET_SIZE;
    char *replyBuffer = new char[replySize];

    for (ll ttl = first_ttl; ttl <= max_ttl; ++ttl)
    {
        cout << ttl << " ";
        for (ll i = 0; i < 3; ++i)
        {
            IP_OPTION_INFORMATION optionInfo = {0};
            optionInfo.Ttl = ttl;

            DWORD result = IcmpSendEcho(icmpHandle, addr.sin_addr.S_un.S_addr, sendData, sizeof(sendData), &optionInfo, replyBuffer, replySize, TIMEOUT_SEC);
            if (result != 0)
            {
                PICMP_ECHO_REPLY echoReply = reinterpret_cast<PICMP_ECHO_REPLY>(replyBuffer);
                struct in_addr replyAddr;
                replyAddr.S_un.S_addr = echoReply->Address;
                cout << inet_ntoa(replyAddr) << " (" << echoReply->RoundTripTime << " ms) ";

                if (echoReply->Status == IP_SUCCESS and echoReply->Address == addr.sin_addr.S_un.S_addr)
                {
                    cout << "Reached destination" << endl;
                    delete[] replyBuffer;
                    IcmpCloseHandle(icmpHandle);
                    return;
                }
            }
            else
            {
                cout << "* ";
            }

            this_thread::sleep_for(milliseconds(500));
        }
        cout << endl;
    }

    delete[] replyBuffer;
    IcmpCloseHandle(icmpHandle);
}

int main(int argc, char *argv[])
{
    ll first_ttl = 1;
    ll max_ttl = MAX_HOPS;
    string destination_host;

    if (!parseCommandLine(argc, argv, first_ttl, max_ttl, destination_host))
    {
        return 1;
    }

    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
    {
        cerr << "WSAStartup failed." << endl;
        return 1;
    }

    struct sockaddr_in dest_addr;
    if (!resolveHostname(destination_host, dest_addr))
    {
        WSACleanup();
        return 1;
    }

    cout << "Tracing route to " << destination_host << " [" << inet_ntoa(dest_addr.sin_addr) << "]" << endl;

    traceRoute(dest_addr, first_ttl, max_ttl);

    WSACleanup();
    return 0;
}
// g++ -std=c++17 -finput-charset=UTF-8 main.cpp -o build/main -lws2_32 -liphlpapi -licmp