// Python callable version of verushash-node for electrumx
//
//

#include <stdint.h>
#include <vector>

#include "crypto/verus_hash.h"
#include "solutiondata.h"
#include <pybind11/pybind11.h>

#include <sstream>

namespace py = pybind11;

bool initialized = false;

void initialize()
{
    if (!initialized)
    {
        CVerusHash::init();
        CVerusHashV2::init();
        sodium_init();
    }
    initialized = true;
}

py::bytes verushash(const std::string bytes) {
    char *result = new char[32];
    
    if (initialized == false) {
        initialize();
    }
    verus_hash(result, bytes.data(), bytes.size());
    return py::bytes((char *)result, 32);
}

py::bytes verushash_v2(const std::string bytes) {
    CVerusHashV2 vh2(SOLUTION_VERUSHHASH_V2);
    unsigned char *result = new unsigned char[32];
    
    if (initialized == false) {
        initialize();
    }

    vh2.Reset();
    vh2.Write((const unsigned char *)bytes.data(), bytes.size());
    vh2.Finalize(result);
    return py::bytes((char *)result, 32);
}

py::bytes verushash_v2b(const std::string bytes) {
    CVerusHashV2 vh2(SOLUTION_VERUSHHASH_V2);
    unsigned char *result = new unsigned char[32];
    
    if (initialized == false) {
        initialize();
    }

    vh2.Reset();
    vh2.Write((const unsigned char *)bytes.data(), bytes.size());
    vh2.Finalize2b(result);
    return py::bytes((char *)result, 32);
}

py::bytes verushash_v2b1(const std::string bytes) {
    CVerusHashV2 vh2b1(SOLUTION_VERUSHHASH_V2_1);
    unsigned char *result = new unsigned char[32];
    
    if (initialized == false) {
        initialize();
    }

    vh2b1.Reset();
    vh2b1.Write((const unsigned char *)bytes.data(), bytes.size());
    vh2b1.Finalize2b(result);
    return py::bytes((char *)result, 32);
}

py::bytes verushash_v2b2(const std::string bytes)
{
    uint256 result;

    if (initialized == false) {
        initialize();
    }

    CBlockHeader bh;
    CDataStream s(bytes.data(), bytes.data() + bytes.size(), SER_GETHASH, 0);

    try
    {
        s >> bh;
        result = bh.GetVerusV2Hash();
    }
    catch(const std::exception& e)
    {
    }

    return py::bytes((char *)&result, 32);
}

namespace py = pybind11;

PYBIND11_MODULE(verushash, m) {
    m.doc() = R"pbdoc(
        VerusHash native module for Python
        ----------------------------------

        .. currentmodule:: verushash

        .. autosummary::
           :toctree: _generate

           initialize
           verushash
           verushash_v2
           verushash_v2b
           verushash_v2b1
           verushash_v2b2
    )pbdoc";

    m.def("initialize", &initialize, R"pbdoc(
        Initialize the verushash module
    )pbdoc");

    m.def("verushash", &verushash, R"pbdoc(
        VerusHash V1
    )pbdoc");

    m.def("verushash_v2", &verushash_v2, R"pbdoc(
        VerusHash V2, return 32 bytes as bytes result
    )pbdoc");

    m.def("verushash_v2b", &verushash_v2b, R"pbdoc(
        VerusHash V2b, return 32 bytes as bytes result
    )pbdoc");

    m.def("verushash_v2b1", &verushash_v2b1, R"pbdoc(
        VerusHash V2b1, return 32 bytes as bytes result
    )pbdoc");

    m.def("verushash_v2b2", &verushash_v2b2, R"pbdoc(
        VerusHash V2b2, return 32 bytes as bytes result
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
