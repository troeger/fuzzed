#pragma once
#include <vector>

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

protected:
	unsigned int computeHeight() const; // for debugging

	std::vector<std::vector<T>> m_data; // rows x cols

	unsigned int m_w;
	unsigned int m_h;
};

template <typename T>
Dynamic2dArray<T>::Dynamic2dArray(unsigned int w, unsigned int h)
{
	m_data.emplace_back(std::vector<T>());
	for (int i = 0; i < w; ++i)
	{
		m_data.emplace_back(std::vector<T>());
		for (int j = 0; j < h; ++j)
			m_data[i].emplace_back(T());
	}
}

template <typename T>
void Dynamic2dArray<T>::set(unsigned int row, unsigned int col, const T& value)
{
	assert(m_data.size() > row && m_data[row].size() > col);
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
	assert(m_data.size() == m_w);
	return m_w;
}

template <typename T>
unsigned int Dynamic2dArray<T>::getHeight() const
{
	assert(computeHeight() == m_h);
	return m_h;
}

template <typename T>
void Dynamic2dArray<T>::addRow()
{
	m_data.emplace_back(std::vector<T>());
}

template <typename T>
void Dynamic2dArray<T>::addColumn()
{
	for (unsigned int rowIndex = 0; rowIndex < m_w; ++rowIndex)
	{
		m_data[rowIndex].emplace_back(T());
	}
}

template <typename T>
unsigned int Dynamic2dArray<T>::computeHeight() const
{
	unsigned int maxH = 0;
	for (const auto r : m_data)
	{
		if (r.size() > maxH)
			maxH = r.size();
	}
	return maxH;
}