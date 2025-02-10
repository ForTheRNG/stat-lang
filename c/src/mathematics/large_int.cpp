#include "large_int.h"
#include <stdexcept>
#include <string.h>

#define MODULO 1ull << (sizeof(int) * 8)
#define last(large) large.num[large.num.size() - 1]

namespace mathematics {
    std::mt19937 large_int::generator { std::random_device{}() };
}
using namespace mathematics;

std::pair<large_int, large_int> const large_int::halve(size_t count) {
    if (count >= num.size())
        return std::make_pair(large_int(0), *this);
    large_int a, b;
    a.num.reserve(count);
    memcpy(a.num.data(), num.data(), count);
    b.num.reserve(num.size() - count);
    memcpy(b.num.data(), num.data() + count, num.size() - count);
    return std::make_pair(a, b);
}

large_int::large_int(uint64_t number) {
    if (number < MODULO) {
        num = std::vector<uint32_t>(1);
    } else {
        num = std::vector<uint32_t>(2);
        num[1] = number / MODULO;
    }
    num[0] = number % MODULO;
}

large_int::large_int(large_int& other) {
    num = std::vector<uint32_t>(other.num);
}

large_int::large_int(const large_int& other) {
    num = std::vector<uint32_t>(other.num);
}

large_int::large_int(std::string& nibbles) {
    uint32_t curr = 0;
    for (size_t idx = nibbles.size() - 1; idx < nibbles.size(); idx++) {
        if (nibbles[idx] > 15) {
            if ('0' <= nibbles[idx] && '9' >= nibbles[idx]) {
                curr = curr + ((nibbles[idx] - '0') << ((idx / 8) * 4));    
            } else if ('a' <= nibbles[idx] && 'f' >= nibbles[idx]) {
                curr = curr + ((nibbles[idx] - 'a' + 10) << ((idx / 8) * 4));    
            } else if ('A' <= nibbles[idx] && 'F' >= nibbles[idx]) {
                curr = curr + ((nibbles[idx] - 'A' + 10) << ((idx / 8) * 4));    
            } else {
                throw std::invalid_argument("Nibbles are not hexadecimal!");
            }
        } else {
            curr = curr + (nibbles[idx] << ((idx / 8) * 4));
        }
    }
}

large_int large_int::operator=(const large_int& other) {
    num = std::vector<uint32_t>(other.num);
    return large_int(*this);
}

large_int large_int::operator++() {
    size_t idx = 0;
    uint32_t carry = 1;
    while (carry + num[idx] == MODULO) {
        num[idx] = 0;
        idx++;
    }
    num[idx]++;
    if (carry)
        num.push_back(carry);
    return large_int(*this);
}

large_int large_int::operator--() {
    if (num.size() == 0 || (num.size() == 1 && num[0] == 0))
        throw std::invalid_argument("Number is 0 and cannot be decremented!");
    size_t idx;
    for (idx = 0; num[idx] == 0; idx++)
        num[idx] = -1;
    num[idx]--;
    return large_int(*this);
}

large_int large_int::operator+(const large_int& other) {
    large_int result = 0UL;
    size_t idx;
    uint32_t carry = 0;
    result.num.pop_back();
    for (idx = 0; idx < num.size() && idx < other.num.size(); idx++){
        result.num.push_back(num[idx] + other.num[idx] + carry);
        carry = num[idx] + other.num[idx] + carry > num[idx] ? 0 : 1;
    }
    for (; idx < num.size(); idx++){
        result.num.push_back(num[idx] + carry);
        carry = num[idx] + carry > num[idx] ? 0 : 1;
    }
    for (; idx < other.num.size(); idx++) {
        result.num.push_back(other.num[idx] + carry);
        carry = other.num[idx] + carry > other.num[idx] ? 0 : 1;
    }
    if (carry)
        result.num.push_back(carry);
    return result;
}

large_int large_int::operator-(const large_int& other) {
    if (*this <= other)
        throw std::invalid_argument("Subtracting large number from small number!");
    large_int result(0);
    size_t idx;
    uint32_t carry = 0;
    for (idx = 0; idx < other.num.size(); idx++) {
        result.num.push_back(num[idx] - other.num[idx] - carry);
        carry = result.num[idx] < num[idx] ? 0 : 1;
    }
    for (; idx < num.size(); idx++) {
        result.num.push_back(num[idx] - carry);
    }
    return result;
}

large_int large_int::operator<<(size_t count) {
    large_int result = *this;
    result.num.reserve(result.num.size() + count);
    memmove(result.num.data() + count, result.num.data(), result.num.size());
    memset(result.num.data(), 0, sizeof(uint32_t) * count);
    return large_int(*this);
}

large_int large_int::operator*(const large_int& other) {
    large_int result;
    if (other.num.size() == 0 || num.size() == 0)
        return large_int(0);
    if (other.num.size() == 1) {
        if (other.num[0] == 0)
            return large_int(0);
        if (other.num[0] == 1) {
            result = *this;
            return result;
        }
        uint32_t carry = 0;
        uint64_t x;
        result = large_int(0);
        result.num.pop_back();
        for (size_t idx = 0; idx < num.size(); idx++) {
            x = ((uint64_t) num[idx]) * other.num[0] + carry;
            result.num.push_back(x % MODULO);
            carry = x / MODULO;
        }
        return result;
    }
    if (num.size() == 1) {
        if (num[0] == 0)
            return large_int(0);
        if (num[0] == 1) {
            result = other;
            return result;
        }
        uint32_t carry = 0;
        uint64_t x;
        result = large_int(0);
        result.num.pop_back();
        for (size_t idx = 0; idx < other.num.size(); idx++) {
            x = ((uint64_t) other.num[idx]) * num[0] + carry;
            result.num.push_back(x % MODULO);
            carry = x / MODULO;
        }
        return result;
    }
    large_int k;
    k = other;
    size_t len = std::max(num.size(), other.num.size());
    len = len / 2;
    auto x = halve(len); auto y = k.halve(len);
    large_int a = x.first * y.first;
    large_int b = (x.first + x.second) * (y.first + y.second);
    large_int c = x.second + y.second;
    b = b - a - c;
    return (c << len * 2) + (b << len) + a;
}

large_int large_int::operator% (const large_int& other) {
    return div(other).second;
}

large_int large_int::operator/ (const large_int& other) {
    return div(other).first;
}

std::pair<large_int, large_int> large_int::div(const large_int& _other) {
    large_int res(0), rest = *this, other = _other;
    res.num.pop_back();
    while (rest > other) {
        uint32_t new_digit = last(rest) / last(other);
        large_int diff = other * uint64_t(new_digit);
        if (diff > rest) {
            new_digit--;
            diff = diff - other;
        }
        res.num.push_back(new_digit);
        for (size_t idx = diff.num.size() - 1; idx < diff.num.size() && diff.num[idx] == rest.num[idx]; idx--) {
            res.num.push_back(0);
        }
        res.num.pop_back();
        res = res - diff;
    }
    for (size_t idx = 0; idx < res.num.size() / 2; idx++)
        std::swap(res.num[idx], res.num[res.num.size() - 1 - idx]);
    return std::make_pair(res, rest);
}

int32_t large_int::delta(const large_int& other) {
    if (num.size() < other.num.size())
        return -1;
    if (num.size() > other.num.size())
        return 1;
    size_t idx = num.size();
    for (idx--; idx < num.size() && num[idx] == other.num[idx]; idx--);
    if (idx > num.size())
        return 0;
    if (num[idx] < other.num[idx])
        return -1;
    if (num[idx] > other.num[idx])
        return 1;
    return 0;
}

#define x(oper) bool large_int::operator oper (const large_int& other) { return delta(other) oper 0; }
bool_oper_list
#undef x

large_int large_int::gcd(const large_int& other) {
    large_int a = *this, b = other, r = a % b;
    while (r != 0) {
        a = b;
        b = r;
        r = a % b;
    }
    return b;
}

uint64_t large_int::gcd (const uint64_t& other) {
    large_int res = gcd(large_int(other));
    return (((uint64_t) res.num[1]) << (sizeof(uint32_t) * 8)) + res.num[0];
}

large_int large_int::random(large_int& low, large_int& high) {
    large_int _low = low, _high = high;
    if (_high > _low) {
        large_int aux = _low;
        _low = _high;
        _high = _low;
    }
    _high = _high - _low;
    large_int res = _high;
    std::uniform_int_distribution<uint32_t> final_dist(0, last(_high));
    while (res >= _high) {
        for (size_t idx = 0; idx < res.num.size() - 1; idx++)
            res.num[idx] = generator();
        last(res) = final_dist(generator);
    }
    while (last(res) == 0)
        res.num.pop_back();
    return res + _low;
}

#define operation(type, sign) \
type large_int::operator sign (uint64_t other) { return *this sign large_int(other); }
#define x(oper) operation(large_int, oper)
num_oper_list
#undef x
#define x(oper) operation(bool, oper)
bool_oper_list
#undef x
#undef operation

#undef last
#undef MODULO