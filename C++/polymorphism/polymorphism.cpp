#include <iostream>
#include <vector>
#include <memory>
        

using namespace std;

class B {
    private:
        vector<shared_ptr<B>> data;
        static int idx;
      
    public:
        B() { cout << "B:B() ctor" << endl; };

        virtual ~B() { cout << "B:~B() virtual dtor" << endl; };

        // The reference returned cannot be used to modify the vector
        const vector<shared_ptr<B>>& getVector() { return data; }

        void loadVector( B * const obj ) { data.emplace_back(obj); }

        int getSize() { return data.size(); }

        /*
         * vfunc() is a pure virtual function and that makes class B
         * and abstract class.
        */
        virtual void vfunc(int rnum) = 0;

        void func() { cout << "B::func()" << endl; }

        int getIdx() { return ++idx; }
};

class D1 : public B {
    private:
        D1(const D1 &obj) {
            cout << "D1(const D1 &obj) - default copy ctor" << endl;
        }

        D1& operator=(const D1& obj) {
            cout << "operator=(const D1 &obj) - assignment operator" << endl;
            return *this;
        }


    public:
        D1() { cout << "D1:D1() ctor" << endl; };

        ~D1() { cout << "D1:~D1() dtor" << endl; };

        /*
         * We define the inherited vfunc() so that D1 not an abstract class
        */
        void vfunc(int rnum) {
            cout << "D1::vfunc(int rnum) Seq=" << rnum << endl; 
            }

        void func() { cout << "D1::func()" << endl; }
};

class D2 : public B {
    private:
       D2(const D2 &obj) {
            cout << "D2(const D2 &obj) - default copy ctor" << endl;
        }

        D2& operator=(const D2& obj) {
            cout << "operator=(const D2 &obj) - assignment operator" << endl;
            return *this;
        }

    public:
        D2() { cout << "D2:D2() ctor" << endl; };

        ~D2() { cout << "D2:~D2() dtor" << endl; };

        /*
         * We define the inherited vfunc() so that D2 not an abstract class
        */
        void vfunc(int rnum) {
            cout << "D1::vfunc(int rnum) Seq=" << rnum << endl; 
        }

        void func() { cout << "D2::func()" << endl; }
};

int B::idx = 0;

int main() { 
    cout << "Entered main()" << endl;
    D1 d1;
    B *bptr = &d1;
    const vector<shared_ptr<B>>& data = bptr->getVector();

    cout << endl;
    cout << "Loading vector..." << endl;
    for (int i = 0; i < 5; i++) {
       bptr->loadVector(new D1()); 
       bptr->loadVector(new D2()); 
    }

    cout << endl;
    cout << "Iterating around vector..." << endl;
    /*
     * Const iterator 'it' is a pointer to a vector container holding objects of type B
    */
    vector<shared_ptr<B>>::const_iterator  it;

    /*
     * Iterate around vector container and called derived class vfunc() polymorphically.
    */
    for (it = data.begin(); it != data.end(); it++) {
        int rnum=bptr->getIdx();
        (*it)->vfunc(rnum);
    }

    cout << endl;
    cout << "Vector Size=" << bptr->getSize() << endl;    

    //D1 copy(d1); // copy disabled as  ‘D1::D1(const D1&)’ is private within this context
    //d1 = copy;   // Assignment disabled

}
