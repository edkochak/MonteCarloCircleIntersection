#include <iostream>
#include <cmath>
#include <algorithm>

bool isInsideCircle(double x, double y, double centerX, double centerY, double radius) {
    double dx = x - centerX;
    double dy = y - centerY;
    return dx * dx + dy * dy <= radius * radius;
}

int main() {
    
    double x1, y1, r1;
    double x2, y2, r2;
    double x3, y3, r3;
    std::cin >> x1 >> y1 >> r1;
    std::cin >> x2 >> y2 >> r2;
    std::cin >> x3 >> y3 >> r3;

    
    double x_min = std::min({x1 - r1, x2 - r2, x3 - r3});
    double x_max = std::max({x1 + r1, x2 + r2, x3 + r3});
    double y_min = std::min({y1 - r1, y2 - r2, y3 - r3});
    double y_max = std::max({y1 + r1, y2 + r2, y3 + r3});

    int N = 1000000; 
    int M = 0;

    for (int i = 0; i < N; ++i) {
        double x = x_min + (x_max - x_min) * rand() / RAND_MAX;
        double y = y_min + (y_max - y_min) * rand() / RAND_MAX;

        if (isInsideCircle(x, y, x1, y1, r1) &&
            isInsideCircle(x, y, x2, y2, r2) &&
            isInsideCircle(x, y, x3, y3, r3)) {
            M++;
        }
    }

    double S_rec = (x_max - x_min) * (y_max - y_min);
    double S_approx = static_cast<double>(M) / N * S_rec;

    std::cout << S_approx << std::endl;

    return 0;
}