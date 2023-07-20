#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include <chrono>

using namespace std;
using namespace std::chrono;

const int INF = 1e9;

int tspHeldKarp(int n, vector<vector<int>>& distance) {
    // n = number of cities
    // distance is 2D distance matrix

    // stores the minimum cost of reaching some subset of cities and ending at particular city
    vector<vector<int>> dp(1 << n, vector<int>(n, INF));

    // previous city to reach current city for each combination
    vector<vector<int>> parent(1 << n, vector<int>(n, -1));

    // cost of 0 to reach the 0th city (we start and end at city 0)
    dp[1][0] = 0;

    // iterate over all possible subsets of cities; skip the first subset
    for (int subset = 1; subset < (1 << n); subset++) {

        // iterate over each possible city that the path ends at
        for (int lastCity = 0; lastCity < n; lastCity++) {

            // check if lastCity is already included in our subset
            if ((subset & (1 << lastCity)) != 0) {

                // remove the lastCity from the current subset
                int prevSubset = subset ^ (1 << lastCity);

                // iterate over each city in prevSubset to see if currCity is already in our subset
                for (int currCity = 0; currCity < n; currCity++) {

                    // check if currCity already in subset
                    if ((prevSubset & (1 << currCity)) != 0) {

                        // the cost to reach currCity is the cost of reachingcurrCity using the previous subset + the distance between currCity and lastCity
                        int cost = dp[prevSubset][currCity] + distance[currCity][lastCity];

                        // if new cost is better than existing one, then update because it is a better solution
                        if (cost < dp[subset][lastCity]) {
                            dp[subset][lastCity] = cost;
                            parent[subset][lastCity] = currCity;
                        }
                    }
                }
            }
        }
    }


    int minCost = INF;
    int lastCity = -1;

    // all cities included in the subset
    int fullMask = (1 << n) - 1;

    // loop over each city and find if the cost of reaching city i in the fullMask subset plus dist from i to 0 is less than current min
    for (int i = 0; i < n; i++) {
        
        // update if true
        if (dp[fullMask][i] + distance[i][0] < minCost) {
            minCost = dp[fullMask][i] + distance[i][0];
            lastCity = i;
        }
    }

    // store the ordered vertices of our tour
    vector<int> tour;

    int mask = fullMask;

    // searching backwards until we reach the starting city
    while (lastCity != -1) {
        // add the last visited city
        tour.push_back(lastCity);

        // get the parent city
        int prevCity = parent[mask][lastCity];

        // remove the lastCity
        mask ^= (1 << lastCity);

        // set the new city to visit backwards
        lastCity = prevCity;
    }

    // iterate over the vertices in the tour and display
    // technically this is backwards but it's a tour so it doesn't matter
    cout << "TSP Tour: ";
    for (int i = 0; i < tour.size(); i++) {
        cout << tour[i] << " ";
    }
    cout << endl;

    cout << minCost << endl;

    return minCost;
}

int main() {
    int n = 23; 
    vector<vector<int>> distance = 
    {
        {0, 777, 7484, 969, 7539, 2454, 2694, 2919, 6400, 2394, 3184, 2226, 2853, 2940, 2615, 3980, 5002, 93, 8028, 8698, 7337, 8045, 286},
        {777, 0, 7887, 1439, 7219, 2217, 2423, 2588, 6238, 2243, 3021, 2117, 2691, 2808, 2377, 4587, 5774, 811, 7902, 8476, 6562, 8149, 979},
        {7484, 7887, 0, 8025, 9764, 9908, 10156, 10401, 10403, 9781, 10455, 9593, 10187, 10208, 10061, 3666, 5002, 7394, 8896, 8473, 8164, 8189, 7199},
        {969, 1439, 8025, 0, 6822, 1904, 2151, 2424, 5586, 1756, 2483, 1568, 2177, 2228, 2046, 4369, 4584, 1043, 7159, 7871, 7571, 7090, 1143},
        {7539, 7219, 9764, 6822, 0, 5088, 4853, 4649, 1354, 5149, 4367, 5322, 4693, 4618, 4926, 10555, 7611, 7632, 1131, 1304, 4099, 2172, 7815},
        {2454, 2217, 9908, 1904, 5088, 0, 248, 523, 4023, 253, 814, 397, 501, 640, 163, 6271, 5947, 2546, 5687, 6289, 5998, 5990, 2734},
        {2694, 2423, 10156, 2151, 4853, 248, 0, 287, 3814, 439, 664, 616, 417, 560, 120, 6519, 6110, 2786, 5479, 6067, 5808, 5824, 2975},
        {2919, 2588, 10401, 2424, 4649, 523, 287, 0, 3670, 726, 705, 904, 585, 705, 407, 6787, 6375, 3010, 5330, 5888, 5530, 5742, 3204},
        {6400, 6238, 10403, 5586, 1354, 4023, 3814, 3670, 0, 4028, 3234, 4183, 3569, 3468, 3862, 9259, 6601, 6492, 1664, 2299, 5063, 2216, 6657},
        {2394, 2243, 9781, 1756, 5149, 253, 439, 726, 4028, 0, 794, 188, 460, 565, 319, 6122, 5697, 2487, 5684, 6316, 6240, 5922, 2666},
        {3184, 3021, 10455, 2483, 4367, 814, 664, 705, 3234, 794, 0, 958, 334, 255, 665, 6798, 5890, 3277, 4892, 5521, 5942, 5176, 3454},
        {2226, 2117, 9593, 1568, 5322, 397, 616, 904, 4183, 188, 958, 0, 629, 715, 499, 5934, 5560, 2319, 5833, 6476, 6394, 6035, 2496},
        {2853, 2691, 10187, 2177, 4693, 501, 417, 585, 3569, 460, 334, 629, 0, 144, 372, 6521, 5819, 2946, 5226, 5855, 6054, 5493, 3124},
        {2940, 2808, 10208, 2228, 4618, 640, 560, 705, 3468, 565, 255, 715, 144, 0, 517, 6547, 5739, 3033, 5120, 5761, 6118, 5365, 3207},
        {2615, 2377, 10061, 2046, 4926, 163, 120, 407, 3862, 319, 665, 499, 372, 517, 0, 6415, 5994, 2708, 5525, 6126, 5928, 5840, 2895},
        {3980, 4587, 3666, 4369, 10555, 6271, 6519, 6787, 9259, 6122, 6798, 5934, 6521, 6547, 6415, 0, 3124, 3901, 9853, 10355, 9932, 8860, 3700},
        {5002, 5774, 5002, 4584, 7611, 5947, 6110, 6375, 6601, 5697, 5890, 5560, 5819, 5739, 5994, 3124, 0, 4984, 6737, 7251, 11659, 5738, 4857},
        {93, 811, 7394, 1043, 7632, 2546, 2786, 3010, 6492, 2487, 3277, 2319, 2946, 3033, 2708, 3901, 4984, 0, 8119, 8791, 7373, 8126, 200},
        {8028, 7902, 8896, 7159, 1131, 5687, 5479, 5330, 1664, 5684, 4892, 5833, 5226, 5120, 5525, 9853, 6737, 8119, 0, 762, 5036, 1067, 8271},
        {8698, 8476, 8473, 7871, 1304, 6289, 6067, 5888, 2299, 6316, 5521, 6476, 5855, 5761, 6126, 10355, 7251, 8791, 762, 0, 4593, 1525, 8956},
        {7337, 6562, 8164, 7571, 4099, 5998, 5808, 5530, 5063, 6240, 5942, 6394, 6054, 6118, 5928, 9932, 11659, 7373, 5036, 4593, 0, 6070, 7529},
        {8045, 8149, 8189, 7090, 2172, 5990, 5824, 5742, 2216, 5922, 5176, 6035, 5493, 5365, 5840, 8860, 5738, 8126, 1067, 1525, 6070, 0, 8231},
        {286, 979, 7199, 1143, 7815, 2734, 2975, 3204, 6657, 2666, 3454, 2496, 3124, 3207, 2895, 3700, 4857, 200, 8271, 8956, 7529, 8231, 0}
    };

    int minCost = tspHeldKarp(n, distance);

    cout << "Minimum cost of the TSP tour: " << minCost << endl;

    return 0;
}