#include "funcions.h"

int main(int argc, char *argv[]) {
    int first_ttl = 1;
    int max_ttl = MAX_HOPS;
    std::string destination_host;

    struct sockaddr_in addr{};

    if (argc == 1 || (argc == 2 && std::string(argv[1]) == "--help")) {
        printHelp(argv[0]);
        return 0;
    }

    if (!parseCommandLine(argc, argv, first_ttl, max_ttl, destination_host)) {
        return 1;
    }

    struct in_addr dest_addr{};
    if (!resolveHostname(destination_host, dest_addr)) {
        return 1;
    }

    int fd;
    fd = createSocket(IPPROTO_ICMP);

    std::memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr = dest_addr;

    std::cout << "Tracing route to " << inet_ntoa(addr.sin_addr) << std::endl;

    traceRoute(fd, addr, first_ttl, max_ttl);

    close(fd);

    return 0;
}