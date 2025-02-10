#ifndef ARITHMETIC_H
#define ARITHMETIC_H

#define num_oper_list x(+) x(-) x(*) x(/) x(%) x(=)
#define bool_oper_list x(>=) x(>) x(<=) x(<) x(==) x(!=)

namespace mathematics {
    template<class arithmetic_t> class arithmetic {
    public:
        typedef arithmetic_t type;
        #define x(a) virtual type operator a(const type& other) = 0;
        num_oper_list
        #undef x
        #define x(a) virtual bool operator a (const type& other) = 0;
        bool_oper_list
        #undef x
        static type random(type low, type high);
    };
}

#endif