#ifndef LARGE_INT_H
#define LARGE_INT_H

#include <vector>
#include <string>
#include <cinttypes>
#include "mathematics/arithmetic.h"
#include <random>
#include <functional>

namespace mathematics {
    class large_int: arithmetic<large_int> {
    private:
    protected:
        std::pair<large_int, large_int> const halve(size_t count);
        std::vector<uint32_t> num;
        static std::mt19937 generator;
        int32_t delta(const large_int& other);
    public:
        #define operation(type, oper) \
            type operator oper(const large_int& other); \
            type operator oper(uint64_t other);
        std::pair<large_int, large_int> div(const large_int& other); 
        large_int(large_int& other);
        large_int(const large_int& other);
        large_int(uint64_t number);
        large_int() : large_int(0ul) {};
        large_int(std::string& nibbles);
        #define x(oper) operation(large_int, oper)
        num_oper_list
        #undef x
        large_int operator ++();
        large_int operator --();
        large_int operator << (size_t num);
        #define x(oper) operation(bool, oper)
        bool_oper_list
        #undef x
        #undef operation
        large_int gcd(const large_int& other);
        uint64_t gcd(const uint64_t& other);
        static large_int random(large_int& low, large_int& high);
    };
}

#endif