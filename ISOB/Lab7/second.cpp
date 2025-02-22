#include <bits/stdc++.h>
#include <winsock2.h>
#include <iphlpapi.h>
#include <ws2tcpip.h>
#include <icmpapi.h>
#pragma comment(lib, "Ws2_32.lib")
#pragma comment(lib, "Iphlpapi.lib")
#pragma comment(lib, "Icmp.lib")
#define a1 32
#define a2 30
#define a3 1000
#define a4 long long
#define a5 std
#define a6 chrono
#define a7 "Error resolving destination host."
#define a8 "Usage: "
#define a9 "First hop value must be in the range 1-255."
#define a10 "Max TTL value must be in the range 1-255."
#define a11 "Missing destination_host."
#define a12 "Max TTL value must be greater than or equal to first TTL value."
#define a13 "Unable to open ICMP handle: "
#define a14 "Reached destination"
#define a15 "Tracing route to "
#define a16 "ms"
#define a17 "* "
#define a18 "  "
#define a19 1
#define a20 255
using namespace a5;
using namespace a6;
bool a21(const string &a22)
{
    try
    {
        size_t a23 = 0;
        a4 a24 = stoi(a22, &a23);
        if (a23 != a22.size())
            return false;
        return (a24 >= a19 && a24 <= a20);
    }
    catch (const invalid_argument &a25)
    {
        return false;
    }
}
void a26(const char *a27) { cerr << a8 << a27 << " [-f first_ttl] [-m max_ttl] <destination_host>" << endl
                                 << "Options:" << endl
                                 << "  -f, --first-ttl=VALUE  Start from the first_ttl hop (instead from 1)" << endl
                                 << "  -m, --max-ttl=VALUE    Set the max number of hops (max TTL to be reached). Default is " << a2 << endl
                                 << "  -h, --help             Read this help and exit" << endl; }
bool a28(a4 a29, char *a30[], a4 &a31, a4 &a32, string &a33)
{
    for (a4 a34 = a19; a34 < a29; ++a34)
    {
        if (strcmp(a30[a34], "-f") == 0 && a34 + a19 < a29)
        {
            if (!a21(a30[a34 + a19]))
            {
                cerr << a9 << endl;
                return false;
            }
            a31 = stoi(a30[++a34]);
        }
        else if (strcmp(a30[a34], "-m") == 0 && a34 + a19 < a29)
        {
            if (!a21(a30[a34 + a19]))
            {
                cerr << a10 << endl;
                return false;
            }
            a32 = stoi(a30[++a34]);
        }
        else if (strcmp(a30[a34], "-h") == 0 || strcmp(a30[a34], "--help") == 0)
        {
            a26(a30[0]);
            return false;
        }
        else
        {
            a33 = a30[a34];
        }
    }
    if (a33.empty())
    {
        cerr << a11 << endl;
        a26(a30[0]);
        return false;
    }
    if (a32 < a31)
    {
        cerr << a12 << endl;
        return false;
    }
    return true;
}
bool a35(const string &a36, struct sockaddr_in &a37)
{
    struct addrinfo a38 = {0};
    struct addrinfo *a39 = nullptr;
    a38.ai_family = AF_INET;
    a38.ai_socktype = SOCK_RAW;
    a38.ai_protocol = IPPROTO_ICMP;
    if (getaddrinfo(a36.c_str(), nullptr, &a38, &a39) != 0)
    {
        cerr << a7 << endl;
        return false;
    }
    a37 = *reinterpret_cast<struct sockaddr_in *>(a39->ai_addr);
    freeaddrinfo(a39);
    return true;
}
void a40(const struct sockaddr_in &a41, a4 a42, a4 a43)
{
    HANDLE a44 = IcmpCreateFile();
    if (a44 == INVALID_HANDLE_VALUE)
    {
        cerr << a13 << GetLastError() << endl;
        return;
    }
    char a45[a1] = {0};
    DWORD a46 = sizeof(ICMP_ECHO_REPLY) + a1;
    char *a47 = new char[a46];
    for (a4 a48 = a42; a48 <= a43; ++a48)
    {
        cout << a48 << a18;
        for (a4 a49 = 0; a49 < 3; ++a49)
        {
            IP_OPTION_INFORMATION a50 = {0};
            a50.Ttl = a48;
            DWORD a51 = IcmpSendEcho(a44, a41.sin_addr.S_un.S_addr, a45, sizeof(a45), &a50, a47, a46, a3);
            if (a51 != 0)
            {
                PICMP_ECHO_REPLY a52 = reinterpret_cast<PICMP_ECHO_REPLY>(a47);
                struct in_addr a53;
                a53.S_un.S_addr = a52->Address;
                cout << inet_ntoa(a53) << " (" << a52->RoundTripTime << " " << a16 << ") ";
                if (a52->Status == IP_SUCCESS && a52->Address == a41.sin_addr.S_un.S_addr)
                {
                    cout << a14 << endl;
                    delete[] a47;
                    IcmpCloseHandle(a44);
                    return;
                }
            }
            else
            {
                cout << a17;
            }
            this_thread::sleep_for(milliseconds(500));
        }
        cout << endl;
    }
    delete[] a47;
    IcmpCloseHandle(a44);
}
int main(int a29, char *a30[])
{
    a4 a54 = a19;
    a4 a55 = a2;
    string a56;
    if (!a28(a29, a30, a54, a55, a56))
    {
        return 1;
    }
    WSADATA a57;
    if (WSAStartup(MAKEWORD(2, 2), &a57) != 0)
    {
        cerr << "WSAStartup failed." << endl;
        return 1;
    }
    struct sockaddr_in a58;
    if (!a35(a56, a58))
    {
        WSACleanup();
        return 1;
    }
    cout << a15 << a56 << " [" << inet_ntoa(a58.sin_addr) << "]" << endl;
    a40(a58, a54, a55);
    WSACleanup();
    return 0;
}
