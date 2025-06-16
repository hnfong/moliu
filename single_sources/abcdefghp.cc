#include <stdio.h>
#include <iostream>

int main() {
    int a, b, c, d, e, f, g, h, p = 1;
    for (int i = 0; i < 100000000; i++) {
        a = i / 1 % 10;
        b = i / 10 % 10;
        c = i / 100 % 10;
        d = i / 1000 % 10;
        e = i / 10000 % 10;
        f = i / 100000 % 10;
        g = i / 1000000 % 10;
        h = i / 10000000 % 10;
        if (
                ((a * 10 + b) - (c * 10 + d) + (g * 10 + h) == p * 111) && ((a * 10 + b) - (c * 10 + d) == (e * 10 + f)) && (a != 0 && c != 0 && e != 0 && g != 0) &&
                (a == a && a != b && a != c && a != d && a != e && a != f && a != g && a != h && a != p) &&
                (b != a && b == b && b != c && b != d && b != e && b != f && b != g && b != h && b != p) &&
                (c != a && c != b && c == c && c != d && c != e && c != f && c != g && c != h && c != p) &&
                (d != a && d != b && d != c && d == d && d != e && d != f && d != g && d != h && d != p) &&
                (e != a && e != b && e != c && e != d && e == e && e != f && e != g && e != h && e != p) &&
                (f != a && f != b && f != c && f != d && f != e && f == f && f != g && f != h && f != p) &&
                (g != a && g != b && g != c && g != d && g != e && g != f && g == g && g != h && g != p) &&
                (h != a && h != b && h != c && h != d && h != e && h != f && h != g && h == h && h != p) &&
                (p != a && p != b && p != c && p != d && p != e && p != f && p != g && p != h && p == p) &&
                1
                ) {
            printf("a=%d b=%d c=%d d=%d e=%d f=%d g=%d h=%d p=%d, %d - %d + %d = %d\n", a, b, c, d, e, f, g, h, p, (a*10+b), (c*10+d), (g*10+h), (p*111));
        }
    }
    return 0;
}
