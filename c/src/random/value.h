#ifndef VALUE_H
#define VALUE_H

#include <cinttypes>
#include <string>

namespace random {
    class value {
    private:
        typedef union {
            bool b;
            int64_t i;
            value* p[2];
        } _value_data;
    public:
        enum types{null, boolean, number, pair} type;
        _value_data data;
        static std::string type_strings[4];
        value();
        value(bool b);
        value(int64_t i);
        value(value* p1, value* p2);
        value(const value& other);
        value operator = (const value& other);
        bool operator <(const value& b) const;
    };
}

namespace std {
    template<> class less<random::value> {
    public:
        bool operator () (const random::value& a, const random::value& b);
    };
}

#endif