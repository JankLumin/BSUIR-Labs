#include <iostream>
#include "conio.h"

int main()
{
    setlocale(LC_ALL, "");
    __int8 A[8] = { 1, 2, 3, 4, 5, 6, 7, 8 };
    __int8 B[8] = { 9, 10, 11, 12, 13, 14, 15, 16 };
    __int8 C[8] = { 17, 18, 19, 20, 21, 22, 23, 24 };
    __int16 D[8] = { 25, 1, 2, 3, 4, 5, 6, 7 };

    __int16 F[8] = { 0 };

    __asm {
        xorpd xmm0, xmm0
        xorpd xmm1, xmm1
        xorpd xmm2, xmm2
        xorpd xmm3, xmm3
        xorpd xmm4, xmm4
        xorpd xmm5, xmm5
        xorpd xmm6, xmm6       //�������� ���������

        movupd xmm4, [A]
        movupd xmm5, [B]
        movupd xmm6, [C]
        movupd xmm3, [D]        //��������� ������ � ��������������� ��������

        punpcklbw xmm0, xmm4
        punpcklbw xmm1, xmm5
        punpcklbw xmm2, xmm6     //���������� ������

        psrl xmm0, 8
        psrl xmm1, 8
        psrl xmm2, 8            //������� ����� � �������

        paddq xmm0, xmm1        //A + B

        pmullw xmm0, xmm2       //(A + B) * C

        paddq xmm0, xmm3        //(A + B) * C + D


        movupd[F], xmm0         //������ ������ � F
    }

    std::cout << "���������� ���������� F[i]: ";
    for (int i = 0; i < 8; ++i) {
        std::cout << F[i] << " ";
    }
    std::cout << std::endl;

    _getch();
    return 0;
}