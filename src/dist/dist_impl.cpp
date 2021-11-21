#include <cmath>
#include <boost/math/distributions/negative_binomial.hpp>
#include "dist.hpp"

namespace nbinomPlotPy {
    Density get_pdf(RealType size, RealType prob, RealType quantile, RealType step) {
        boost::math::negative_binomial_distribution<> dist(size, prob);
        auto upper = boost::math::quantile(dist, quantile);
        upper = (1.0 + std::ceil(upper / step)) * step;

        Density density;
        for (RealType x = 0.0; x < upper; x += step) {
            density.push_back(boost::math::pdf(dist, x));
        }

        return density;
    }
}

/*
Local Variables:
mode: c++
coding: utf-8-unix
tab-width: nil
c-file-style: "stroustrup"
End:
*/
