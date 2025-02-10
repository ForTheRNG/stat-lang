#include <fstream>
#include <iostream>
#include "mathematics/large_int.h"
#include "mathematics/large_int.cpp"

int main(int argc, char** argv) {
    std::ifstream in("input.txt");
    std::ifstream ben("bench.txt");
    char oper;
    uint64_t a, b, t;
    size_t idx = 0;
    std::vector<size_t> errs;
    std::string input;
    mathematics::large_int x, y, z;
    try {
    while (in >> oper) {
        switch(oper) {
            #define opers x(+) x(-) x(/) x(%)
            #define x(sign) case #sign[0]: \
                in >> std::hex >> a >> b; \
                ben >> std::hex >> t; \
                x = a; y = b; z = t; \
                if (x sign y != t) { \
                    errs.push_back(idx); \
                } \
                break;
            opers
            #undef x
            #undef opers
            case '*':
                ben >> input;
                z = mathematics::large_int(input); 
                in >> a >> b;
                x = a; y = b;
                if (x * y != z) {
                    errs.push_back(idx);
                }
                break;
            case '>':
                oper = in.get();
                in >> std::hex >> a >> b;
                ben >> std::hex >> t;
                if (oper == ' ') {
                    if ((a > b ? 1 : 0) ^ t) {
                        errs.push_back(idx);
                    }
                } else {
                    if ((a >= b ? 1 : 0) ^ t) {
                        errs.push_back(idx);
                    }
                }
                break;
            case '<':
                oper = in.get();
                in >> std::hex >> a >> b;
                ben >> std::hex >> t;
                if (oper == ' ') {
                    if ((a < b ? 1 : 0) ^ t) {
                        errs.push_back(idx);
                    }
                } else {
                    if ((a <= b ? 1 : 0) ^ t) {
                        errs.push_back(idx);
                    }
                }
                break;
            case '=':
                oper = in.get();
                in >> std::hex >> a >> b;
                ben >> std::hex >> t;
                if ((a == b ? 1 : 0) ^ t) {
                    errs.push_back(idx);
                }
                break;
            case '!':
                oper = in.get();
                in >> std::hex >> a >> b;
                ben >> std::hex >> t;
                if ((a != b ? 1 : 0) ^ t) {
                    errs.push_back(idx);
                }
                break;
            default:
                std::cout << "Read character '" << oper << "'\n";
                break;
        }
        idx++;
    }
    } catch (std::exception ex){}
    std::cout << errs.size() << " / " << idx << " tests were wrong.";
    if (errs.size() > 0) {
        std::cout << " IDs:";
        for (auto& x: errs) std::cout << ' ' << x ;
    }
    std::cout << std::endl;
}