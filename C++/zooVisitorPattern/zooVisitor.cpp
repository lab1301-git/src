/*
 * Lakshman Brodie
 * August 2020
 *
 * The code addresses the following specification: 
 * Write a simple Zoo simulator which contains 3 different types of animals:
 *  monkey,
 *  giraffe
 *  elephant
 *
 * The zoo should open with 5 of each type of animal.
 * Each animal has a health value held as a percentage (100% is completely
 * healthy)
 * Every animal starts at 100% health. This value should be a floating point
 * value.
 *
 * The application should act as a simulator, with time passing at the rate of 
 * 1 hour with each iteration. Every hour that passes, a random value between 0
 * and 20 is to be generated for each animal. This value should be passed to 
 * the appropriate animal, whose health is then reduced by that percentage of 
 * their current health.
 *
 * The user must be able to feed the animals in the zoo. When this happens,
 * the zoo should generate three random values between 10 and 25; one for each
 * type of animal. The health of the respective animals is to be increased by 
 * the specified percentage of their current health. Health should be capped 
 * at 100%.
 *
 * When an Elephant has a health below 70% it cannot walk. If its health does 
 * not return above 70% once the subsequent hour has elapsed, it is pronounced 
 * dead.
 * When a Monkey has a health below 30%, or a Giraffe below 50%, it is
 * pronounced dead straight away.
 *
 * This program demonstrate the OO "Is a" relationship and the visitor design 
 * pattern.
*/

#include <iostream>
#include <memory>
#include <vector>
#include <random>
#include <string>

using namespace std;

const string LIVE = "Live";
const string LAME = "Lame";
const string DEAD = "Dead";

const int ELEPHANT_THRESHOLD = 70;
const int GIRAFFE_THRESHOLD  = 50;
const int MONKEY_THRESHOLD   = 30;
const int HOURLY_MIN_RVAL    = 0;
const int HOURLY_MAX_RVAL    = 20;
const int FEED_MIN_RVAL      = 10;
const int FEED_MAX_RVAL      = 25;

const float getRangeNumber(const int min, const int max);

class animal;

class zoo {
    private:
        int n;

    public:
        zoo() {}
        animal *aptr;
};

class animal {
    private:
        // Access to zoo container is only via getContainer() or loadVector().
        vector<shared_ptr<animal>> zoo; 
        static int idx;
    
    public:
        /*
         * We are using a shared_ptr so there is no memory to free in the dtor.
         * Nevertheless, the dtor should be virtual as this is a virtual base.
        */
        virtual ~animal() { cout << "virtual ~animal::animal() dtor" << endl; };

        virtual void accept(class visitorBase*) = 0;

        /*
         * getContainer() returns a reference to a const vector container.
         * This ensures that the reference, zoo, that getContainer() returns is
         * read only.
        */
        const vector<shared_ptr<animal>>& getContainer() { return zoo; }

        int getIdx() { return ++idx; }

        /*
         * The vector container, zoo, can only be populated by this method and
         * it is available in all inherited classes.
        */
        void loadVector(animal * const obj) {
            zoo.emplace_back(obj);
            return;
        } 

        int getVectorSize() { return zoo.size(); }

        virtual void setCount(int count) = 0;

        virtual int getCount() = 0;

        virtual void setHealth(float nhealth) = 0; 

        virtual float getHealth() = 0;

        virtual void setType(string type) = 0;

        virtual string getType() = 0;

        virtual void setFeed(int feed) = 0;

        virtual int getFeed() = 0;

        virtual void  setId(int id) = 0;

        virtual int getId() = 0;

        virtual void setStatus(string status) = 0;

        virtual string getStatus() = 0;

        void printInstance() {
            cout << "        Animal:     " << getType() << endl;
            cout << "        id:         " << getId() << endl;
            cout << "        Count:      " << getCount() << endl;
            cout << "        Health:     " << getHealth() << endl;
            cout << "        Feed:       " << getFeed() << endl;
            cout << "        Status:     " << getStatus() << endl;
            cout << "-----------------------------------" << endl;
            return;
        }

        virtual void getZooStatus() = 0;
        
        /*
         * In an ideal world feedAnimal(float& rnum) should be defined in the
         * callFeedAnimal class but it uses methods defined in the animal sub class's.
        */
        void feedAnimal(const float& rnum) {
            float chealth = 0;
    
            if (getStatus() == DEAD) {
             cout << getType() << " Id: " << getId() << " can't be fed as it is "
                                                      << getStatus() << "..." << endl;
                return;
            }
            chealth = getHealth();   // current health
            float nhealth = (getHealth() + ((getHealth() * (rnum/100))));
            nhealth = (nhealth > 100 ? 100 : nhealth);

            cout << "Animal just fed so increasing health of: '" << getType()
                << "' (id="<< getId() << ") by: " << rnum << "% from: "
                                          << chealth << " to: " << nhealth << endl;
            setHealth(nhealth);
            cout << "    Health for id <" << getId() << "> changed to: "
                   << getHealth() << ".  Current/old status: " << getStatus() << endl;
            return;
        }

        void adjustHealthDown() {
            float chealth = 0;
            chealth = getHealth();

            if (getStatus() == DEAD) {
                cout << "Animal: " << getId() << " health can't be adjusted as it is already " << getStatus() << endl;
                return;
            }

            float rnum = getRangeNumber(HOURLY_MIN_RVAL, HOURLY_MAX_RVAL);
            float nhealth = (getHealth() - ((getHealth() * (rnum/100))));
            cout << "Reducing health of: '" << getType()
                << "' (id="<< getId() << ") by: " << rnum << "% from: "
                                          << chealth << " to: " << nhealth << endl;
            setHealth(nhealth);
            cout << "    Health for id <" << getId() << "> changed to: "
                        << getHealth() << ". Current/old status: " << getStatus()
                                                                              << endl;
            return;
        }

        virtual void changeStatus() = 0;
};

class elephant : public animal {
    private:
        static int    count;
        float  health;
        string type;
        int    feed;
        int    id;
        string status;

    public:
        elephant() { cout << "elephant() default ctor" << endl; }

        elephant(int id) : health(100), type("Elephant"), feed(0), id(id), status(LIVE) {
            setCount(count + 1);
        }

        elephant(const elephant &obj) {
            cout << "elephant(const elephant &obj) - default copy ctor" << endl;
        }

        elephant& operator=(const elephant& obj) {
            cout << "operator=(const elephant &obj) - assignment operator" << endl;
            return *this;
        }

        virtual void accept(visitorBase*);

        virtual void setCount(int count) { this->count = count; }

        virtual int getCount() { return count; }

        virtual void setHealth( float nhealth) { this->health = nhealth; }

        virtual float getHealth() { return health; }

        virtual void setType(string type) { this->type = type; }

        virtual string getType() { return type; }

        virtual void setFeed(int feed) { this->feed = feed; }

        virtual int getFeed() { return feed; }

        void setId(int id) { this->id = id; }

        virtual int getId() { return id; }

        virtual void setStatus(string status) { this->status = status; }

        virtual void changeStatus() {
            bool chg = false;
            string old(getStatus());
            
            if (getStatus() == DEAD) {
                cout << "Elephant id: " << getId() << " Status: "
                                                               <<  getStatus() << endl;
                return;
            } else if (getStatus() == LAME && getHealth() < ELEPHANT_THRESHOLD) {
                setStatus(DEAD);
                chg = true; 
            } else if (getStatus() == LAME && getHealth() >= ELEPHANT_THRESHOLD) {
                setStatus(LIVE);
                chg = true; 
            } else if (getHealth() < ELEPHANT_THRESHOLD) {
                setStatus(LAME);
                chg = true; 
            } else {
                cout << "Elephant id: " << getId() << " No change to status" << endl; 
            }

            if (chg == true) 
                cout << "Elephant id: " << getId() << " status changed from: " << old << " to: " <<  getStatus() << endl;
            return;
        }

        virtual string getStatus() { return status; }

        virtual void getZooStatus() {
            cout << endl << "---------------------" << endl;
            cout << "Number of Elephants in zoo:  " << count << endl;
            cout << "---------------------" << endl;
            return;
        }
};

class monkey : public animal {
    private:
        static int    count;
        float  health;
        string type;
        int    feed;
        int    id;
        string status;

    public:
        monkey(int id) : health(100), type("Monkey"), feed(0), id(id), status(LIVE) {
            setCount(count + 1);
        }

        monkey() { cout << "monkey() default ctor" << endl; }

        monkey(const monkey &obj) {
            cout << "monkey(const monkey &obj) - default copy ctor" << endl;
        }

        monkey& operator=(const monkey& obj) {
            cout << "operator=(const monkey &obj) - assignment operator" << endl;
            return *this;
        }

        virtual void accept(visitorBase*);

        virtual void setCount(int count) { this->count = count; }

        virtual int getCount() { return count; }

        virtual void setHealth( float nhealth) { this->health = nhealth; }

        virtual float getHealth() { return health; }

        virtual void setType(string type) { this->type = type; }

        virtual string getType() { return type; }

        virtual void setFeed(int feed) { this->feed = feed; }

        virtual int getFeed() { return feed; }

        virtual void setId(int id) { this->id = id; }

        virtual int getId() { return id; }

        virtual void setStatus(string status) { this->status = status; }

        virtual void changeStatus() {
            if (getHealth() < MONKEY_THRESHOLD && getStatus() == LIVE) {
                cout << "Monkey id: " << getId() << " status changed from: " << getStatus();
                setStatus(DEAD);
                cout <<  " to: " << getStatus() << endl;
            } else {
                cout << "Monkey id: " << getId() << " No change to status" << endl; 
            }
            return;
        }

        virtual string getStatus() { return status; }

        virtual void getZooStatus() {
            cout << endl << "---------------------" << endl;
            cout << "Number of Monkeys in zoo:  " << count << endl;
            cout << "---------------------" << endl;
            return;
        }
};

class giraffe : public animal {
    private:
        static int    count;
        float  health;
        string type;
        int    feed;
        int    id;
        string status;

    public:
        giraffe(int id) : health(100), type("Giraffe"), feed(0), id(id), status(LIVE) {
            setCount(count + 1);
        }

        giraffe() { cout << "giraffe() default ctor" << endl; }

        giraffe(const giraffe &obj) {
            cout << "giraffe(const giraffe &obj) - default copy ctor" << endl;
        }

        giraffe& operator=(const giraffe& obj) {
            cout << "operator=(const giraffe &obj) - assignment operator" << endl;
            return *this;
        }

        virtual void accept(visitorBase*);

        virtual void setCount(int count) { this->count = count; }

        virtual int getCount() { return count; }

        virtual void setHealth( float nhealth) { this->health = nhealth; }

        virtual float getHealth() { return health; }

        virtual void setType(string type) { this->type = type; }

        virtual string getType() { return type; }

        virtual void setFeed(int feed) { this->feed = feed; }

        virtual int getFeed() { return feed; }

        virtual void setId(int id) { this->id = id; }

        virtual int getId() { return id; }

        virtual void setStatus(string status) { this->status = status; }

        virtual void changeStatus() {
            if (getHealth() < GIRAFFE_THRESHOLD && getStatus() == LIVE) {
                cout << "Giraffe id: " << getId() << " status changed from: " << getStatus();
                setStatus(DEAD);
                cout <<  " to: " << getStatus() << endl;
            } else {
                cout << "Giraffe id: " << getId() << " No change to status" << endl; 
            } 
            return;
        }

        virtual string getStatus() { return status; }

        virtual void getZooStatus() {
            cout << endl << "---------------------" << endl;
            cout << "Number of Giraffe's's in zoo:  " << count << endl;
            cout << "---------------------" << endl;
            return;
        }
};

class visitorBase {
    private:
        static int srand_flg;

    public:
        virtual void visit(monkey *mptr) = 0;

        virtual void visit(giraffe *gptr) = 0;

        virtual void visit(elephant *eptr) = 0;
};

class callFeedAnimal: public visitorBase {
    private:
        float m_rnum;
        float g_rnum;
        float e_rnum;

    public:
        /*
         * The random number passed as arg to animal::feedAnimal(const float&) are 
         * generated in the default ctor below via resetRandomNumbers().
        */
        callFeedAnimal() {
            resetRandomNumbers();
            cout << "callFeedAnimal::callFeedAnimal() ctor" << endl;
        }

        ~callFeedAnimal() {
            cout << "~callFeedAnimal::callFeedAnimal() dtor" << endl; 
        }

        callFeedAnimal(const callFeedAnimal& obj) {
            cout << "callFeedAnimal() copy ctor" << endl;
        }

        callFeedAnimal& operator=(const callFeedAnimal& obj) {
            cout << "operator=(const callFeedAnimal &obj) - assignment operator"
                                                                             << endl;
            return *this;
        }

        float get_m_rnum() { return m_rnum; }

        float get_g_rnum() { return g_rnum; }

        float get_e_rnum() { return e_rnum; }

        /*
         * In an ideal world method void feedAnimal(const float&) should be defined
         * in this class rather than in class animal.  Unfortunately it uses methods
         * that are only available in the animal hierarchy and they will all need to
         * be moved here as well.
        */

        void resetRandomNumbers() {
            /*
             * Everytime an animal is fed,  generate three random values between 10
             * and 25; one for each type of animal.
            */
            m_rnum = getRangeNumber(FEED_MIN_RVAL, FEED_MAX_RVAL); 
            g_rnum = getRangeNumber(FEED_MIN_RVAL, FEED_MAX_RVAL); 
            e_rnum = getRangeNumber(FEED_MIN_RVAL, FEED_MAX_RVAL); 
            cout << "Feed random numbers generated by callFeedAnimal::resetRandomNumbers() are:" << endl;
            cout << "    m_rnum=" << m_rnum << "  g_rnum=" << g_rnum
                                                   << "  e_rnum=" << e_rnum << endl;
            return;
        }

        virtual void visit(monkey *mptr)   { mptr->feedAnimal(m_rnum); }

        virtual void visit(giraffe *gptr)  { gptr->feedAnimal(g_rnum); }

        virtual void visit(elephant *eptr) { eptr->feedAnimal(e_rnum); }
};

void monkey::accept(visitorBase *v) {v->visit(this); }

void giraffe::accept(visitorBase *v) {v->visit(this); }

void elephant::accept(visitorBase *v) {v->visit(this); }


const float getRangeNumber(const int min, const int max) {
    static bool srand_flg;
    if (srand_flg == 0) {
        srand_flg = 1;
        srand(time(NULL));
    }
    int range = max - min + 1;
    return (rand() % range + min);
}

void adjustAllAnimalHealthDownWrapper(animal *aptr) {

    cout << "** An hour has passed so adjusting health of all animals down... **" << endl;

    cout << "-----------------------------------" << endl;
    const vector<shared_ptr<animal>>& zoo = aptr->getContainer();

    /*
     *  infer type of iterator 'it' using the new C++ 11 auto keyword as
     *  well as using range based loop rather than the less readable commented
     *  out code below.
    for (vector<shared_ptr<animal>>::const_iterator it = zoo.begin();
                                                      it != zoo.end(); it++) {
    */
    for (auto it : zoo) {
        (*it).adjustHealthDown();

        /*
         * Reset the status to reflect the changed health
        */
        (*it).changeStatus();
    }
    return;
}

void printVectorContentsWrapper(animal *aptr) {

    const vector<shared_ptr<animal>>& zoo = aptr->getContainer();
    cout << "-----------------------------------" << endl;
    /*
     *  infer type of iterator 'it' using the new C++ 11 auto keyword as
     *  well as using range based loop rather than the less readable commented
     *  out code below.
    for (vector<shared_ptr<animal>>::const_iterator it = zoo.begin();
                                                     it != zoo.end(); it++) { 
    */
    for (auto it : zoo) {
        (*it).printInstance();
    }
    return;
}

void feedAllAnimalsWrapper(animal *aptr) {

    cout << "Feeding animals..." << endl;
    cout << "-----------------------------------" << endl;
    /*
     * The three feed random numbers are generated everytime a callFeedAnimal
     * instance is created.  And an instance of feedAnimal is only used once in
     * feedAllAnimalsWrapper() function so that ensures that we generate fresh
     * random numbers whenever this function is called.
     * But potentially someone could break this by creating another loop in this
     * function and using the feedAnimal instance again and that would lead to
     * the same random numbers being reused!
     * You could restrict how callFeedAnimal objects are created by making the copy
     * constructor, destructor & assignment operator private and
     * then using code to destroy the instance in the heap after use but we are
     * not doing  that here!  You just need to be aware that I'm aware of this issue!
    */
    callFeedAnimal feedAnimal;
    const vector<shared_ptr<animal>>& zoo = aptr->getContainer();

    /*
     *  infer type of iterator 'it' using the new C++ 11 auto keyword as
     *  well as using range based loop rather than the less readable commented
     *  out code below.
    for (vector<shared_ptr<animal>>::const_iterator it = zoo.begin(); it != zoo.end(); it++) { 
     *
    */
    for (auto it : zoo) {
        (*it).accept(&feedAnimal);

        /*
         * Reset the status as animals have been fed
        */
        (*it).changeStatus();
    }
    return;
}


// keep linker happy for static variables
int animal::idx=0;
int monkey::count = 0;
int giraffe::count = 0;
int elephant::count = 0;
int visitorBase::srand_flg=0;

int main(int argc, char **argv) {
    cout << "Entered zoo...." << endl;

    // Use different ptr for each animal for better readability
    animal   *eptr;
    animal   *mptr;
    animal   *gptr;
    elephant e;
    animal   *aptr = &e;
    int idx = 0;

    // Populate the zoo with 15 animals (five of each)

    for (int i=0; i < 5; i++) { 
        mptr = new monkey(idx);
        aptr->loadVector(mptr);

        idx = aptr->getIdx();
        gptr = new giraffe(idx);
        aptr->loadVector(gptr);

        idx = aptr->getIdx();
        eptr = new elephant(idx);
        aptr->loadVector(eptr);
        idx = aptr->getIdx();
    }

    eptr->getZooStatus();
    mptr->getZooStatus();
    gptr->getZooStatus();

    cout << "================================================" << endl;
    cout << "Zoo vector populated with <" << aptr->getVectorSize() << "> animals." << endl;
    cout << "================================================" << endl;

    cout << endl;
    cout << endl;

    cout << "Printing vector initial contents...." << endl;
    printVectorContentsWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    feedAllAnimalsWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    cout << "Printing vector contents...." << endl;
    printVectorContentsWrapper(aptr);

    cout << endl;
    cout << endl;
    feedAllAnimalsWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    feedAllAnimalsWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);


    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    adjustAllAnimalHealthDownWrapper(aptr);

    cout << endl;
    cout << endl;
    feedAllAnimalsWrapper(aptr);

    cout << endl;
    cout << endl;
    feedAllAnimalsWrapper(aptr);

    cout << endl;
    cout << endl;
    cout << "Printing vector contents...." << endl;
    printVectorContentsWrapper(aptr);

    return 0;
}
