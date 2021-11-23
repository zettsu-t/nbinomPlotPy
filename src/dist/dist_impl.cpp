#include <cmath>
#include <boost/math/distributions/negative_binomial.hpp>
#include "dist.hpp"

namespace nbinomPlotPy {
    Density get_pdf(RealType size, RealType prob, RealType upper, RealType step) {
        Density density;

        try {
            if (step > 0) {
                boost::math::negative_binomial_distribution<> dist(size, prob);
                for (RealType x = 0.0; x <= upper; x += step) {
                    density.push_back(boost::math::pdf(dist, x));
                }
            }
        } catch (std::exception& e) {
            // Bad size or prob parameters
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
