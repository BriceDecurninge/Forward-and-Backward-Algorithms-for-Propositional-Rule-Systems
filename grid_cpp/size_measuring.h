#ifndef SIZE_MEASURING_H
#define SIZE_MEASURING_H

#include <vector>
#include <memory>
#include "classes.h"

/**
 * @brief Estimates the memory usage of a vector.
 *
 * This template function estimates the memory usage of a vector, including the memory allocated
 * for its elements.
 *
 * @tparam T The type of elements stored in the vector.
 * @param vec The vector whose memory usage is to be estimated.
 * @return The estimated memory usage in bytes.
 */
template<typename T>
size_t estimate_vector_memory(const std::vector<T>& vec);

/**
 * @brief Estimates the memory usage of a vector of shared_ptr.
 *
 * This template function estimates the memory usage of a vector containing shared_ptr elements.
 * The estimation considers the size of the vector itself and the size of the shared_ptrs.
 *
 * @tparam T The type of elements pointed to by the shared_ptr in the vector.
 * @param vec The vector of shared_ptr whose memory usage is to be estimated.
 * @return The estimated memory usage in bytes.
 */
template<typename T>
size_t estimate_shared_ptr_vector_memory(const std::vector<std::shared_ptr<T>>& vec);

/**
 * @brief Estimates the memory usage of a vector of weak_ptr.
 *
 * This template function estimates the memory usage of a vector containing weak_ptr elements.
 * The estimation considers the size of the vector itself and the size of the weak_ptrs.
 *
 * @tparam T The type of elements pointed to by the weak_ptr in the vector.
 * @param vec The vector of weak_ptr whose memory usage is to be estimated.
 * @return The estimated memory usage in bytes.
 */
template<typename T>
size_t estimate_weak_ptr_vector_memory(const std::vector<std::weak_ptr<T>>& vec);

/**
 * @brief Estimates the memory usage of a Variable object.
 *
 * This function estimates the memory usage of a Variable object, including the size of its member variables,
 * such as the name string, the rules vector, and boolean flags.
 *
 * @param var The Variable object whose memory usage is to be estimated.
 * @return The estimated memory usage in bytes.
 */
size_t estimate_variable_memory(const Variable& var);

/**
 * @brief Estimates the memory usage of a Rule object.
 *
 * This function estimates the memory usage of a Rule object, including the size of its member variables,
 * such as the antecedents vector, the connector string, and the successors vector.
 *
 * @param rule The Rule object whose memory usage is to be estimated.
 * @return The estimated memory usage in bytes.
 */
size_t estimate_rule_memory(const Rule& rule);

#endif // SIZE_MEASURING_H
