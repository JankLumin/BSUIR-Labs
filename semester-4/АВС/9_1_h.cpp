#include <iostream>
#include "conio.h"

int main()
{
    setlocale(LC_ALL, "");
    __int8 A[8] = { 1, 2, 3, 4, 5, 6, 7, 8 };
    __int8 B[8] = { 9, 10, 11, 12, 13, 14, 15, 16 };
    __int8 C[8] = { 17, 18, 19, 20, 21, 22, 23, 24 };
    __int16 D[8] = { 25, 2, 7, 8, 10, 6, 11, 12 };

    __int16 F[8] = { 0 };

    __asm {
        
        movq mm0, [A]
        movq mm1, [B]
        movq mm2, [C]
        movq mm3, [D]           // Загружаем значения из массивов A, B, C и D в регистры MMX

        punpcklbw mm4, mm0      // Нижние 4 байта A в mm4
        punpckhbw mm5, mm0      // Верхние 4 байта A в mm5                     

        punpcklbw mm6, mm1      // Нижние 4 байта B в mm6                     
        punpckhbw mm7, mm1      // Верхние 4 байта B в mm7                   

        pxor mm0, mm0
        pxor mm1, mm1           // Отчистка

        punpcklbw mm0, mm2      // Нижние 4 байта C в mm0
        punpckhbw mm1, mm2      // Верхние 4 байта C в mm1 

        pxor mm2, mm2
        movq mm2, [D + 8]       // Отчистка и запись 8 байт регистра D в mm2

        psrlw mm0, 8
        psrlw mm1, 8            // Старший байт в младший

        paddsw mm4, mm6         // A + B

        pxor mm6, mm6
        movq mm6, mm4           // A + B
                                
        pmullw mm4, mm0         // Нижние 4
        pmulhw mm6, mm0         // Верхние 4        
                                // (A + B) * C
                                    
        psllw mm6, 12
        psrlw mm4, 4            // Форматирование

        paddsw mm6, mm4
        psrlw mm6, 4            // Старший байт в младший

        paddsw mm6, mm3         // (A + B) * C + D нижние 4

        movq[F], mm6            // Сохранение в F
                                
        paddsw mm5, mm7
        pxor mm7, mm7
        movq mm7, mm5           // A + B

        pmullw mm7, mm1
        pmulhw mm5, mm1         // (A + B) * C

        psllw mm5, 12
        psrlw mm7, 4            // Форматирование

        paddsw mm7, mm5
        psrlw mm7, 4            // Старший байт в младший

        paddsw mm7, mm2         // (A + B) * C + D

        movq[F + 8], mm7        // Сохранение в F
    }

    std::cout << "Результаты вычислений F[i]: ";
    for (int i = 0; i < 8; ++i) {
        std::cout << F[i] << " ";
    }
    std::cout << std::endl;

    _getch();
    return 0;
}