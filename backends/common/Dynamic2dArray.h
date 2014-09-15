#pragma once
#include <vector>
#include <iostream>

/**
 * Class: Dynamic2dArray
 * Template class for managing a twodimensional array of growing size.
 */
template <typename T>
class Dynamic2dArray
{
public:
	Dynamic2dArray(unsigned int w, unsigned int h);

	void set(unsigned int row, unsigned int col, const T& value);
	const T& get(unsigned int row, unsigned int col) const;

	void addRow();
	void addColumn();

	unsigned int getWidth() const;
	unsigned int getHeight() const;

	const std::vector<T>& getRow(unsigned int index) const;

protected:
	unsigned int computeWidth() const; // for debugging

	/**
	 * Variable: m_data
	 * The actual data container, of size #rows x #cols
	 */
	std::vector<std::vector<T>> m_data;

	unsigned int m_w;
	unsigned int m_h;
};

template <typename T>
Dynamic2dArray<T>::Dynamic2dArray(unsigned int w, unsigned int h)
{
	for (int i = 0; i < w; ++i)
	{
		m_data.emplace_back(std::vector<T>());
		for (int j = 0; j < h; ++j)
			m_data[i].emplace_back(T());
	}
	m_w = w;
	m_h = h;
	assert(getWidth() == w && getHeight() == h);
}

template <typename T>
void Dynamic2dArray<T>::set(unsigned int row, unsigned int col, const T& value)
{
	assert(m_data.size() >= row && m_data[row].size() >= col);
	m_data[row][col] = value;
}

template <typename T>
const T& Dynamic2dArray<T>::get(unsigned int row, unsigned int col) const
{
	assert(m_data.size() > row && m_data[row].size() > col);
	return m_data[row][col];
}

template <typename T>
unsigned int Dynamic2dArray<T>::getWidth() const
{
	assert(computeWidth() == m_w);
	return m_w;
}

template <typename T>
unsigned int Dynamic2dArray<T>::getHeight() const
{
	assert(m_data.size() == m_h);
	return m_h;
}

template <typename T>
void Dynamic2dArray<T>::addRow()
{
	m_data.emplace_back(std::vector<T>());
	for (unsigned int i = 0; i < m_h; ++i)
	{
		m_data.back().emplace_back(T());
	}
	++m_h;
}

template <typename T>
void Dynamic2dArray<T>::addColumn()
{
	for (unsigned int rowIndex = 0; rowIndex < m_h; ++rowIndex)
		m_data[rowIndex].emplace_back(T());

	++m_w;
}

template <typename T>
unsigned int Dynamic2dArray<T>::computeWidth() const
{
	unsigned int maxW = 0;
	for (const auto r : m_data)
	{
		if (r.size() > maxW)
			maxW = r.size();
	}
	return maxW;
}

template <typename T>
const std::vector<T>& Dynamic2dArray<T>::getRow(unsigned int index) const
{
	return m_data[index];
}