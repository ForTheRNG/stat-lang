#ifndef NUMERIC_OPERATOR_H
#define NUMERIC_OPERATOR_H

#include "random/operator.h"
#include "random/variable.h"

#define _num_oper_classes x(addition, +) x(subtraction, -) x(multiplication, *) x(division, /) x(modulo, %)

namespace random {
    #define x(class_name, oper) class class_name: binary_operator<value::number, class_name> {\
        value operator * () { \
            value v; \
            check(); \
            v.type = value::number; \
            v.data.i = (**a).data.i oper (**b).data.i; \
            return v; \
        } \
        variable operator () () { return (*a)() oper (*b)(); } \
    };
    _num_oper_classes
    #undef x

    // TODO add ternary operator
}

#undef _num_oper_classes

#endif