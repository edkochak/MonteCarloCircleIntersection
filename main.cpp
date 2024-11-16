#include <iostream>
#include <cmath>
#include <random>
#include <vector>

struct SimulationResult
{
    int N;
    double area;
    double error;
};

bool isInsideCircle(double x, double y, double centerX, double centerY, double radius)
{
    double dx = x - centerX;
    double dy = y - centerY;
    return dx * dx + dy * dy <= radius * radius;
}

SimulationResult runSimulation(std::string area_type, int N,
                               const std::vector<std::tuple<double, double, double>> &circles,
                               double exact_area,
                               double min_coord, double max_coord)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);

    double x_min = min_coord;
    double x_max = max_coord;
    double y_min = min_coord;
    double y_max = max_coord;

    int M = 0;
    for (int i = 0; i < N; ++i)
    {
        double x = x_min + (x_max - x_min) * dis(gen);
        double y = y_min + (y_max - y_min) * dis(gen);

        bool inside = true;
        for (const auto &circle : circles)
        {
            if (!isInsideCircle(x, y, std::get<0>(circle), std::get<1>(circle), std::get<2>(circle)))
            {
                inside = false;
                break;
            }
        }
        if (inside)
            M++;
    }

    double S_rec = (x_max - x_min) * (y_max - y_min);
    double S_approx = static_cast<double>(M) / N * S_rec;
    double relative_error = std::abs(S_approx - exact_area) / exact_area;

    return {N, S_approx, relative_error};
}

int main()
{
    const int NUM_RUNS = 10;
    std::vector<std::tuple<double, double, double>> circles = {
        {1.0, 1.0, 1.0},
        {1.5, 2.0, std::sqrt(5) / 2.0},
        {2.0, 1.5, std::sqrt(5) / 2.0}};

    double exact_area = 0.25 * M_PI + 1.25 * asin(0.8) - 1;

    
    std::vector<std::pair<std::string, std::pair<double, double>>> areas = {
        {"tight", {0.7, 2.1}}, 
        {"wide", {0.5, 3.1}}  
    };

    for (const auto &area : areas)
    {
        for (int N = 100; N <= 100000; N += 500)
        {
            double avg_area = 0.0, avg_error = 0.0;

            for (int run = 0; run < NUM_RUNS; ++run)
            {
                auto result = runSimulation(area.first, N, circles, exact_area,
                                            area.second.first, area.second.second);
                avg_area += result.area;
                avg_error += result.error;
            }

            avg_area /= NUM_RUNS;
            avg_error /= NUM_RUNS;

            std::cout << area.first << " " << N << " " << avg_area << " " << avg_error << std::endl;
        }
    }
    return 0;
}
