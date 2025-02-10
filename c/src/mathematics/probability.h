#ifndef PROBABILITY_H
#define PROBABILITY_H

#include "mathematics/large_int.h"
#include "mathematics/arithmetic.h"

namespace mathematics {
    class probability: arithmetic<probability> {
    private:
        bool sign;
        large_int numerator;
        large_int denominator;
    public:
        probability(const large_int& numerator, const large_int& denominator, bool sign = true);
        probability() : probability(0, 1, true) {} ;
        probability(const probability& other);
        probability(double f);
        #define x(o) probability operator o (const probability& other);
        num_oper_list
        #undef x
        #define x(o) bool operator o (const probability& other);
        bool_oper_list
        #undef x
        // returns sign after flip
        bool operator!();
        static probability random(const probability& low, const probability& high);
        static const probability zero, one;
    };
}

#endif