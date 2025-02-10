#ifndef OPERATOR_H
#define OPERATOR_H

#include "random/rollable.h"
#include "random/variable.h"
#include <stdexcept>

namespace random {
    class validable {
    protected:
        virtual void check(int code = -1) = 0;
    };

    template<value::types coercion, class operation> class binary_operator: public rollable<value, variable>, public validable {
    protected:
        rollable<value, variable>* a;
        rollable<value, variable>* b;

        void check(int code = -1);
    };

    class ternary_operator: public rollable<value, variable>, public validable {
    private:
        rollable<value, variable> *c, *a, *b;
    protected:
        void check(int _ignored = -1);
    };

    // TODO add functions
}

#endif