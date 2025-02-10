#include "variable.h"
#include <random>

// TODO add variable functions

using namespace mathematics;

namespace random {

    value variable::operator * () {
        large_int cap = large_int(-1UL) * -1UL + -1UL + -1UL;
        large_int bottom(0ul);
        large_int roll = large_int::random(bottom, cap);
        probability prob(roll, cap), aggregate(0, 1);
        for (auto& ref: data) {
            for (auto& ref2: ref.second)
                aggregate = aggregate + ref2.chance;
            if (aggregate > prob)
                return ref.first;
        }
        return value();
    }

    probability variable::chance(value a) {
        probability res = probability::zero;
        if (data.find(a) == data.end()) {
            return res;
        }
        auto v = data[a];
        for (auto& ref: v)
            res = res + ref.chance;
        return res;
    }

    variable variable::ternary(const variable* a, const variable* b) {
        variable res = *a;
        probability t = chance(value(true)), f = chance(value(false)), s = f + t;
        if (t == probability::zero) {
            res = *b;
            return res;
        }
        if (f == probability::zero)
            return res;
        t = t / s;
        f = f / s;
        // TODO complete this function
    }
}