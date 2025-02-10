#ifndef ROLLABLE_H
#define ROLLABLE_H

namespace random {
    template<class select_t, class analyze_t> class rollable {
    public:
        virtual select_t operator * () = 0;
        virtual analyze_t operator () () = 0;
    };
}

#endif