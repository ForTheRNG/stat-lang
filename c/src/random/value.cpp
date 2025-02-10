#include "value.h"
namespace random {

    std::string value::type_strings[4] = {
        std::string("null"),
        std::string("boolean"),
        std::string("number"),
        std::string("pair")
    };

    value::value() {
        type = types::null;
        data.b = false;
    }

    value::value(bool b) {
        type = types::boolean;
        data.b = b;
    }

    value::value(int64_t i) {
        type = types::number;
        data.b = i;
    }

    value::value(value* p1, value* p2) {
        type = types::pair;
        data.p[0] = p1;
        data.p[1] = p2;
    }

    value::value(const value& other) {
        *this = other;
    }
    
    value value::operator=(const value& other) {
        type = other.type;
        switch(type) {
            case types::number:
                data.i = other.data.i;
                break;
            case types::boolean:
                data.b = other.data.b;
                break;
            case types::pair:
                data.p[0] = other.data.p[0];
                data.p[1] = other.data.p[1];
                break;
            default:
                break;
        }
        return other;
    }

    bool value::operator < (const value& other) {
        if (type < other.type)
            return true;
        if (type > other.type)
            return false;
        bool retval = false;
        switch(type) {
            case value::null:
                retval = false;
                break;
            case value::boolean:
                retval = !(data.b) && other.data.b;
                break;
            case value::number:
                retval = data.i < other.data.i;
                break;
            case value::pair:
                if (*(data.p[0]) < *(other.data.p[0]))
                    retval = true;
                if (*(other.data.p[0]) < *(data.p[0]))
                    retval = false;
                return *(data.p[1]) < *(other.data.p[1]);
            default:
                break;
        }
        return retval;
    }
}