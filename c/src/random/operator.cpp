#include "operator.h"

namespace random {
    template<value::types coercion, class output> void binary_operator<coercion, output>::check(int code) {
        value v;
        switch (code) {
        case -1:
            v = **b;
            if (v.type != coercion) {
                throw new std::invalid_argument(std::string("Argument not of correct type; is ") +
                                                value::type_strings[v.type] +
                                                std::string(", should be ") +
                                                value::type_strings[coercion]);
            }
        case 0:
            v = **a;
            if (v.type != coercion) {
                throw new std::invalid_argument(std::string("Argument not of correct type; is ") +
                                                value::type_strings[v.type] +
                                                std::string(", should be ") +
                                                value::type_strings[coercion]);
            }
            break;
        case 1:
            v = **b;
            if (v.type != coercion) {
                throw new std::invalid_argument(std::string("Argument not of correct type; is ") +
                                                value::type_strings[v.type] +
                                                std::string(", should be ") +
                                                value::type_strings[coercion]);
            }
            break;
        default:
            break;
        }
    }

    void ternary_operator::check(int _ignored)  {
        value v = **c;
        if (v.type != value::boolean)
            throw new std::invalid_argument(std::string("Argument not of correct type; is ") +
                                            value::type_strings[v.type] +
                                            std::string(", should be ") +
                                            value::type_strings[value::boolean]);
        value va = **a, vb = **b;
        if (va.type != vb.type)
            throw new std::invalid_argument(std::string("Argument not of correct type; is ") +
                                            value::type_strings[vb.type] +
                                            std::string(", should be ") +
                                            value::type_strings[va.type]);
    }
}