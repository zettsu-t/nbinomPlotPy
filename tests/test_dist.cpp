#include <gtest/gtest.h>
#include "dist.hpp"

class TestDist : public ::testing::Test {};

TEST_F(TestDist, Integers) {
    constexpr nbinomPlotPy::RealType size = 6.0;
    constexpr nbinomPlotPy::RealType prob = 0.75;
    const nbinomPlotPy::Density expected {
        0.177978516, 0.266967773, 0.233596802, 0.155731201, 0.087598801,
        0.043799400, 0.020074725, 0.008603454, 0.003495153, 0.001359226};

    const auto actual = nbinomPlotPy::get_pdf(size, prob, 9.0, 1.0);
    ASSERT_EQ(expected.size(), actual.size());

    auto length = expected.size();
    for(decltype(length) i {0}; i < length; ++i) {
        EXPECT_NEAR(expected.at(i), actual.at(i), 1e-6);
    }
}

TEST_F(TestDist, Fractions) {
    constexpr nbinomPlotPy::RealType size = 2.0;
    constexpr nbinomPlotPy::RealType prob = 0.25;
    const nbinomPlotPy::Density expected {
        0.0625, 0.0811899, 0.09375, 0.101487, 0.105469, 0.106562};

    const auto actual = nbinomPlotPy::get_pdf(size, prob, 2.6, 0.5);
    ASSERT_EQ(expected.size(), actual.size());

    auto length = expected.size();
    for(decltype(length) i {0}; i < length; ++i) {
        EXPECT_NEAR(expected.at(i), actual.at(i), 1e-6);
    }
}

TEST_F(TestDist, OneOrNone) {
    constexpr nbinomPlotPy::RealType size = 6.0;
    constexpr nbinomPlotPy::RealType prob = 0.75;

    constexpr nbinomPlotPy::RealType expected = 0.177978516;
    auto actual = nbinomPlotPy::get_pdf(size, prob, 0.0, 1.0);
    EXPECT_NEAR(expected, actual.front(), 1e-6);

    actual = nbinomPlotPy::get_pdf(size, prob, -1.0, 1.0);
    EXPECT_TRUE(actual.empty());
}

TEST_F(TestDist, BadParameters) {
    EXPECT_TRUE(nbinomPlotPy::get_pdf(-1.0, 0.75, 9.0, 1.0).empty());
    EXPECT_TRUE(nbinomPlotPy::get_pdf(0.0, 0.75, 9.0, 1.0).empty());

    EXPECT_TRUE(nbinomPlotPy::get_pdf(6.0, 1.5, 9.0, 1.0).empty());
    EXPECT_TRUE(nbinomPlotPy::get_pdf(6.0, -0.75, 9.0, 1.0).empty());

    EXPECT_TRUE(nbinomPlotPy::get_pdf(6.0, 0.75, 9.0, 0.0).empty());
    EXPECT_TRUE(nbinomPlotPy::get_pdf(6.0, 0.75, 9.0, -1.0).empty());
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
