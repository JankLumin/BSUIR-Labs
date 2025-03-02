
#ifndef TRACEROUTE_FUNCIONS_H
#define TRACEROUTE_FUNCIONS_H

#include <iostream>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/time.h>
#include <stdexcept>
#include <getopt.h>

#define PACKET_SIZE 4096
#define MAX_HOPS 30
#define TIMEOUT_SEC 1

bool isValidTTL(const std::string& ttl_str);
int createSocket(int protocol);
void printHelp(const char *programName);
void traceRoute(int fd, const struct sockaddr_in& addr, int first_ttl, int max_ttl);
bool parseCommandLine(int argc, char *argv[], int& first_ttl, int& max_ttl, std::string& destination_host);
bool resolveHostname(const std::string& hostname, struct in_addr& address);
unsigned short checksum(void *b, int len);
long long currentTimeMicroseconds();

#endif
