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

    bool value::operator < (const value& b) {
        value a = *this;
        if (a.type < b.type)
            return true;
        if (a.type > b.type)
            return false;
        bool retval = false;
        switch(a.type) {
            case value::null:
                break;
            case value::boolean:
                retval = !(a.data.b) && b.data.b;
                break;
            case value::number:
                retval = a.data.i < b.data.i;
                break;
            case value::pair:
                if (*(a.data.p[0]) < *(b.data.p[0]))
                    retval = true;
                if (*(b.data.p[0]) < *(a.data.p[0]))
                    retval = false;
                return *(a.data.p[1]) < *(b.data.p[1]);
            default:
                break;
        }
        return retval;
    }
}

namespace std {
    bool less<random::value>::operator () (const random::value& a, const random::value& b) {
        if (a.type < b.type)
            return true;
        if (a.type > b.type)
            return false;
        bool retval = false;
        switch(a.type) {
            case random::value::null:
                break;
            case random::value::boolean:
                retval = !(a.data.b) && b.data.b;
                break;
            case random::value::number:
                retval = a.data.i < b.data.i;
                break;
            case random::value::pair:
                if (*(a.data.p[0]) < *(b.data.p[0]))
                    retval = true;
                if (*(b.data.p[0]) < *(a.data.p[0]))
                    retval = false;
                return *(a.data.p[1]) < *(b.data.p[1]);
            default:
                break;
        }
        return retval;
    }
}