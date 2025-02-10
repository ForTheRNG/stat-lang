#ifndef VARIABLE_H
#define VARIABLE_H

#include "mathematics/probability.h"
#include "random/rollable.h"
#include "random/value.h"
#include <map>

namespace random {

    class variable: mathematics::arithmetic<variable>, rollable<value, variable> {
    private:
        typedef struct {
            mathematics::probability chance;
            std::vector<value> vals;
        } dependency;
        std::vector<variable*> deps;
        std::map<value, std::vector<dependency>> data;
        variable();
    protected:
    public:
        variable(int64_t a, int64_t b);
        mathematics::probability chance(value v);
        #define x(o) variable operator o (const variable& other);
        num_oper_list
        #undef x
        #define x(o) bool operator o (const variable& other);
        bool_oper_list
        #undef x
        value operator * ();
        variable operator () () { return *this; };
        variable operator && (const variable& other);
        variable operator || (const variable& other);
        variable operator ! ();
        variable ternary(const variable* a, const variable* b);
        static variable random(variable low, variable high) { return variable(); };
    };
}

#endif