#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUFFER_SIZE 16

void vulnerableFunction(const char *input)
{
    char buffer[BUFFER_SIZE];
    strcpy(buffer, input);
    printf("Содержимое буфера (уязвимый режим): %s\n", buffer);
}

void safeFunction(const char *input)
{
    char buffer[BUFFER_SIZE];
    strncpy(buffer, input, BUFFER_SIZE - 1);
    buffer[BUFFER_SIZE - 1] = '\0';
    printf("Содержимое буфера (защищённый режим): %s\n", buffer);
}

int main()
{
    char mode;
    char attackInput[128];

    printf("Выберите режим:\n");
    printf("  p - защищённый режим\n");
    printf("  u - уязвимый режим\n");
    printf("Ваш выбор: ");
    scanf(" %c", &mode);
    getchar();

    printf("Введите строку для имитации атаки: ");
    fgets(attackInput, sizeof(attackInput), stdin);
    attackInput[strcspn(attackInput, "\n")] = '\0';

    if (mode == 'p' || mode == 'P')
    {
        safeFunction(attackInput);
    }
    else if (mode == 'u' || mode == 'U')
    {
        vulnerableFunction(attackInput);
    }
    else
    {
        printf("Неверный выбор режима.\n");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
