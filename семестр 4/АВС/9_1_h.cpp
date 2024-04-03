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
        movq mm3, [D]           // ��������� �������� �� �������� A, B, C � D � �������� MMX

        punpcklbw mm4, mm0      // ������ 4 ����� A � mm4
        punpckhbw mm5, mm0      // ������� 4 ����� A � mm5                     

        punpcklbw mm6, mm1      // ������ 4 ����� B � mm6                     
        punpckhbw mm7, mm1      // ������� 4 ����� B � mm7                   

        pxor mm0, mm0
        pxor mm1, mm1           // ��������

        punpcklbw mm0, mm2      // ������ 4 ����� C � mm0
        punpckhbw mm1, mm2      // ������� 4 ����� C � mm1 

        pxor mm2, mm2
        movq mm2, [D + 8]       // �������� � ������ 8 ���� �������� D � mm2

        psrlw mm0, 8
        psrlw mm1, 8            // ������� ���� � �������

        paddsw mm4, mm6         // A + B

        pxor mm6, mm6
        movq mm6, mm4           // A + B
                                
        pmullw mm4, mm0         // ������ 4
        pmulhw mm6, mm0         // ������� 4        
                                // (A + B) * C
                                    
        psllw mm6, 12
        psrlw mm4, 4            // ��������������

        paddsw mm6, mm4
        psrlw mm6, 4            // ������� ���� � �������

        paddsw mm6, mm3         // (A + B) * C + D ������ 4

        movq[F], mm6            // ���������� � F
                                
        paddsw mm5, mm7
        pxor mm7, mm7
        movq mm7, mm5           // A + B

        pmullw mm7, mm1
        pmulhw mm5, mm1         // (A + B) * C

        psllw mm5, 12
        psrlw mm7, 4            // ��������������

        paddsw mm7, mm5
        psrlw mm7, 4            // ������� ���� � �������

        paddsw mm7, mm2         // (A + B) * C + D

        movq[F + 8], mm7        // ���������� � F
    }

    std::cout << "���������� ���������� F[i]: ";
    for (int i = 0; i < 8; ++i) {
        std::cout << F[i] << " ";
    }
    std::cout << std::endl;

    _getch();
    return 0;
}