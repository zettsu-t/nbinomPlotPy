#include <gtest/gtest.h>
#include "dist.hpp"

class TestDist : public ::testing::Test {};

TEST_F(TestDist, All) {
    constexpr nbinomPlotPy::RealType size = 6.0;
    constexpr nbinomPlotPy::RealType prob = 0.75;
    const nbinomPlotPy::Density expected {
        0.177978516, 0.266967773, 0.233596802, 0.155731201, 0.087598801,
        0.043799400, 0.020074725, 0.008603454, 0.003495153, 0.001359226};

    const auto actual = nbinomPlotPy::get_pdf(size, prob, 0.999, 1.0);
    ASSERT_EQ(expected.size(), actual.size());

    auto length = expected.size();
    for(decltype(length) i {0}; i < length; ++i) {
        EXPECT_NEAR(expected.at(i), actual.at(i), 1e-6);
    }
}

int main(int argc, char *argv[]) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

/*
Local Variables:
mode: c++
coding: utf-8-unix
tab-width: nil
c-file-style: "stroustrup"
End:
*/
