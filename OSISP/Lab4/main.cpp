#include <bits/stdc++.h>

#define ll long long
#define ld long double
#define vt vector<thread>
#define vm vector<mutex>

using namespace std;
using namespace chrono;

#define NUM_PHILOSOPHERS 5

#define CONFLICT_STRATEGY ConflictResolutionStrategy::ResourceHierarchy // ResourceHierarchy, Waiter

ll THINK_MIN = 50;
ll THINK_MAX = 1000;

ll EAT_MIN = 50;
ll EAT_MAX = 100;

#define SIMULATION_TIME 5

enum class ConflictResolutionStrategy
{
    ResourceHierarchy,
    Waiter
};

class Philosopher
{
public:
    Philosopher(ll id, mutex &leftFork, mutex &rightFork, ConflictResolutionStrategy strategy,
                mutex &waiter, atomic<bool> &stopFlag,
                mt19937 &rng, uniform_int_distribution<int> &thinkDist,
                uniform_int_distribution<int> &eatDist)
        : id(id), leftFork(leftFork), rightFork(rightFork), strategy(strategy),
          waiter(waiter), stopFlag(stopFlag),
          rng(rng), thinkDist(thinkDist), eatDist(eatDist),
          totalThinkingTime(0), totalEatingTime(0),
          successfulEats(0), failedAttempts(0) {}

    void dine()
    {
        while (!stopFlag.load())
        {
            auto thinkTime = thinkDist(rng);
            auto startThink = steady_clock::now();
            this_thread::sleep_for(milliseconds(thinkTime));
            auto endThink = steady_clock::now();
            totalThinkingTime += duration_cast<milliseconds>(endThink - startThink).count();

            bool eaten = false;

            if (strategy == ConflictResolutionStrategy::ResourceHierarchy)
            {
                if (id % 2 == 0)
                {
                    eaten = pickUpForks(leftFork, rightFork);
                }
                else
                {
                    eaten = pickUpForks(rightFork, leftFork);
                }
            }
            else if (strategy == ConflictResolutionStrategy::Waiter)
            {
                unique_lock<mutex> lock(waiter);
                eaten = pickUpForks(leftFork, rightFork);
            }

            if (eaten)
            {
                auto eatTime = eatDist(rng);
                auto startEat = steady_clock::now();
                this_thread::sleep_for(milliseconds(eatTime));
                auto endEat = steady_clock::now();
                totalEatingTime += duration_cast<milliseconds>(endEat - startEat).count();
                successfulEats++;

                leftFork.unlock();
                rightFork.unlock();
            }
            else
            {
                failedAttempts++;
            }
        }
    }

    ll totalThinkingTime;
    ll totalEatingTime;
    ll successfulEats;
    ll failedAttempts;

    ll id;

private:
    mutex &leftFork;
    mutex &rightFork;
    ConflictResolutionStrategy strategy;
    mutex &waiter;
    atomic<bool> &stopFlag;
    mt19937 &rng;
    uniform_int_distribution<int> &thinkDist;
    uniform_int_distribution<int> &eatDist;

    bool pickUpForks(mutex &firstFork, mutex &secondFork)
    {
        if (!firstFork.try_lock())
        {
            return false;
        }
        if (!secondFork.try_lock())
        {
            firstFork.unlock();
            return false;
        }
        return true;
    }
};

class Table
{
public:
    Table(int numPhilosophers, ConflictResolutionStrategy strategy,
          int thinkMin, int thinkMax, int eatMin, int eatMax, int simulationTime)
        : numPhilosophers(numPhilosophers), strategy(strategy),
          thinkDist(thinkMin, thinkMax), eatDist(eatMin, eatMax),
          simulationTime(simulationTime), stopFlag(false),
          waiter()
    {
        forks = vm(numPhilosophers);

        for (ll i = 0; i < numPhilosophers; ++i)
        {
            philosophers.emplace_back(new Philosopher(
                i,
                forks[i],
                forks[(i + 1) % numPhilosophers],
                strategy,
                waiter,
                stopFlag,
                rng,
                thinkDist,
                eatDist));
        }
    }

    ~Table()
    {
        for (auto p : philosophers)
        {
            delete p;
        }
    }

    void startDinner()
    {
        for (auto p : philosophers)
        {
            threads.emplace_back(&Philosopher::dine, p);
        }

        this_thread::sleep_for(seconds(simulationTime));

        stopFlag.store(true);

        for (auto &t : threads)
        {
            if (t.joinable())
                t.join();
        }
    }

    void printStatistics() const
    {
        cout << "Статистика моделирования:\n";
        ll totalThinking = 0;
        ll totalEating = 0;
        ll totalSuccess = 0;
        ll totalFailures = 0;

        for (const auto p : philosophers)
        {
            cout << "Философ " << p->id << ":" << endl;
            cout << "  Время размышлений: " << p->totalThinkingTime << " мс" << endl;
            cout << "  Время еды: " << p->totalEatingTime << " мс" << endl;
            cout << "  Успешных приемов пищи: " << p->successfulEats << endl;
            cout << "  Неудачных попыток: " << p->failedAttempts << endl;
            totalThinking += p->totalThinkingTime;
            totalEating += p->totalEatingTime;
            totalSuccess += p->successfulEats;
            totalFailures += p->failedAttempts;
        }

        cout << endl
             << "Общая статистика:" << endl;
        cout << "  Общее время размышлений: " << totalThinking << " мс" << endl;
        cout << "  Общее время еды: " << totalEating << " мс" << endl;
        cout << "  Общие успешные приемы пищи: " << totalSuccess << endl;
        cout << "  Общие неудачные попытки: " << totalFailures << endl;
        cout << "  Общая эффективность (пропускная способность): "
             << static_cast<ld>(totalSuccess) / simulationTime << " приемов пищи в секунду\n";
    }

private:
    ll numPhilosophers;
    ConflictResolutionStrategy strategy;
    vm forks;
    vector<Philosopher *> philosophers;
    vt threads;
    uniform_int_distribution<int> thinkDist;
    uniform_int_distribution<int> eatDist;
    mt19937 rng{random_device{}()};
    ll simulationTime;
    atomic<bool> stopFlag;
    mutex waiter;
};

int main()
{
    ConflictResolutionStrategy strategy;
    try
    {
        strategy = CONFLICT_STRATEGY;
    }
    catch (exception &e)
    {
        cerr << e.what() << endl;
        return 1;
    }

    cout << "Моделирование проблемы обедающих философов" << endl;
    cout << "Количество философов: " << NUM_PHILOSOPHERS << endl;
    cout << "Стратегия разрешения конфликтов: "
         << (strategy == ConflictResolutionStrategy::ResourceHierarchy ? "ResourceHierarchy" : "Waiter")
         << endl;
    cout << "Время размышлений: " << THINK_MIN << "-" << THINK_MAX << " мс" << endl;
    cout << "Время еды: " << EAT_MIN << "-" << EAT_MAX << " мс" << endl;
    cout << "Время симуляции: " << SIMULATION_TIME << " секунд" << endl
         << endl;

    Table table(NUM_PHILOSOPHERS, strategy, THINK_MIN, THINK_MAX, EAT_MIN, EAT_MAX, SIMULATION_TIME);
    table.startDinner();
    table.printStatistics();

    return 0;
}
