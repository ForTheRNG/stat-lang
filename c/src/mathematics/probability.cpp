#include "probability.h"

namespace mathematics {  

    const probability probability::zero = probability();
    const probability probability::one = probability(1, 1);

    bool probability::operator!() {
        sign = !sign;
        return sign;
    }

    probability::probability(const large_int& _numerator, const large_int& _denominator, bool _sign) {
        numerator = _numerator;
        denominator = _denominator;
        sign = _sign;
    }

    probability::probability(double f) : probability() {
    }

    probability::probability(const probability& other) {
        sign = other.sign;
        numerator = other.numerator;
        denominator = other.denominator;
    }

    probability probability::operator+(const probability& other) {
        large_int t1 = numerator * other.denominator;
        large_int t2 = denominator * other.numerator;
        large_int d = denominator * other.denominator;
        return sign ?
            other.sign ?
                probability(t1 + t2, d) :
                t1 > t2 ?
                    probability(t1 - t2, d) :
                    probability(t2 - t1, d, false) :
            other.sign ?
                t1 > t2 ?
                    probability(t1 - t2, d, false) :
                    probability(t2 - t1, d):
                probability(t1 + t2, d, false);
    }

    probability probability::operator-(const probability& other) {
        !*this;
        probability res = *this + other;
        !*this;
        !res;
        return res;
    }

    probability probability::operator*(const probability& other) {
        large_int a = numerator * other.numerator;
        large_int b = denominator * other.denominator;
        large_int g = a.gcd(b);
        return probability(a / g, b / g, (!sign || !other.sign) && (sign || other.sign));
    }

    probability probability::operator/(const probability& other) {
        large_int a = numerator * other.denominator;
        large_int b = denominator * other.numerator;
        large_int g = a.gcd(b);
        return probability(a / g, b / g, (!sign || !other.sign) && (sign || other.sign));
    }

    probability probability::operator%(const probability& other) {
        return probability(probability::zero);
    }

    probability probability::random(const probability& low, const probability& high) {
        probability _high = high;
        probability top = _high - low;
        large_int bottom = large_int();
        return probability(large_int::random(bottom, top.numerator), top.denominator) + low;
    }

    // TODO add logical operators
}