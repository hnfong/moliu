#include <stdio.h>
#include <algorithm>
using namespace std;
int main() {
    int data[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    int &a = data[0], &b = data[1], &c = data[2], &d = data[3], &e = data[4], &f = data[5], &g = data[6], &h = data[7], &p = data[8];
    do {
        if ((a * 10 + b) - (c * 10 + d) + (g * 10 + h) == p * 111 && ((a * 10 + b) - (c * 10 + d) == (e * 10 + f)) && (a != 0 && c != 0 && e != 0 && g != 0)) {
            printf("a=%d b=%d c=%d d=%d e=%d f=%d g=%d h=%d p=%d, %d - %d + %d = %d\n", a, b, c, d, e, f, g, h, p, (a*10+b), (c*10+d), (g*10+h), (p*111));
        }
    } while (next_permutation(data, data+9));
    return 0;
}
