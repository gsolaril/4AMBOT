#include <Clustering.mqh>

//==========================================================================================
// SIGNATURES                                                                             ||
//==========================================================================================

class LineArray {

    private:
        uchar     Length = 0;              
        double    Values[0] = {};
        datetime  dTimes[0] = {};
        string    cMode;
    protected:
        double    mStep;
        uchar     mLength;
        uchar     first;
        string    tag;
        void      append(datetime dtime, double value, bool draw = true);
        void      bind(double & interval, double value);
        void      cluster(double & values[]);
    public:
        LineArray(double minStep, uchar maxLength, string scanMode);
        enum clusterModes;
        void values(double & array);
        void dtimes(datetime & array);
        uchar length();
        double min_step();
        uchar max_length();
        string cmode();
        void draw(short index, color marker);        
};