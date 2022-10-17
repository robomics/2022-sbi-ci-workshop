#include <cstddef>
#include <iostream>
#include <span>  // Requires c++20 support


int main(int argc, char** argv) {
    std::size_t i = 0;
    // Loop over CLI arguments and print n: arg,
    // where n is the argument index and arg is the actual argument.
    for (const auto& arg: std::span(argv, argc).subspan(1)) {
        std::cout << i++ << ": " << arg << "\n";
    }
}
