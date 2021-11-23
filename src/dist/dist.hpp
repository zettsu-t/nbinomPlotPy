#include <vector>

namespace nbinomPlotPy {
    using RealType = double;
    using Density = std::vector<RealType>;
    extern Density get_pdf(RealType size, RealType prob, RealType upper, RealType step);
}

/*
Local Variables:
mode: c++
coding: utf-8-unix
tab-width: nil
c-file-style: "stroustrup"
End:
*/
