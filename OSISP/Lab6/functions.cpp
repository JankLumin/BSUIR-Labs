#include <netinet/tcp.h>
#include "funcions.h"

bool isValidTTL(const std::string& ttl_str) {
    try {
        size_t pos = 0;
        int ttl_value = std::stoi(ttl_str, &pos);
        if (pos != ttl_str.size()) {
            return false;
        }
        return (ttl_value >= 1 && ttl_value <= 255);
    } catch (const std::invalid_argument& e) {
        return false;
    }
}


void printHelp(const char *programName) {
    std::cerr << "Usage: sudo " << programName << " [-f first_ttl] [-m max_ttl] <destination_host>\n";
    std::cerr << "Options:\n";
    std::cerr << "  -f, --first-ttl=VALUE  Start from the first_ttl hop (instead from 1)\n";
    std::cerr << "  -m, --max-ttl=VALUE    Set the max number of hops (max TTL to be reached). Default is 30\n";
    std::cerr << "  -h, --help             Read this help and exit\n";
}

int createSocket(int protocol) {
    int sock;
    if ((sock = socket(AF_INET, SOCK_RAW, protocol)) < 0) {
        exit(EXIT_FAILURE);
    }
    return sock;
}

bool parseCommandLine(int argc, char *argv[], int& first_ttl, int& max_ttl, std::string& destination_host) {
    struct option long_options[] = {
            {"first-ttl", required_argument, nullptr, 'f'},
            {"max-ttl", required_argument, nullptr, 'm'},
            {"help", no_argument, nullptr, 'h'},
            {nullptr, 0, nullptr, 0}
    };

    int opt;
    while ((opt = getopt_long(argc, argv, "f:m:h", long_options, nullptr)) != -1) {
        switch (opt) {
            case 'f':
                if (!isValidTTL(optarg)) {
                    std::cerr << "First hop value must be in the range 1-255.\n";
                    return false;
                }
                first_ttl = std::stoi(optarg);
                break;
            case 'm':
                if (!isValidTTL(optarg)) {
                    std::cerr << "Max TTL value must be in the range 1-255.\n";
                    return false;
                }
                max_ttl = std::stoi(optarg);
                break;
            case 'h':
                printHelp(argv[0]);
                return false;
            case '?':
                std::cerr << "Unknown option character '" << static_cast<char>(optopt) << "'.\n";
                printHelp(argv[0]);
                return false;
            default:
                abort();
        }
    }

    if (optind >= argc) {
        std::cerr << "Missing destination_host.\n";
        printHelp(argv[0]);
        return false;
    }

    destination_host = argv[optind];

    if (max_ttl < first_ttl) {
        std::cerr << "Max TTL value must be greater than or equal to first TTL value.\n";
        return false;
    }

    return true;
}

bool resolveHostname(const std::string& hostname, struct in_addr& address) {
    struct hostent *host = gethostbyname(hostname.c_str());
    if (host == nullptr) {
        if (h_errno == TRY_AGAIN) {
            std::cerr << "Temporary failure in name resolution. Please try again later.\n";
        } else {
            std::cerr << "Error resolving destination host.\n";
        }
        return false;
    }
    std::memcpy(&address, host->h_addr_list[0], sizeof(struct in_addr));
    return true;
}

unsigned short checksum(void *b, int len) {
    auto *buf = reinterpret_cast<unsigned short *>(b);
    unsigned int sum;
    unsigned short result;

    for (sum = 0; len > 1; len -= 2)
        sum += *buf++;

    if (len == 1)
        sum += *(reinterpret_cast<unsigned char *>(buf));

    sum = (sum >> 16) + (sum & 0xFFFF);
    sum += (sum >> 16);
    result = ~sum;
    return result;
}

long long currentTimeMicroseconds() {
    struct timeval tv{};
    if (gettimeofday(&tv, nullptr) == -1) {
        perror("geotargetting");
        return -1;
    }
    return static_cast<long long>(tv.tv_sec) * 1000000LL + static_cast<long long>(tv.tv_usec);
}

void traceRoute(int fd, const struct sockaddr_in& addr, int first_ttl, int max_ttl)
{
    fd_set read_set;
    struct timeval timeout{};
    struct icmphdr icmp_packet{};
    char packet[PACKET_SIZE];
    int ttl;
    bool reachedDestination = false;

    for (ttl = first_ttl; ttl <= max_ttl && !reachedDestination; ++ttl) {
        std::cout << ttl << " ";
        for (int i = 0; i < 3; ++i) {
            if (setsockopt(fd, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl)) < 0) {
                perror("SocketRocket");
                return;
            }
            long long sendTime = currentTimeMicroseconds();
            if (sendTime == -1) {
                return;
            }
            std::memset(&icmp_packet, 0, sizeof(icmp_packet));
            icmp_packet.type = ICMP_ECHO;
            icmp_packet.code = 0;
            icmp_packet.un.echo.id = getpid();
            icmp_packet.un.echo.sequence = ttl;
            icmp_packet.checksum = checksum(&icmp_packet, sizeof(icmp_packet));

            std::memcpy(packet, &icmp_packet, sizeof(icmp_packet));

            if (sendto(fd, packet, sizeof(icmp_packet), 0, reinterpret_cast<const struct sockaddr *>(&addr),
                       sizeof(addr)) <= 0) {
                perror("sendto");
                return;
            }

            FD_ZERO(&read_set);
            FD_SET(fd, &read_set);
            timeout.tv_sec = TIMEOUT_SEC;
            timeout.tv_usec = 0;
            if (select(fd + 1, &read_set, nullptr, nullptr, &timeout) > 0) {
                char reply[PACKET_SIZE];
                struct sockaddr_in in{};
                socklen_t addr_len = sizeof(in);
                ssize_t bytes_received = recvfrom(fd, reply, sizeof(reply), 0,
                                                  reinterpret_cast<struct sockaddr *>(&in), &addr_len);
                if (bytes_received < 0) {
                    perror("therefrom");
                    return;
                }
                std::cout << inet_ntoa(in.sin_addr) << " ";

                struct hostent *host_info = gethostbyaddr(&in.sin_addr, sizeof(in.sin_addr), AF_INET);
                if (host_info != nullptr) {
                    std::cout << " (" << host_info->h_name << ")";
                }

                if (in.sin_addr.s_addr == addr.sin_addr.s_addr) {
                    reachedDestination = true;
                }
            } else {
                std::cout << "* ";
            }
            long long receiveTime = currentTimeMicroseconds();
            if (receiveTime == -1) {
                return;
            }
            std::cout << " Time: " << static_cast<long double>(receiveTime - sendTime) / 1000.0 << " ms ";
        }
        std::cout << std::endl;
    }
}