#include <iostream>
using namespace std;

struct Cell
{
    int id;
    bool occupied;
};

class Box
{
private:
    Cell **box;
    int row;
    int column;

public:
    Box(int row, int column) : box(nullptr), row(row), column(column)
    {
        if (row > 0 && column > 0)
        {
            box = new Cell *[row];
            for (int i = 0; i < row; ++i)
            {
                box[i] = new Cell[column];
            }
        }
    }
    ~Box()
    {
        if (box != nullptr)
        {
            for (int i = 0; i < row; ++i)
            {
                delete[] box[i];
            }
            delete[] box;
        }
    }
};

int main()
{
}