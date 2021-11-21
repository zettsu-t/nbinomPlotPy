#define BOOST_PYTHON_STATIC_LIB
#include <memory>
#include <boost/python.hpp>
#include "dist.hpp"

// Based on
// https://stackoverflow.com/questions/5314319/how-to-export-stdvector
struct ConvertToPyList {
    static PyObject* convert(const nbinomPlotPy::Density& vec) {
        auto pylist = std::make_unique<boost::python::list>();
        auto p = pylist.get();
        for(const auto& element : vec) {
            p->append(element);
        }
        pylist.release();
        return p->ptr();
    }
};

BOOST_PYTHON_MODULE(dist) {
    boost::python::to_python_converter<nbinomPlotPy::Density, ConvertToPyList>();
    boost::python::def("get_pdf", nbinomPlotPy::get_pdf,
                       boost::python::return_value_policy<boost::python::return_by_value>());
}

/*
Local Variables:
mode: c++
coding: utf-8-unix
tab-width: nil
c-file-style: "stroustrup"
End:
*/
