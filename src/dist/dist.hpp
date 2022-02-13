#include <vector>

/**
 C++ implementation
 */
namespace nbinomPlotPy {
    using RealType = double;
    using Density = std::vector<RealType>;
    /**
     * Get the probability density of a negative binomial distribution for Xs
     * @param[in] size The size parameter of a negative binomial distribution
     * @param[in] prob The prob parameter of a negative binomial distribution
     * @param[in] upper The upper limit of Xs
     * @param[in] step The step of Xs
     * @return Density density of negative binomial distribution the for Xs
     */
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
